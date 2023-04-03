import os
import discord
from discord.ext import commands
import requests
import urllib.parse
import sqlite3
from bs4 import BeautifulSoup
from crawler import Crawler


# Get the values of the DATABASE_URL and API_KEY variables
token = os.getenv("TOKEN")
bot_key = os.getenv("PUBLIC_KEY")
client_id = os.getenv("CLIENT_ID")
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")
db_name = "dbbot"

# Define your bot intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True

# Inicializing the DB Connection
db = Crawler()

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
		await message.author.send("pies are better than cakes. change my mind.")

	# INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
	await bot.process_commands(message)

@bot.command(
	help="Looks like you need some help.",
	brief="This command say to you the project's github."
)
async def source(ctx, *args):
	await ctx.author.send("https://github.com/heliopn/ATM-Bot/")

@bot.command(
	help="Looks like you need some help.",
	brief="This command say my name and my email."
)
async def author(ctx, *args):
	await ctx.author.send("""
	I'm a Helio's creation
	If you want to contact him, send a message to: josehpn@al.insper.edu.br
	""")

@bot.command(
	help="Looks like you need some help.",
	brief="This command can search for a anime moment using a URL image"
)
async def rewind(ctx, *args):
	response = requests.get(base_url+"/search?url={}".format(urllib.parse.quote_plus(args[0])))
	
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(response.json()['result'][0]['video'])

@bot.command(
	help="Looks like you need some help.",
	brief="This command can save pages you send to it."
)
async def crawl(ctx, *args):
	# Fetch the HTML document from the URL
	url = args[0]
	response = db.crawl(url,)
	
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(response)

@bot.command(
	help="Looks like you need some help.",
	brief="This command can search terms inside all saved pages."
)
async def search(ctx, *args):
	query = ' '.join(args)
	response = db.search(query)

	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(response)

@bot.command(
	help="Looks like you need some help.",
	brief="This command can search terms inside all saved pages."
)
async def wn_search(ctx, *args):
	query = ' '.join(args)
	response = db.wn_search(query)
	
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(response)

bot.run(token)
