"""
AI Engine - OpenAI Connection
Handles all OpenAI API interactions
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEngine:
    """
    AI Engine for OpenAI GPT interactions
    """
    
    def __init__(self):
        """Initialize OpenAI client with API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5-turbo for cost efficiency
    
    
    def generate_response(self, prompt, max_tokens=1500, temperature=0.7):
        """
        Generate AI response using OpenAI
        
        Args:
            prompt (str): The prompt to send to AI
            max_tokens (int): Maximum tokens in response
            temperature (float): Creativity level (0.0 to 1.0)
            
        Returns:
            dict: Response containing success status and generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational AI assistant helping students learn from video content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "text": generated_text,
                "tokens_used": response.usage.total_tokens
            }
            
        except openai.AuthenticationError:
            return {
                "success": False,
                "error": "Invalid API key. Please check your OPENAI_API_KEY."
            }
        except openai.RateLimitError:
            return {
                "success": False,
                "error": "Rate limit exceeded. Please try again later."
            }
        except openai.APIError as e:
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }


# Global AI engine instance
ai_engine = None

def get_ai_engine():
    """Get or create AI engine instance"""
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine


if __name__ == "__main__":
    # Test the AI engine
    try:
        engine = AIEngine()
        result = engine.generate_response("What is machine learning in one sentence?")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
