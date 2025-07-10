#!/usr/bin/env python3
"""
Basic Grok4 Chat Demo
Demonstrates simple text generation with Grok4
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def main():
    # Initialize the client
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
    
    print("🤖 Grok4 Basic Chat Demo")
    print("=" * 40)
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
            
        try:
            response = client.chat.completions.create(
                model="grok-4",
                messages=[
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            print(f"Grok4: {response.choices[0].message.content}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
