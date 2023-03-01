
from config import TOKEN, OPEN_AI_TOKEN, ORGANIZATION_ID
import logging
import openai
import asyncio
import aiogram
#import aiogram.executor
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import requests



# Set up logging
logging.basicConfig(level=logging.INFO)


# Set up the bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



# Define a handler for the /start command
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await message.answer("Hello! I'm a ChatGPT bot. Send me a message and I'll generate a response for you.")


# Define a handler for text messages
@dp.message_handler(Text(contains='hello'))
async def hello_handler(message: types.Message):
    await message.answer("Hello there!")


# Define a handler for generating responses with ChatGPT
@dp.message_handler()
async def generate_response_handler(message: types.Message):
    # Call your ChatGPT API to generate a response
    response = await generate_response(message.text)

    # Send the generated response to the user
    await message.answer(response)


# Define a function to generate a response using ChatGPT
async def generate_response(input_text: str) -> str:
    # Call your ChatGPT API to generate a response
    url = 'https://api.openai.com/v1/chat/completions'
    #url = 'https://your-chatgpt-api.com/generate'
    data = {'input_text': input_text}
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {OPEN_AI_TOKEN}', 'X-Organization-ID': ORGANIZATION_ID}
    response = requests.post(url, json=data, headers=headers)

    # Check if the API call was successful
    if response.status_code == 200:
        # Extract the generated response from the API response
        generated_text = response.json()['generated_text']
        await generated_text
    else:
        # Raise an exception if the API call failed
        raise Exception(f"Failed to generate response: {response.status_code} {response.reason}")


# Start the bot
def main():
    executor = aiogram.executor.Executor(dispatcher=dp)
    executor.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
