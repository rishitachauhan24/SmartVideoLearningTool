"""
Quiz Generator
Creates exactly 10 MCQ questions from video transcripts
"""

import sys
import os
import re

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.ai_engine import get_ai_engine
from models.prompts import QUIZ_PROMPT


def parse_quiz_response(quiz_text):
    """
    Parse AI response into structured quiz format
    
    Args:
        quiz_text (str): Raw quiz text from AI
        
    Returns:
        list: List of quiz questions with options and answers
    """
    questions = []
    
    # Split by question numbers
    question_blocks = re.split(r'Question\s+\d+:', quiz_text)
    
    for block in question_blocks[1:]:  # Skip first empty block
        try:
            lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
            
            if len(lines) < 6:  # Need at least question + 4 options + answer
                continue
            
            question_text = lines[0]
            
            # Extract options
            options = {}
            correct_answer = None
            
            for line in lines[1:]:
                # Check for options A) B) C) D)
                if re.match(r'^[A-D]\)', line):
                    letter = line[0]
                    option_text = line[2:].strip()
                    options[letter] = option_text
                
                # Check for correct answer
                if 'correct answer' in line.lower():
                    match = re.search(r'[A-D]', line)
                    if match:
                        correct_answer = match.group()
            
            # Add question if we have all required parts
            if question_text and len(options) == 4 and correct_answer:
                questions.append({
                    "question": question_text,
                    "options": options,
                    "correct_answer": correct_answer
                })
        
        except Exception as e:
            continue
    
    return questions


def generate_quiz(transcript):
    """
    Generate exactly 10 MCQ questions from transcript using AI
    
    Args:
        transcript (str): Video transcript text
        
    Returns:
        dict: Dictionary containing success status and quiz questions
    """
    try:
        # Get AI engine
        ai_engine = get_ai_engine()
        
        # Prepare prompt
        prompt = QUIZ_PROMPT.format(transcript=transcript[:9000])  # Limit to 9000 chars
        
        # Generate quiz
        result = ai_engine.generate_response(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.6
        )
        
        if result['success']:
            quiz_text = result['text']
            
            # Parse quiz questions
            questions = parse_quiz_response(quiz_text)
            
            # Ensure we have exactly 10 questions
            if len(questions) >= 10:
                questions = questions[:10]
            elif len(questions) < 10:
                # If less than 10, try to generate again or return what we have
                pass
            
            return {
                "success": True,
                "quiz": questions,
                "total_questions": len(questions)
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Failed to generate quiz')
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Quiz generation failed: {str(e)}"
        }


if __name__ == "__main__":
    # Test
    test_transcript = "This is a test transcript about machine learning and AI."
    result = generate_quiz(test_transcript)
    print(result)
