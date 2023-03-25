# Creating a Discord Chatbot using Python
## Prerequisites

* A Discord account
* A server where you have administrator privileges
* Python 3 installed on your computer

## Creating a Discord Bot

* Go to the Discord Developer Portal and create a new application.
* Give your application a name and click on "Create".
* Go to the "Bot" section in the left-hand menu and click on "Add Bot".
* Customize your bot's display name and avatar, if desired.
* Copy the bot token.

## Writing the Bot script

* Create a new Python script and import the Discord API module.
* Paste the bot token into the script and use it to create a new instance of the discord.Client class.
* Use the @bot decorator to define functions that will handle events such as when the bot is ready or when a message is received.
* Write your bot's functions using the @bot.command to get the commands executed with the command prefix defined
* To make the bot answer just to the author of the message in private you can send the ctx with author flag

## Adding the Bot to the server

* Go to the Discord Developer Portal and select your application.
* Go to the "OAuth2" section in the left-hand menu and select the "bot" scope.
* Select the permissions you want your bot to have and copy the generated URL.
* Paste the URL into your web browser and select the server where you want to add the bot.

## Running the Bot

Run the script using the python command.
    
    python path/to/file/botfile.py
    
Verify that the bot is online by checking the Discord server where it was added.
