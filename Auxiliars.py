#!/usr/bin/env python
# -*- coding: utf-8 -*-


from  random import randint




class Item:
	def __init__(self, name, location, units):
		self.name = name
		self.location = location
		self.units = units


class Enclave:

	def __init__(self, next, distance, adyacents):
		self.next = next
		self.distance = distance
		self.adyacents = adyacents # dictionary[enclave, distance]



def fill_connected():
	"""Fill a dictionary with all connections of the map"""
	connected = dict()
	
	# place=  current next distance adyacents
	all_places = [ 
		["c1", "c2", 10, {"s1":5, "s5": 5}],
		["c2", "c3", 10, {"s2":5, "s6": 5}],
		["c3", "c4", 10, {"s3":5, "s7": 5}],
		["c4", "pT", 10, {"s4":5, "s8": 5}],
		["pS", "c1", 10,{}],
		["pT", "c4", -10,{}],
		["s1", "c1", 5, {}],
		["s2", "c2", 5, {}],
		["s3", "c3", 5, {}],
		["s4", "c4", 5, {}],
		["s5", "c1", 5, {}],
		["s6", "c2", 5, {}],
		["s7", "c3", 5, {}],
		["s8", "c4", 5, {}]
		]
	
	for place in all_places:
		enclave = place[1]
		distance = place[2]
		adyacents = dict()
		for en, dis in place[3].items():
			adyacents[en] = dis
		connected[place[0]] = Enclave(enclave, distance, adyacents)

	return connected


def fill_warehouse():
	"""Fill a dictionary with the content of the warehouse"""
	

	items = [ 
		Item("patatas","s1",200),
		Item("melones","s1",100),
		Item("boligrafos","s2",500),
		Item("boligrafos","s3",400),
		Item("melocotones","s4",200),
		Item("berzas","s4",100),
		Item("papeles","s5",500),
		Item("boligrafos","s6",400),
		Item("colonias","s3",150),
		Item("ratones","s4",210),
		Item("plumas","s7",500),
		Item("plumas","s8",400)
		# ,
		# Item("melones","s2",100)
		# Item("patatas","s1",200),
		# Item("melones","s1",100)
	]
	

	warehouse = dict()
	for item in items:
		if not item.name in warehouse:
			warehouse[item.name] = list()
		warehouse[item.name].append(item)

	return warehouse

def fill_order(num_items):

	order = list()

	if num_items == 0: # Comun order
		order = [
			Item("patatas","",40),
			Item("boligrafos","",40),
			Item("plumas","",10)
			# ,Item("papeles", "", 10)
			]
	else:
		warehouse = fill_warehouse()
		for i in range(0, num_items):
			val=randint(0, (len(warehouse)-1))
			item = warehouse.values()[ val ]
			val=randint(0, (len(item)-1))
			product = item[val]
			new_order = Item(product.name, "", randint(int(product.units*0.2), int(product.units*1.2)))
			# print(new_order.name, new_order.units, warehouse[new_order.name][0].units)
			order.append(new_order)

	
	return order





















