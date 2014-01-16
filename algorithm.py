#!/usr/bin/env python

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher
from kd2_new import graph_db, node_root

import subprocess
import random
import math
import string
import sys

#Storing command line arguments
total = len(sys.argv)
cmdargs = str(sys.argv)
#print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
#print ("Script name: %s" % str(sys.argv[0]))
#for i in xrange(total):
 #   print ("Argument # %d : %s" % (i, str(sys.argv[i])))

geom_object = str(sys.argv[1])
concept = str(sys.argv[2])
theorem = str(sys.argv[3])
num_questions = str(sys.argv[4])

#Assigning difficulty points to geometric objects addition
addLinePoints = 10
addTrianglePoints = 20

#Assigning difficulty points to geometric concept addition
addPerpendicularPoints = 15
addMedianPoints = 15

#Assigning difficulty points to geometric theorem addition
adding_line_diff_level = {"both_existing_points":1, "one_new_point":2,"both_new_points":3}
adding_Triangle_diff_level = {"all_existing_points":1,"existing_point_existing_line":2,"existing_point_new_line":3, "existing_line_new_point" :4, "common_vertex ":5, "common_side" :6}
theoremList_diff_level = {"pythagorus" :6, "converse_pythagorus" :2, "Inequality_min" :4, "Inequality_max" :3}
theoremList_concept_map = {"pythagorus" :"perp", "converse_pythagorus" :"perp", "Inequality_min" :"triangle", "Inequality_max" :"triangle"}

#Initial difficulty level
diff_level = []
diff_level.append(0)

#Getting new and different characters for naming each time this function is called
listChar = []
string.letters = 'DEFGHIJKLMNOSTUVWXYZ'
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
fo.write("hello\n")

# Define a new row handler...
dictLine_Point = []
count = []
def print_row_new(row):
    a, b = row
    count.append(1)
    dictLine_Point.append([str(a["name"]),str(b["name"])])
    print(a["name"] + " is perpendicular " + b["name"])

# Define a row handler for file writing...
def print_file_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])
    writeToFile(a["name"], r.type, b["name"])
#End Of Function

# Define a row handler...
def print_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])
#End of Function

# Define a relationship handler...
dict1 = {}
dict2 = {}
def handle_relationship(row):
    a, b,r = row
    tempStr = str(a["name"] + str(r.type) + str(b["name"]))
    dict1[tempStr] = a["name"]
    dict2[tempStr] = b["name"]
    print(a["name"] + " has relationship " + r.type + " with " + b["name"])
#End of Function


def writeToFile(objectName, relationName, objectName1 = None, value=0):
	print(" inside writeToFile function ")
	if relationName == "KD1":
		fo.write("triangle("+ objectName1[0].lower()+objectName1[0] + "," + objectName1[1].lower()+objectName1[1]+","+objectName1[2].lower() +objectName1[2]+"),\n")
	elif relationName == "PERPENDICULAR":
		fo.write("perp(" +objectName[0].lower() +objectName[0] + "," +objectName[1].lower() +objectName[1] + "," +objectName1[0].lower() +objectName1[0] + "," +objectName1[1].lower() + objectName1[1]+ "),\n")
	elif relationName == "length":
		fo.write("length(" +objectName[0].lower() +objectName[0] + "," +objectName[1].lower() +objectName[1]+","+str(value)+"),\n")	
	else:
		print(relationName + " has not been added till now\n")

#End Of Functioni

def writeFig_Data_to_File():
	print(" inside writeFig_Data_to_File function ")
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_file_row)
#End Of Function

def write_Name_In_File(letter):
	#name(A,'A'),
	fo.write("name(" +letter.lower() +letter + ",'" + letter + "'),\n") 
#End Of Function

def generateTriangle(quesArray, cordArray, triangleName,node_root):
	diff_level[0] = diff_level[0] + addTrianglePoints
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

def angle_lines(pt1, pt2,pt3,pt4):
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

def generate_join_three_new_points():
	print("inside generate_join_three_new_points function")
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

	ang1 = 10 #angle_lines(cord, temp)
	ang2 = 10 #angle_lines(temp, temp1)
	ang3 = 10 #angle_lines(cord, temp1)

	quesArray.append(ang1)
	quesArray.append(ang2)
	quesArray.append(ang3)
	p1 = getNewPointName()
	p2 = getNewPointName()
	p3 = getNewPointName()
	triangleName = p1+p2+p3
	generateTriangle(quesArray, cordArray, triangleName,node_root)

#End Of Function

count_row = 0
dict_three_Point = []
def print_three_points_row(row):
	a ,b,c = row
	count_row = count_row+1
	dict_three_popint.append([a.b.c])
	print(a["name"] +" and "+ b["name"] + " and "+c["name"]) 

def check_join_Existing_three_non_collinear_Points():

	print("Pick existing set of three points which are not connected")
	query = "START b=node(*),a=node(*),c=node(*) MATCH b-[r?:CONNECTED]-a, b-[s?:CONNECTED]-c,c-[t?:CONNECTED]-a WHERE NOT(a = b) AND NOT(b = c) AND NOT(a = c) AND  b.type = {B} AND a.type = {B} AND c.type = {B} AND t IS NULL AND s IS NULL AND r IS NULL  RETURN a,b,c"
	cypher.execute(graph_db, query, {"B":"point"}, row_handler=print_three_points_row)
	if count_row == 0:return false

	#Join these points and add info to the triangle TODO  (Please fill the values of angle and length in the below code)
	randomSet = random.sample(dict_three_Point,1)
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

def check_join_Existing_line_existing_point_not_on_line():
	print(" inside check_join_Existing_line_existing_point_not_on_line function")

	print("Pick existing set of  point and line not connected to it")
	query = "START b=node(*),a=node(*) MATCH b-[r?:CONTAIN]->a WHERE b.type = {A} AND a.type = {B}  AND r IS NULL RETURN a,b"
	cypher.execute(graph_db, query, {"A" :"line","B":"point"}, row_handler=print_row_new)

	if len(count) == 0: return false

	#Join this point with the end-points of the chosen line
	randomSet = random.sample(dictLine_Point,1)
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


def check_join_Existing_line_new_point_not_on_line():
	print(" inside check_join_Existing_line_new_point_not_on_line function ")
	addPointOnLine()
	check_join_Existing_line_existing_point_not_on_line()

#End Of Function

def addTriangleFig():
	print("inside addTriangleFig function")
	#if (check_join_Existing_Three_non_collinear_Points()):return
	#elif (check_join_Existing_line_existing_point_not_on_line()) :return
	#elif (check_join_Existing_line_new_point_not_on_line()):return
	#else :
	generate_join_three_new_points()
	return
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
	diff_level[0] = diff_level[0] + addLinePoints
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
	        # TODO addTriangle(tempSide1)
		#Compute angles and addAngleRelationship TODO
		p3 = [row[0]["cordx"],row[0]["cordy"]]	
		print("Before calculating angle for first point")
		print(p1)
		print(p2)
		print(p3)
		ang1 = angle_lines(p1, p2, p1, p3)
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
	        # TODO addTriangle(tempSide1)
		#Compute angles and addAngleRelationship TODO
		p3 = [row[0]["cordx"],row[0]["cordy"]]	
		print("Before calculating angle for second point")
		print(p1)
		print(p2)
		print(p3)
		ang1 = angle_lines(p1, p2, p2, p3)
		temp.create_relationship_to(row[0], "ANGLE", {"value": ang1})

	#print("Add triangles via hardcoding")
	#addTriangle("PSR")
	#addTriangle("PSQ")
	
	print("Exiting addLineInTriangle function")
	
	
#End Of Function

save_perp = None
old_perp_line = None
def drawPerpendicular(change = 0):

	print("Inside drawPerpendicular function")
	diff_level[0] = diff_level[0] + addPerpendicularPoints
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
	if change == 1:
	    while save_perp == randomset:
		randomSet = random.sample(dictLine_Point,1)
	    
	    # TODO Remove old perpendicular line
	    removeLine_Fig(old_perp_line)
	save_perp = randomSet
	print(" randomset of line and point chosen is ")
	print( "selectedPoint is " +randomSet[0][0])
	print( "selectedLine is " +randomSet[0][1])
	selectedLine = randomSet[0][1]
	selectedPoint = randomSet[0][0]

	#Find new point by computation TODO

	#Add point on line
	newPoint = getNewPointName()
	print(newPoint)
	write_Name_In_File(newPoint)
	addPointOnLine(newPoint,10,20,selectedLine,40,40,node_triangle)

	#Add line in triangle
	newLine = selectedPoint + newPoint
	old_perp_line = newLine
	addLineInTriangle(newLine, 40, 90, 90,20,25,node_triangle)

	#Currently hard coding for perpendicular line, PS perp QR, PS perp QS, PS perp SR
	perpBase1 = newPoint + selectedLine[0]
	perpBase2 = newPoint + selectedLine[1]
	perpBase3 = selectedLine
	addPerpendicularAngle(newLine,perpBase1)
	addPerpendicularAngle(newLine,perpBase2)
	addPerpendicularAngle(newLine,perpBase3)
	
	print("Exiting drawPerpendicular function")
	
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

    query = "START a=node(*),b=node(*),c=node(*) MATCH a-[:HAS|INDIRECTLY_HAS]->b-[:PERPENDICULAR]-c<-[:HAS|INDIRECTLY_HAS]-a WHERE a.type = {B} RETURN a"
    data,metadata = cypher.execute(graph_db, query,{"B": "triangle"})
    for row in data:
	temp3 = row[0]
        list_right_triangles.append(temp3)
        print("one of the right angle triangle is "+temp3["name"])
    print("Exiting getAllRightAngleTriangle function")
#End Of Function

def saveObjFigure():
	print("inside saveOBjFigure function ")
#End of Function

def addObjFigure(geom_object):
	print("inside addOBjFigure function ")
	if geom_object == "triangle":
		addTriangleFig()
	if geom_object == "line":
		print("add here")
#End of Function

def saveConceptFigure():
	print("inside saveConceptFigure function ")
#End of Function

def addConceptFigure(concept):
	print("inside addConceptFigure function ")
	if concept == "perp":
		drawPerpendicular()
#End of Function

def saveDataFigure():
	print("inside saveDataFigure function ")
#End of Function

def getInput_OutputFromSide(selectedSide, originalSide, originalTriangle, input1, output1):

    print("inside getInput_Output function")

    conversionDict = {}
    conversionDict[selectedSide[0]] = originalSide[0]
    conversionDict[selectedSide[1]] = originalSide[1]

    print("selected side is " + selectedSide)
    inputStr = "ABC"
    index0 = inputStr.index(selectedSide[0])
    index1 = inputStr.index(selectedSide[1])

    if index0 == 0 : 
	if index1 == 1: saveIndex = 2
	if index1 == 2:saveIndex = 1
    elif index0 == 1:
	if index1 == 0: saveIndex = 2
	if index1 == 2:saveIndex = 0
    else:
	if index1 == 0: saveIndex = 1
	if index1 == 1:saveIndex = 0

    print("original triangle is " + originalTriangle)
    print("original side is " + originalSide)

    #inputStr1 = "PQS"
    inputStr1 = originalTriangle
    index0 = inputStr1.index(originalSide[0])
    index1 = inputStr1.index(originalSide[1])

    if index0 == 0 : 
	if index1 == 1: saveIndex1 = 2
	if index1 == 2:saveIndex1 = 1
    elif index0 == 1:
	if index1 == 0: saveIndex1 = 2
	if index1 == 2:saveIndex1 = 0
    else:
	if index1 == 0: saveIndex1 = 1
	if index1 == 1:saveIndex1 = 0

    print("saveIndex is " + str(saveIndex) + " and saveIndex1 is " + str(saveIndex1))
    conversionDict[inputStr[saveIndex]] = inputStr1[saveIndex1]

    if input1 == 1:
	print("Query for getting input for a given side from KD2")
	query = "START a=node(*) MATCH a-[:INPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c" 
	data,metadata = cypher.execute(graph_db, query, {"A" :selectedSide})
    
    if output1 == 1:
	print("Query for getting output for a given side from KD2")
	query = "START a=node(*) MATCH a-[:OUTPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c"
	data,metadata = cypher.execute(graph_db, query, {"A" :selectedSide})

    #Randomly select one of the input
    print(" Printing query result of input/output")
    array = []
    for row in data:
        print(row[0]["name"])
	array.append(str(row[0]["name"]))

    print (array)
    node = random.sample((array),  1)
    str1 = ''.join(node)
 
    print("node selected is " + str1)
    print("Query for getting exact I/O for a given side from KD2")
    query = "START a=node(*) MATCH a-[:NEEDS]->b WHERE a.name = {A} RETURN b"
    data,metadata = cypher.execute(graph_db, query, {"A" :str1})
    for row in data:
	print("printing first row")
	print(row[0]["name"])
	resultName = str(row[0]["name"])

	conversionString  = conversionDict[resultName[0]] + conversionDict[resultName[1]]
	conversionString1 = conversionDict[resultName[1]] + conversionDict[resultName[0]]
	print("Get the values of the length or the angle from the fig graph")
	query = "START z=node(*) WHERE z.name={A} OR z.name = {B} RETURN z"
	data, metadata = cypher.execute(graph_db, query, {"A": conversionString,"B": conversionString1})
	temp3 = data[0][0]
	print(temp3["value"])
	writeToFile(conversionString, "length", None, temp3["value"])
    print("Exiting getInput_Output function")
    
#EndOfFunction	

#Get Input and Output for these objects
def getSideFromRelationship(rel, originalSide, originalObject):   
    print("Inside getSideFromRelationship function")
    sideName = None 

    #Get relationship between originalSide with othersides of the triangle(OriginalObject) in this case
    index1 = originalObject.index(originalSide[0])
    index2 = originalObject.index(originalSide[1])
    index3 = -1
    if index1 == 0: 
	if index2 == 1: index3 = 2
	if index2 == 2: index3 = 1
    elif index1 == 1: 
	if index2 == 0: index3 = 2
	if index2 == 2: index3 = 0
    elif index1 == 2: 
	if index2 == 1: index3 = 0
	if index2 == 0: index3 = 1
     
    side1 = originalSide[0] + originalObject[index3]
    side2 = originalSide[1] + originalObject[index3]
    side3 = originalObject[index3] + originalSide[0]
    side4 = originalObject[index3] + originalSide[1]
    
    #Get the relations stored in data
    query = "START a=node(*) MATCH a-[r:PERPENDICULAR]-b WHERE a.name = {A}  RETURN r"
    data,metadata = cypher.execute(graph_db, query, {"A" :originalSide})
    count = 0
    for row in data:
	count = count +1
    if count > 0 : rel = "PERP"
    else: rel = "HYP"
    rel1 = "PERP"
    rel2 = "HYP"

    #For time being commenting it TODO
    #rel1 = "HAS_AS_PERP_SIDE"
    #rel2 = "HAS_AS_HYP_SIDE"
    if rel == rel1:
	options = {"AB","BC"}
	index_ = random.randint(0, 1)
	if index_ == 0:	sideName = "AB"
	if index_ == 1:	sideName = "BC"
    elif rel == rel2:
	sideName = "CA"
    return sideName
    print("Exiting getSideFromRelationship function")
#EndOfFunction


def addDataFigure(concept, theorem):
	print("inside addDataFigure function ")
	if theorem == "pythagorean" :
		
		#Get all right angle triangles in the figure
		getAllRightAngleTriangles()
		randomSet = random.sample(list_right_triangles,1)
		a = randomSet
		print(a[0]["name"])

		#Choose one triangle randomly
		selectedNode = a[0]

		#Query for getting all sides of a given triangle through its name
		query = "START a=node({A}) MATCH a-[:HAS]-b RETURN b"
		data,metadata = cypher.execute(graph_db, query, {"A" :selectedNode.id})

		#Getting random side from above array
		print(" Printing result from data in query ");
		array = []
		for row in data:
			print(row[0]["name"])
		array.append(str(row[0]["name"]))

		print (array)
		side1 = random.sample((array),  1)
		side2 = ''.join(side1) 
		print(side2)

		#Query for getting all relationships of a selected side with other objects
		print("Query for getting all relationships of a selected side with other objects")
		query = "START a=node(*) MATCH a-[r:HAS]-b WHERE a.name = {A}  RETURN a,b,r"
		cypher.execute(graph_db, query, {"A" :side2}, row_handler=handle_relationship)
		
		#Get the relations stored in data
		query = "START a=node(*) MATCH a-[r:HAS]-b WHERE a.name = {A}  RETURN r"
		data,metadata = cypher.execute(graph_db, query, {"A" :side2})
		
		print(len(dict1))
		rel = random.choice(dict1.keys())
		print(rel)
		originalSide = dict1[rel]
		originalObject = dict2[rel]
		print("original side is " + originalSide)
		print("original object is " + originalObject)
		#tempDict[rel] = originalSide
		del dict1[rel]
	   
		#For input data
		selectedSide = str(getSideFromRelationship(rel,originalSide,originalObject))
		print("selected side is " + str(selectedSide))
		if selectedSide :
			getInput_OutputFromSide(selectedSide, originalSide, originalObject,1,0)
		
		if len(dict1) > 0:
			#For output data
			print(len(dict1))
			rel1 = random.choice(dict1.keys())
			print(rel1)
			originalSide = dict1[rel1]
			originalObject = dict2[rel1]
			selectedSide = str(getSideFromRelationship(rel1,originalSide, originalObject))
			print("selected side is " + str(selectedSide))
			if selectedSide :
				getInput_OutputFromSide(selectedSide, originalSide,originalObject,0,1)
		
	print("Exiting addDataFigure function")

#EndOfFunction

def generateObjFigure(geom_object, firstTime = 1, change_fig_not_possible = 0):
	print("inside generateObjFigure function ")
	while 1:
		if firstTime == 1:
			if change_fig_not_possible == 1:
				changeObjFigure() 
				saveRemainingOptions()
				break
			else:
				addObjFigure(geom_object)
				firstTime = 0
				saveObjFigure()
				break
		else:
			changeObjFigure()
			saveRemainingOptions()
			#TODO IF ALL CHANGES OVER make change_fig_not_possible = 1
	#End of while 
	
#End of Function

def generateConceptFigure(concept, firstTime = 1, change_concept_not_possible = 0):
	print("inside generateConceptFigure function ")
	while 1:
		if firstTime == 1:
			if change_concept_not_possible == 1:
				#TODO addObjfigure which is different from the previous one
				saveConceptFigure()
				break
			else:
				addConceptFigure(concept)
				firstTime = 0
				saveConceptFigure()
				break
		else:
			changeConceptFigure()
			saveConceptFigure()
			#TODO IF ALL CHANGES OVER make change_fig_not_possible = 1
	#End of while 
	
#End of Function

def generateFigure(geom_object, concept):

	print("inside generateFigure function ")
	generateObjFigure(geom_object, 1, 0)
	print("AFTER DRAWING FIGURE OBJECT SHOWING ALL RELATIONS")
	#Checking graph nodes by printing all nodes along with their relationship
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_row)
	generateConceptFigure(concept)
	print("AFTER DRAWING FIGURE CONCEPT SHOWING ALL RELATIONS")
	#Checking graph nodes by printing all nodes along with their relationship
	query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
	cypher.execute(graph_db, query, row_handler=print_row)

	writeFig_Data_to_File()
#End of Function


def generateData(concept,theorem, firstTime = 1, change_data_not_possible = 0):
	print(" inside generateData function")
	while 1:
		if firstTime == 1:
			if change_data_not_possible == 1:
				#TODO addData which is different from the previous one
				saveDataFigure()
				break
			else:
				addDataFigure(concept, theorem)
				firstTime = 0
				saveDataFigure()
				break
		else:
			changeDataFigure()
			saveDataFigure()
			#TODO IF ALL CHANGES OVER make change_fig_not_possible = 1
	#End of while 
#End of Function

def runCHR():
	print(" inside runCHR function")
	#subprocess.call(["/home/rahul/Dropbox/Public/pythonFiles/shellScript.sh"], shell=True)
#End Of Function
	
def generate_solve_new_facts():
	print(" inside generate_solve_new_facts function ")
	runCHR()
#End of Function

def generateQuestion(geom_object, concept, theorem, num_questions, nowGenerateFigure):
	print("Inside generateQuestion function geom_object is "+ str(geom_object)+ "\n concept is "+str(concept)+"\n theorem is "+ str(theorem) + "\n num_questions are "+str(num_questions)+ "\n nowGenerateFigure is "+ str(nowGenerateFigure))
	while num_questions > 0:
		if nowGenerateFigure == 1:
			generateFigure(geom_object, concept)
			nowGenerateFig = 0
		#End of if
		generateData(concept, theorem) #TODO CHECK IF EVERYCASE IS OVER, nowGenerateFig = 1
		generate_solve_new_facts()
	#	//TODO 
	#	num_new_facts = Get num of new facts from CHR result file
		num_new_facts = 1 
		num_questions = int(num_questions) - num_new_facts
		
		if num_questions == 0 :
			nowGenerateFig = 0
			break
	#End of while	
#End of function

generateQuestion(geom_object, concept, theorem, num_questions, nowGenerateFigure = 1)

fo.close()
