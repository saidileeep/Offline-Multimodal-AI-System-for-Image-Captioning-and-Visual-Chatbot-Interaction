import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def answer_question(question, objects, counts, summary_text):

    print("CHAT QUESTION:", question)
    print("CHAT COUNTS:", counts)

    # -------- Build image context --------
    visual_context = f"""
Detected object counts:
{counts}

Detected object details:
{objects}
"""

    # -------- Prompt for Ollama --------
    prompt = f"""
You are an intelligent multimodal AI assistant.

You receive object detection data from an image.

If the question is about the image:
Use ONLY the detected objects provided.

If the question is general knowledge:
Answer normally.

Keep answers short and clear.

Image detection data:
{visual_context}

User Question: {question}

Answer:
"""

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if response.status_code != 200:
            print("OLLAMA ERROR:", response.text)
            return {
                "answer": "AI model returned an error."
            }

        result = response.json()

        print("OLLAMA RESPONSE:", result)

        answer = result.get("response")

        if answer:
            answer = answer.strip()

        if not answer:
            answer = "I could not generate a response."

        return {
            "answer": answer
        }

    except requests.exceptions.ConnectionError:
        return {
            "answer": "Cannot connect to local AI model. Make sure Ollama is running."
        }

    except Exception as e:
        print("CHATBOT ERROR:", e)

        return {
            "answer": "Error connecting to local AI model."
        }