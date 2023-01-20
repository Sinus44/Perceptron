from random import random

class Perceptron:
	def __init__(self, inputs):
		self.input = [0 for i in range(inputs)]
		self.w = [random() for i in range(inputs + 1)]
		self.sum = 0

	def exp(self, x):
		e = 2.718
		return e ** x

	def derivative(self, x):
		return x * (1 - x)

	def activation(self, x):
		return 1 / (1 + self.exp(-x))

	def predict(self, input):
		self.input = input + [1]
		sum = 0
		for i in range(len(self.input)):
			sum += self.input[i] * self.w[i]
		self.sum = sum
		self.out = self.activation(sum)
		return self.out

	def learn(self, input, out):
		y = self.predict(input)
		err = out - y
		LR = 0.2
		for i in range(len(self.w)):
			self.w[i] += (LR * (err)) * self.input[i]
		return err