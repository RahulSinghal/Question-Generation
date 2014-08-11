#!/usr/bin/env python

from __future__ import print_function
import wx
# Import Neo4j modules
from py2neo import neo4j, cypher
from cypher_handling_functions import *
from math import *
#from kd2_new import graph_db, node_root

#######These lines insides hashes have been added to protect kd2 from entering here #########
# Attach to the graph db instance
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

graph_db.clear()
#Create root node
root = "Root"
node_root, = graph_db.create({"name":root,"type":"node"})
######################################################

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

def getNewTriangleName():
	p1 = getNewPointName()
	p2 = getNewPointName()
	p3 = getNewPointName()
	triangleName = p1+p2+p3
	print(triangleName)
	return str(triangleName)
#EOF

def write_Name_In_File(letter):
	#name(A,'A'),
	global fo
	fo = open("data.txt", "a")
	fo.write("name(" +letter.lower() +letter + ",'" + letter + "'),\n") 
#End Of Function

#This array contains the value of length of sides and values of angles between them
figureInfoArray = [10,20,30,50,60,70]
#This array contains the coordinate values of each point
cordArray = [200,300,400,500,600,700]

#Generating random info for triangle coordinates and angle info which will replace above arrays
def generateTriangleInfo():
    print(" inside generateTriangleInfo")
#End Of Function

#Generate a set of nodes representing the triangle
def generateTriangle(figureInfoArray, cordArray, triangleName,node_root):
	print("Inside generateTriangle  function")
	write_Name_In_File(triangleName[0])
	write_Name_In_File(triangleName[1])
	write_Name_In_File(triangleName[2])
	side1 = str(triangleName[0] + triangleName[1])
	side2 = str(triangleName[1] + triangleName[2])
	side3 = str(triangleName[0] + triangleName[2])

	angle2 = triangleName
	angle3 = (side2 + triangleName[0])
	angle1 = str(triangleName[1] + triangleName[0]+ triangleName[2])

	point1 = triangleName[0]
	point2 = triangleName[1]
	point3 = triangleName[2]

	#Create root node
	node_triangle, = graph_db.create({"name": triangleName,"type":"triangle"})
	rel_triangle_root = node_root.create_relationship_to(node_triangle, "KD1")

	# Create three nodes
	node_a, node_b, node_c = graph_db.create(
    {"name": side1, "value":figureInfoArray[0],"type":"line"},
    {"name": side2, "value":figureInfoArray[1],"type":"line"},
    {"name": side3, "value":figureInfoArray[2],"type":"line"}
)

	# Join the nodes with a HAS relationship
	rel_triangle_a = node_triangle.create_relationship_to(node_a, "HAS")
	rel_triangle_b = node_triangle.create_relationship_to(node_b, "HAS")
	rel_triangle_c = node_triangle.create_relationship_to(node_c, "HAS")

	rel_a_b, = graph_db.get_or_create_relationships((node_a, "ANGLE",node_b, {"value": quesArray[3]}))
	rel_b_c, = graph_db.get_or_create_relationships((node_b, "ANGLE",node_c, {"value": quesArray[4]}))
	rel_a_c, = graph_db.get_or_create_relationships((node_a, "ANGLE",node_c, {"value": quesArray[5]}))

	#Create input nodes
	node_point1, node_point2, node_point3= graph_db.create({"name":point1, "cordx":cordArray[0],"cordy":cordArray[1],"type":"point"},{"name":point2, "cordx":cordArray[2],"cordy":cordArray[3],"type":"point"},{"name":point3, "cordx":cordArray[4],"cordy":cordArray[5],"type":"point"})

	# Join the nodes with a  INPUT relationship
	rel_a_point1 = node_a.create_relationship_to(node_point1, "CONTAIN")
	rel_a_point2 = node_a.create_relationship_to(node_point2, "CONTAIN")
	rel_b_point2 = node_b.create_relationship_to(node_point2, "CONTAIN")
	rel_b_point3 = node_b.create_relationship_to(node_point3, "CONTAIN")
	rel_c_point1 = node_c.create_relationship_to(node_point1, "CONTAIN")
	rel_c_point3 = node_c.create_relationship_to(node_point3, "CONTAIN")

	# Join the point nodes with a  CONNECTED relationship
	node_point1.create_relationship_to(node_point2, "CONNECTED")
	node_point2.create_relationship_to(node_point3, "CONNECTED")
	node_point1.create_relationship_to(node_point3, "CONNECTED")
	
	print("Exiting generate triangle function")
#End Of Function


def printTree(graph_db):
	print(" printing whole tree")
	#Checking graph nodes by printing all nodes along with their relationship
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_row)

#EOF

stepsStack = []	
save_triangle_three_new_points = []
save_triangle_line_point_connected_one_end_point = []
save_triangle_line_point_not_connected_both_end_points = []
save_triangle_existing_three_points = []
def check_saveObjFigure(objType, objName = None):
	print("saving obj of the figure ")
	global dict_three_point
	global stepsStack

	if objType == "Triangle_three_existing_points":
	        randomSet = random.sample(dict_three_point,1)
		#This is for generating a new triangle different from previous one
		global save_triangle_existing_three_points
        	if len(save_triangle_existing_three_points) > 0 :
                	for randomSet in save_triangle_existing_three_points:
                        	randomSet = random.sample(dict_three_point,1)
        	#End of inner if

		#It is done to save each step which can later be emptied
		temp = {"triangle",randomSet[0][0]+randomSet[0][1]+randomSet[0][2]}
		stepsStack.append(temp)

        	save_triangle_existing_three_points.append(randomSet)
		return randomSet
	#End of outer if
	if objType == "Triangle_line_point_connected_one_end_point":
		randomSet = random.sample(dict_three_point,1)
		#This is for generating a new triangle different from previous one
        	global save_triangle_line_point_connected_one_end_point
        	if len(save_triangle_line_point_connected_one_end_point) > 0 :
                	for randomSet in save_triangle_line_point_connected_one_end_point:
                        	randomSet = random.sample(dict_three_point,1)
        	#End of if

		#It is done to save each step which can later be emptied
		temp = {"line",randomSet[0][0]+randomSet[0][1]}
		stepsStack.append(temp)
		temp = {"triangle",randomSet[0][0]+randomSet[0][1]+ randomSet[0][2]}
		stepsStack.append(temp)

        	save_triangle_line_point_connected_one_end_point.append(randomSet)
		return randomSet
	#End of outer if
	if objType == "Triangle_line_point_not_connected_both_ends":
		randomSet = random.sample(dict_three_point,1)
		#This is for generating a new triangle different from previous one
		global save_triangle_line_point_not_connected_both_end_points
        	if len(save_triangle_line_point_not_connected_both_end_points) > 0 :
                	for randomSet in save_triangle_line_point_not_connected_both_end_points:
                        	randomSet = random.sample(dict_three_point,1)
        	#End of if

		#It is done to save each step which can later be emptied
		temp = {"line",randomSet[0][0]+randomSet[0][1]}
		stepsStack.append(temp)
		temp1 = {"line1",randomSet[0][0]+randomSet[0][2]}
		stepsStack.append(temp1)
		temp = {"triangle",randomSet[0][0]+randomSet[0][1]+ randomSet[0][2]}
		stepsStack.append(temp)

        	save_triangle_line_point_not_connected_both_end_points.append(randomSet)
		return randomSet
	#End of outer if
	if objType == "Triangle_three_new_points":
		global save_triangle_three_new_points
		save_triangle_three_new_points.append(objName)

		#It is done to save each step which can later be emptied
		temp = {"point",objName[0]}
		stepsStack.append(temp)
		temp = {"point",objName[1]}
		stepsStack.append(temp)
		temp = {"point",objName[2]}
		stepsStack.append(temp)
		temp = {"triangle",objName}
		stepsStack.append(temp)

		return 
	#End of outer if
	if objType == "Line_two_existing_points":
	        randomSet = random.sample(dictPoint_Point,1)
		#This is for generating a new triangle different from previous one
		global save_line_existing_two_points
        	if len(save_line_existing_two_points) > 0 :
                	for randomSet in save_line_existing_two_points:
                        	randomSet = random.sample(dictPoint_Point,1)
        	#End of inner if

		#It is done to save each step which can later be emptied
		temp = {"line",randomSet[0][0]+randomSet[0][1]}
		stepsStack.append(temp)

        	save_line_existing_two_points.append(randomSet)
		return randomSet
	#End of outer if
#EOF

def emptyStack():
	global stepsStack
	count = len(stepsStack)
	while count > 0 :
		if stepsStack[count -1][0] == "line" :
			print(" deleting line "+ stepsStack[count - 1][1])
			removeLine_Fig(stepsStack[count - 1][1])
		elif stepsStack[count -1][0] == "point" :
			print(" deleting point "+ stepsStack[count - 1][1])
			removePoint_Fig(stepsStack[count - 1][1])
		elif stepsStack[count -1][0] == "triangle" :
			print(" deleting triangle"+ stepsStack[count - 1][1])
			removeTriangle_Fig(stepsStack[count - 1][1])
		else:
			print("error is present in emptyStack")
			break
		count = count - 1
	#End of while loop

#EOF

def addPerpendicularAngle(lineName1, lineName2):
	print("Inside addPerpendicularAngle function")
	lineName3 = lineName1[1] + lineName1[0]
	lineName4 = lineName2[1] + lineName2[0]

	#Getting the node of line for making perpendicular relationship
    	query = "START z=node(*) WHERE z.name={A} OR z.name = {B} RETURN z"
    	data, metadata = cypher.execute(graph_db, query, {"A": lineName1, "B":lineName3})
    	node_line1 = data[0][0]
    	print(node_line1["name"])

    	query = "START z=node(*) WHERE z.name={A} OR z.name = {B} RETURN z"
    	data, metadata = cypher.execute(graph_db, query, {"A": lineName2, "B":lineName4})
    	node_line2 = data[0][0]
    	print(node_line2["name"])
	
	#node_line1.create_relationship_to(node_line2, "PERPENDICULAR")
	graph_db.get_or_create_relationships((node_line1, "PERPENDICULAR",node_line2, {"value": "90"}))
	print("Exiting addPerpendicularAngle function")
#End Of Function


save_perp = []
old_perp_line = None

#TODO TRIANGLE NAME SHOULD BE GIVEN AS AN ARGUMENT*********************
def drawPerpendicular(firstTime, change = 0):

	print("Inside drawPerpendicular function")
	#Pick any one triangle 
	query = "START z=node(*) WHERE z.type={A} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": "triangle"})
    	for row in data:
            print(row[0]["name"])
	    node_triangle = row[0]
	

	#Pick existing set of  point and line not connected to it
	query = "START c = node(*) , b= node(*), a= node(*)MATCH c-[:KD1]->d-[:HAS]->b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

	#Pick any one set randomly
	randomSet = random.sample(dictLine_Point,1)
	if change == 1 :
	
	    for save_perp in randomset:
		randomSet = random.sample(dictLine_Point,1)
	    
	    # TODO Remove old perpendicular line ********************
	    removeLine_Fig(old_perp_line)
	
	save_perp.append(randomset)
	print(" randomset of line and point chosen is ")
	print( "selectedPoint is " +randomSet[0][0])
	print( "selectedLine is " +randomSet[0][1])
	selectedLine = randomSet[0][1]
	selectedPoint = randomSet[0][0]

	#Find new point by computation TODO *************

	#Add point on line
	newPoint = getNewPointName()
	print(newPoint)
	write_Name_In_File(newPoint)
	addPointOnLine(newPoint,10,20,selectedLine,40,40,node_triangle)

	#Add line in triangle
	newLine = selectedPoint + newPoint
	old_perp_line = newLine
	
	addLineInTriangle(newLine, 40, 90, 90,20,25,node_triangle)


	perpBase1 = newPoint + selectedLine[0]
	perpBase2 = newPoint + selectedLine[1]
	perpBase3 = selectedLine
	addPerpendicularAngle(newLine,perpBase1)
	addPerpendicularAngle(newLine,perpBase2)
	addPerpendicularAngle(newLine,perpBase3)
	
	print("Exiting drawPerpendicular function")	
#End Of Function


def addPointOnLine(pointName,cordx,cordy,lineName, line1Length, line2Length,node_triangle):
	print("Inside addPointOnLine function and lineName is "+ lineName + " and pointName is "+pointName)
    
	#Getting the node of line for making collinear relationship
	query = "START z=node(*) WHERE z.name={A} AND z.type = {B} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": lineName, "B":"line"})
	temp = data[0][0]
	print(temp["name"])

    #Create two nodes for two new lines made
	line1Name = lineName[0]+pointName
	line2Name = lineName[1]+pointName
	node_line1new, = graph_db.create({"name": line1Name, "value":line1Length,"type":"line"})
	node_line2new, = graph_db.create({"name": line2Name, "value":line2Length,"type":"line"})
    
    #Create a new node for point
	node_new, = graph_db.create({"name": pointName, "cordx":cordx,"cordy":cordy,"type":"point"})
    
    #Get othernodes of given line
	nodeCollection  = temp.get_related_nodes(0,"CONTAIN")
	for node in nodeCollection:
		node.create_relationship_to(node_new, "COLLINEAR")
		node.create_relationship_to(node_new, "MIDPOINT")
		graph_db.get_or_create_relationships((node, "CONNECTED",node_new))
 

    #Create new relationships between these two new lines and points
	node_line1new.create_relationship_to(node_new, "CONTAIN")
	node_line2new.create_relationship_to(node_new, "CONTAIN")
    
	for node in nodeCollection:
		if(node["name"] == lineName[0]):	node_line1new.create_relationship_to(node, "CONTAIN")
		if(node["name"] == lineName[1]):	node_line2new.create_relationship_to(node, "CONTAIN")
    

        #Create new relationships between these two new lines and triangle
	node_triangle.create_relationship_to(node_line1new, "INDIRECTLY_HAS")
	node_triangle.create_relationship_to(node_line2new, "INDIRECTLY_HAS")
	
	print("Exiting addPointOnLine function")
#End of Function

def addLineInTriangle(lineName, length, ang1, ang2,ang3,ang4,node_triangle):
	print("Inside addLineInTriangle function")
	
	node_new, = graph_db.create({"name": lineName, "value":length,"type":"line"})
    
	node_triangle.create_relationship_to(node_new, "INDIRECTLY_HAS")
 
	query = "START z=node(*) WHERE z.name={A} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": lineName[0]})
	temp = data[0][0]
	print(temp["name"])


	query = "START z=node(*) WHERE z.name={A} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": lineName[1]})
	temp1 = data[0][0]
	print(temp1["name"])

	node_new.create_relationship_to(temp, "CONTAIN")
	node_new.create_relationship_to(temp1, "CONTAIN")
	graph_db.get_or_create_relationships((temp, "CONNECTED",temp1))


	p1 = [temp["cordx"],temp["cordy"]]	
	p2 = [temp1["cordx"],temp1["cordy"]]	
	print("Find all possible triangles formed by adding this line TODO")
	query = "START z=node({B}), c=node({C}) MATCH z-[:CONNECTED]-b-[:CONNECTED]-c WHERE z.type={A} AND c.type={A} RETURN b"
        data, metadata = cypher.execute(graph_db, query, {"A": "point","B": temp.id,"C":temp1.id})
    	for row in data:
            print(row[0]["name"])
	    tempPoint = str(row[0]["name"])
	    if tempPoint in lineName: print("found point "+ tempPoint)
	    else: 
	        tempSide1 = lineName + tempPoint
	        print("calling addTriangle for " + tempSide1)
	        addTriangle(tempSide1)
		#Compute angles and addAngleRelationship TODO
		p3 = [row[0]["cordx"],row[0]["cordy"]]	
		print("Before calculating angle for first point")
		print(p1)
		print(p2)
		print(p3)
		ang1 = 10  #TODO angle_lines(p1, p2, p1, p3)
		temp.create_relationship_to(row[0], "ANGLE", {"value": ang1})
		graph_db.get_or_create_relationships((temp, "CONNECTED",row[0]))

	'''
	query = "START z=node({B}) MATCH z-[:CONNECTED]-b WHERE z.type={A} RETURN b"
    	data, metadata = cypher.execute(graph_db, query, {"A": "point","B": temp1.id})
    	for row in data:
        	print(row[0]["name"])
	 	tempPoint = str(row[0]["name"])
	if tempPoint in lineName: print("found point "+ tempPoint)
	else: 
	    tempSide1 = lineName + tempPoint
	    print("calling addTriangle for " + tempSide1)
	    addTriangle(tempSide1)
	#Compute angles and addAngleRelationship TODO
	p3 = [row[0]["cordx"],row[0]["cordy"]]	
	print("Before calculating angle for second point")
	print(p1)
	print(p2)
	print(p3)
	ang1 = 10  #TODO angle_lines(p1, p2, p2, p3)
	temp.create_relationship_to(row[0], "ANGLE", {"value": ang1})
	graph_db.get_or_create_relationships((temp, "CONNECTED",row[0]))

	#print("Add triangles via hardcoding")
	#addTriangle("PSR")
	#addTriangle("PSQ")
	'''
	print("Exiting addLineInTriangle function")	
#End Of Function

#This function will simply add triangle node to the graph
save_triangle = []
def addTriangle(triangleName):
    print("Inside addTriangleName function")
	
    #This function will save triangle which will help in checking changeTriangle
    #save_triangle.append(triangleName)
	
    
    node_new, = graph_db.create({"name":triangleName,"type":"triangle"})
  
    node_root.create_relationship_to(node_new, "KD1")
  
    side1 = triangleName[0]+ triangleName[1]
    side4 = triangleName[1]+ triangleName[0]
    side5 = triangleName[2]+ triangleName[1]
    side6 = triangleName[0]+ triangleName[2]
    side2 = triangleName[1]+ triangleName[2]
    side3 = triangleName[2]+ triangleName[0]
    
    query = "START z=node(*) WHERE z.name={A} OR z.name={B}  RETURN z"
    data, metadata = cypher.execute(graph_db, query, {"A": side1, "B":side4})
    temp1 = data[0][0]
    print(temp1["name"])

    query = "START z=node(*) WHERE z.name={A} OR z.name={B} RETURN z"
    data, metadata = cypher.execute(graph_db, query, {"A": side2, "B":side5})
    temp2 = data[0][0]
    print(temp2["name"])

    query = "START z=node(*) WHERE z.name={A} OR z.name={B} RETURN z"
    data, metadata = cypher.execute(graph_db, query, {"A": side3, "B":side6})
    temp3 = data[0][0]
    print(temp3["name"])

    #graph_db.get_or_create_relationships(node_new, "HAS",temp1)
    node_new.create_relationship_to(temp1, "HAS")
    node_new.create_relationship_to(temp2, "HAS")
    node_new.create_relationship_to(temp3, "HAS")
    #graph_db.get_or_create_relationships(node_new, "HAS",temp2)
    #graph_db.get_or_create_relationships(node_new, "HAS",temp3)
    print("Exiting addTriangleName function")
#End Of Function


def check_join_two_non_connecting_Points():
	print("Pick existing set of two points which are not connected")
	global dictPoint_Point
	dictPoint_Point = []
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONNECTED]-a WHERE NOT(a = b) AND  b.type = {B} AND a.type = {B} AND r IS NULL  RETURN a,b"
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=handle_two_non_connecting_points)
	if len(dictPoint_Point) == 0: 
		print(" NOT found any set of non connecting points, hence returning false ")
		return False

	#Join these two points
	randomSet = check_saveObjFigure("Line_two_existing_points")
	#randomSet = random.sample(dictPoint_Point,1)

    	print(" randomset of line and point chosen is ")
    	print( "first selectedPoint is " + randomSet[0][0]["name"])
    	print( "second selectedPoint is " +randomSet[0][1]["name"])
	node1 = randomSet[0][0]
	node2 = randomSet[0][1]
	#node1.create_relationship_to(node2, "CONNECTED")

	lineName1 = randomSet[0][0]["name"] + randomSet[0][1]["name"]
	
	query = "START a=node(*),b=node(*) MATCH a-[:KD1]->b WHERE b.type = {A} return b"
	data,metadata = cypher.execute(graph_db, query, {"A" :"triangle"})
	node_triangle = data[0][0]
	triangleName = node_triangle["name"]
	print(" adding in two points function line "+ lineName1 +" to triangle "+ triangleName)
	length = 10
	ang1 = 10
	ang2 = 30
	ang3 = 40
	ang4 = 50

	addLineInTriangle(lineName1, length, ang1, ang2,ang3,ang4,node_triangle)
	return True
#End Of Function



def check_join_Existing_three_non_collinear_non_connected_Points():

	print("Pick existing set of three non collinear points which are not connected")
	global count_row
	global dict_three_point
	count_row = 0
	dict_three_point = []
	query = "START b=node(*),a=node(*),c=node(*) MATCH a-[r?:CONNECTED]-b, b-[s?:CONNECTED]-c,c-[t?:CONNECTED]-a WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type = {B} AND a.type = {B} AND c.type = {B} AND t IS NULL AND s IS NULL AND r IS NULL  RETURN a,b,c"
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_three_points_row)
	#global count_row
	if count_row == 0:
		print(" Not found 3 points, hence exiting from this function")
		return False

	#Join these points and add info to the triangle TODO  (Please fill the values of angle and length in the below code)
	
	randomSet = check_saveObjFigure("Triangle_three_existing_points")
    	print( "first selectedPoint is " +randomSet[0][0])
    	print( "second selectedPoint is " +randomSet[0][1])
    	print( "third selectedPoint is " +randomSet[0][2])
	    
	query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	data,metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][0]})
	node1 = data[0][0]
    	
	query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	data,metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][1]})
	node2 = data[0][0]

	query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	data,metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][2]})
	node3 = data[0][0]

	node1.create_relationship(node2, "CONNECTED")
	node2.create_relationship(node3, "CONNECTED")
	node3.create_relationship(node1, "CONNECTED")

	sideName1 = node1["name"] + node2["name"]
	sideName2 = node2["name"] + node3["name"]
	sideName3 = node1["name"] + node3["name"]

	node_a, node_b, node_c = graph_db.create(
    {"name": sideName1, "value":quesArray[0],"type":"line"},
    {"name": sideName2, "value":quesArray[1],"type":"line"},
    {"name": sideName3, "value":quesArray[2],"type":"line"})
	
	node_a.create_relationship_to(node_b, "ANGLE")
	node_b.create_relationship_to(node_c, "ANGLE")
	node_c.create_relationship_to(node_a, "ANGLE")

	triangleName = node1["name"] + node2["name"] + node3["name"]
	addTriangle(triangleName)
	count_row = 0
	print("exiting from check_join_Existing_three_non_collinear_non_connected_Points function")
	return True
#End Of Function

save_triangle_line_point = []
def check_join_Existing_line_existing_non_connected_point_not_on_line():
	print("Pick existing set of a point and line connected to one end but not connected to other end")
	global count_row
	global dict_three_point
	count_row = 0
	dict_three_point = []
	query = "START b=node(*),a=node(*),c=node(*) MATCH b-[s?:CONNECTED]-c, a-[:CONNECTED]-b, a-[:CONNECTED]-c WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type={B} AND a.type={B} AND c.type={B} AND s IS NULL  RETURN c,a,b"
	#cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_row)
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_three_points_row)
	if count_row == 0:
		print("NOT found a point and a line not connected to it, hence checking other case where point is not connected to both end points")
		#return False
	
		print("Pick existing set of a point and line not connected to both ends ")
		query = "START b=node(*),a=node(*),c=node(*) MATCH b-[:CONNECTED]-a, b-[s?:CONNECTED]-c,c-[t?:CONNECTED]-a WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type = {B} AND a.type = {B} AND c.type = {B} AND t IS NULL AND s IS NULL  RETURN a,b,c"
		cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_three_points_row)
		#global count_row
		if count_row == 0:
			print(" not found a point and a line not connected to it, hence exiting")
			return False

		randomSet = check_saveObjFigure("Triangle_line_point_not_connected_both_ends")
    		print(" randomset of line and point chosen is "+ randomSet[0])
    		print( "selectedPoint is " +randomSet[0][0])
    		print( "selectedLine is " +randomSet[0][1])
    		node1 = randomSet[0][0]
    		node2 = randomSet[0][1]

		#Fill in the details of the calling function TODO
		lineName1 = node1 + node2[0]
		lineName2 = node1 + node2[1]
		triangleName = node1 + node2
		length = 10
		ang1 = 10
		ang2 = 30
		ang3 = 40
		ang4 = 50

		quesArray = [10,10,10,20,30,40]
		cordArray = [10,10,20,20,30,30]
		generateTriangle(quesArray, cordArray, triangleName,node_root)

		#addLineInTriangle(lineName1, length, ang1, ang2,ang3,ang4,node_triangle)
		#addLineInTriangle(lineName2, length, ang1, ang2,ang3,ang4,node_triangle)
		count_row = 0
		return True
	else:
		printTree(graph_db)
		print("found a line and a point connected to one end only")
		randomSet = check_saveObjFigure("Triangle_line_point_connected_one_end_point")
    		print( "selectedPoint is " +randomSet[0][0])
    		print( "selectedLine is " +str(randomSet[0][1]+ randomSet[0][2]))
    		node1 = randomSet[0][0]
    		node2 = randomSet[0][1]
    		node3 = randomSet[0][2]

		#Fill in the details of the calling function TODO
		lineName1 = node1 + node3[0]
		triangleName = None
		#Get the triangle node
                query = "START z=node(*) MATCH z-[:INDIRECTLY_HAS]-a-[:CONTAIN]-b WHERE z.type={A} AND b.type={C} AND b.name={B} RETURN z"
                data, metadata = cypher.execute(graph_db, query, {"A": "triangle","B":node1,"C":"point"})
		if len(data) == 0:
                	data, metadata = cypher.execute(graph_db, query, {"A": "triangle","B":node3,"C":"point"})
                for row in data:
                	print(row[0])
                	node_triangle = row[0]
			triangleName = row[0]["name"]
		print(" adding line "+ lineName1 +" to triangle "+ triangleName)
		length = 10
		ang1 = 10
		ang2 = 30
		ang3 = 40
		ang4 = 50

		addLineInTriangle(lineName1, length, ang1, ang2,ang3,ang4,node_triangle)
		print(" exiting from check_join_Existing_line_existing_non_connected_point_not_on_line function")
		return True		
#End Of Function



def generate_join_three_new_points():
	print(" Generate data for triangle generation ")
	p1x = 500 #random.randint(1,1000)
	p1y = 100 #random.randint(1,1000)
	cord = {p1x, p1y}

	while True:
		p2x = 300#random.randint(1,100)
		p2y = 400#random.randint(1,100)
		temp = {p2x,p2y}
		if temp != cord:break

	while True:
		p3x = 700#random.randint(1,100)
		p3y = 300#random.randint(1,100)
		temp1 = {p3x,p3y}
		if temp1 != temp :break
	
	cordArray = []
	cordArray.append(p1x)
	cordArray.append(p1y)
	cordArray.append(p2x)
	cordArray.append(p2y)
	cordArray.append(p3x)
	cordArray.append(p3y)
	print("first number x is " +str(p1x))
	print("first number y is " +str(p1y))
	print("second number x is " +str(p2x))
	print("second number y is " +str(p2y))
	print("third number x is " +str(p3x))
	print("third number y is " +str(p3y))

	quesArray = []
	dist1 = math.hypot(p2x - p1x, p2y - p1y)
	dist2 = math.hypot(p2x - p3x, p2y - p3y)
	dist3 = math.hypot(p3x - p1x, p3y - p1y)
	quesArray.append(dist1)
	quesArray.append(dist2)
	quesArray.append(dist3)
	print("distance is " +str(dist1))
	print("distance is " +str(dist2))
	print("distance is " +str(dist3))

	ang1 = 10  #TODO angle_lines(cord, temp)
	ang2 = 10  #TODO angle_lines(temp, temp1)
	ang3 = 10  #TODO angle_lines(cord, temp1)

	quesArray.append(ang1)
	quesArray.append(ang2)
	quesArray.append(ang3)
	triangleName = getNewTriangleName() 
	generateTriangle(quesArray, cordArray, triangleName,node_root)
	check_saveObjFigure("Triangle_three_new_points", triangleName)
	print(" exiting from generate three new points function")
#End Of Function


save_point = []
def addPointFig():
	print("Inside adding point, find an existing line not having existing mid point")
	global countLine
	global dictLine_Point
	countLine = []
	dictLine_Point = []
	query = "START c=node(*), b=node(*),a=node(*) MATCH c-[:KD1]->d-[:HAS]->b-[r?:MIDPOINT]->a,b-[s?:CONTAIN]-a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL AND s IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

	#If above case fails, then
	if len(countLine) != 0: 
	    #Get the mid-point of the chosen line
	    randomSet = random.sample(dictLine_Point,1)
	    #####TODO This is for generating a new triangle different from previous one
	    '''
	    if len(save_point) > 0 :
		for randomSet in save_point:
			randomSet = random.sample(dict_three_point,1)
		#End of if
		save_point.append(randomSet)
	    '''
            print(" randomset of line chosen is ")
            print( "selectedPoint is " +randomSet[0][0])
            print( "selectedLine is " +randomSet[0][1])
	    
	    #Get nodes of the end points of lines, from nodes get the cord values for computing mid-point
	    query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	    data,metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][1][0]})
	    cord1x = data[0][0]["cordx"]
	    cord1y = data[0][0]["cordy"]
	    
	    query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	    data,metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][1][1]})
	    cord2x = data[0][0]["cordx"]
	    cord2y = data[0][0]["cordy"]

	    cord3x = 0.5 *(cord1x + cord2x)
	    cord3y = 0.5 *(cord1y + cord2y)

	    query = "START a=node(*) MATCH a-[:HAS]->b WHERE a.type = {A} AND b.name = {B} return a"
	    data,metadata = cypher.execute(graph_db, query, {"A" :"triangle","B":randomSet[0][1]})
	    triangle = data[0][0]
	    
	    #TODO
	    #addPointOnLine(pointName,cordx,cordy,line, line1Length, line2Length,node_triangle):
	    p1 = getNewPointName()
	    addPointOnLine(p1, cord3x, cord3y, randomSet[0][1], 10,20,triangle)
	    countLine = []
	else:
		print("need to think ....this case should not arrive soooooooooon except for first time")
	return True
#End Of Function


save_line_existing_line_point_not_on_line = []
def check_existing_line_point_not_on_line():
	print("Pick existing set of  point and line not connected to it")
	'''
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)
	global countLine
	if len(countLine) == 0: return False

	#TODO Join this point with the mid-point of the chosen line
	pointName = getNewPointName()
	addPointOnLine(pointName,cordx,cordy,lineName, line1Length, line2Length,node_triangle):
	countLine = []
	return True
	'''
#End Of Function



def check_join_Existing_line_new_point_not_on_line():
	print("Adding a new point on a random line inside check_join_Existing_line_new_point_not_on_line function")
	addPointFig()
	if check_join_Existing_line_existing_non_connected_point_not_on_line() == True:return True
	return False
#End Of Function



def addTriangleInFig(firstTime = 0):
	if firstTime == 1:
	     generate_join_three_new_points() 
	     return 1
	if check_join_Existing_three_non_collinear_non_connected_Points() == True :return 1
	elif check_join_Existing_line_existing_non_connected_point_not_on_line() == True:return 1
	elif check_join_Existing_line_new_point_not_on_line() == True:return 1
	else :
		    print("no more triangle can be added in addTriangleInFig function")
		    return 0
#End Of Function

def addLineInFig(firstTime = 0):
	if check_join_two_non_connecting_Points() == True:return 1
	elif check_join_Existing_line_existing_non_connected_point_not_on_line() == True:return 1
	elif check_join_Existing_line_new_point_not_on_line() == True:return 1
	else :
		    print("no more line can be added in addLineInFig function")
		    return 0

	'''
	elif check_existing_line_point_not_on_line() == True:return 1
	elif addPointFig() == True:
		if addLineInFig() == True:
			return 1
		else:
			print("no more line can be added in the given figure ")
			return 0
	else:
		print(" no more point can be added into the figure")
		return 0
	'''
#End Of Function

def drawMedian(firstTime):
	print("inside draw median function ")
	return 0
#EOF

def addConceptFigure(concept, firstTime):
	if geom_object == "Perpendicular" :
		if drawPerpendicular(firstTime) == 1 :return 1
		return 0
	if geom_object == "Median" :
		if drawMedian(firstTime) == 1: return 1
	else :
		print(" Inside addConceptFigure, concept not defined ")
		return 0
#End of function


def addObjFigure(geom_object, firstTime):
	if geom_object == "Triangle" :
		if firstTime == 0:
			print("Changing object from triangle to line just for testing, later needs to remove")
			geom_object = "Line"
	if geom_object == "Triangle" :
		if addTriangleInFig(firstTime) == 1 :return 1
		return 0
	if geom_object == "Line" :
		if addLineInFig(firstTime) == 1: return 1
	else :
		print(" Inside addObjFigure, geom_object not defined ")
		return 0
#End of function

	
def generateObjFigure(geom_object, firstTime = 1, change_fig_possible = 1):
	print("inside generateObjFigure obj is "+ geom_object)
	while 1:
		if  firstTime == 1:
		    addObjFigure(geom_object,firstTime)
		    firstTime = 0
		    printTree(graph_db)
		    #saveObjFigure(geom_object)
		    break
		else :
			change_fig_possible = addObjFigure(geom_object, firstTime)
			if  change_fig_possible == 1 :
		    		printTree(graph_db)
				break
			else :
		    		printTree(graph_db)
				print("cannot add any more object in the problem ")
				return False
	print("exiting from generateObjFigure ")	
	return True
#End of Function

def generateConceptFigure(concept, firstTime = 1, change_concept_possible = 0):
	print(" inside generateConceptFigure ")
	while 1:
		if  firstTime == 1:
		    addConceptFigure(concept,firstTime)
		    firstTime = 0
		    printTree(graph_db)
		    #saveConceptFigure(geom_object)
		    break
		else :
			change_concept_possible = addConceptFigure(concept, firstTime)
			if  change_concept_possible == 1 :
		    		printTree(graph_db)
				break
			else :
		    		printTree(graph_db)
				print("cannot add any more concept in the problem ")
				return False
	print("exiting from generateConceptFigure ")	
	return True
#End of Function

point_Name_Cord_Map = {}
def drawTree_UI(dc, graph_db):
	print("entering into drawTree_UI function ")
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

#This is the main function of this component. It will generate a figure configuration	
def generateFigure(dc,geom_object, firstTime, concept, theorem):
	print("inside generateFigure function ")
	if generateObjFigure(geom_object, firstTime) == True :
		drawTree_UI(dc,graph_db)
		print("Calling generateObject second time ******************")
		if generateObjFigure(geom_object, 0) == True:#Passing firstTime = 0
			drawTree_UI(dc, graph_db)
			print("Calling generateObject third time ******************")
			if generateObjFigure(geom_object, 0) == True:#Passing firstTime = 0
				drawTree_UI(dc, graph_db)
				print("Calling generateObject fourth time ******************")
				if generateObjFigure(geom_object, 0) == True:#Passing firstTime = 0
					drawTree_UI(dc, graph_db)
		######################generateConceptFigure(concept)
		#####################writeFig_Data_to_File()
		return True
	else :
		print(" cannot add more objects, hence terminationg algorithm ")
		return False
	print(" exiting from generateFigure ")
#EndOfFunction


def removeTriangle_Fig(triangleName):
	print("Inside removeTriangle_Fig function")
	#lineName = triangleName[0] + triangleName[1]
	#removeLine_Fig(lineName)
	#lineName = triangleName[1] + triangleName[2]
	#removeLine_Fig(lineName)
	#lineName = triangleName[0] + triangleName[2]
	#removeLine_Fig(lineName)
	
	#del all the relations of this node with other line
	query = "START a=node(*) MATCH a-[r:HAS]-() , a-[r:INDIRECTLY_HAS]-() WHERE a.type={A} AND a.name={B}  DELETE r"
    	cypher.execute(graph_db, query,{"A": "triangle", "B":triangleName})

	#del kd1 relation of this node including this node
	query = "START a=node(*) MATCH a-[r:KD1]-() WHERE a.type={A} AND a.name={B}  DELETE a,r"
    	cypher.execute(graph_db, query,{"A": "triangle", "B":triangleName})
	print("Exiting removeTriangle_Fig function")
#End Of Function


# This function is used to delete the line including angles.
# Need to consider various cases
# Remove relations such as median, perpendicular etc..if the line has
# Remove the triangle also if this line is forming
# Remove the point nodes if required
def removeLine_Fig(lineName):
	
	#Search the two end points of the given line and then remove line and angle from KD1
	print("Inside removeLine_Fig")	
	query = "START a=node(*), b=node(*), c=node(*)  MATCH c-[:CONTAIN]-a-[:CONNECTED]-b,c-[:CONTAIN]-b WHERE a.type={A} AND a.name={B} AND b.type={A} AND b.name={C} AND c.type={D} RETURN a,b,c"
    	cypher.execute(graph_db, query, {"A": "point", "B":lineName[1], "C":lineName[1],"D":"line"},row_handler=handle_line)
    	node_line1 = line_container[0][2]
    	print(node_line1["name"])
	pointNode1 = line_container[0][0]
	pointNode2 = line_container[0][1]

	#TODO DELETE line FROM GRAPH DATABASE and check if it is a part of a triangle, remove triangle also
	print("Query for removing line")	
	query = "START a=node(*), b=node(*), c=node(*)  MATCH c-[r:CONTAIN]-a-[s:CONNECTED]-b,c-[:CONTAIN]-b WHERE a.type={A} AND a.name={B} AND b.type={A} AND b.name={C} AND c.type={D} DELETE r,s"
    	cypher.execute(graph_db, query,{"A": "point", "B":lineName[1], "C":lineName[1],"D":"line"})
	
	#get the parent node of this node
	query = "START a=node(*), b=node({B}) MATCH a-[r:HAS]-b WHERE b.type={A} RETURN a"
    	data,Metadata = cypher.execute(graph_db, query,{"A": "line", "B":node_line1.id})
	node_triangle = data[0][0]

	#del HAS relation of this node including this node
	query = "START a=node(*), b=node({B}) MATCH a-[r:HAS]-b WHERE b.type={A}  DELETE b,r"
    	cypher.execute(graph_db, query,{"A": "line", "B":node_line1.id})
	
	removeTriangle_Fig(node_triangle["name"])

	#removePoint_Fig(pointNode1)
	#removePoint_Fig(pointNode2)
	print("Exiting removeLine_Fig")	
#End Of Function

# This function removes the node of the point passed as an argument
def removePoint_Fig(pointName):
	print("inside removePoint_Fig function")

	#get the node of this point
	query = "START a=node(*) WHERE a.type={A} AND a.name={B} RETURN a"
    	data,Metadata = cypher.execute(graph_db, query,{"A": "point", "B":pointName})
	node_point = data[0][0]

	#get all the lines connected this node from KD1 
	query = "START a=node(*),b=node(*) MATCH a-[r:CONTAIN]-b WHERE a.type={A} AND b.type={C} AND b.name={B}  RETURN a"
    	data,Metadata = cypher.execute(graph_db, query,{"A": "line", "B":pointNode["name"], "C":"point"})

	#deleting all the line nodes containing this point node
	for row in data:
		print(row[0]["name"])
		removeLine_Fig(row[0])

	#Deleting the point node
	query = "START a=node({A}) WHERE a.type={C} AND a.name={B}  DELETE a"
    	cypher.execute(graph_db, query,{"A": node_point.id, "B":pointNode["name"], "C":"point"})
		
#End Of Function


#Defining new terms without testing
def changePerpendicularLine():
	drawPerpendicular(1)
#End Of Function

def addTheorems_Fig(theoremName):
	print("Inside addTheorems_Fig function")
	if theoremList_concept_map[theoremName] == "perp":
		#Check if perpendicular is not present, if not then draw otherwise nothing to do 
		drawPerpendicular()
	elif theoremList_concept_map[theoremName] == "median":
		#Check if perpendicular is not present, if not then draw otherwise nothing to do
		print("need to do coding for adding median")
#End Of Function

def changeTheorems_Fig(theoremName):
	print("Inside changeTheorems_Fig function")
	if theoremList_concept_map[theoremName] == "perp":
		#Check if perpendicular is not present, if not then draw otherwise nothing to do 
		drawPerpendicular(1)
	elif theoremList_concept_map[theoremName] == "median":
		#Check if perpendicular is present, if yes then remove it and save it and draw different one
		print("need to do coding for adding median")
#End Of Function

