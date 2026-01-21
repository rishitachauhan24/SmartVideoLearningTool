"""
Summary Generator
Generates comprehensive summaries from video transcripts
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.ai_engine import get_ai_engine
from models.prompts import SUMMARY_PROMPT


def generate_summary(transcript):
    """
    Generate summary from transcript using AI
    
    Args:
        transcript (str): Video transcript text
        
    Returns:
        dict: Dictionary containing success status and summary
    """
    try:
        # Get AI engine
        ai_engine = get_ai_engine()
        
        # Prepare prompt
        prompt = SUMMARY_PROMPT.format(transcript=transcript[:8000])  # Limit to 8000 chars
        
        # Generate summary
        result = ai_engine.generate_response(
            prompt=prompt,
            max_tokens=800,
            temperature=0.5
        )
        
        if result['success']:
            return {
                "success": True,
                "summary": result['text']
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Failed to generate summary')
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Summary generation failed: {str(e)}"
        }


if __name__ == "__main__":
    # Test
    test_transcript = "This is a test transcript about machine learning and AI."
    result = generate_summary(test_transcript)
    print(result)
