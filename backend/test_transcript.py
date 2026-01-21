from youtube_transcript_api import YouTubeTranscriptApi

# Try with a different video that has English transcript
video_id = 'dQw4w9WgXcQ'  # Rick Astley - Never Gonna Give You Up

try:
    # Get English transcript directly
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    print("Success! Got", len(transcript_list), "segments")
    
    # Print first few segments
    if transcript_list:
        print("\nFirst 3 segments:")
        for i in range(min(3, len(transcript_list))):
            print(f"  {i+1}. {transcript_list[i]['text']}")
        
        # Join all text
        full_text = " ".join([segment['text'] for segment in transcript_list])
        print(f"\nTotal words: {len(full_text.split())}")
        
except Exception as e:
    print("Error:", e)
