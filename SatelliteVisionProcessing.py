# Projeto Final
# Componentes
# • Samuel Ferreira Gomes
# • Ibson Costa Suassuna
# • kayllane Cândida

import pygame
import math
from queue import PriorityQueue
from PIL import Image
import cv2
import numpy as np
import serial 
import time
import pygame.camera
import pygame.image
Arduino = serial.Serial('com4', 115200)

robot = []
movement = []



	





WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Algorítmo de melhor caminho A*")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)



class Spot: #Nodes/spots
	# métodos
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self): # dá a posição
		return self.row, self.col

	def is_closed(self): # já foi analisado?
		return self.color == RED

	def is_open(self): # Está sendo analisado?
		return self.color == GREEN

	def is_barrier(self): # bool é barreira?
		return self.color == BLACK

	def is_start(self): # bool é inicial?
		return self.color == ORANGE

	def is_end(self): # bool é final?
		return self.color == TURQUOISE

	def reset(self): # reseta quadrado
		self.color = WHITE

	def make_start(self): # torna início
		self.color = ORANGE

	def make_closed(self): # torna node já analisado
		self.color = RED

	def make_open(self): # torna node sendo analisado
		self.color = GREEN

	def make_barrier(self): #torna barreira
		self.color = BLACK

	def make_end(self): # torna final
		self.color = TURQUOISE

	def make_path(self): # torna caminho final
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid): 
		# adição dos visinhos não barreiras em uma lista
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2): # heurística
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def reconstruct_path(came_from, current, draw, pq):

	while current in came_from:
		current = came_from[current] #passando os elementos do dicionário do final para o início
		robot.append(current) #Inserindo os objetos dos quadrados em uma outra lista
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() #heap 
	open_set.put((0, count, start)) #adiciona o quadrado inicial
	came_from = {} # Dicionário do melhor caminho
	g_score = {spot: float("inf") for row in grid for spot in row} # tabela soma pesos sem H
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row} # tabela soma pesos com H
	f_score[start] = h(start.get_pos(), end.get_pos())
	open_set_hash = {start}

	while not open_set.empty(): #enquanto a priorityqueue tiver elementos
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] #remove da lista de prioridade e analisa
		open_set_hash.remove(current) #remove do hash

		if current == end: #se o quadrado atual for o objetivo
			reconstruct_path(came_from, end, draw, open_set)
			end.make_end()
			moves(end)
			print("cheguei")
			return True

		for neighbor in current.neighbors: #Analisa os vizinhos
			temp_g_score = g_score[current] + 1 

			if temp_g_score < g_score[neighbor]: #Se quadrado atual for caminho mais eficiente para vizinho
				came_from[neighbor] = current # inserir quadrado atual no indice do dicionário do vizinho
				g_score[neighbor] = temp_g_score #atualizar valor do peso sem H
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) #Peso Com H
				if neighbor not in open_set_hash: #Se vizinho não está na fila de prioridade
					count += 1 # +1 para fila
					open_set.put((f_score[neighbor], count, neighbor)) #vizinho entra com peso com H
					open_set_hash.add(neighbor) # vizinho entra no hash
					neighbor.make_open() # vizinho está na fila = verde
		draw()

		if current != start:
			current.make_closed() #quadrado já analisado vira vermelho

	return False #se não der caminho para o final.


def make_grid(rows, width): #transforma todo x,y em node
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width): #produz as linhas do grid
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width): #everry frame action
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)


	draw_grid(win, rows, width)
	pygame.display.update()

'''		
def get_clicked_pos(pos, rows, width): # identifica qual node clicado
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap
	print(row)
	print(col)
	print('\n')
	#retorne o x, y do node dividido pelo tamanho dos quadrados 
	return row, col 
'''		

#------------------------------------------------------------------------------------------------------------------

#Mecanismo de processamento de informações visuais para Arduino.
def moves(end):
	robot.reverse() #Inverte a lista
	for i in range(0, len(robot)): #Analisa cada quadrado na lista
		if i > 0:
			if robot[i-1].row < robot[i].row: #right
				print("right\n")
				Arduino.write("right\r".encode()) #envia para o Arduino
			if robot[i-1].row > robot[i].row: #left
				print("left\n")
				Arduino.write("left\r".encode()) #envia para o Arduino
			if robot[i-1].col < robot[i].col: #down
				print("down\n")
				Arduino.write("down\r".encode()) #envia para o Arduino
			if robot[i-1].col > robot[i].col: #up
				print("up\n")
				Arduino.write("up\r".encode()) #envia para o Arduino
	if robot[len(robot)-1].row < end.row: #right
		print("right\n")
		Arduino.write("right\r".encode()) #envia para o Arduino
	if robot[len(robot)-1].row > end.row: #left
		print("left\n")
		Arduino.write("left\r".encode()) #envia para o Arduino
	if robot[len(robot)-1].col < end.col: #down
		print("down\n")
		Arduino.write("down\r".encode()) #envia para o Arduino
	if robot[len(robot)-1].col > end.col: #up
		print("up\n")
		Arduino.write("up\r".encode()) #envia para o Arduino
		


#-----------------------------------------------------------------------------------------------------------------------

def main(win, width): #Controle central
	ROWS = 6 # quantidade de Nodes
	grid = make_grid(ROWS, width)

	start = grid[0][5]
	end = grid[5][0]
	
	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get(): # procura por eventos
			if event.type == pygame.QUIT: # X superiorDireito clicado
				run = False
			'''		
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos() #x,y do mouse
				row, col = get_clicked_pos(pos, ROWS, width)


				spot = grid[row][col]


				if not start and spot != end:

					#verf se inicio n colocado e se n é o final
					start = spot
					start.make_start() # coloque inicio

				elif not end and spot != start:
					# verificando se final já foi colocado
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					#se inicio e final já clicado, e n é ambos, BARREIRA
					spot.make_barrier()
			'''		
			'''			
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
			'''							

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print("chegueiespaço")
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					
					print("cheguei lambda")
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_p:
					pygame.camera.init()
					cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(1280,720))
					cam.start()
					time.sleep(3)
					webcamImage = cam.get_image()
					pil_string_image = pygame.image.tostring(webcamImage,"RGBA",False)
					im = Image.frombytes("RGBA",(1280,720),pil_string_image)
					threshold = 57
					img_threshold = im.point(lambda x: 255 if x > threshold else 0)
					img_threshold = img_threshold.convert("1")
					img_threshold.show()
					px = img_threshold.load()


					grid[0][5].make_start
					grid[5][0].make_end
					
					if(px[556, 646]!=255):
						grid[1][5].make_barrier()
					if(px[693, 649]!=255):
						grid[2][5].make_barrier()
					if(px[830, 650]!=255):
						grid[3][5].make_barrier()
					if(px[960, 650]!=255):
						grid[4][5].make_barrier()
					if(px[1100, 650]!=255):
						grid[5][5].make_barrier()

						
					if(px[430, 510]!=255):
						grid[0][4].make_barrier()
					if(px[561, 514]!=255):
						grid[1][4].make_barrier()
					if(px[692, 516]!=255):
						grid[2][4].make_barrier()
					if(px[823, 518]!=255):
						grid[3][4].make_barrier()
					if(px[950, 518]!=255):
						grid[4][4].make_barrier()
					if(px[1090, 518]!=255):
						grid[5][4].make_barrier()
					
					if(px[444, 386]!=255):
						grid[0][3].make_barrier()
					if(px[566, 390]!=255):
						grid[1][3].make_barrier()
					if(px[694, 390]!=255):
						grid[2][3].make_barrier()
					if(px[820, 388]!=255):
						grid[3][3].make_barrier()
					if(px[950, 392]!=255):
						grid[4][3].make_barrier()
					if(px[1082, 388]!=255):
						grid[5][3].make_barrier()

					if(px[449, 271]!=255):
						grid[0][2].make_barrier()
					if(px[574, 267]!=255):
						grid[1][2].make_barrier()
					if(px[700, 270]!=255):
						grid[2][2].make_barrier()
					if(px[825, 300]!=255):
						grid[3][2].make_barrier()
					if(px[944, 273]!=255):
						grid[4][2].make_barrier()
					if(px[1077, 275]!=255):
						grid[5][2].make_barrier()

					
					if(px[464, 153]!=255):
						grid[0][1].make_barrier()
					if(px[582, 154]!=255):
						grid[1][1].make_barrier()
					if(px[700, 157]!=255):
						grid[2][1].make_barrier()
					if(px[823, 157]!=255):
						grid[3][1].make_barrier()
					if(px[943, 159]!=255):
						grid[4][1].make_barrier()
					if(px[1070, 157]!=255):				
						grid[5][1].make_barrier()

					if(px[470, 50]!=255):
						grid[0][0].make_barrier()
					if(px[588, 52]!=255):
						grid[1][0].make_barrier()
					if(px[702, 49]!=255):
						grid[2][0].make_barrier()
					if(px[819, 53]!=255):
						grid[3][0].make_barrier()
					if(px[935, 51]!=255):
						grid[4][0].make_barrier()
					draw(win, grid, ROWS, width)
					

					
					print(px[556, 646])
					print(px[693, 649])
					print(px[830, 650])
					print(px[960, 650])
					print(px[1100, 650])

					print(px[430, 510])
					print(px[561, 514])
					print(px[692, 516])
					print(px[823, 518])
					print(px[950, 518])
					print(px[1090, 518])

					print(px[444, 386])
					print(px[566, 390])
					print(px[694, 390])
					print(px[820, 388])
					print(px[950, 392])
					print(px[1082, 388])

					print(px[449, 271])
					print(px[574, 267])
					print(px[700, 270])
					print(px[825, 300])
					print(px[944, 273])
					print(px[1077, 275])

					print(px[464, 153])
					print(px[582, 154])
					print(px[700, 157])
					print(px[823, 157])
					print(px[943, 159])
					print(px[1070, 157])

					print(px[470, 50])
					print(px[588, 52])
					print(px[702, 49])
					print(px[819, 53])
					print(px[935, 51])
					print(px[1063, 52])

	pygame.quit()

main(WIN, WIDTH)
