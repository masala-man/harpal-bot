from discord.ext import commands
import discord
import random
from os import getenv
import pymongo
from discord.utils import get
from cogs.helpers.checks import perms_check

db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["harpal-bot"]
db_conf = db["conf"]
db_trig = db["trig"]

if db_conf.find({"_id": "global"}).count() == 0:
	db_conf.insert_one({
		"_id": "global",
		"prefix": {"default": "&", "custom": ""},
		"manager": "",
		"cogs": ["coffee", "fun", "poetry", "utils"]
		}
		)
if db_conf.find({"_id": "core"}).count() == 0:
	db_conf.insert_one({
		"_id": "core",
		"cogs": {
			"load": {"role": ""},
			"unload": {"role": ""},
			"list": {"role": ""}
		},
		"trigger": {
			"add": {"role": ""},
			"remove": {"role": ""},
			"list": {"role": ""}
		},
		"perms": {
			"role": {"role": ""},
		},
		"settings": {
			"prefix": {"role": ""}
		},
		"&help": {"role": ""}
		})

async def determine_prefix(bot, message):
	guild = message.guild
	query = db_conf.find_one({"_id": "global"}, {"prefix": 1})
	if guild:
		if query['prefix']['custom'] != "":
			return query['prefix']['custom']
		else:
			return query['prefix']['default']
	else:
		return query['prefix']['default']

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
@commands.check(perms_check)
async def list_cogs(ctx):
	cog_list_embed = discord.Embed(title="Active Cogs", description=f"{' , '.join(active_extensions)}", color=0x3CC73E)
	await ctx.send(embed=cog_list_embed)
	cog_list_embed = discord.Embed(title="Inactive Cogs", description=f"{' , '.join(inactive_extensions)}", color=0xEB4934)
	await ctx.send(embed=cog_list_embed)

@plugins.command(name='load')
@commands.check(perms_check)
async def load_cogs(ctx, cog_name):
	client.load_extension(f"cogs.{cog_name}")
	await ctx.send(f"Added `{cog_name}`")
	active_extensions.append(inactive_extensions.pop(inactive_extensions.index(cog_name)))

@plugins.command(name='unload')
@commands.check(perms_check)
async def unload_cogs(ctx, cog_name):
	client.unload_extension(f"cogs.{cog_name}")
	await ctx.send(f"Removed `{cog_name}`")
	print(f"removed {cog_name}")
	inactive_extensions.append(active_extensions.pop(active_extensions.index(cog_name)))

## SETTINGS

@client.group(name="settings")
async def settings(ctx):
	if ctx.invoked_subcommand is None:
		desc = "Core settings\n\n`&settings manager role` : sets the role that is allowed to manage all bot functions\n`&settings prefix yourprefix` : sets the bot's prefix (& by default)"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@settings.command()
@commands.check(perms_check)
@commands.guild_only()
async def prefix(ctx, prefix):
	db_conf.update({"_id": "global"}, {"$set": {"prefix": {"custom": prefix, "default": "&"}}})
	await ctx.send(f"Prefix set to `{prefix}`")

@settings.command()
@commands.has_permissions(administrator=True)
async def manager(ctx, role: discord.Role):
	db_conf.update({"_id": "global"}, {"$set": {"manager": role.id}})
	db_conf.update({"_id": "core"},{
	"cogs": {
		"load": {"role": role.id},
		"unload": {"role": role.id},
		"list": {"role": role.id}
	},
	"trigger": {
		"add": {"role": role.id},
		"remove": {"role": role.id},
		"list": {"role": role.id}
	},
	"perms": {
		"role": {"role": role.id},
	},
	"settings": {
		"prefix": {"role": role.id}
	},
	"help": {"role": role.id}
	})
	await ctx.send(f"Manager role set to `{role.name}`")

# TRIGGERS

@client.group(name="trigger")
async def trigger(ctx):
	if ctx.invoked_subcommand is None:
		desc = "Auto-responses based on a specific trigger\n\n`&trigger add \"word\" \"the response\"` : adds a trigger to the bot\n`&trigger remove id` : removes the trigger with specified context\n`&trigger list` : lists all registered triggers"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@trigger.command()
@commands.check(perms_check)
async def add(ctx, trigger_context, trigger_response):
	trigger = {}
	trigger['context'] = trigger_context
	trigger['response'] = trigger_response
	db_trig.insert_one({"context": trigger_context, "response": trigger_response})
	await ctx.send(f"Added trigger for `{trigger_context}`")

@trigger.command()
@commands.check(perms_check)
async def remove(ctx, trigger_context):
	db_trig.remove({"context": trigger_context})
	await ctx.send(f"Removed trigger for `{trigger_context}`")

@trigger.command()
@commands.check(perms_check)
async def list(ctx):
	triggers = db_trig.find()
	desc = ""
	n = 0
	for trigger in triggers:
		desc += f"**{n+1}.**\n   Trigger: `{trigger['context']}`\n   Response: `{trigger['response']}`\n\n"
		n += 1
	embed = discord.Embed(title="Triggers", description=desc, color=0x00f1de)
	await ctx.send(embed=embed)

@client.group(name="perms")
async def perms(ctx):
	if ctx.invoked_subcommand is None:
		desc="Oppressing gamers 101\n\n`&perms role cog command.subcommand role` : restricts command.subcommnd to a role"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

@perms.command(name='role')
@commands.check(perms_check)
async def role(ctx, cog, command, role: discord.Role):
	query = db_conf.find_one({"_id": cog})
	db_conf.update({"_id": cog}, {"$set": {f"{command}.role": role.id}})
	await ctx.send(f'{command} restricted to the {role} role')

@client.event
async def on_message(message):
	if client.user.id != message.author.id:
		if "namak" in message.content:
			await message.channel.send("shamak")
			await message.channel.send("namak")
			await message.channel.send("shamak")
			await message.channel.send("daal dete hai")
		triggers = db_trig.find()
		for trigger in triggers:
			if trigger['context'] in message.content:
				await message.channel.send(trigger['response'].format(mention=message.author.mention))
	await client.process_commands(message)
@client.event
async def on_message_cousin(message):
	if client.user.id != message.author.id:
		if "cousin" in message.content and "konkani" in message.content:
			await message.channel.send("https://cdn.discordapp.com/attachments/647475308819382276/756423027646005268/Screenshot_20200831-091353-1.png")
	await client.process_commands(message)
				       
				       

@client.event
async def on_server_join(ctx):
	for guild in bot.guilds:
		for channel in guild.text_channels:
			if channel.permissions_for(guild.me).say:
				embed = discord.Embed(title="Help", description="Hello!\nSetup with `&settings manager @role`\nHelp with `&help`", color=0x00f1de)
				await ctx.send(embed=embed)
	
initial_extensions = db_conf.find_one({"_id": "global"},{"cogs": 1})['cogs']
active_extensions = []
inactive_extensions = []

if __name__ == '__main__':
	for extension in initial_extensions:
		client.load_extension(f"cogs.{extension}")
		active_extensions.append(extension)

client.run(getenv("DISCORD_TOKEN"))
