import random
import copy

class Neural_Network:

	def __init__(self, shape):
		self.shape = shape
		self.network = [[Node(2*random.random()-1) for _ in range(layer)] for layer in shape]
		self.connect_all_random()

	def connect_all_random(self):
		for i in range(len(self.network [:-1])):
				for n in self.network[i+1]:
					for m in self.network[i]:
						n.connect(m, 2*random.random()-1)

	def get_copy(self):
		temp =Neural_Network(self.shape)
		for i in range(len(self.network)):
			for j in range(len(self.network[i])):
				temp.network[i][j].bias = self.network[i][j].bias
				temp.network[i][j].weights = copy.deepcopy(self.network[i][j].weights)
		return temp

	def breed(father, mother, fitness):
		print("breeding")
		t_f = father.get_copy()
		t_m = mother.get_copy()
		child = Neural_Network(t_f.shape)
		for i in range(len(child.network)):
			for j in range(len(child.network[i])):
				if random.random() < .5:
					child.network[i][j].bias = t_f.network[i][j].bias
				else:
					child.network[i][j].bias = t_m.network[i][j].bias
				if random.random() < 1/fitness:
					child.network[i][j].bias *= (6*random.random())-3
				for k in range(len(child.network[i][j].weights)):
					if random.random() < .5:
						child.network[i][j].weights[k] = t_f.network[i][j].weights[k]
					else:
						child.network[i][j].weights[k] = t_f.network[i][j].weights[k]
					if random.random() < 1/fitness:
						child.network[i][j].weights[k] *= (4*random.random())-2
		return child

	def __str__(self):
		ret = ""
		for out in self.network[-1]:
			ret = ret + "\n" + out.__str__()
		return ret + "\n"

	def evaluate(self, inputs):
		#print(inputs)
		for i in range(len(self.network[0])):
			self.network[0][i].bias = inputs[i]
		return [out.evaluate() for out in self.network[-1]]


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
		if summation < 0:
			return 0
		else:
			return 1

	def __str__(self):
		ret = "Bias: " + str(self.bias) + "\n"

		for p in self.preconnected:
			ret = ret + "\n" + p.__str__()

		return ret


def main():
	'''
	nn = Neural_Network([5,3,2,2])
	#print(nn)
	
	nn.network[1][0].weights = [1,-1,0,0,0]
	nn.network[1][1].weights = [0,0,1,-1,0]
	nn.network[1][2].weights = [0,0,0,-1,1]
	nn.network[1][0].bias = 0
	nn.network[1][1].bias = 0
	nn.network[1][2].bias = 0

	nn.network[2][0].weights = [1,1,0]
	nn.network[2][1].weights = [-1,0,-1]
	nn.network[2][0].bias = -2
	nn.network[2][1].bias = 0

	nn.network[3][0].weights = [1,1]
	nn.network[3][1].weights = [-1,-1]
	nn.network[3][0].bias = -1
	nn.network[3][1].bias = 0
	'''
	nn = Neural_Network([2,2])


	
	print("child: ",Neural_Network.breed(nn,nn,1000000))
	nn.network[0][0].bias *= -1
	print("nn: ",nn)



if __name__ == "__main__":
	main()





