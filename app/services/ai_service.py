import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_lesson(prompt: str) -> str:
    """
    Generate a lesson using OpenAI GPT API
    """
    try:
        print("\n=== Starting AI Request ===")
        print(f"1. Prompt received: {prompt}")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"2. API Key exists: {bool(api_key)}")
        print(f"3. API Key length: {len(api_key) if api_key else 0}")
        print(f"4. API Key first/last 5 chars: {api_key[:5]}...{api_key[-5:] if len(api_key) > 5 else ''}")
        print("5. Creating chat completion...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational AI assistant. Create comprehensive, engaging lessons based on the user's request. Structure your response with clear sections, examples, and key takeaways."
                },
                {
                    "role": "user",
                    "content": f"Create a detailed lesson about: {prompt}"
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"API Key exists: {bool(api_key)}")
        if not api_key:
            error_message = "OpenAI API key is missing. Please add it to your .env file."
        elif "Invalid API key" in str(e):
            error_message = "The OpenAI API key is invalid. Please check your .env file."
        else:
            error_message = f"An error occurred while calling OpenAI API: {str(e)}"
        
        print(error_message)
        return f"""# Error Generating Lesson
I apologize, but I couldn't generate a lesson about {prompt} at the moment.
Error: {error_message}
Please try again later or contact support if the problem persists.
"""

def generate_mock_lesson(prompt: str) -> str:
    return f"""# Lesson: {prompt}

This is a comprehensive lesson about {prompt}.

## Overview
{prompt} is an important topic that deserves careful study.

## Key Points
- Understanding the fundamentals
- Practical applications
- Advanced concepts

## Conclusion
This lesson provides a solid foundation for understanding {prompt}.
"""