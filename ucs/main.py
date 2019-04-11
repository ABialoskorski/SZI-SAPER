import time
from ucs.graph import *
from ucs.priority_queue import *
import random
from neuralNetwork.imagerec import whatBombIsThis, createExamples
from mapGeneratorPygame.dataRandomGenerator import getTime, getCost
from decisionTree.decisionTree import build_default_tree, simple_classify
import cv2
from mapGeneratorPygame.setBomb import printBombAndPos
import sys

graphNodes = []

posList = []
randWeightList = []
# Ścieżka do danych tekstowych dla AI
exPath = '../neuralNetwork/numArEx.txt'
# Ścieżka do bazy przykładów dla AI
bombsPath = '../neuralNetwork/images/bombs/'
priority = []
bombType = []
bombTypeOnly = []
bombArr = printBombAndPos()
bombProp = bombArr[0]
mapMatrix = bombArr[1]
img_rgb = []
bombsForUCS = []
counter, counterText = [], []

def returnMapWithBombs():
    for i in range(10):
        bombsForUCS.append((bombProp[i][0], bombProp[i][1], bombProp[i][2]))
    return bombsForUCS, mapMatrix, bombProp

bombMaps = returnMapWithBombs()[0]
bombMatrix = returnMapWithBombs()[1]

def treeAndNeuralNetwork():
	for i in range(10):
		image = cv2.imread(bombProp[i][3])
		resized_image = cv2.resize(image, (250, 250))
		img_rgb.append(resized_image)

	createExamples(bombsPath, exPath)
	tree = build_default_tree()

	for i in range(10):
		whatBombIsIt = whatBombIsThis(bombProp[i][3], exPath)
		bombType.append((whatBombIsIt, getTime(whatBombIsIt), getCost(whatBombIsIt), bombProp[i][2], bombProp[i][4], bombProp[i][5]))
		cv2.imshow('Sprawdzana bomba', img_rgb[i])
		cv2.waitKey(1500)
		bombTypeOnly.append(whatBombIsIt)
		print('Progres skanowania pola minowego: ', 10 * len(bombType), '%')

	for row in bombType:
		priorityVal = simple_classify(row, tree)
		priority.append(priorityVal)
		print(row, ' => ', priorityVal)
		counter.append(row[1])
		if row[1] != sys.maxsize:
			counterText.append(str(row[1]).rjust(2))
		else:
			counterText.append(str('').rjust(2))

def run(graph, key_node_start, key_node_goal, verbose=False, time_sleep=0):
	if key_node_start not in graph.getNodes() or key_node_goal not in graph.getNodes():
		print('Error: key_node_start \'%s\' or key_node_goal \'%s\' not exists!!' % (key_node_start, key_node_goal))
	else:
		# UCS uses priority queue, priority is the cumulative cost (smaller cost)
		queue = PriorityQueue()

		# expands initial node

		# get the keys of all successors of initial node
		keys_successors = graph.getSuccessors(key_node_start)

		# adds the keys of successors in priority queue
		for key_sucessor in keys_successors:
			weight = graph.getWeightEdge(key_node_start, key_sucessor)
			# each item of queue is a tuple (key, cumulative_cost)
			queue.insert((key_sucessor, weight), weight)


		reached_goal, cumulative_cost_goal = False, -1
		while not queue.is_empty():
			# remove item of queue, remember: item of queue is a tuple (key, cumulative_cost)
			key_current_node, cost_node = queue.remove() 
			if(key_current_node == key_node_goal):
				reached_goal, cumulative_cost_goal = True, cost_node
				break

			if verbose:
				# shows a friendly message
				print('Expands node \'%s\' with cumulative cost %s ...' % (key_current_node, cost_node))
				graphNodes.append((key_current_node, cost_node))
				time.sleep(time_sleep)

			# get all successors of key_current_node
			keys_successors = graph.getSuccessors(key_current_node)

			if keys_successors: # checks if contains successors
				# insert all successors of key_current_node in the queue
				for key_sucessor in keys_successors:
					cumulative_cost = graph.getWeightEdge(key_current_node, key_sucessor) + cost_node
					queue.insert((key_sucessor, cumulative_cost), cumulative_cost)

		if(reached_goal):
			print('\nReached goal! Cost: %s\n' % cumulative_cost_goal)
			cv2.destroyAllWindows()

		else:
			print('\nUnfulfilled goal.\n')
			cv2.destroyAllWindows()

def graphBuild():
	treeAndNeuralNetwork()
	# build the graph...
	# adds nodes in the graph
	graph = Graph()


	graph.addNode((0, 0))
	posList.append([0, 0, 1, 1])

	for i in range(10):
		graph.addNode((bombMaps[i][0], bombMaps[i][1]))
		posList.append([bombMaps[i][0], bombMaps[i][1], (bombMaps[i][0] + bombMaps[i][1]) * priority[i], bombProp[i][2]])

	graph.addNode((9, 9))

	posList.sort(key=lambda x: x[2])

	posList.append([9, 9, 1, 15])

	# linking the nodes
	# 0 -> 1 | 0 -> 2 | 0 -> 3
	graph.connect((posList[0][0], posList[0][1]), (posList[1][0], posList[1][1]), posList[1][2])
	graph.connect((posList[0][0], posList[0][1]), (posList[2][0], posList[2][1]), posList[2][2])
	graph.connect((posList[0][0], posList[0][1]), (posList[3][0], posList[3][1]), posList[3][2])

	# 1 -> 2 | 1 -> 4 | 1 -> 5
	graph.connect((posList[1][0], posList[1][1]), (posList[2][0], posList[2][1]), posList[2][2])
	graph.connect((posList[1][0], posList[1][1]), (posList[4][0], posList[4][1]), posList[4][2])
	graph.connect((posList[1][0], posList[1][1]), (posList[5][0], posList[5][1]), posList[5][2])

	# 2 -> 3 | 2 -> 6 | 2 -> 7
	graph.connect((posList[2][0], posList[2][1]), (posList[3][0], posList[3][1]), posList[3][2])
	graph.connect((posList[2][0], posList[2][1]), (posList[6][0], posList[6][1]), posList[6][2])
	graph.connect((posList[2][0], posList[2][1]), (posList[7][0], posList[7][1]), posList[7][2])

	# 3 -> 8 | 3 -> 9
	graph.connect((posList[3][0], posList[3][1]), (posList[8][0], posList[8][1]), posList[8][2])
	graph.connect((posList[3][0], posList[3][1]), (posList[9][0], posList[9][1]), posList[9][2])

	# 4 -> 5
	graph.connect((posList[4][0], posList[4][1]), (posList[5][0], posList[5][1]), posList[5][2])

	# 9 -> 10
	graph.connect((posList[9][0], posList[9][1]), (posList[10][0], posList[10][1]), posList[10][2])

	#10 -> 11
	graph.connect((posList[10][0], posList[10][1]), (posList[11][0], posList[11][1]), posList[11][2])

def returnTreeWithWeight():
	graphBuild()
	return bombType, graphNodes, posList, priority, bombProp, mapMatrix, counter, counterText, bombTypeOnly

