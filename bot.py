from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import random
from dotenv import load_dotenv
from os import getenv
import json
load_dotenv()

with open('./conf/global.json') as config_file:
	config = json.load(config_file)

prefix = config['prefix']
client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
	print('<<CONNECTED>>')

@client.command()
async def pingspam(ctx, user: discord.Member):
	await ctx.channel.send(user.display_name)
	await ctx.channel.send('{} {}'.format(user.mention, user.display_name))
	await ctx.channel.send('{} {}'.format(user.display_name, user.mention))
	await ctx.channel.send(user.mention)

@pingspam.error
async def pingspam_error(ctx, error):
	if isinstance(error, (MissingRequiredArgument)):
		await ctx.send("Ping someone to annoy, wanker `{}pingspam @masala_man#4534`".format(prefix))
	else:
		raise error

@client.event
async def on_message(message):
	if client.user.id != message.author.id:
		if 'namak' in message.content:
			await message.channel.send("shamak")
			await message.channel.send("namak")
			await message.channel.send("shamak")
			await message.channel.send("daal dete hai")
	await client.process_commands(message)

initial_extensions = ['cogs.culture']
					  
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(getenv("TOKEN"))