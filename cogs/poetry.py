from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import json
import requests

class poetry(commands.Cog, name='Poemtry'):
	def __init__(self, client):
		self.bot = client
		self.path = "https://poetrydb.org/"

	@commands.group()
	async def poetry(self, ctx):
		if ctx.invoked_subcommand is None:
			ctx.send("testing cog")

	@poetry.command()
	@commands.has_role('Moderator')
	async def fetch(self, ctx, author, title):
		request_path = self.path + "author,title/{};{}".format(author,title)
		print(request_path)
		request = requests.get(request_path)
		print(request)
		poem_title = json.loads(request.content)[0]['title']
		poem_lines = json.loads(request.content)[0]['lines']
		desc = ""
		for x in range(10):
			desc = desc + poem_lines[x] + "\n"
		embed = discord.Embed(title=poem_title, description=desc, color=0x00f1de)
		embed.set_author(name=json.loads(request.content)[0]['author'])
		await ctx.send(embed=embed)


def setup(client):
	client.add_cog(poetry(client))
	print("added poetry")