import openai
from db import getPostContentById

openai.api_key = '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'

def createPost(prompt:str) :
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )
    return completion.choices[0].text