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
    # Remove whitespace
    youtube_url = youtube_url.strip()
    
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:m\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
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
                "error": "Invalid YouTube URL. Please provide a valid YouTube video link. Supported formats: youtube.com/watch?v=..., youtu.be/..., youtube.com/shorts/..."
            }
        
        print(f"Attempting to fetch transcript for video ID: {video_id}")
        
        # Try to get transcript with multiple language options
        transcript_list = None
        language_used = "unknown"
        error_messages = []
        
        # List of language codes to try in order
        language_preferences = [
            ['en'],           # English
            ['en-US'],        # English (US)
            ['en-GB'],        # English (UK)
            ['hi'],           # Hindi
            ['hi-IN'],        # Hindi (India)
            ['es'],           # Spanish
            ['fr'],           # French
            ['de'],           # German
            ['pt'],           # Portuguese
            ['ja'],           # Japanese
            ['ko'],           # Korean
        ]
        
        # Try each language preference
        for languages in language_preferences:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=languages
                )
                language_used = languages[0]
                print(f"✓ Found transcript in language: {language_used}")
                break
            except Exception as e:
                error_messages.append(f"{languages[0]}: {str(e)}")
                continue
        
        # If no specific language worked, try getting any available transcript
        if not transcript_list:
            try:
                print("Trying to get any available transcript...")
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                language_used = "auto-detected"
                print(f"✓ Found auto-detected transcript")
            except Exception as e:
                error_messages.append(f"auto-detect: {str(e)}")
        
        # Final check
        if not transcript_list:
            error_detail = "; ".join(error_messages[:3]) if error_messages else "Unknown error"
            return {
                "success": False,
                "error": f"No transcript available for this video. The video may not have captions/subtitles enabled. Tried languages: {', '.join([l[0] for l in language_preferences[:5]])}. Error: {error_detail}"
            }
        
        # Combine all transcript segments
        full_transcript = " ".join([segment['text'] for segment in transcript_list])
        
        # Validate transcript
        if not full_transcript or len(full_transcript.strip()) < 50:
            return {
                "success": False,
                "error": "Transcript is too short or empty. Please try a different video."
            }
        
        # Save transcript to file
        save_transcript(video_id, full_transcript, transcript_list)
        
        word_count = len(full_transcript.split())
        char_count = len(full_transcript)
        
        print(f"✓ Successfully extracted transcript:")
        print(f"  - Language: {language_used}")
        print(f"  - Characters: {char_count:,}")
        print(f"  - Words: {word_count:,}")
        print(f"  - Segments: {len(transcript_list)}")
        
        return {
            "success": True,
            "video_id": video_id,
            "transcript": full_transcript,
            "segments": transcript_list,
            "word_count": word_count,
            "language": language_used
        }
        
    except Exception as e:
        error_type = type(e).__name__
        return {
            "success": False,
            "error": f"Failed to extract transcript ({error_type}): {str(e)}"
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
        
        print(f"✓ Transcript saved to: {filepath}")
            
    except Exception as e:
        print(f"⚠ Warning: Could not save transcript: {str(e)}")


if __name__ == "__main__":
    # Test the function
    print("=" * 70)
    print("YouTube Transcript Extractor - Test Mode")
    print("=" * 70)
    
    # You can test with real YouTube videos that have captions
    test_urls = [
        # Add your test URL here
        # Example: "https://www.youtube.com/watch?v=VIDEO_ID"
    ]
    
    if not test_urls:
        print("\n⚠ No test URLs provided.")
        print("To test, add a YouTube URL with captions to the test_urls list.")
        print("\nExample usage:")
        print('  result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")')
        print('  if result["success"]:')
        print('      print(result["transcript"])')
    else:
        for test_url in test_urls:
            print(f"\n{'='*70}")
            print(f"Testing URL: {test_url}")
            print('='*70)
            result = get_transcript(test_url)
            
            if result['success']:
                print(f"\n✓ SUCCESS!")
                print(f"  Video ID: {result['video_id']}")
                print(f"  Language: {result.get('language', 'unknown')}")
                print(f"  Word count: {result['word_count']:,}")
                print(f"\n  Preview (first 200 chars):")
                print(f"  {result['transcript'][:200]}...")
            else:
                print(f"\n✗ FAILED!")
                print(f"  Error: {result['error']}")
    
    print("\n" + "="*70)
