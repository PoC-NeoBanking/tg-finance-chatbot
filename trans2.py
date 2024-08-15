from transformers import pipeline

# Завантаження моделі для генерації тексту
generator = pipeline('text-generation', model='EleutherAI/gpt-j-6B')

# Prompt для створення фінансового експерта
financial_prompt = """
You are a highly knowledgeable financial expert. You only respond to questions and provide advice related to finance, including investments, market trends, financial planning, and economic analysis. If a question is not related to finance, politely inform the user that you can only address financial matters.

Answer the following question:

Q: What are the best strategies for long-term investment in the stock market?
"""

response = generator(financial_prompt, max_length=150, do_sample=True, temperature=0.7)

print(response[0]['generated_text'])
