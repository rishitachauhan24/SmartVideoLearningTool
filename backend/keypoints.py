"""
Key Points Generator
Extracts and highlights core learning points from transcripts
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.ai_engine import get_ai_engine
from models.prompts import KEYPOINTS_PROMPT


def generate_keypoints(transcript):
    """
    Generate key learning points from transcript using AI
    
    Args:
        transcript (str): Video transcript text
        
    Returns:
        dict: Dictionary containing success status and key points list
    """
    try:
        # Get AI engine
        ai_engine = get_ai_engine()
        
        # Prepare prompt
        prompt = KEYPOINTS_PROMPT.format(transcript=transcript[:8000])  # Limit to 8000 chars
        
        # Generate key points
        result = ai_engine.generate_response(
            prompt=prompt,
            max_tokens=600,
            temperature=0.5
        )
        
        if result['success']:
            # Parse the key points from response
            keypoints_text = result['text']
            
            # Extract numbered points
            keypoints_list = []
            lines = keypoints_text.split('\n')
            
            for line in lines:
                line = line.strip()
                # Look for numbered points (1. 2. 3. etc or 1) 2) 3) etc)
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Clean up the point
                    cleaned_point = line
                    # Remove numbering
                    for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', 
                                   '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)',
                                   '-', '•', '*']:
                        if cleaned_point.startswith(prefix):
                            cleaned_point = cleaned_point[len(prefix):].strip()
                            break
                    
                    if cleaned_point:
                        keypoints_list.append(cleaned_point)
            
            # If parsing failed, just return the full text
            if not keypoints_list:
                keypoints_list = [keypoints_text]
            
            return {
                "success": True,
                "keypoints": keypoints_list[:8]  # Max 8 points
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Failed to generate key points')
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Key points generation failed: {str(e)}"
        }


if __name__ == "__main__":
    # Test
    test_transcript = "This is a test transcript about machine learning and AI."
    result = generate_keypoints(test_transcript)
    print(result)
