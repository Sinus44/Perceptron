from Engine import *
import time
import random
from Perceptron import Perceptron

class Game_Scene(Scene):
	def select(self):
		# Settings
		self.rocketW = 4

		# Object initialitaion
		self.nn = Perceptron(3, 0.01)
		self.ball = [random.randint(0, self.window.w - 1), 0]
		self.balls = [[random.randint(0, self.window.w - 1), 0], [random.randint(0, self.window.w - 1), 0]]
		self.racket = [self.window.w // 3, self.window.h - 1]

		# Sys vars
		self.y = 0
		self.score = 0
		self.force = False
		self.enterPrevState = False
		self.escPrevState = False

	def update(self):
		self.res = self.nn.predict([self.balls[0][0] / self.window.w, self.balls[0][1] / self.window.h, self.racket[0] / self.window.w])
		
		if self.res > 0.5:
			if self.racket[0] + self.rocketW < self.window.w:
				self.racket[0] += 1
			
		else:
			if self.racket[0] > 0:
				self.racket[0] += -1
		
		self.y += 1
		self.balls[0][1] += self.y % 2
		self.balls[1][1] += self.y % 2

		if self.balls[0][1] == self.racket[1]:
			self.balls[0][1] = 0
			
			if self.racket[0] <= self.balls[0][0] <= self.racket[0] + self.rocketW:
				self.score += 1
			else:
				if self.racket[0] + self.rocketW < self.balls[0][0]:
					self.nn.learnNoLearer(1)
					
				elif self.racket[0] > self.balls[0][0]:
					self.nn.learnNoLearer(-1)
			
			self.balls[1][1] = self.window.h // 2
			self.balls[0][0] = self.balls[1][0]
			self.balls[0][1] = self.balls[1][1]
			self.balls[1] = [random.randint(0, self.window.w - 1), 0]

	def draw(self):
		for event in self.window.input_tick():
			if event["type"] == "exit":
				self.window.close()
				quit()

			if event["type"] == "keyboard":
				if event["key_code"] == 13:
					if event["key_state"] == 1:
						if self.enterPrevState == 0:
							with open("nn.w", "w") as file:
								out = ""
								for w in self.nn.w:
									out += str(w) + "\n"
								file.write(out)
					self.enterPrevState = event["key_state"]

				elif event["key_code"] == 27:
					if event["key_state"] == 1:
						if self.escPrevState == 0:
							weights = open("nn.w", "r").read().split("\n")
							for i in range(len(self.nn.w)):
								self.nn.w[i] = float(weights[i])
					self.escPrevState = event["key_state"]

		self.window.set_title(str(self.score))
		self.window.fill()
		self.window.point(self.balls[0][0], self.balls[0][1], Symbol(char="*"))
		self.window.point(self.balls[1][0], self.balls[1][1], Symbol(char="*"))

		self.window.rect(self.racket[0], self.racket[1], self.rocketW, 1, Symbol(char="-"))
		self.window.print()

class Game:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.window = Window(self.width, self.height)
		self.window.set_title("Neuron example")

		self.scene_control = Scene_Control(update_time=0.1, frame_time=0.1)
		self.scene_control.add("game", Game_Scene(window=self.window, app=self))
		self.scene_control.set('game')

	def run(self):
		self.scene_control.play()


if __name__ == "__main__":

	game = Game(30, 30)
	game.run()