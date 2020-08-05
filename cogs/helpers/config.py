import json

class config_helper():

	def __init__(self, file_path):
		self.file = file_path

	def read(self):
		file_obj = open(self.file, 'r')
		return json.load(file_obj)

	def write(self, content):
		file_obj = open(self.file, 'w+')
		json.dump(content, file_obj)