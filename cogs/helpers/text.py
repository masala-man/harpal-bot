import random

class text_helper():

	def __init__(self):
		pass

	def number_blocks(self, num):
		emotes = {
			" ": "  ",
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
		for x in [chr(x) for x in range(ord('a'), ord('z') + 1)]:
			emotes[x] = f":regional_indicator_{x}:"
		emotized = ""
		for x in range(len(str(num))):
			if str(num)[x] not in emotes:
				continue
			else:
				emotized = emotized + emotes[str(num)[x]]
		return emotized
 
	def mock(self, text, diversity_bias=0.5, random_seed=None):
		# Error handling
		if diversity_bias < 0 or diversity_bias > 1:
			raise ValueError('diversity_bias must be between the inclusive range [0,1]')
		# Seed the random number generator
		random.seed(random_seed)
		# Mock the text
		out = ''
		last_was_upper = True
		swap_chance = 0.5
		for c in text:
			if c.isalpha():
				if random.random() < swap_chance:
					last_was_upper = not last_was_upper
					swap_chance = 0.5
				c = c.upper() if last_was_upper else c.lower()
				swap_chance += (1-swap_chance)*diversity_bias
			out += c
		return out