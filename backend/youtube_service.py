"""
YouTube Transcript Extractor
Extracts video transcripts from YouTube videos
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
import json
from datetime import datetime


def extract_video_id(youtube_url):
    """
    Extract video ID from various YouTube URL formats
    
    Args:
        youtube_url (str): YouTube video URL
        
    Returns:
        str: Video ID or None if not found
    """
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    # If URL is just the video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', youtube_url):
        return youtube_url
    
    return None


def get_transcript(youtube_url):
    """
    Get transcript from YouTube video
    
    Args:
        youtube_url (str): YouTube video URL
        
    Returns:
        dict: Dictionary containing transcript text and metadata
    """
    try:
        video_id = extract_video_id(youtube_url)
        
        if not video_id:
            return {
                "success": False,
                "error": "Invalid YouTube URL. Please provide a valid YouTube video link."
            }
        
        # Try to get transcript - use simpler approach to avoid rate limiting
        transcript_list = None
        error_msg = ""
        
        try:
            # Try to get transcript in order of preference
            # 1. English
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            except:
                # 2. Hindi
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
                except:
                    # 3. Any available language
                    try:
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    except Exception as e:
                        error_msg = str(e)
        except Exception as e:
            error_msg = str(e)
        
        if not transcript_list:
            return {
                "success": False,
                "error": f"Could not retrieve transcript for this video. Please try again later or use a different video. Error: {error_msg}"
            }
        
        # Combine all transcript segments
        full_transcript = " ".join([segment['text'] for segment in transcript_list])
        
        # Save transcript to file
        save_transcript(video_id, full_transcript, transcript_list)
        
        return {
            "success": True,
            "video_id": video_id,
            "transcript": full_transcript,
            "segments": transcript_list,
            "word_count": len(full_transcript.split())
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to extract transcript: {str(e)}"
        }


def save_transcript(video_id, full_transcript, segments):
    """
    Save transcript to data/transcripts folder
    
    Args:
        video_id (str): YouTube video ID
        full_transcript (str): Full transcript text
        segments (list): List of transcript segments with timestamps
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transcripts')
        os.makedirs(data_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{video_id}_{timestamp}.json"
        filepath = os.path.join(data_dir, filename)
        
        # Save transcript data
        transcript_data = {
            "video_id": video_id,
            "timestamp": timestamp,
            "full_transcript": full_transcript,
            "segments": segments,
            "word_count": len(full_transcript.split())
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Warning: Could not save transcript: {str(e)}")


if __name__ == "__main__":
    # Test the function
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = get_transcript(test_url)
    print(result)
