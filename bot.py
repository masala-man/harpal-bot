from discord.ext import commands
import discord
import random
from dotenv import load_dotenv
from os import getenv
from cogs.helpers.config import config_helper
import json
load_dotenv()

config_file = config_helper('./conf/global.json')
trigger_file = config_helper('./data/triggers.json')
config = config_file.read()
triggers = trigger_file.read()

default_prefix = config['prefix']['default']
custom_prefix = config['prefix']['custom']

async def determine_prefix(bot, message):
	guild = message.guild
	if guild:
		if str(guild.id) in custom_prefix:
			return custom_prefix[str(guild.id)]
		else:
			return default_prefix
	else:
		return default_prefix

client = commands.Bot(command_prefix=determine_prefix)

@client.event
async def on_ready():
	print('<<CONNECTED>>')

## COG MANAGEMENT ##

@client.group(name="cogs")
async def plugins(ctx):
	if ctx.invoked_subcommand is None:
		desc = "Commands to manage harpal cogs\n\n`&cogs list` : posts a list of all available cogs\n`&cogs load cog` : loads a cog\n`&cogs unload cog` : unloads a cog\n`&cogs` : this screen"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@plugins.command(name='list')
@commands.has_role(config['manager'])
async def list_cogs(ctx):
	cog_list_embed = discord.Embed(title="Active Cogs", description=f"{' , '.join(active_extensions)}", color=0x3CC73E)
	await ctx.send(embed=cog_list_embed)
	cog_list_embed = discord.Embed(title="Inactive Cogs", description=f"{' , '.join(inactive_extensions)}", color=0xEB4934)
	await ctx.send(embed=cog_list_embed)

@plugins.command(name='load')
@commands.has_role(config['manager'])
async def load_cogs(ctx, cog_name):
	client.load_extension("cogs.{}".format(cog_name))
	await ctx.send("Added `{}`".format(cog_name))
	active_extensions.append(inactive_extensions.pop(inactive_extensions.index(cog_name)))

@plugins.command(name='unload')
@commands.has_role(config['manager'])
async def unload_cogs(ctx, cog_name):
	client.unload_extension("cogs.{}".format(cog_name))
	await ctx.send("Removed `{}`".format(cog_name))
	print("removed {}".format(cog_name))
	inactive_extensions.append(active_extensions.pop(active_extensions.index(cog_name)))

## SETTINGS

@client.group(name="settings")
async def settings(ctx):
	if ctx.invoked_subcommand is None:
		desc = "Core settings\n\n`&settings manager role` : sets the role that is allowed to manage all bot functions\n`&settings prefix yourprefix` : sets the bot's prefix (& by default)"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@settings.command()
@commands.guild_only()
@commands.has_role(config['manager'])
async def prefix(ctx, prefix):
	custom_prefix[ctx.guild.id] = prefix
	await ctx.send(f"Prefix set to `{prefix}`")
	config_file.write(config)

@settings.command()
@commands.has_permissions(administrator=True)
async def manager(ctx, role: discord.Role):
	config['manager'] = role.id
	config_file.write(config)

# TRIGGERS

@client.group(name="trigger")
async def trigger(ctx):
	if ctx.invoked_subcommand is None:
		desc = "Auto-responses based on a specific trigger\n\n`&trigger add \"word\" \"the response\"` : adds a trigger to the bot\n`&trigger remove id` : removes the trigger with that id\n`&trigger list` : lists all registered triggers"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@trigger.command()
@commands.has_role(config['manager'])
async def add(ctx, trigger_context, trigger_response):
	trigger = {}
	trigger['context'] = trigger_context
	trigger['response'] = trigger_response
	triggers['triggers'].append(trigger)
	trigger_file.write(triggers)
	await ctx.send("Added trigger")


@trigger.command()
@commands.has_role(config['manager'])
async def remove(ctx, trigger_id):
	triggers['triggers'].pop(int(trigger_id)-1)
	trigger_file.write(triggers)
	await ctx.send("Removed trigger")

@trigger.command()
@commands.has_role(config['manager'])
async def list(ctx):
	desc = ""
	for x in range(len(triggers['triggers'])):
		desc = desc + f"**{x+1}.**\n   Trigger: `{triggers['triggers'][x]['context']}`\n   Response: `{triggers['triggers'][x]['response']}`\n\n"
	embed = discord.Embed(title="Triggers", description=desc, color=0x00f1de)
	await ctx.send(embed=embed)

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
	if isinstance(error, (commands.MissingRequiredArgument)):
		await ctx.send("Ping someone to annoy, wanker `&pingspam @masala_man#4534`")
	else:
		raise error

@client.event
async def on_message(message):
	if client.user.id != message.author.id:
		if "namak" in message.content:
			await message.channel.send("shamak")
			await message.channel.send("namak")
			await message.channel.send("shamak")
			await message.channel.send("daal dete hai")
		for x in range(len(triggers['triggers'])):
			if triggers['triggers'][x]['context'] in message.content:
				await message.channel.send(triggers['triggers'][x]['response'])
	await client.process_commands(message)

initial_extensions = ['cogs.culture', 'cogs.poetry', 'cogs.fun']
active_extensions = []
inactive_extensions = []

if __name__ == '__main__':
	for extension in initial_extensions:
		client.load_extension(extension)
		active_extensions.append(extension[5:])

client.run(getenv("TOKEN"))