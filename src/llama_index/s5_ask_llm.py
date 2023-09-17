import os
import openai
from .s4_find_relevant import find_relevant

openai.api_key = os.environ['OPENAI_API_KEY']


SYSTEM_PROMPT = """
You are a Q&A assistant for developers using LlamaIndex, a data framework for LLM applications to ingest, structure, and access private or domain-specific data.
"""


def ask_llm(question):
    relevant_chunks = find_relevant(question)
    user_prompt = "\n\n".join([
        question,
        "Here are some pieces of code that I thought might be relevant in helping answer this question.",
        "\n---\n".join(relevant_chunks)
    ])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )
    return completion.choices[0].message.content


print(ask_llm("How can I get started with LlamaIndex?"))
