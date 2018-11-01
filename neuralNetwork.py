import random
import copy

class Neural_Network:

	def __init__(self, inputs, outputs, output_funcs, nodes_per_layer):
		self.inputs = inputs
		self.outputs = outputs
		self.output_funcs = output_funcs
		self.nodes_per_layer = nodes_per_layer
		self.hidden = []
		for n in range(len(nodes_per_layer)):
			self.hidden.append([])
			for i in range(nodes_per_layer[n]):
				self.hidden[n].append(Node(2*random.random()-1))

		for out in self.outputs:
			out.bias = 2*random.random() - 1

		self.connect_all_random()

	def fire_test(self):
		for func in self.output_funcs:
			func()

	def connect_all_random(self):
		for out in self.outputs:
			for n in self.hidden[-1]:
				out.connect(n, 2*random.random()-1)

		for i in range(len(self.hidden[:-1])):
			for n in self.hidden[i+1]:
				for m in self.hidden[i]:
					n.connect(m, 2*random.random()-1)

		for inp in self.inputs:
			for n in self.hidden[0]:
				n.connect(inp, 2*random.random()-1)


	@staticmethod
	def breed(mother, father):
		children = []
		for _ in range(4):
			child = Neural_Network(copy.deepcopy(mother.inputs), copy.deepcopy(mother.outputs), mother.output_funcs, mother.nodes_per_layer)

			# Loop through the parameters and pick params for the kid.
			for h in range(len(child.hidden)):
				for n in range(len(child.hidden[h])):
					if random.random() > 0.5:
						child.hidden[h][n] = copy.deepcopy(father.hidden[h][n])
					'''if random.random() < 0.1:
						print("shuffling")
						child.hidden[h] = random.shuffle(child.hidden[h])
					elif random.random() < 0.1:
						r = random.choice(range(len(child.hidden[h])))
						print("random2")
						child.hidden[h][r].weights = random.shuffle(child.hidden[h][r].weights)'''

			for i in range(len(child.outputs)):
				if random.random() > 0.5:
					child.outputs[i] = copy.deepcopy(father.outputs[i])

			child.reconnect()
			children.append(child)

		return children


	def reconnect(self):
		for out in self.outputs:
			out.preconnected = self.hidden[-1]

		for i in range(len(self.hidden[:-1])):
			for n in self.hidden[i+1]:
				n.preconnected = self.hidden[i]

		for n in self.hidden[0]:
			n.preconnected = self.inputs

	def evaluate(self, values):
		for i in range(len(self.inputs)):
			self.inputs[i].set_bias(values[i]) #updates the value of all the inputs

		for o in range(len(self.outputs)): # executes the output functions if the node fires
			if self.outputs[o].evaluate() == 1:
				self.output_funcs[o]()

	def __str__(self):
		string = "\nInputs: "
		for inp in self.inputs:
			string = string + inp.__str__()
		string += "\nHidden: "
		for layer in self.hidden:
			string += "\n"
			for l in layer:
				string = string + l.__str__()
			string += "\n"
		string += "\nOutputs: "
		for out in self.outputs:
			string = string + out.__str__()
		return string

class Node:
	def __init__(self, bias, weights = [], preconnected = []):
		self.bias = bias
		self.weights = copy.deepcopy(weights)
		self.preconnected = copy.deepcopy(preconnected)

	def __repr__(self):
		return Node(bias, weights, preconnected)

	def connect(self, n, weight):
		self.weights.append(weight)
		self.preconnected.append(n)

	def set_bias(self, v):
		self.bias = v

	def evaluate(self):
		"""
		This function returns whether this output should fire or not
		"""
		if len(self.preconnected) == 0:
			# print("nothing connected")
			return self.bias

		summation = 0
		for i in range(len(self.weights)):
			summation += self.weights[i]*self.preconnected[i].evaluate()
		summation += self.bias
		if summation <= 0:
			return 0
		else:
			return 1

	def __str__(self):
		return_string = "\nbias = "+str(self.bias)+"\nconnected to " + str(len(self.preconnected))
		return return_string



def main():
	bx = Node(260)
	by = Node(310)
	mx = Node(270)

	ml = Node(0)
	mr = Node(0)

	inputs_test = [bx, by, mx]
	outputs_test = [ml, mr]

	mousex = 0

	def move_right():
		print("move_right")
		mousex += 1

	def move_left():
		print("move_left")
		mousex -= 1

	output_funcs = [move_left, move_right]



	nn = Neural_Network(inputs_test, outputs_test, output_funcs, [3, 3])

	print(nn)



if __name__ == "__main__":
	main()





