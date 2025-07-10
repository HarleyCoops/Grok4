import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key from environment
XAI_API_KEY = os.getenv('XAI_API_KEY')

if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY environment variable is not set")

# Read the universe.txt file
try:
    with open('universe.txt', 'r', encoding='utf-8') as file:
        universe_content = file.read()
except FileNotFoundError:
    print("Error: universe.txt file not found!")
    exit(1)

client = OpenAI(
  api_key=XAI_API_KEY,
  base_url="https://api.x.ai/v1",
)

# Create the prompt for Grok4 to convert the content to Manim code
prompt = f"""Please convert the following animation description into a complete, fully rendered Manim Community v.19 Python code. 

The description is for a Quantum Field Theory animation with multiple scenes. Please create a complete, runnable Manim script that includes:

1. All necessary imports for Manim Community v.19
2. A main scene class that contains all the described scenes as methods
3. Proper scene transitions and timing
4. All mathematical equations rendered using LaTeX
5. 3D elements, colors, animations, and effects as described
6. Proper camera movements and positioning
7. All the visual elements mentioned in the description

Here's the animation description:

{universe_content}

Please provide the complete Python code that can be run directly with Manim Community v.19. Make sure to include all necessary imports and create a complete, self-contained script."""

completion = client.chat.completions.create(
  model="grok-3",
  messages=[
    {"role": "user", "content": prompt}
  ],
  max_tokens=4000,  # Increased for longer code generation
  temperature=0.1   # Lower temperature for more focused code generation
)

print("Response:", completion.choices[0].message.content)

# Optionally save the response to a file
with open('manim_quantum_field_theory.py', 'w', encoding='utf-8') as f:
    f.write(completion.choices[0].message.content)

print("\nManim code has been saved to 'manim_quantum_field_theory.py'")