"""
Output Formatter
Structures and formats the complete learning package
"""

import json
from datetime import datetime


def format_learning_package(video_id, transcript_data, summary_data, keypoints_data, quiz_data):
    """
    Format complete learning package with all components
    
    Args:
        video_id (str): YouTube video ID
        transcript_data (dict): Transcript information
        summary_data (dict): Summary content
        keypoints_data (dict): Key learning points
        quiz_data (dict): Quiz questions
        
    Returns:
        dict: Formatted learning package
    """
    
    package = {
        "success": True,
        "video_id": video_id,
        "generated_at": datetime.now().isoformat(),
        "transcript": {
            "text": transcript_data.get('transcript', ''),
            "word_count": transcript_data.get('word_count', 0)
        },
        "summary": {
            "text": summary_data.get('summary', 'Summary not available')
        },
        "key_points": {
            "points": keypoints_data.get('keypoints', []),
            "total": len(keypoints_data.get('keypoints', []))
        },
        "quiz": {
            "questions": quiz_data.get('quiz', []),
            "total_questions": len(quiz_data.get('quiz', []))
        }
    }
    
    return package


def format_error_response(error_message, stage="unknown"):
    """
    Format error response
    
    Args:
        error_message (str): Error message
        stage (str): Stage where error occurred
        
    Returns:
        dict: Formatted error response
    """
    return {
        "success": False,
        "error": error_message,
        "stage": stage,
        "timestamp": datetime.now().isoformat()
    }


def save_learning_package(package, output_path):
    """
    Save learning package to JSON file
    
    Args:
        package (dict): Learning package data
        output_path (str): Output file path
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving package: {str(e)}")
        return False


if __name__ == "__main__":
    # Test formatter
    test_package = format_learning_package(
        "test123",
        {"transcript": "Test transcript", "word_count": 2},
        {"summary": "Test summary"},
        {"keypoints": ["Point 1", "Point 2"]},
        {"quiz": []}
    )
    print(json.dumps(test_package, indent=2))
