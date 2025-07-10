from openai import OpenAI
    
client = OpenAI(
  api_key=XAI_API_KEY,
  base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
  model="grok-3",
  messages=[
    {"role": "user", "content": "What is the meaning of life, the universe, and everything?"}
  ]
)