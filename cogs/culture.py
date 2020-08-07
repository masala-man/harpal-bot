from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import random
import json
from .helpers.config import config_helper
from .helpers.text import text_helper

class culture(commands.Cog, name='Kulcha'):
	def __init__(self, client):
		self.bot = client
		self.config = config_helper("./data/music.json")
		self.text = text_helper()

	@commands.group()
	async def culture(self, ctx):
		if ctx.invoked_subcommand is None:
			file = self.config.read()
			link = file['videos'][random.randint(0, (len(file['videos']) - 1))]
			await ctx.send(link)

	@culture.command()
	@commands.has_role('Moderator')
	async def add(self, ctx, link):
		file = self.config.read()
		file['videos'].append(link)
		await ctx.send("Added your pretentious taste")
		self.config.write(file)

	@culture.command()
	@commands.has_role('Moderator')
	async def remove(self, ctx, link):
		file = self.config.read()
		if link == "last":
			del file['videos'][-1]
			await ctx.send("Thank god for that")
		else:
			file['videos'].pop(file['videos'].index(link))
		self.config.write(file)
		await ctx.send("It sucked anyway")

	@culture.command()
	async def list(self, ctx):
		file = self.config.read()
		desc = ""
		for x in range(len(file['videos'])):
			desc = desc + "**{}** {}\n".format(self.text.number_blocks(x+1), file['videos'][x])
		embed = discord.Embed(title="PP's Taste", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

	@culture.command()
	async def help(self, ctx):
		desc = f"Commands to post links randomly from a stored list\n\n`&culture` : Posts a random link\n`&culture add link` : Adds link\n`&culture remove link` : removes link\n`&culture list` : Posts a embed listing all links\n`&culture help` : This screen"
		embed = discord.Embed(title="Help", description=desc, color=0x00f1de)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(culture(client))
	print("added culture")