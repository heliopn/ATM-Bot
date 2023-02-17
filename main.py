import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import requests
import urllib.parse

# Load the environment variables from the .env file
load_dotenv()

# Get the values of the DATABASE_URL and API_KEY variables
token = os.getenv('TOKEN')
bot_key = os.getenv('PUBLIC_KEY')
client_id = os.getenv('CLIENT_ID')

# Define your bot intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True

# Create client for Discord
bot = commands.Bot(intents=intents,command_prefix="!")

# TURN ON API 
base_url = "https://api.trace.moe"

# ON_MESSAGE() EVENT LISTENER. NOTICE IT IS USING @BOT.EVENT AS OPPOSED TO @BOT.COMMAND().
@bot.event
async def on_message(message):
	# CHECK IF THE MESSAGE SENT TO THE CHANNEL IS "HELLO".
	if message.content == "hello":
		# SENDS A MESSAGE TO THE CHANNEL.
		await message.channel.send("pies are better than cakes. change my mind.")

	# INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
	await bot.process_commands(message)

@bot.command(
	help="Looks like you need some help.",
	brief="This command say to you the project's github."
)
async def source(ctx, *args):
	await ctx.channel.send("https://github.com/heliopn/ATM-Bot/")

@bot.command(
	help="Looks like you need some help.",
	brief="This command can search for a anime moment using a URL image"
)
async def rewind(ctx, *args):
	response = requests.get(base_url+"/search?url={}"
    .format(urllib.parse.quote_plus(args[0]))
    )
	# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
	await ctx.channel.send(response.json()['result'][0]['video'])

bot.run(token)
