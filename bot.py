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

prefix = config['prefix']['default']
client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
	print('<<CONNECTED>>')

## COG MANAGEMENT ##

@client.group(name="cogs")
async def plugins(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send("cogs halp")
		# add help embed

@plugins.command(name='list')
@commands.has_role('Moderator')
async def list_cogs(ctx):
	cog_list_embed = discord.Embed(title="Cog List", description="all the cogs", color=0x00f1de)
	await ctx.send(embed=cog_list_embed)

@plugins.command(name='load')
@commands.has_role('Moderator')
async def load_cogs(ctx, cog_name):
	client.load_extension("cogs.{}".format(cog_name))
	await ctx.send("Added `{}`".format(cog_name))

@plugins.command(name='unload')
@commands.has_role('Moderator')
async def unload_cogs(ctx, cog_name):
	client.unload_extension("cogs.{}".format(cog_name))
	await ctx.send("Removed `{}`".format(cog_name))
	print("removed {}".format(cog_name))

## SETTINGS

@client.group(name="settings")
async def settings(ctx):
	if ctx.invoked_subcommand is None:
 		await ctx.send("Settings help")
		# add helptext

# @settings.command(name='prefix')
# @commands.has_role('Moderator')
# async def prefix(ctx, prefix):
#	pass

## OTHER

@client.command()
async def avatar(ctx, user: discord.Member):
	await ctx.send(user.avatar_url)

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

initial_extensions = ['cogs.culture', 'cogs.poetry', 'cogs.fun']
					  
if __name__ == '__main__':
	for extension in initial_extensions:
		client.load_extension(extension)

client.run(getenv("TOKEN"))