from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import discord
import random
import json
from dotenv import load_dotenv
from os import getenv
import os

class culture(commands.Cog, name='Kulcha'):
	def __init__(self, client):
		self.bot = client

	def numberBlocks(self, num):
		emotes = {
			"0": ":zero:",
			"1": ":one:",
			"2": ":two:",
			"3": ":three:",
			"4": ":four:",
			"5": ":five:",
			"6": ":six:",
			"7": ":seven:",
			"8": ":eight:",
			"9": ":nine:"
		}
		emotized = ""
		for x in range(len(str(num))):
			emotized = emotized + emotes[str(num)[x]]
		return emotized

	@commands.group()
	async def culture(self, ctx):
		if ctx.invoked_subcommand is None:
			with open('./music.json') as f:
				file = json.load(f)
			link = file['videos'][random.randint(0, (len(file['videos']) - 1))]
			await ctx.send(link)

	@culture.command()
	@commands.has_role('admin')
	async def add(self, ctx, link):
		with open('./data/music.json', mode='r') as f:
			file = json.load(f)
		if link == "last":
			del file['videos'][-1]
			await ctx.send("Thank god for that")
		else:
			file['videos'].append(link)
			await ctx.send("Added your pretentious taste")
		with open('./data/music.json', mode='w+') as f:
			json.dump(file, f)

	@culture.command()
	@commands.has_role('admin')
	async def remove(self, ctx, link):
		with open('./data/music.json', mode='r') as f:
			file = json.load(f)
		file['videos'].pop(file['videos'].index(link))
		with open('./data/music.json', mode='w+') as f:
			json.dump(file, f)
		await ctx.send("It sucked anyway")

	@culture.command()
	async def list(self, ctx):
		with open('./data/music.json', mode='r') as f:
			file = json.load(f)
		desc = ""
		for x in range(len(file['videos'])):
			desc = desc + "**" + self.numberBlocks(x+1) + "** " + file['videos'][x] + "\n"
		listEmbed = discord.Embed(title="PP's Taste", description=desc, color=0x00f1de)
		await ctx.send(embed=listEmbed)

def setup(client):
	client.add_cog(culture(client))
	print("SETUP COG => CULTURE")