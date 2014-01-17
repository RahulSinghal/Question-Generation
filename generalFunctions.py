#!/usr/bin/env python

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher
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

# Define a row handler for file writing...
def print_file_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])
    writeToFile(a["name"], r.type, b["name"])
#End Of Function

def writeToFile(objectName, relationName, objectName1 = None, value=0):
	if relationName == "KD1":
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

def angle_between_lines(pt1, pt2,pt3,pt4):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    x3 = pt3[0]
    y3 = pt3[1]
    x4 = pt4[0]
    y4 = pt4[1]
    #TODO
    return 10
#End Of Function

p1 = getNewPointName()
p2 = getNewPointName()
p3 = getNewPointName()
triangleName = p1+p2+p3
print(triangleName)

def write_Name_In_File(letter):
	#name(A,'A'),
	fo.write("name(" +letter.lower() +letter + ",'" + letter + "'),\n") 
#End Of Function

#This array contains the value of length of sides and values of angles between them
quesArray = [10,20,30,50,60,70]
#This array contains the coordinate values of each point
cordArray = [20,30,40,50,60,70]

def generateTriangle(quesArray, cordArray, triangleName,node_root):
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
    {"name": side1, "value":quesArray[0],"type":"line"},
    {"name": side2, "value":quesArray[1],"type":"line"},
    {"name": side3, "value":quesArray[2],"type":"line"}
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

dictPoint_Point = []
count = 0
def handle_two_non_connecting_points(row):
    a,b = row
    count = count +1
    dictPoint_Point.append([a,b])
    print(a["name"] + " with " + b["name"])
#End Of Function

# Define a new row handler...
dictLine_Point = []
countLine = []
def print_row_new(row):
    a, b = row
    countLine.append(1)
    dictLine_Point.append([str(a["name"]),str(b["name"])])
    print(a["name"] + " is perpendicular " + b["name"])

# Define a relationship handler...
dict1 = {}
dict2 = {}
def handle_relationship(row):
    a, b,r = row
    tempStr = str(a["name"] + str(r.type) + str(b["name"]))
    dict1[tempStr] = a["name"]
    dict2[tempStr] = b["name"]
    print(a["name"] + " has relationship " + r.type + " with " + b["name"])

def handle_row(row):
    node = row[0]
    print (node)

# Define a row handler...
def print_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])

# Define a three non connected points handler...
def handle_three_points(row):
    a, b,c = row
    print(a["name"] + " and " +b["name"] + "and " + c["name"])
#End Of Function

list_right_triangles = []
def getAllRightAngleTriangles():
    print("Inside getAllRightAngleTriangle function")
    #Get all nodes with relationship ANGLE and having value 90

    length = len(dictLine_Point)
    del dictLine_Point[0:length]
    query = "START a=node(*) MATCH a-[:PERPENDICULAR]-b WHERE a.type = {B} AND b.type = {B}  RETURN a,b"
    cypher.execute(graph_db, query,{"B" :"line"},row_handler=print_row_new)
    print("Printing nodes having angle 90 ")
    print(dictLine_Point)

    query = "START a=node(*),b=node(*),c=node(*) MATCH a-[:HAS]->b-[:PERPENDICULAR]-c<-[:HAS]-a WHERE a.type = {B} RETURN a"
    data,metadata = cypher.execute(graph_db, query,{"B": "triangle"})
    for row in data:
	temp3 = row[0]
        list_right_triangles.append(temp3)
        #print("one of the right angle triangle is "+temp3["name"])
    print("Exiting getAllRightAngleTriangle function")
#End Of Function

save_perp = []
old_perp_line = None

#TODO TRIANGLE NAME SHOULD BE GIVEN AS AN ARGUMENT*********************
def drawPerpendicular(change = 0):

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

def addPointOnLine(pointName,cordx,cordy,lineName, line1Length, line2Length,node_triangle):
	print("Inside addPointOnLine function and lineName is "+ lineName)
    
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
	query = "START z=node({B}) MATCH z-[:CONNECTED]-b WHERE z.type={A} RETURN b"
        data, metadata = cypher.execute(graph_db, query, {"A": "point","B": temp.id})
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

	print("Find all possible triangles formed by adding this line ")
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

	#print("Add triangles via hardcoding")
	#addTriangle("PSR")
	#addTriangle("PSQ")
	
	print("Exiting addLineInTriangle function")	
#End Of Function

save_triangle = []
def addTriangle(triangleName):
    print("Inside addTRiangleName function")
	
    #This function will save triangle which will help in checking changeTriangle
    save_triangle.append(triangleName)
	
    #This function will simply add triangle node to the graph
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



count_row = 0
dict_three_Point = []
def print_three_points_row(row):
	a ,b,c = row
	global count_row
	count_row = count_row+1
	dict_three_popint.append([a.b.c])
	print(a["name"] +" and "+ b["name"] + " and "+c["name"]) 

def check_join_Existing_three_non_collinear_Points():

	print("Pick existing set of three points which are not connected")
	query = "START b=node(*),a=node(*),c=node(*) MATCH b-[r?:CONNECTED]-a, b-[s?:CONNECTED]-c,c-[t?:CONNECTED]-a WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type = {B} AND a.type = {B} AND c.type = {B} AND t IS NULL AND s IS NULL AND r IS NULL  RETURN a,b,c"
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_three_points_row)
	global count_row
	if count_row == 0:return False

	#Join these points and add info to the triangle TODO  (Please fill the values of angle and length in the below code)
	randomSet = random.sample(dict_three_Point,1)
	
	#This is for generating a new triangle different from previous one
	if save_triangle.length > 0 :
		for randomSet in save_triangle:
			randomSet = random.sample(dict_three_Point,1)
	#End of if
	save_triangle.append(randomSet)
    	print(" randomset of line and point chosen is ")
    	print( "first selectedPoint is " +randomSet[0][0])
    	print( "second selectedPoint is " +randomSet[0][1])
    	node1 = randomSet[0][0]
    	node2 = randomSet[0][1]
    	node3 = randomSet[0][2]

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
	return true
#End Of Function

save_triangle_line_point = []
def check_join_Existing_line_existing_point_not_on_line():
	print("Pick existing set of  point and line not connected to it")
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)
	global count
	if count == 0: return False

	#Join this point with the end-points of the chosen line
	randomSet = random.sample(dictLine_Point,1)
	#This is for generating a new triangle different from previous one
	if save_triangle_line_point.length > 0 :
		for randomSet in save_triangle_line_point:
			randomSet = random.sample(dict_three_Point,1)
	#End of if
	save_triangle_line_point.append(randomSet)
    	print(" randomset of line and point chosen is ")
    	print( "selectedPoint is " +randomSet[0][0])
    	print( "selectedLine is " +randomSet[0][1])
    	node1 = randomSet[0][0]
    	node2 = randomSet[0][1]

	#Fill in the details of the calling function TODO
	lineMane = "hjk"
	length = 10
	ang1 = 10
	ang2 = 30
	ang3 = 40
	ang4 = 50
	node_triangle = "fdg"
	addLineInTriangle(lineName, length, ang1, ang2,ang3,ang4,node_triangle)
	count = 0
	return true
#End Of Function



def generate_join_three_new_points():
	#Generate data for triangle generation
	p1x = random.randint(1,100)
	p1y = random.randint(1,100)
	cord = {p1x, p1y}

	while True:
		p2x = random.randint(1,100)
		p2y = random.randint(1,100)
		temp = {p2x,p2y}
		if temp != cord:break

	while True:
		p3x = random.randint(1,100)
		p3y = random.randint(1,100)
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
	print("second number x is " +str(p2y))
	print("third number x is " +str(p3x))
	print("third number x is " +str(p3y))

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
	triangleName = "PQR" 
	generateTriangle(quesArray, cordArray, triangleName,node_root)
#End Of Function


save_point = []
def addPointFig():
	print("Find an existing line not having existing mid point")
	query = "START c=node(*), b=node(*),a=node(*) MATCH c-[:KD1]->d-[:HAS]->b-[r?:MIDPOINT]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

	#If above case fails, then
	global count
	if count != 0: 
	    #Get the mid-point of the chosen line
	    count = 0
	    randomSet = random.sample(dictLine_Point,1)
	    #This is for generating a new triangle different from previous one
	    if save_point.length > 0 :
		for randomSet in save_point:
			randomSet = random.sample(dict_three_Point,1)
		#End of if
		save_point.append(randomSet)
            print(" randomset of line and point chosen is ")
            print( "selectedPoint is " +randomSet[0][0])
            print( "selectedLine is " +randomSet[0][1])
	    
	    #Get nodes for the end points of the lines, from nodes get the cord values for computing mid-point
	    query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	    data.metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][1][0]})
	    cord1x = data[0]["cordx"]
	    cord1y = data[0]["cordy"]
	    
	    query = "START a=node(*) WHERE a.type = {A} AND a.name = {B} return a"
	    data.metadata = cypher.execute(graph_db, query, {"A" :"point","B":randomSet[0][1][1]})
	    cord2x = data[0]["cordx"]
	    cord2y = data[0]["cordy"]

	    cord3x = 0.5 *(cord1x + cord2x)
	    cord3y = 0.5 *(cord1y + cord2y)

	    query = "START a=node(*) MATCH a-[:HAS]->b WHERE a.type = {A} AND b.name = {B} return a"
	    data.metadata = cypher.execute(graph_db, query, {"A" :"triangle","B":randomSet[0][1]})
	    triangle = data[0]["name"]
	    
	    #TODO
	    #addPointOnLine(pointName,cordx,cordy,line, line1Length, line2Length,node_triangle):
	    addPointOnLine("T", cord3x, cord3y, randomSet[0][1], 10,20,triangle)
	else:
		print("need to think ....this case should not arrive soooooooooon")
	return True
#End Of Function


save_line_existing_line_point_not_on_line = []
def check_existing_line_point_not_on_line():
	print("Pick existing set of  point and line not connected to it")
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

	if len(count) == 0: return False

	#TODO Join this point with the mid-point of the chosen line
	count = 0
	return True

#End Of Function



def check_join_Existing_line_new_point_not_on_line():
	print("Inside check_join_Existing_line_new_point_not_on_line function")
	addPointFig()
	check_join_Existing_line_existing_point_not_on_line()
#End Of Function



def addTriangleFig():
	if check_join_Existing_three_non_collinear_Points() == True :return
	elif check_join_Existing_line_existing_point_not_on_line() == True:return
	elif check_join_Existing_line_new_point_not_on_line() == True:return
	else :
		generate_join_three_new_points()
		return
#End Of Function

def changeObjFigure(geom_object):
	if geom_object == "triangle" :
		print(triangleName)
	if geom_object == "line" :
		#Adding median instead of a simple line
		addMedianTriangle()
	else :
		print(" Inside changeObjFigure, geom_object not defined ")
#End of function

def addObjFigure(geom_object):
	if geom_object == "Triangle" :
		addTriangleFig()
		return
	if geom_object == "line" :
		addLineFig()
	else :
		print(" Inside addObjFigure, geom_object not defined ")
#End of function

def saveObjFigure(obj):
	print("inside save obj figure ")
#EOF
	
def generateObjFigure(geom_object, firstTime = 1, change_fig_not_possible = 0):
	print("inside generateObjFigure obj is "+ geom_object)
	while 1:
		if  firstTime == 1:
		    addObjFigure(geom_object)
		    firstTime = 0
		    saveObjFigure(geom_object)
		    break
		else :
			if  change_fig_not_possible == 1 :
				#TODO addObjfigure which is different from the previous one
				saveObjFigure(geom_object)
				break
			else :
				changeObjFigure(geom_object)
				saveObjFigure(geom_object)
				#TODO IF ALL CHANGES OVER make change_fig_not_possible = 1 **************
	print("exiting from generateObjFigure ")	
#End of Function

def generateConceptFigure(concept, firstTime = 1, change_fig_not_possible = 0):
	print(" inside generateConceptFigure ")
	while 1:
		if firstTime == 1:
			if change_fig_not_possible == 1:
				#TODO addConceptfigure which is different from the previous one
				saveConceptFigure()
				break
			else:
				addConceptFigure()
				firstTime = 0
				saveConceptFigure()
				break
		else:
			changeConceptFigure()
			saveConceptFigure()
			#TODO IF ALL CHANGES OVER make change_fig_not_possible = 1
	print(" exiting from generateConceoptFigure ")
#End of Function
	
def generateFigure(geom_object, concept, theorem):
	print("inside generateFigure function ")
	generateObjFigure(geom_object)
	###########################generateConceptFigure(concept)
	
	#TODO check the functions below
	###########################generateTriangle(quesArray, cordArray, triangleName,node_root)
	###########################drawPerpendicular()
	###########################print("AFTER DRAWING PERPENDICULAR LINE SHOWING ALL RELATIONS")
	#Checking graph nodes by printing all nodes along with their relationship
	###########################query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	###########################cypher.execute(graph_db, query, row_handler=print_row)
	###########################writeFig_Data_to_File()
	print(" exiting from generateFigure ")
#EndOfFunction

#This function is being called from gui.py
def generateQuestion(obj, concept, theorem, num_questions, nowGenerateFigure = 1):
	print("Inside generateQuestion function")
	print(" geom_object is " + str(obj) + " concept is " + str(concept) + " theorem is " + str(theorem) + " num_questions is "+ str(num_questions))
	while num_questions > 0:
		if nowGenerateFigure == 1:
			generateFigure(obj, concept = None, theorem = None)
			nowGenerateFig = 0
		while True :
			generate_solve_new_facts()
			runCHR()
			canGenerateMoreData = generateData(concept, theorem)  #TODO CHECK IF EVERYCASE IS OVER, nowGenerateFig = 1
			#TODO *****************************
			#num_new_facts = Get num of new facts from CHR result file
			num_new_facts = 0 // TODO
			num_questions = num_questions - num_new_facts
			
			if num_questions == 0 :
				break				
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
generateQuestion("Triangle", "Perpendicular", "Pythagoras", "1", nowGenerateFigure = 1)
fo.close()

def runCHR():
	print("inside running CHR function ")
	subprocess.call(["/home/rahul/pythonfiles/v4/shellScript1sh"], shell=True)
#End Of Function


def removeTriangle_Fig(triangleName):
	print("Inside removeTriangle_Fig function")
	oldPerp_Line = triangleName[0] + triangleName[1]
	removeLine_Fig(oldPerp_Line)
	oldPerp_Line = triangleName[1] + triangleName[2]
	removeLine_Fig(oldPerp_Line)
	oldPerp_Line = triangleName[0] + triangleName[2]
	removeLine_Fig(oldPerp_Line)
#End Of Function

#This function is used to delete all lines including median, perpendicular, angle-bisector.
def removeLine_Fig(oldPerp_Line):
	
	#Search the two end points of the given line and then remove line and angle from KD1
	print("Inside removeLine_Triangle")	
	query = "START z=node({B}) MATCH z-[:CONNECTED]-b WHERE z.type={A} RETURN b"
    	data, metadata = cypher.execute(graph_db, query, {"A": oldPerp_Line[0], "B":oldPerp_Line[1]})
    	node_line1 = data[0][0]
    	print(node_line1["name"])
	#del all relations of this node with the figure such as angle, median, perpendicular or length etc
	removePoint_Fig(pointNode)
	#del this node from KD1	
#End Of Function

def removePoint_Fig(pointNode):
	print("inside removePoint_Fig function")
	#del all the relations of this node with other nodes from KDI **************
#End Of Function


'''
#Pick existing set of  point and line not connected to it
query = "START b=node(*),a=node(*) MATCH b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
#cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

#Pick existing set of two points which are not connected
query = "START b=node(*),a=node(*) MATCH b-[r?]->a WHERE NOT(a = b) AND  b.type = {B} AND a.type = {B} AND r IS NULL  RETURN a,b"
#cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_row_new)

#Pick existing set of three points which are not connected
query = "START b=node(*),a=node(*),c=node(*) MATCH b-[r?]-a, b-[s?]-c,c-[t?]-a WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type = {B} AND a.type = {B} AND c.type = {B} AND t IS NULL AND s IS NULL AND r IS NULL  RETURN a,b"
#cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_row_new)

#Pick existing set of two random lines 
query = "START b=node(*) MATCH b-[:HAS]->a, b-[:HAS]->c  WHERE NOT(a = c) AND  b.type = {B} RETURN a,c"
cypher.execute(graph_db, query, {"B":"triangle"}, row_handler=print_row_new)
'''


def slope(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    
    xslope = x2 - x1
    if xslope == 0 : return math.pi/2
    yslope = y2 - y1
    return math.atan(yslope/xslope)
#End Of Function

temp1 = [0, 0]
cord1 = [0, 1]
ang = slope(temp1,cord1)*180/math.pi
print (ang)


save_line_two_non_connecting_Points = []
def check_join_two_non_connecting_Points():
	print("Pick existing set of two points which are not connected")
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONNECTED]->a WHERE NOT(a = b) AND  b.type = {B} AND a.type = {B} AND r IS NULL  RETURN a,b"
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=handle_two_non_connecting_points)
	if len(dictLine_Point) == 0: return false

	#Join these two points
	randomSet = random.sample(dictPoint_Point,1)
	#This is for generating a new triangle different from previous one
	if save_line_two_non_connecting_Points.length > 0 :
		for randomSet in save_line:
			randomSet = random.sample(dict_three_Point,1)
	#End of if
	save_line_two_non_connecting_Points.append(randomSet)
    	print(" randomset of line and point chosen is ")
    	print( "first selectedPoint is " +randomSet[0][0])
    	print( "second selectedPoint is " +randomSet[0][1])
	node1 = randomSet[0][0]
	node2 = randomSet[0][1]
	node1.create_relationship_to(node2, "CONNECTED")
	count = 0
	return True
#End Of Function


def addLineInFig():
	if (check_join_two_non_connecting_Points()):return

	if (check_existing_line_point_not_on_line()):return

	addPointFig()
	addLineInFig()
	return True
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
