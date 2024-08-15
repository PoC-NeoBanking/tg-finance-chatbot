"""
Моделька ЧатуGpt для чатботу(невикористовується)
"""

from transformers import pipeline

from huggingface_hub import login

# Використання моделі GPT-J через Hugging Face
generator = pipeline('text-generation', model='EleutherAI/gpt-j-6B')

prompt = "Help me to understand the future of artificial intelligence."
response = generator(prompt, max_length=100, do_sample=True, temperature=0.8)

print(response[0]['generated_text'])
