#!/usr/bin/env python

from __future__ import print_function
import wx
# Import Neo4j modules
from py2neo import neo4j, cypher
from generateFacts_solutions import *
from generateDataComponent import generateData
from generateConfiguration import generateFigure
from macro import graph_db, node_root

import subprocess
import random
import math
import string
import sys

listChar = []
string.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def getNewPointName():
    char = None
    while True:
        char = random.choice(string.letters)
        if char in listChar:continue
        else:
            listChar.append(char)
            break
    return char
#End Of Function

#Creating a file which contains all the data
fo = open("data.txt", "wb")
#fo.write( "Writing data to be passed to CHR\n")
fo.close()
fo = open("data.txt", "a")


def writeToFile(objectName, relationName, objectName1 = None, value=0):
	if relationName == "KD1":
		global fo
		fo.write("triangle("+ objectName1[0].lower()+objectName1[0] + "," + objectName1[1].lower()+objectName1[1]+","+objectName1[2].lower() +objectName1[2]+"),\n")
	elif relationName == "PERPENDICULAR":
		fo.write("perp(" +objectName[0].lower() +objectName[0] + "," +objectName[1].lower() +objectName[1] + "," +objectName1[0].lower() +objectName1[0] + "," +objectName1[1].lower() + objectName1[1]+ "),\n")
	elif relationName == "length":
		fo.write("length(" +objectName[0].lower() +objectName[0] + "," +objectName[1].lower() +objectName[1]+","+str(value)+"),\n")	
	else:
		print(relationName + " has not been added till now\n")
#End Of Function

def writeFig_Data_to_File():
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_file_row)
#End Of Function


def write_Name_In_File(letter):
	#name(A,'A'),
	global fo
	fo = open("data.txt", "a")
	fo.write("name(" +letter.lower() +letter + ",'" + letter + "'),\n") 
#End Of Function


def printTree():
	print(" printing whole tree")
	#Checking graph nodes by printing all nodes along with their relationship
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_row)

#EOF


point_Name_Cord_Map = {}
def drawTree(dc):
	print("entering into drawTree function ")
	dc.SetPen(wx.Pen(wx.BLACK, 4))
	#Pick all the points and save their cordinates 
	query = "START z=node(*) WHERE z.type={A} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": "point"})
    	for row in data:
            #print(row[0]["name"])
	    pointName = row[0]["name"] 
	    pointCordx = row[0]["cordx"]
	    pointCordy = row[0]["cordy"]
	    global point_Name_Cord_Map 
	    cord_list = [pointCordx, pointCordy]
	    point_Name_Cord_Map[pointName] = cord_list
	    #print(point_Name_Cord_Map[pointName])
	    node_point = row[0]

	#print(point_Name_Cord_Map)

	query = "START z=node(*) WHERE z.type={A} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": "line"})
    	for row in data:
            #print(row[0])
            #print(row[0]["name"])
	    pointName1 = row[0]["name"][0] 
	    pointName2 = row[0]["name"][1] 
	    cordx1 = point_Name_Cord_Map[pointName1][0]
	    cordy1 = point_Name_Cord_Map[pointName1][1]
	    cordx2 = point_Name_Cord_Map[pointName2][0]
	    cordy2 = point_Name_Cord_Map[pointName2][1]
	    #print(cordx1)
	    #print(cordy1)
	    #print(cordx2)
	    #print(cordy2)
            dc.DrawLine(int(cordx1), 100+int(cordy1), int(cordx2), 100+int(cordy2))
            dc.DrawCircle(int(cordx1), 100+int(cordy1), 20)
	    dc.DrawText(pointName1, int(cordx1), 90+ int(cordy1))
            dc.DrawCircle(int(cordx2), 100+int(cordy2), 20)
	    dc.DrawText(pointName2, int(cordx2), 90+ int(cordy2))
#EOF

	
#This function is being called from gui.py
def generateQuestion(obj, concept, theorem, num_questions, nowGenerateFigure = 1, dc = None):
	print("Inside generateQuestion function")
	print(" geom_object is " + str(obj) + " concept is " + str(concept) + " theorem is " + str(theorem) + " num_questions is "+ str(num_questions))
	if dc == None :
	    	print("dc is none ")
	else :
		print(" dc is nnnnnnnnnnnnnnnnnnnnnnnnot none")
	firstTime  = 1
	while num_questions > 0:
		if nowGenerateFigure == 1:
			canGenerateFigure = generateFigure(dc, obj, firstTime, concept = None, theorem = None)
			if canGenerateFigure == False :
				print(" exiting from question generation as no more obj can be added ")
				return
			nowGenerateFig = 0
			firstTime = 0
			#return #######For ending here, needs to remove later
		while True :
			drawTree(dc)
			runCHR()
			#TODO *****************************
			#num_new_facts = Get num of new facts from CHR result file
			#num_new_facts = 0 #// TODO
			#num_questions = num_questions - num_new_facts
			
			if num_questions == 0 :
				break			
			canGenerateMoreData = generateData(graph_db, theorem , 1)  #TODO CHECK IF EVERYCASE IS OVER, nowGenerateFig = 1
				
			if canGenerateMoreData == 0 :
				nowGenerateFig = 1
				break
		#End of inner while loop	
		
		if num_questions == 0 :
			nowGenerateFig = 0
	#End of while
	print(" exiting from generateQuestion function ")	
#End of function

#This function is being called from gui.py
#generateQuestion("Triangle", "Perpendicular", "Pythagoras", "1", nowGenerateFigure = 1)
fo.close()





