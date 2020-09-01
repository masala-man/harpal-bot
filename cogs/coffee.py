from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import random
from .helpers.checks import perms_check
from .helpers.text import text_helper
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:80")
db = db_client["harpal-bot"]
db_conf = db['conf']

class coffee(commands.Cog, name='coffee'):
	def __init__(self, client):
		self.bot = client
		self.data = db['data']
		if self.data.find({"_id": "coffee"}).count() == 0:
			self.data.insert_one({"_id": "coffee", "videos": []})

	@commands.group(name='culture')
	async def culture(self, ctx):
		if ctx.invoked_subcommand is None:
			query = self.data.find_one({"_id": "coffee"})
			link = query['videos'][random.randint(0, (len(query['videos']) - 1))]
			await ctx.send(link)

	@culture.command(name='add')
	@commands.check(perms_check)
	async def add(self, ctx, link):
		self.data.update({"_id": "coffee"},{ "$addToSet": { "videos": link }})
		await ctx.send("Added your pretentious taste")

	@culture.command(name='remove')
	@commands.check(perms_check)
	async def remove(self, ctx, link):
		if link == "last":
			self.data.update({"_id": "coffee"},{ "$pop": { "videos": 1 }})
			await ctx.send("Thank god for that")
		else:
			self.data.update({"_id": "coffee"},{ "$pull": { "videos": link }})
		await ctx.send("It sucked anyway")

	@culture.command(name='list')
	@commands.check(perms_check)
	async def list(self, ctx):
		query = self.data.find_one({"_id": "coffee"})
		desc = ""
		for index, video in enumerate(query['videos']):
			desc += f"**{index+1}**.\n{video}\n\n"
		embed = discord.Embed(title="PP's Taste", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

	@culture.command(name='help')
	@commands.check(perms_check)
	async def help(self, ctx):
		desc = f"Hindustani cultural imposition toolkit v1.0 \n\n`&culture` : Posts a random link\n`&culture add link` : Adds link\n`&culture remove id` : removes link with that id\n`&culture list` : Posts a embed listing all links with their ids\n`&culture help` : This screen"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

	@commands.command(name='pingspam')
	@commands.check(perms_check)
	async def pingspam(self, ctx, user: discord.Member):
		await ctx.channel.send(user.display_name)
		await ctx.channel.send('{} {}'.format(user.mention, user.display_name))
		await ctx.channel.send('{} {}'.format(user.display_name, user.mention))
		await ctx.channel.send(user.mention)

	@pingspam.error
	async def pingspam_error(self, ctx, error):
		if isinstance(error, (commands.MissingRequiredArgument)):
			await ctx.send("Ping someone to annoy, wanker `&pingspam @masala_man#4534`")
		else:
			raise error

def setup(client):
	if db_conf.find({"_id": "coffee"}).count() == 0:
		db_conf.insert_one({
			"_id": "coffee",
			"culture": {
				"add": {"role": "@everyone"},
				"remove": {"role": "@everyone"},
				"list": {"role": "@everyone"},
				"help": {"role": "@everyone"},
			},
			"pingspam": {"role": "@everyone"}
			})
		print("coffee --> db")
	client.add_cog(coffee(client))
	print("added coffee")