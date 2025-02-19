import asyncio
import logging
import sys
from os import getenv
import psycopg2
import re
from aiogram import Bot,Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from openai import OpenAI

conn=psycopg2.connect(database="Vocabulary",user="postgres",host= "localhost",password="@Sai7259",port="5432")

cur = conn.cursor()

cur.execute('''
DROP TABLE My_words;
CREATE TABLE IF NOT EXISTS My_words (
  ID SERIAL PRIMARY KEY,
  Words TEXT ,
  Synonyms TEXT ,
  Sentence TEXT )
  ''')

conn.commit()

TOKEN = "8029409133:AAFWeaFDjXMPoysJ86vMC7Szxy2LxqlRQPo"

client = OpenAI(
  api_key="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"
)



dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)} \n Your SuperBot Here Please paste the text you wanted to covert")


@dp.message(Command("vocab"))
async def vocal_handler(message: Message):
    
    await message.answer("This Feature Will Be Available soon⚡.\n till now stay logged in...")



@dp.message()
async def random_message(message: Message) :
   
    
    try:
        user_input = message.text

        
        completion = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "system",
              "content": """Act as a text simplification expert. Your tasks are:
                1. Rewrite any complex text in simple, easy-to-understand language.
                2. Identify and list all complex keywords with: 
                   - Up to 2 synonyms ( Both synonyms must be inside  ***, ex: ***synonym1, synonym2***)
                   - Use the word in a sentence(sentence must be inside ****, ex: ****sentence****)
                3. Ensure the total output does not exceed 500 characters.
                Present both sections clearly, using simple vocabulary everyone can understand. (use little bit emojis)"""
            },
            {
              "role": "user",
              "content": f"Simplify this text and explain complex terms: {user_input}"
            }
          ]
        )

        # Extract the response
        response = completion.choices[0].message.content

        word = re.findall(r"\*\*([A-Za-z ]+)\*\*", response) #for finding the word including** * *
        synonym = re.findall(r"\*\*\*([A-Za-z, ]+)\*\*\*",response)# synonyms insside # 
        sentence = re.findall(r'''\*\*\*\*([A-Za-z0-9.,'"\-!?() ]+)\*\*\*\*''',response)

        for w in word:
          cur.execute('''INSERT INTO My_words (Words) VALUES (%s);''', (w,))
        
        count=1
        for s in synonym:
          cur.execute(''' UPDATE My_words SET Synonyms = (%s)  WHERE ID = (%s);''',(s,count))
          count=count+1

        countt=1  
        for sent in sentence: 
          cur.execute(''' UPDATE My_words SET Sentence = (%s)  WHERE ID = (%s);''',(sent,countt))
          countt=countt+1 

          
        conn.commit()
        conn.close()
  




        response = response.replace("### ", "")
        #response= response.replace("*","")
        


        # Ensure the response does not exceed 4000 characters
        if len(response) > 4000:
            response = response[:4000]  # Truncate to 4000 characters

        # Send the response back to the user
        await message.answer("wait for a second ⌛")
         
        await message.answer(response,parse_mode=None)

    except Exception as e:
        print(e)  # Print the error for debugging
        await Bot.send_message(message, "An error occurred while processing your request. Please try again later.")



async def main() -> None:
   
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())