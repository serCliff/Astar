#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

import Astar



def main():
	
	# print("EMPIEZA EL JUEGO\n")
	# print(a.warehouse)
	# print(a.connected)
	val= randint(1,20)
	a = Astar.Astar(initial_location="pS", final_location="pT", num_items=val)
	# for k,i in a.connected.items():
	# 	print(k, i.next, i.distance)
	# 	for ad in i.adyacents:
	# 		print(" >",ad)

	# print a.distance("pS","pS")
	# print a.distance("s8","pT")
	# print a.distance("pS","s8")

	# a.best_location()
	# a.heuristic( "pS", "pT")
	# a.heuristic( "c1", "pT")
	# a.heuristic( "s1", "pT")

	# a.location = "s2"
	# a.collect_item()
	a.start()


if __name__ == '__main__':
    main()
