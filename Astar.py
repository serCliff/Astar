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

	def __init__(self, initial_location, final_location):
		self.location = initial_location
		self.final = final_location
		self.connected = fill_connected()
		self.order = fill_order(0)
		self.warehouse = fill_warehouse()
		self.collected = list()

	def start(self):

	    # The set of nodes already evaluated				
	    closedSet = list()

	    # The set of currently discovered nodes that are not evaluated yet.
	    # Initially, only the start node is known.
	    openSet = list() 
	    openSet.append(self.location)

	    # For each node, which node it can most efficiently be reached from.
	    # If a node can be reached from many nodes, cameFrom will eventually contain the
	    # most efficient previous step.
	    cameFrom = list()

	    # For each node, the cost of getting from the start node to that node.
	    gScore = self.fill_gscore(self.location)


	    # The cost of going from start to start is zero.
	    # gScore[start] := 0

	    # For each node, the total cost of getting from the start node to the goal
	    # by passing by that node. That value is partly known, partly heuristic.
	    fScore = self.fill_fscore()
		

	    # # For the first node, that value is completely heuristic.
	    # fScore[start] := heuristic_cost_estimate(start, goal)


	    while openSet:


	    	print("OPEN SET: "+str(openSet))
	        self.location = self.get_current(openSet, fScore)
	        print("Opening: "+ self.location+"\n")
	        self.collect_item()

	        cameFrom.append(self.location)

	        if self.location == self.final:
	            return self.reconstruct_path(cameFrom, self.location)

	        openSet = list()
	        closedSet.append(self.location)

	        neighbors_of_current = self.get_neighbors(self.location)

	        for neighbor in neighbors_of_current:
	            
	            # if neighbor in closedSet:
	            #     continue		# Ignore the neighbor which is already evaluated.

	            
	            if neighbor not in openSet:	# Discover a new node
	                openSet.append(neighbor)
	            
	            # The distance from start to a neighbor
	            # the "dist_between" function may vary as per the solution requirements.

	            
	            tentative_gScore = gScore[self.location] + self.distance(self.location, neighbor) 

	            if tentative_gScore >= gScore[neighbor]:
	                continue		# This is not a better path.

	            #WITH THIS PROBLEM NEVER CONTNIUE BECAUSE ONLY THERE ARE ONE PATH TO GET THE NEXT NODE
	            # This path is the best until now. Record it!
	            # cameFrom[neighbor] = self.location
	            gScore[neighbor] = tentative_gScore
	            fScore[neighbor] = gScore[neighbor] + self.heuristic(neighbor)

	    return False

	
	def get_neighbors(self, current_location):
		
		print("GETTING NEIGHBORS OF "+ current_location)
		neighbors = list()
		neighbors.append(self.connected[current_location].next)

		if len(self.connected[current_location].adyacents) > 0:
			for neighbor in self.connected[current_location].adyacents.keys():
				neighbors.append(neighbor)

		print(neighbors)
		print
		return neighbors

	def get_current(self, openSet, fScore):
		
		# print("get current: "+str(openSet))
		fScore = self.fill_fscore()
		
		selected = ""
		lowest_fScore = self.heuristic("pS") # MAX POSSIBLE FSCORE 
		
		for item in openSet:
			# print("fscore de:" + item + ": "+str(fScore[item]) + " <= "+str(lowest_fScore))
			if fScore[item] <= lowest_fScore and fScore[item] >= 0:
				selected = item
				lowest_fScore = fScore[item]

		# print("SELECTED: ",selected)

		return selected

	def fill_gscore(self, current_location):
		# print("\n*** gSCORE ***")
		

		gscore = dict()
		for place in self.connected.keys():
			gscore[place] = self.distance(current_location, place)

		gscore[self.final] = self.distance(current_location, self.final)
		return gscore
	
	def fill_fscore(self):

		# print("\n\n### FSCORE ###")
		fscore = dict()

		for place in self.connected.keys():
			# print("\n------------------------FSCORE", place)
			fscore[place] = self.heuristic(place)

		fscore[self.final] = 10
		return fscore

	def heuristic(self, current):
		"""
		Returns the heuristic of a item based on

			h(E) = ((distance(E,item1)+...+distance(E,itemN)) * len(N)) + distance(E,pT)

		"""
		order_distance = 0
		final_distance = 0
		multiplier = 0

		#CALCULATE THE BEST LOCATION OF ALL ITEMS (Only the first time)
		if len(self.order) > 0:
			if self.order[0].location == "":
				self.best_location() # Calculate the best location of all items of our order
				print("THAT IS THE BEST LOCATION OF OUR ORDER ITEMS\n")


		#CALCULATE THE HEURISTIC
		for item in self.order:
			if item.location != current:
				# print("orders")
				order_distance += self.distance(current, item.location)
				multiplier += 1

		# print("final")
		final_distance = self.distance(current, self.final)
		result = (order_distance * multiplier) + final_distance

		# print("h("+str(current)+") = ("+str(order_distance)+" * "+str(multiplier)+") + "+str(final_distance) +" = "+str(result))
		return result



	def distance(self, current, goal):
		"""Recursive method which calculate the distance between current and goal"""
		final_distance=0
		final=False

		# print("DISTANCE: current: " + current+ ", next: "+ self.connected[current].next+ " goal: " + goal)
		if current == goal:
			return final_distance

		if self.connected[current].next == self.final and self.final != goal:
			return -100
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

		print("\nTAKING THE BEST LOCATION")
		locations = dict()
		if self.order[0].location == "":
			
			#Group items on enclaves to choose the able locations
			for item in self.order:
				for warehouse_item in self.warehouse[item.name]:
					if item.units < warehouse_item.units:
						if not warehouse_item.location in locations:
							locations[warehouse_item.location] = list()
						locations[warehouse_item.location].append(item.name)
					else:
						print("NO HAY SUFICIENTES UNIDADES DE: " + item.name +" EN: "+warehouse_item.location)

			
			#Choose the best options for all items
			while locations:
				max_len = 0
				max_loc = ""
				for loc, items in locations.items():
					# print(loc, len(items), items)
					

					if len(items) >= max_len:
						# If the location is equals than the best location, choose the nearest location, to start
						if max_loc == "":
							max_len = len(items)
							max_loc=loc
						elif self.distance(self.location, loc) < self.distance(self.location, max_loc):
							max_len = len(items)
							max_loc=loc
				
				# print
				# print(max_loc + " and "+ str(max_len))	
				# print(pretty(locations))
				
				
				to_delete = list() # list of locations collocated to delete of the best locations
				if max_len > 1: 
				# if len is one, all locations are separated, choose nearest location
				#Select the best location of each item
					for item in locations[max_loc]:
						for product in self.order:
							if product.name == item and product.location == "":
								product.location = max_loc
								to_delete.append(item)

				else: 
					#For any product without asigned enclave, choose the nearest enclave of all
					for product in self.order:
						best_enclave = ""
						
						if product.location == "":
							# print("Empty enclave of: ", product.name)

							for enclave, loc in locations.items():
								if len(loc) > 0:
									# print(enclave, ">>>", best_enclave)
									if product.name == loc[0]:

										if best_enclave == "":
											best_enclave = enclave
										else:
											if self.distance(self.location, enclave) < self.distance(self.location, best_enclave):
												best_enclave = enclave
										# print("Best enclave: ",best_enclave)
										to_delete.append(loc[0])
								else:
									del locations[loc]
							product.location = best_enclave

				#DELETE CHOSEN ENCLAVES
				for item_d in to_delete:
					for k, v in locations.items():
						if item_d in v:
							v.remove(item_d)
						if len(v) == 0:
							del locations[k]
				
				# print(pretty(locations))

			#Delete the orders that can't be delivered due at haven´t enough resources
			have_no_resources = list()
			for item in self.order:
				if item.location == "":
					have_no_resources.append(item)
			for item in have_no_resources:
				print("\nDeleted ("+str(item.name)+") due the warehouse don´t have enough resources of it\n")
				self.collected.append(item)
				self.order.remove(item)

			self.print_order()

				
			


	def collect_item(self):
		"""Check if we are in the location of any product and collect the product"""

		# print("\nBefore collect items")
		# self.print_order()

		for item in self.order:
			if item.location == self.location:
				self.collected.append(item)

		for item in self.collected:
			if item in self.order:
				self.order.remove(item)

		# print("After collect items")
		# self.print_order()
		# print



	def reconstruct_path(self, cameFrom, current):
		# CHEQUEAR SI EN UN ESTADO EN EL QUE ESTAMOS HAY UN ITEM EN RECOGIDOS Y MOSTRAR QUE RECOGEMOS ESE
		for route in cameFrom:
			print(route)
			



	def print_order(self):
		for i in self.order:
			print(i.name+": location ("+i.location+"), units: "+str(i.units))
		# print("")

	
















