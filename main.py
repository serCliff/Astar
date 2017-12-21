#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import Astar



def main():
	
	print("Empieza el juego")
	# print(a.warehouse)
	# print(a.connected)

	a = Astar.Astar()
	# for k,i in a.connected.items():
	# 	print(k, i.next, i.distance)
	# 	for ad in i.adyacents:
	# 		print(" >",ad)

	# print a.distance("pS","s2")

	a.best_location()



if __name__ == '__main__':
    main()
