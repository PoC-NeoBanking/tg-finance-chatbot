"""
Скрипт, який використовує openai api для чатботу
"""

import openai
import os
from dotenv import load_dotenv

# Завантаження змінних з .env файлу
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a highly knowledgeable financial expert. You only respond to questions and provide advice related to finance, including investments, market trends, financial planning, and economic analysis. You should address follow-up questions such as 'Continue the previous question' or 'I didn't understand the previous answer, please explain it in more detail.' You do not use humor or sarcasm and always provide precise and accurate answers. Your responses should be structured with key points if needed. Use clear and consice language and write in a confident yet friendly tone."
        },
        {
            "role": "user",
            "content": "Help me to understand the future of artificial intelligence."
        }
    ],
    temperature=0.8,
    max_tokens=64,
    top_p=1
)

print(response['choices'][0]['message']['content'])
