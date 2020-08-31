import motor.motor_asyncio as motor
import asyncio

class db_helper():

	def __init__(self, collection):
		self.client = motor.AsyncIOMotorClient('localhost', 27017)
		self.db = self.client['harpal-bot'][collection] 

	async def get(self, scope, filter=None, projection=None):
		if projection is None:
			projection = {}
		if filter is None:
			

		docs = self.db.test_collection.find()
		docs = await docs.to_list(length=None)
		return docs

loop = asyncio.get_event_loop()
n = db_helper('conf')
x = loop.run_until_complete(n.get({"a": "test"}))
print(type(x))
print(x)