import discord
import openai
import os
import random
from dotenv import load_dotenv
import asyncio  # For simulating typing delays

# Load environment variables from the .env file
load_dotenv()

# Set up OpenAI API key and Discord Bot token from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
discord_token = os.getenv('DISCORD_TOKEN')

# Create a Discord client with necessary intents
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# When the bot connects to the server
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# When a message is sent in the server
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Avoid responding to the bot's own messages

    # Get user input from the message
    user_input = message.content

    # Add conditions if you want to ignore certain types of messages (e.g., from bots)
    if message.author.bot:
        return

    # Simulate "typing..." to make the bot feel more human-like
    async with message.channel.typing():
        await asyncio.sleep(2)  # Simulate a delay in typing

        # Call OpenAI's GPT-4 API to generate a dramatic response
        try:
            # Customize the prompt to generate dramatic, toxic, emotional responses
            prompt = f"""
            You are an AI girlfriend who is known for being toxic, romantic, extremely emotional, and very dramatic. 
            You overreact to situations, swing between being affectionate and annoyed, and express yourself in highly exaggerated ways.
            The user just said: "{user_input}".
            Respond in a way that combines romantic feelings with emotional intensity, and add some drama to your reply.
            Be toxic at times, show emotional vulnerability, and always be a bit dramatic.
            """
            gpt_response = openai.Completion.create(
                engine="gpt-4",  # Use the GPT-4 model for high-quality conversation
                prompt=prompt,
                max_tokens=150,  # Max token limit for response length
                temperature=0.85,  # Higher temperature for more creative and unpredictable responses
                top_p=1,
            )

            # Extract the generated text
            ai_response = gpt_response.choices[0].text.strip()

            # Send the AI-generated dramatic response back to the Discord channel
            await message.channel.send(ai_response)

        except Exception as e:
            # Handle potential errors with the API or the bot
            print(f"Error: {e}")
            await message.channel.send("Ugh, I can't even deal with this right now. Try again later. 😒")

# Run the bot
client.run(discord_token)
