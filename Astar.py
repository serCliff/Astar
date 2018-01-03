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

	def __init__(self, initial_location, final_location, num_items):
		self.location = initial_location
		self.final = final_location
		self.connected = fill_connected()
		self.order = fill_order(num_items)
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
	    cameFrom = dict()

	    # For each node, the cost of getting from the start node to that node.
	    gScore = self.fill_gscore(self.location)


	    # The cost of going from start to start is zero.
	    # gScore[start] := 0

	    # For each node, the total cost of getting from the start node to the goal
	    # by passing by that node. That value is partly known, partly heuristic.
	    fScore = self.fill_fscore(gScore)
		

	    # # For the first node, that value is completely heuristic.
	    # fScore[start] := heuristic_cost_estimate(start, goal)


	    while openSet:

	    	last_location = self.location
	    	# print("OPEN SET: "+str(openSet))
	        self.location = self.get_current(openSet, fScore)
	        # print(" *** OPENING: "+ self.location+" ***\n")
	        self.collect_item()


	        if not self.location in cameFrom:
				cameFrom[self.location]= list()
	        cameFrom[self.location].append(last_location)

	        if self.location == self.final:
	            return self.reconstruct_path(cameFrom, self.location)


	        openSet.remove(self.location)
	        closedSet.append(self.location)

	        neighbors_of_current = self.get_neighbors(self.location)

	        for neighbor in neighbors_of_current:
	            
	            if neighbor in closedSet:
	                continue		# Ignore the neighbor which is already evaluated.

	            
	            if neighbor not in openSet:	# Discover a new node
	                openSet.append(neighbor)
	            
	            
	            # The distance from start to a neighbor
	            # the "dist_between" function may vary as per the solution requirements.
	            tentative_gScore = gScore[self.location] + self.distance(self.location, neighbor)
	            
	            # print(self.location, neighbor, str(tentative_gScore)+" = "+str(gScore[self.location])+" + "+str(self.distance(self.location, neighbor))  )
	            # print(tentative_gScore, gScore[neighbor])

	            if tentative_gScore >= gScore[neighbor]:
	                continue		# This is not a better path.

	            #WITH THIS PROBLEM NEVER CONTNIUE BECAUSE ONLY THERE ARE ONE PATH TO GET THE NEXT NODE
	            # This path is the best until now. Record it!
	            # cameFrom[neighbor] = self.location
	            gScore[neighbor] = tentative_gScore
	            fScore[neighbor] = gScore[neighbor] + self.heuristic(neighbor)
	            # print("NEW FSCORE OF: "+neighbor+" = "+str(fScore[neighbor]))

	    return False

	
	def get_neighbors(self, current_location):
		
		# print("GETTING NEIGHBORS OF "+ current_location)
		neighbors = list()
		neighbors.append(self.connected[current_location].next)

		if len(self.connected[current_location].adyacents) > 0:
			for neighbor in self.connected[current_location].adyacents.keys():
				neighbors.append(neighbor)

		# print(neighbors)
		# print
		return neighbors

	def get_current(self, openSet, fScore):
		
		# print("GET CURRENT BETWEEN: "+str(openSet))
		
		# print("VIEJO: "+pretty(fScore))
		# fScore = self.fill_fscore()
		# print("NUEVO: "+pretty(fScore)+"\n")

		
		selected = ""
		lowest_fScore = fScore[openSet[0]] # MAX POSSIBLE FSCORE 
		
		for item in openSet:
			# print("FSCORE de: " + item + ": "+str(fScore[item]) + " <= "+str(lowest_fScore))
			if fScore[item] <= lowest_fScore:
				selected = item
				lowest_fScore = fScore[item]
				# if fScore[item] == lowest_fScore:
				# 	if self.distance(self.location, item) < self.distance(self.location, selected): 
						


		# print("SELECTED: ",selected)
		# print("")

		return selected

	def fill_gscore(self, current_location):
		# print("\n*** gSCORE ***")
		

		gscore = dict()
		for place in self.connected.keys():
			gscore[place] = self.distance(current_location, place)

		gscore[self.final] = self.distance(current_location, self.final)
		return gscore
	
	def fill_fscore(self, gScore):

		# print("\n\n### FSCORE ###")
		fscore = dict()

		for place in self.connected.keys():
			fscore[place] = gScore[place] + self.heuristic(place)
			# print("\n------------------------FSCORE: "+ place+": "+str(fscore[place])+" = "+str(gScore[place])+" + "+str(self.heuristic(place)))

		# fscore[self.final] = 10
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
				print("THAT IS THE BEST LOCATION OF OUR ORDERED ITEMS\n")


		#CALCULATE THE HEURISTIC
		for item in self.order:
			if item.location != current:
				# print("orders")
				new_distance = self.distance(current, item.location)
				
				if new_distance < 0:
					new_distance = self.distance(item.location, current)

				order_distance += new_distance
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

		if self.connected[current].next == goal:
			final_distance = self.connected[current].distance
			final=True
		else:
			for enclave, dist in self.connected[current].adyacents.items():
				if enclave == goal:
					final_distance = dist
					final=True

		if self.connected[current].next == self.final and self.final != goal and final == False:
			#IF WANT TO GET A PAST STATE, RETURNS NEGATIVE VALUE TO TRY REVERSE DISTANCE 
			return -100

		if final == True:
			return final_distance
		else:
			new_distance = self.distance(self.connected[current].next, goal)
			if new_distance < 0:
				new_distance = self.distance(goal, self.connected[current].next)
			return self.connected[current].distance + new_distance

	
	def best_location(self):
		"""
			Set the best location of all items
				It thinks on:
					- nearest location
					- location with multiple items
		"""

		self.print_warehouse()
		print("")
		self.print_order()
		print("\n#################################")
		print("TAKING THE BEST LOCATION")
		print("#################################")
		locations = dict()
		if self.order[0].location == "":
			
			#Group items on enclaves to choose the able locations
			for item in self.order:
				for warehouse_item in self.warehouse[item.name]:
					if item.units < warehouse_item.units:
						if not warehouse_item.location in locations:
							locations[warehouse_item.location] = list()
						locations[warehouse_item.location].append(item.name)
						warehouse_item.units = warehouse_item.units - item.units
					# else:
						# print("HAVN`T ENOUGH UNITS OF: " + item.name +" IN: "+warehouse_item.location)

			
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
				print("DELETED ("+str(item.name)+") due the warehouse don´t have enough resources of it")
				self.collected.append(item)
				self.order.remove(item)

			self.print_warehouse()
			print("")
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





	def reconstruct_path(self, cameFrom, current):
		# CHEQUEAR SI EN UN ESTADO EN EL QUE ESTAMOS HAY UN ITEM EN RECOGIDOS Y MOSTRAR QUE RECOGEMOS ESE
		
		
		

		start=0
		total_distance=0
		path = list()
		# print(pretty(cameFrom))

		while cameFrom:
			path.append(current)
			last = cameFrom[current]
			current = last.pop()
			
			if current == "pS":
				path.append(current)
				path.reverse()
				cameFrom = dict()

		
		print("\n### PATH WALKED ###")
		for i in range(len(path)-1):
			distance = 0
			# if self.connected[path[i]].next == path[i+1]:
			# 	distance = self.connected[path[i]].distance
			# else:
			# 	for item, dis in self.connected[path[i]].adyacents.items():
			# 		if item == path[i+1]:
			# 			distance = dis

			distance = self.distance(path[i], path[i+1])
			total_distance+=distance

			print(path[i] +" -> "+ path[i+1]+" ("+str(distance)+"m.)")
			
			for product in self.collected:
				if path[i+1] == product.location:
					print("WE COLLECT: "+product.name)

		print("TOTAL WALKED  ("+str(total_distance)+"m.) ")

	def print_order(self):
		print("--- ORDER ("+str(len(self.order))+" products) ---")
		for i in self.order:
			print(i.name+": ("+i.location+"), units: "+str(i.units))
		# print("")

	def print_warehouse(self):
		print("--- WAREHOUSE ---")
		for list_i in self.warehouse.values():
			for i in list_i:
				print(i.name+": ("+i.location+"), units: "+str(i.units))
		# print("")

	
















