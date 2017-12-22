#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import Astar



def main():
	
	print("EMPIEZA EL JUEGO\n")
	# print(a.warehouse)
	# print(a.connected)

	a = Astar.Astar("pS", "pT")
	# for k,i in a.connected.items():
	# 	print(k, i.next, i.distance)
	# 	for ad in i.adyacents:
	# 		print(" >",ad)

	# print a.distance("pS","pS")
	# print a.distance("s8","pT")

	# a.best_location()
	# a.heuristic( "pS", "pT")
	# a.heuristic( "c1", "pT")
	# a.heuristic( "s1", "pT")

	# a.location = "s2"
	# a.collect_item()
	a.start()


if __name__ == '__main__':
    main()
