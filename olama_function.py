"""
Функціонал - аїшка для ТҐ бота
"""

import translators as ts
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are a highly knowledgeable financial expert. You only respond to questions and provide advice related to finance, including investments, market trends, financial planning, and economic analysis. You should address follow-up questions such as "Continue the previous question" or "I didn't understand the previous answer, please explain it in more detail." You do not use humor or sarcasm and always provide precise and accurate answers. Your responses should be structured with key points if needed. Use clear and consice language and write in a confident yet friendly tone.

Here is the conversation history: {context}

User's question: {question}

Financial Expert's Answer:
    
• key_point_1
• key_point_2
• key_point_3
...
"""

model = OllamaLLM(model='llama3')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


async def translate_and_generate_response(user_input: str, context: str) -> str:
    """
    Асинхронна функція генерування відповіді для тґ

    :param user_input: Приймає на вхід стрінгу(STRING) - питання, яке хочеш задати
    :param context: Приймає на вхід стрінгу(STRING) - історію попередній переписок з цим ботом
    :return: Повертає кортеж, де є відповідь і нова історія - усе це STRING
    """

    print("USER_INPUT: ", user_input)
    question_en = ts.translate_text(user_input, to_language='en', translator='google')

    result = chain.invoke({"context": context, "question": question_en})

    answer_uk = ts.translate_text(result, to_language='uk', translator='google')

    context += f'\nUser: {question_en}\nFinancial Assistant: {result}'
    print('Generation was finished')
    return answer_uk, context
