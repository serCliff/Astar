#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from Auxiliars import Enclave
from Auxiliars import Item
from Auxiliars import fill_connected
from Auxiliars import fill_order
from Auxiliars import fill_warehouse

def pretty(data):
	return json.dumps(data, sort_keys=True, indent=3, separators=(',', ': '))


class Astar:

	def __init__(self):
		self.connected = fill_connected()
		self.order = fill_order(0)
		self.warehouse = fill_warehouse()
		self.collected = list()

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

		if self.connected[current].next == goal:
			final_distance = self.connected[current].distance
			final=True
		else:
			for enclave, dist in self.connected[current].adyacents.items():
				if enclave == goal:
					final_distance = dist
					final=True

		if final == True:
			return final_distance
		else:
			return self.connected[current].distance + self.distance(self.connected[current].next, goal)

	
	def best_location(self):
		"""
		Set the best location of all items
			It thinks on:
				- nearest location
				- location with multiple items

		"""
		locations = dict()
		if self.order[0].enclave == "":
			
			#Group items on enclaves
			for item in self.order:
				for warehouse_item in self.warehouse[item.name]:
					if item.units < warehouse_item.units:
						if not warehouse_item.enclave in locations:
							locations[warehouse_item.enclave] = list()
						locations[warehouse_item.enclave].append(item.name)
					else:
						print("NO HAY SUFICIENTES: " + item.name)

			# print(pretty(locations))
			
			#Choose the best options for all items
			while locations:
				max_len = 0
				max_loc = ""
				for loc, items in locations.items():
					if len(items) > max_len:
						max_len = len(items)
						max_loc=loc
				
				print
				print(max_loc + " and "+ str(max_len))	
				print(pretty(locations))
				
				#TODO: Diferenciar cuando max_len es == 1 y coger de los elementos iguales aquellos cuya distancia sea más cercana
				# Por ejemplo recorrer e ir almacenando siempre y cuando la nueva distancia sea menor

				# if max_len > 1: # if len is one all locations are separated, choose nearest location
				#Select the best location of each item
				to_delete = list() 
				for item in locations[max_loc]:
					for product in self.order:
						if product.name == item and product.enclave == "":
							product.enclave = max_loc
							to_delete.append(item)

				for item_d in to_delete:
					for k, v in locations.items():
						if item_d in v:
							v.remove(item_d)
						if len(v) == 0:
							del locations[k]
				
				print(pretty(locations))
				


			
			self.print_order()
				



	def collect_item(self, item):
		print("")

	def fill_data(self):
		print("")

	def show_results(self, opened):
		# CHEQUEAR SI EN UN ESTADO EN EL QUE ESTAMOS HAY UN ITEM EN RECOGIDOS Y MOSTRAR QUE RECOGEMOS ESE
		print("")


	def print_order(self):
		for i in self.order:
			print(i.name+": location ("+i.enclave+"), units: "+str(i.units))
		print("")
















