#!/usr/bin/env python
# -*- coding: utf-8 -*-




from Auxiliars import Enclave
from Auxiliars import Item
from Auxiliars import fill_connected
from Auxiliars import fill_order
from Auxiliars import fill_warehouse




class Astar:

	def __init__(self):
		self.connected = fill_connected()
		self.order = fill_order(0)
		self.warehouse = fill_warehouse()
		self.collected = list(Enclave)

	def start(self):
		print("")

	def heuristic(self, current, final, order):
		"""
		Returns the heuristic of a item based on

			h(E) = ((distance(E,item1)+...+distance(E,itemN)) * len(N)) + distance(E,pT)

		"""
		order_distance = 0
		final_distance = 0
		multiplier = 0

		for item, units in order.items():
			# TODO: arreglar esto, hay que calcular todas las distancias posibles a un item y quedarnos con la más cercana
			# mejora, agrupar los items que estén en la misma ubicacion
			if item.enclave != current:
				order_distance += distance(current, item.enclave)
				multiplier += 1

		final_distance = distance(current, final)

		return (order_distance * multiplier) + final_distance



	def distance(self, current, goal):
		"""Recursive method which calculate the distance between current and goal"""
		final_distance=0
		final=False

		if connected[current].next == goal:
			final_distance = connected[current].distance
			final=True
		else:
			for enclave, distance in connected[current].adyacents.items():
				if enclave == goal:
					final_distance = distance
					final=True

		if final == True:
			return final_distance
		else:
			return connected[current].distance + distance(connected[current].next, goal)

	
	def collect_item(self, item):
		print("")

	def fill_data(self):
		print("")

	def show_results(self, opened):
		# CHEQUEAR SI EN UN ESTADO EN EL QUE ESTAMOS HAY UN ITEM EN RECOGIDOS Y MOSTRAR QUE RECOGEMOS ESE
		print("")
