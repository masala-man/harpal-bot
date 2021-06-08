import discord
from discord.ext import commands
from .helpers.text import text_helper
from .helpers.checks import perms_check
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["harpal-bot"]
db_conf = db['conf']

class fun(commands.Cog, name='fun'):
	def __init__(self, client):
		self.bot = client
		self.text = text_helper()

	@commands.command(name='clap')
	@commands.check(perms_check)
	async def clap(self, ctx, sentence, emote: discord.Emoji=None):
		if emote is None:
			emote = ":clap:"
		sentence = sentence.replace(" ", f"{emote}{emote}{emote}")
		await ctx.send(sentence)

	@clap.error
	async def clap_error(self, ctx, error):
		if not perms_check(ctx) == False:
			await ctx.send("`&clap \"this is a sentence\"`\nor\n`&clap \"This is a sentence\" :emote:`")
	
	@commands.command(name='mock')
	@commands.check(perms_check)
	async def mock(self, ctx, sentence):
		await ctx.send(self.text.mock(sentence))

	@mock.error
	async def mock_error(self, ctx, error):
		if not perms_check(ctx) == False:
			await ctx.send("`&mock This is a sentence`")

	@commands.command(name='shout')
	@commands.check(perms_check)
	async def shout(self, ctx, sentence, channel: discord.TextChannel=None):
		if channel is None:
			channel = ctx.channel
		await channel.send(self.text.number_blocks(sentence))
	
	@shout.error
	async def shout_error(self, ctx, error):
		if not perms_check(ctx) == False:
			await ctx.send("`&shout \"this is a sentence\"`\nor\n`&shout \"This is a sentence\" #channel`")

	@commands.command(name='say')
	@commands.check(perms_check)
	async def say(self, ctx, sentence, channel: discord.TextChannel=None):
		if channel is None:
			channel = ctx.channel
		await channel.send(sentence)
	
	@say.error
	async def say_error(self, ctx, error):
		if not perms_check(ctx) == False:
			await ctx.send("`&say \"this is a sentence\"`\nor\n`&say \"This is a sentence\" #channel`")

def setup(client):
	if db_conf.find({"_id": "fun"}).count() == 0:
		db_conf.insert_one({
			"_id": "fun",
			"clap": {"role": "@everyone"},
			"mock": {"role": "@everyone"},
			"shout": {"role": "@everyone"},
			"say": {"role": "@everyone"}
			})
		print("fun --> db")
	client.add_cog(fun(client))
	print("added fun")