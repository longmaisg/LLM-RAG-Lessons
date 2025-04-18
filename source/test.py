from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
cl.instrument_openai()
# how to run: chainlit run -w test.py

settings = {
    "model": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    "temperature": 0.7,
    # ... more settings
}

@cl.on_message
async def on_message(message: cl.Message):
    input = message.content
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are expert in making jokes."},
            {"role": "user", "content": input}
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
