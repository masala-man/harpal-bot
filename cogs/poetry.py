from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import json
import requests
import pymongo
from .helpers.checks import perms_check

db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["harpal-bot"]
db_conf = db['conf']

class poetry(commands.Cog, name='poetry'):
	def __init__(self, client):
		self.bot = client
		self.path = "https://poetrydb.org/"

	@commands.group(name='poetry')
	async def poetry(self, ctx):
		if ctx.invoked_subcommand is None:
			ctx.send("testing cog")

	@poetry.command(name='fetch')
	@commands.check(perms_check)
	async def fetch(self, ctx, author, title):
		request_path = self.path + f"author,title/{author};{title}"
		request = requests.get(request_path)
		poem_title = json.loads(request.content)[0]['title']
		poem_lines = json.loads(request.content)[0]['lines']
		desc = ""
		for x in range(10):
			desc += poem_lines[x] + "\n"
		embed = discord.Embed(title=poem_title, description=desc, color=0x00f1de)
		embed.set_author(name=json.loads(request.content)[0]['author'])
		await ctx.send(embed=embed)


def setup(client):
	if db_conf.find({"_id": "poetry"}).count() == 0:
		db_conf.insert_one({
			"_id": "poetry",
			"poetry": {
				"fetch": {"role": "@everyone"}
			}
			})
		print("poetry --> db")
	client.add_cog(poetry(client))
	print("added poetry")