from discord.ext import commands
import discord
from .helpers.checks import perms_check
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:80")
db = db_client["harpal-bot"]
db_conf = db['conf']

class utils(commands.Cog, name='utils'):
	def __init__(self, client):
		self.bot = client

	@commands.command(name='avatar')
	@commands.check(perms_check)
	async def avatar(self, ctx, user: discord.Member):
		await ctx.send(user.avatar_url)

	@commands.command(name='id')
	@commands.check(perms_check)
	async def id(self, ctx, user: discord.Member):
		await ctx.send(user.id)

def setup(client):
	if db_conf.find({"_id": "utils"}).count() == 0:
		db_conf.insert_one({
			"_id": "utils",
			"id": {"role": "@everyone"},
			"avatar": {"role": "@everyone"}
			})
		print("utils --> db")
	client.add_cog(utils(client))
	print("added utils")