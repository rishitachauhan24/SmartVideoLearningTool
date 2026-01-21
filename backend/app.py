"""
Smart Video Learning Tool - Flask Backend Server
Main application server handling all API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.youtube_service import get_transcript
from backend.summarizer import generate_summary
from backend.keypoints import generate_keypoints
from backend.quiz_generator import generate_quiz
from backend.formatter import format_learning_package, format_error_response

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "Smart Video Learning Tool API",
        "version": "1.0.0"
    })


@app.route('/api/process', methods=['POST'])
def process_video():
    """
    Main endpoint to process YouTube video and generate learning package
    
    Expected JSON body:
    {
        "youtube_url": "https://www.youtube.com/watch?v=..."
    }
    
    Returns:
    {
        "success": true/false,
        "video_id": "...",
        "transcript": {...},
        "summary": {...},
        "key_points": {...},
        "quiz": {...}
    }
    """
    try:
        # Get YouTube URL from request
        data = request.get_json()
        
        if not data or 'youtube_url' not in data:
            return jsonify(format_error_response(
                "Missing youtube_url in request body",
                "validation"
            )), 400
        
        youtube_url = data['youtube_url']
        
        # Step 1: Extract transcript
        print(f"Extracting transcript for: {youtube_url}")
        transcript_result = get_transcript(youtube_url)
        
        if not transcript_result['success']:
            return jsonify(format_error_response(
                transcript_result.get('error', 'Transcript extraction failed'),
                "transcript_extraction"
            )), 400
        
        video_id = transcript_result['video_id']
        transcript_text = transcript_result['transcript']
        
        # Step 2: Generate summary
        print("Generating summary...")
        summary_result = generate_summary(transcript_text)
        
        if not summary_result['success']:
            return jsonify(format_error_response(
                summary_result.get('error', 'Summary generation failed'),
                "summary_generation"
            )), 500
        
        # Step 3: Generate key points
        print("Generating key points...")
        keypoints_result = generate_keypoints(transcript_text)
        
        if not keypoints_result['success']:
            return jsonify(format_error_response(
                keypoints_result.get('error', 'Key points generation failed'),
                "keypoints_generation"
            )), 500
        
        # Step 4: Generate quiz
        print("Generating quiz questions...")
        quiz_result = generate_quiz(transcript_text)
        
        if not quiz_result['success']:
            return jsonify(format_error_response(
                quiz_result.get('error', 'Quiz generation failed'),
                "quiz_generation"
            )), 500
        
        # Step 5: Format complete package
        learning_package = format_learning_package(
            video_id,
            transcript_result,
            summary_result,
            keypoints_result,
            quiz_result
        )
        
        print(f"Successfully generated learning package for video: {video_id}")
        
        return jsonify(learning_package), 200
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify(format_error_response(
            f"Unexpected server error: {str(e)}",
            "server_error"
        )), 500


@app.route('/api/transcript', methods=['POST'])
def get_transcript_only():
    """
    Endpoint to get only transcript
    
    Expected JSON body:
    {
        "youtube_url": "https://www.youtube.com/watch?v=..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'youtube_url' not in data:
            return jsonify(format_error_response(
                "Missing youtube_url in request body",
                "validation"
            )), 400
        
        youtube_url = data['youtube_url']
        result = get_transcript(youtube_url)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify(format_error_response(
            str(e),
            "transcript_extraction"
        )), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Smart Video Learning Tool - Backend Server")
    print("=" * 60)
    print("\nServer starting on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  - GET  /              : Health check")
    print("  - POST /api/process   : Process video and generate learning package")
    print("  - POST /api/transcript: Get transcript only")
    print("\nMake sure to set OPENAI_API_KEY in .env file")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
