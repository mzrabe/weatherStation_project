class DHT22(Exception):
	"""Exception raised for errors in the DHT22 logging process.

	Attributes:
		expression -- input expression in which the error occurred
		message -- explanation of the error
	"""

	def __init__(self, expression, message: str):
		self.expression = expression
		self.message = message
