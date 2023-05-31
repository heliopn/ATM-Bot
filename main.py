import os
import discord
from discord.ext import commands
import requests
import urllib.parse
import sqlite3
from bs4 import BeautifulSoup


# Get the values of the DATABASE_URL and API_KEY variables
token = os.getenv("TOKEN")
bot_key = os.getenv("PUBLIC_KEY")
client_id = os.getenv("CLIENT_ID")

# Define your bot intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True

# Create client for Discord
bot = commands.Bot(intents=intents,command_prefix="!")

# TURN ON API 
base_url = "https://api.trace.moe"

crawler_url = 'http://localhost:5000'

data = {
	'url': 'https://www.example.com/',
	'query': 'domain'
}

def format_message(urls, ids):
	embed = discord.Embed(title="Crawler Results", color=0x00ff00)
	for i in range(len(urls)):
		embed.add_field(name=f"URL {i+1}", value=urls[i], inline=False)
		embed.add_field(name=f"Task ID {i+1}", value=ids[i], inline=False)
	return embed

def format_error(type_err):
	embed = discord.Embed(title=f"{type_err} Error", color=0x00ff00)
	embed.add_field(name=f"Too much arguments. You can't make more them 3 {type_err.lower()} at once.", inline=False)
	return embed

def format_status(ids, status):
	embed = discord.Embed(title="Crawl Status", color=0x00ff00)
	for i in range(len(ids)):
		embed.add_field(name=f"Task ID {i+1}", value=ids[i], inline=False)
		embed.add_field(name=f"Status {i+1}", value=status[i], inline=False)
	return embed

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
	await ctx.author.send("""
	ATM Bot - https://github.com/heliopn/ATM-Bot/
	
	RedCrow(Crawler api) - https://github.com/heliopn/red_crow
	""")

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
	list_ids = []
	for i in args:
		# if len(args)>3:
		# 	break
		url = crawler_url + '/crawl'
		data['url'] = i
		response = requests.post(url, json=data)
		if response.status_code == 202:
			response_data = response.json()
			if isinstance(response_data, dict):
				task_id = response_data.get('task_id')
				if task_id:
					list_ids.append(task_id)
				else:
					print('Task ID not found in response data.')
			else:
				print('Invalid response data type:', type(response_data))
		else:
			print('Request failed with status code:', response.status_code)
	# if len(args)>3:
	# 	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	# 	formatted_message = format_error("Crawler")
	# else:
	# 	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	formatted_message = format_message(args, list_ids)
	await ctx.author.send(embed=formatted_message)

@bot.command(
	help="Looks like you need some help.",
	brief="This command can show you the status a list of Crawlers."
)
async def status(ctx, *args):
	list_status = []
	for i in args:
		if len(args)>3:
			break
		url = crawler_url + '/crawl/status/' + i
		response = requests.get(url, json=data)
		if response.status_code == 202:
			response_data = response.json()
			if isinstance(response_data, dict):
				status_r = response_data.get('status')
				if status_r:
					list_status.append(status_r)
				else:
					print('Status or URL not found in response data.')
			else:
				print('Invalid response data type:', type(response_data))
		else:
			print('Request failed with status code:', response.status_code)
	
	if len(args)>3:
		# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
		formatted_message = format_error("Status")
	else:
		# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
		formatted_message = format_status(args,list_status)
	await ctx.author.send(embed=formatted_message)

@bot.command(
	help="Looks like you need some help.",
	brief="""
	This command can search terms inside all saved pages.
	You can add a parameter -t followed by a number between -1 and 1, where 1 = good content and -1 = bad content
	"""
)
async def search(ctx, *args):
	# Get the last argument and store it in a separate variable
	if len(args)>=2 and args[-2]=="-t":
		threshold = args[-1]
		data['threshold'] = str(threshold)
		# Remove the last argument from args
		args = args[:-2]
	res = "Nothing"
	url = crawler_url + '/search'
	data['query'] = " ".join(args)
	response = requests.get(url, json=data)
	if response.status_code == 202:
		response_data = response.json()
		if isinstance(response_data, dict):
			result = response_data.get('result')
			if result:
				res = result
			else:
				print('Result not found in response data.')
		else:
			print('Invalid response data type:', type(response_data))
	else:
		print('Request failed with status code:', response.status_code)
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(res)

@bot.command(
	help="Looks like you need some help.",
	brief="""
	This command can search terms inside all saved pages.
	You can add a parameter -t followed by a number between -1 and 1, where 1 = good content and -1 = bad content
	"""
)
async def wn_search(ctx, *args):
	if len(args)>=2 and args[-2]=="-t":
		threshold = args[-1]
		data['threshold'] = str(threshold)
		# Remove the last argument from args
		args = args[:-2]
	res = "Nothing"
	url = crawler_url + '/wn_search'
	data['query'] = " ".join(args)
	response = requests.get(url, json=data)
	if response.status_code == 202:
		response_data = response.json()
		if isinstance(response_data, dict):
			result = response_data.get('result')
			if result:
				res = result
			else:
				print('Result not found in response data.')
		else:
			print('Invalid response data type:', type(response_data))
	else:
		print('Request failed with status code:', response.status_code)
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(res)

""" GENERATE COMMAND """
@bot.command(
	help="Generates content based on a search query.",
	brief="""
	This command can search terms inside all saved pages.
	You can add a parameter -t followed by a number between -1 and 1, where 1 = good content and -1 = bad content.
	After getting site contente it generates a new sentense.
	"""
)
async def generate(ctx, *args):
	if len(args)>=2 and args[-2]=="-t":
		threshold = args[-1]
		data['threshold'] = str(threshold)
		# Remove the last argument from args1
		args = args[:-2]
	res = "Nothing"
	url = crawler_url + '/generate'
	data['query'] = " ".join(args)
	response = requests.get(url, json=data)
	if response.status_code == 202:
		response_data = response.json()
		if isinstance(response_data, dict):
			result = response_data.get('result')
			if result:
				res = result
			else:
				print('Result not found in response data.')
		else:
			print('Invalid response data type:', type(response_data))
	else:
		print('Request failed with status code:', response.status_code)
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(res)

""" GENERATE COMMAND WITH CHATGPT """
@bot.command(
	help="Generates content with ChatGPT based on a search query.",
	brief="""
	This command can search terms inside all saved pages.
	You can add a parameter -t followed by a number between -1 and 1, where 1 = good content and -1 = bad content.
	After getting site contente it generates a new sentense using ChatGPT.
	"""
)
async def chatgpt(ctx, *args):
	if len(args)>=2 and args[-2]=="-t":
		threshold = args[-1]
		data['threshold'] = str(threshold)
		# Remove the last argument from args1
		args = args[:-2]
	res = "Nothing"
	url = crawler_url + '/chatgpt'
	data['query'] = " ".join(args)
	response = requests.get(url, json=data)
	if response.status_code == 202:
		response_data = response.json()
		if isinstance(response_data, dict):
			result = response_data.get('result')
			if result:
				res = result
			else:
				print('Result not found in response data.')
		else:
			print('Invalid response data type:', type(response_data))
	else:
		print('Request failed with status code:', response.status_code)
	# SENDS A MESSAGE TO THE author USING THE CONTEXT OBJECT.
	await ctx.author.send(res)

bot.run(token)
