import monster


class Wave:
	def __init__(self, instructions, path):
		self.instructions = instructions
		self.path = path
		self.ic = 0
		self.counter = 0

	def action(self):
		self.counter += 1
		if self.ic == len(self.instructions):
			return False, None

		monster_type, delay = self.instructions[self.ic]
		if self.counter >= delay:
			self.counter = 0
			self.ic += 1
			return True, monster.Monster(monster_type, self.path)
		return True, None
