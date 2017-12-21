#!/usr/bin/env python
# -*- coding: utf-8 -*-









class Item:
	def __init__(self, name, enclave, units):
		self.name = name
		self.enclave = enclave
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
	place1 =  ["c1", "c2", 10, {"s1":5, "s5": 5}]
	place2 =  ["c2", "c3", 10, {"s2":5, "s6": 5}]
	place3 =  ["c3", "c4", 10, {"s3":5, "s7": 5}]
	place4 =  ["c3", "pT", 10, {"s4":5, "s8": 5}]
	
	place5 =  ["pS", "c1", 10,{}]
	place6 =  ["s1", "c1", 5, {}]
	place7 =  ["s2", "c2", 5, {}]
	place8 =  ["s3", "c3", 5, {}]
	place9 =  ["s4", "c4", 5, {}]
	place10 = ["s5", "c1", 5, {}]
	place11 = ["s6", "c2", 5, {}]
	place12 = ["s7", "c3", 5, {}]
	place13 = ["s8", "c4", 5, {}]
	
	all_places = [ place1, place2, place3, place4, place5, place6, place7, place8, place9, place10, place11, place12, place13 ]
	
	for place in all_places:
		enclave = place[1]
		distance = place[2]
		adyacents = dict()
		for en, dis in place[3].items():
			adyacents[en] = dis
		connected[place[0]] = Enclave(next, distance, adyacents)

	return connected


def fill_warehouse():
	"""Fill a dictionary with the content of the warehouse"""
    item1 = Item("patatas","s1",200)
    item2 = Item("melones","s1",100)
    item3 = Item("boligrafos","s2",500)
    item4 = Item("boligrafos","s3",400)
    item5 = Item("melocotones","s4",200)
    item6 = Item("berzas","s4",100)
    item7 = Item("papeles","s5",500)
    item8 = Item("boligrafos","s6",400)
    item9 = Item("patatas","s1",200)
    item10 = Item("melones","s1",100)
    item11 = Item("plumas","s7",500)
    item12 = Item("plumas","s8",400)
    item13 = Item("colonias","s3",150)
    item14 = Item("ratones","s4",210)

    items = [ item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14 ]

	warehouse = dict()
	for item in items:
		if not warehouse[item.name]:
			warehouse[item.name] = list()
		warehouse[item.name].append(item)

	return warehouse

def fill_order(num_items):
	print("")
	return list(Item)





















