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

	def mock(self, text): 
		output_text = "" 
		for char in text: 
			if char.isalpha(): 
				if random.random() > 0.5: 
					output_text += char.upper() 
				else: 
					output_text += char.lower() 
			else: 
				output_text += char 
		return output_text