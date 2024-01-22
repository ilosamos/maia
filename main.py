"""Running a simple prompt"""
from maia.openai.llm import chat

if __name__ == "__main__":
    prompt = "Hi who are you and what can you do?"
    print(chat(prompt))
