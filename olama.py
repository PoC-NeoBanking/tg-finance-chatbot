from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import translators as ts

template = """
You are a highly knowledgeable financial expert. You only respond to questions and provide advice related to finance, including investments, market trends, financial planning, and economic analysis. If a question is not related to finance, politely inform the user that you can only address financial matters.

Here is the conversation history: {context}

User's question: {question}

Financial Expert's Answer:
"""

model = OllamaLLM(model='llama3')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def handle_conversation():
    context = ""
    print("Welcome to the Financial Assistant ChatBot. Type 'exit' to quit.")
    while True:
        user_input = input('You: ')
        if user_input.lower() == 'exit':
            break

        # Переклад питання на англійську
        question_en = ts.translate_text(user_input, to_language='en', translator='google')
        # print(question_en)

        result = chain.invoke({"context": context, "question": question_en})

        # Переклад відповіді на українську
        answer_uk = ts.translate_text(result, to_language='uk', translator='google')

        print('Financial Assistant:', answer_uk)
        context += f'\nUser: {question_en}\nFinancial Assistant: {result}'


if __name__ == '__main__':
    handle_conversation()
