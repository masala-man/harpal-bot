import discord
import pymongo
from discord.utils import get

db_client = pymongo.MongoClient("mongodb://localhost:80")
db = db_client["harpal-bot"]
db_conf = db['conf']

def perms_check(ctx):
	cog = ctx.command.cog
	parent = ctx.command.parent
	command = ctx.command.name
	if cog is None:
		cog = "core"
	else:
		cog = cog.qualified_name
	query = db_conf.find_one({"_id": cog})
	if parent is None:
		role = query[command]['role']
	else:
		role = query[parent.name][command]['role']
	if role == "all" or role == "@everyone":
		return True
	if get(ctx.guild.roles, id=role) in ctx.message.author.roles:
		return True
	else:
		return False