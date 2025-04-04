import requests
import json


def sendRequest(model, question):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {"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"}",
            "HTTP-Referer": "test-app",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "test-app",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": f"{question}"
                }
            ],
            "max_tokens": 10000
        })
    )
    return response.json()


def requestDeepSeek(question, mode="question", documents=None):
    model = 'deepseek/deepseek-r1:free'
    match mode:
        case "question":
            req = sendRequest(model, question)
            return req['choices'][0]['message']['content']
        case "document":
            documentsText = ""
            for i in documents:
                documentsText += i + "\n"
                with open(i, "r", encoding="utf-8") as f:
                    documentsText += "\n".join(f.readlines())
                documentsText += '\n'
            prefixToQuestion = f"Посмотри текст следующих документов и ответь на вопрос.\n {documentsText}\n"
            req = sendRequest(model, prefixToQuestion + question)
            return req['choices'][0]['message']['content']

"""
print(requestDeepSeek("Подробно скажи что там написано?", "document", ["test.txt"]))
"""
