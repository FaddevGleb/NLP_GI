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
            return sendRequest(model, question)
        case "document":
            documentsText = ""
            for i in documents:
                documentsText += i + "\n"
                with open(i, "r", encoding="utf-8") as f:
                    documentsText += "\n".join(f.readlines())
                documentsText += '\n'
            prefixToQuestion = f"Посмотри текст следующих документов и ответь на вопрос.\n {documentsText}\n"
            return sendRequest(model, prefixToQuestion + question)

"""
res = requestDeepSeek("Подробно скажи что там написано?", "document", ["test.txt"])
print(res['choices'][0]['message']['content'])
"""