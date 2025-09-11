import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Check if API key exists
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print(" Missing OPENAI_API_KEY in environment variables")
    print(" Using mock service instead of real AI")
    api_key = None

client = OpenAI(api_key=api_key)

async def generate_lesson(prompt: str) -> str:
    """
    Generate a lesson using OpenAI GPT API or mock service
    """
    if not api_key:
        print(f" Using mock AI lesson for: {prompt}")
        return generate_mock_lesson(prompt)
    
    try:
        print(f" Generating AI lesson for: {prompt}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        
        ai_response = response.choices[0].message.content
        if not ai_response:
            return "No response from AI"
            
        print(f"AI lesson generated successfully")
        return ai_response
        
    except Exception as error:
        print(f" Error generating AI response: {error}")
        print(f" Falling back to mock service")
        return generate_mock_lesson(prompt)

def generate_mock_lesson(prompt: str) -> str:
    return f"""#  AI Learning Lesson: {prompt}

##  Introduction
Welcome to your personalized AI-generated lesson about **{prompt}**! This comprehensive guide will help you understand this fascinating topic step by step.

## 🔍 What is {prompt}?
{prompt} is a complex and interesting subject that has many applications in our daily lives. Understanding this topic can open doors to new knowledge and opportunities.

##  Key Concepts

### 1. **Fundamentals**
- Basic principles and definitions
- Core terminology and concepts
- Historical context and development

### 2. **Practical Applications**
- Real-world examples and use cases
- How it affects our daily lives
- Industry applications and benefits

### 3. **Advanced Topics**
- Complex theories and advanced concepts
- Current research and developments
- Future trends and possibilities

##  Examples and Case Studies

**Example 1:** A practical demonstration of {prompt} in action
**Example 2:** A real-world case study showing its importance
**Example 3:** An interactive scenario to test your understanding

##  Learning Activities

1. **Reflection Questions:**
   - How does {prompt} relate to your personal experience?
   - What aspects of this topic interest you most?

2. **Practice Exercises:**
   - Try to explain {prompt} to someone else
   - Look for examples of {prompt} in your environment

##  Summary

This lesson has covered the essential aspects of {prompt}. You now have a solid foundation for understanding this topic and can continue exploring it further.

##  Next Steps

- **Practice:** Apply what you've learned in real situations
- **Explore:** Look for additional resources and materials
- **Connect:** Discuss this topic with others who share your interest
- **Advance:** Move on to more advanced topics in this field

---

*Note: This is a mock lesson generated for demonstration purposes. For real AI-generated content, please configure your OpenAI API key.*

**Happy Learning! **
"""
