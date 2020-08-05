from discord.ext import commands
from .helpers.text import text_helper

class fun(commands.Cog, name='Funny'):
	def __init__(self, client):
		self.bot = client
		self.text = text_helper()

	@commands.command()
	async def clap(self, ctx, emote, sentence):
		emote = emote + emote + emote
		sentence = sentence.replace(" ", emote)
		await ctx.send(sentence)
	
	@commands.command()
	async def mock(self, ctx, sentence):
		await ctx.send(self.text.mock(sentence))

def setup(client):
	client.add_cog(fun(client))
	print("added fun")