import discord
from discord.ext import commands
from .helpers.text import text_helper

class fun(commands.Cog, name='Funny'):
	def __init__(self, client):
		self.bot = client
		self.text = text_helper()

	@commands.command()
	async def clap(self, ctx, sentence, emote: discord.Emoji=None):
		if emote is None:
			emote = ":clap:"
		emote = emote + emote + emote
		sentence = sentence.replace(" ", emote)
		await ctx.send(sentence)

	@clap.error
	async def clap_error(self, ctx, error):
		await ctx.send("`&clap \"this is a sentence\"`\nor\n`&clap \"This is a sentence\" :emote:`")
	
	@commands.command()
	async def mock(self, ctx, sentence, *args):
		for ar in args:
			sentence = f"{sentence} {ar}"
		await ctx.send(self.text.mock(sentence))

	@mock.error
	async def mock_error(self, ctx, error):
		await ctx.send("`&mock This is a sentence`")

	@commands.command()
	async def shout(self, ctx, sentence, channel: discord.TextChannel=None):
		if channel is None:
			channel = ctx.channel
		await channel.send(self.text.number_blocks(sentence))
	
	@shout.error
	async def shout_error(self, ctx, error):
		await ctx.send("`&shout \"this is a sentence\"`\nor\n`&shout \"This is a sentence\" #channel`")

	@commands.command()
	async def say(self, ctx, sentence, channel: discord.TextChannel=None):
		if channel is None:
			channel = ctx.channel
		await channel.send(sentence)
	
	@say.error
	async def say_error(self, ctx, error):
		await ctx.send("`&say \"this is a sentence\"`\nor\n`&say \"This is a sentence\" #channel`")

def setup(client):
	client.add_cog(fun(client))
	print("added fun")