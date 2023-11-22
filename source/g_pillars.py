import pandas as pd
import openai, os
from utils.pillars import user_message


def get_completion_from_messages(
    messages, model="gpt-3.5-turbo-16k", temperature=0, max_tokens=500
):
    response = openai.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message["content"]  # type: ignore


def classification(text):
    try:
        mssg = user_message(text)
        response = get_completion_from_messages(mssg)
        return response
    except:
        return None
