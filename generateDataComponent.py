#!/usr/bin/env python

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher
from macro import *
from cypher_handling_functions import *
from macro import graph_db, node_root
import random

# Get all the right angles in a given configuration used in pythagorean theorem
#list_right_triangles = []
def getAllRightAngleTriangles(list_right_triangles, ):
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
    return list_right_triangles
#End Of Function

# Get input and output options from the given side
def getInput_OutputFromSide(theorem, selectedSide, originalSide, originalTriangle, input1, output1):

    print("inside getInput_OutputFromSide function")

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
    
    #First reach to the theorem asked , then go inside it to get the sides
    if theorem == "pythagoras" :
        query = "START a=node(*) MATCH a-[r:PYTHAGORAS]-b WHERE b.type = {A}  RETURN b"
        data,metadata = cypher.execute(graph_db, query, {"A" :"triangle"})
	node_triangle_temp = data[0]
	print(node_triangle_temp["name"])
    if theorem == "Inequlaity" :
	print("pythagoas theorem is not selected ")

    if input1 == 1:
	print("Query for getting input for a given side from KD2")
	query = "START a=node({B}) MATCH a-[:INPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c" 
	data,metadata = cypher.execute(graph_db, query, {"A" :selectedSide, "B" : node_triangle_temp.id})
    
    if output1 == 1:
	print("Query for getting output for a given side from KD2")
	query = "START a=node({B}) MATCH a-[:OUTPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c"
	data,metadata = cypher.execute(graph_db, query, {"A" :selectedSide, "B": node_triangle_temp.id})

    #Randomly select one of the input
    print(" Printing query result of input/output")
    array = []
    for row in data:
        print(row[0]["name"])
	array.append(str(row[0]["name"]))

    print (array)
    node = random.sample((array),  1)
    str1 = ''.join(node)
	
    input_list = []
    print("node selected is " + str1)
    print("Query for getting exact I/O for a given side from KD2")
    query = "START a=node(*) MATCH a-[:NEEDS]->b WHERE a.name = {A} RETURN b"
    data,metadata = cypher.execute(graph_db, query, {"A" :str1})
    for row in data:
		print("printing first row")
		print(row[0]["name"])
		resultName = str(row[0]["name"])
		input_list.append(str(row[0]["name"]))
		
	#TODO same thing as above, for storing output in output_list

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

#Get side from the relationship such as base, perpendicular or hypotenuse
def getSideFromRelationship(theorem,rel, originalSide, originalObject):   
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
    
    #First reach to the theorem asked , then go inside it to get the sides
    if theorem == "pythagoras" :
        query = "START a=node(*) MATCH a-[r:PYTHAGORAS]-b WHERE b.type = {A}  RETURN b"
        data,metadata = cypher.execute(graph_db, query, {"A" :"triangle"})
	node_triangle_temp = data[0]
	print(node_triangle_temp["name"])

        #Get the relations stored in data
        if rel == "PERP" :
    	    query = "START a=node({B}) MATCH a-[:HAS]-c-[r:PERPENDICULAR]-b WHERE b.name = {A}  RETURN r"
        elif rel == "HAS": 
    	    query = "START a=node({B}) MATCH a-[:HAS]-b WHERE b.name = {A}  RETURN r"
        else :
			print("given relationship not found ")
        data,metadata = cypher.execute(graph_db, query, {"A" :originalSide, "B":node_triangle_temp.id})
        count = 0
        for row in data:
	    count = count +1
        if count > 0 : _rel = "PERP"
        else: _rel = "HYP"
        rel1 = "PERP"
        rel2 = "HYP"

        #For time being commenting it TODO
        #rel1 = "HAS_AS_PERP_SIDE"
        #rel2 = "HAS_AS_HYP_SIDE"
        if _rel == rel1:
	    options = {"AB","BC"}
	    index_ = random.randint(0, 1)
	    if index_ == 0:	sideName = "AB"
	    if index_ == 1:	sideName = "BC"
        elif _rel == rel2:
	    sideName = "CA"
    #End of pythagoras theorem
    else :
		print("theorem selected is not pythagoras ")
    return sideName
    print("Exiting getSideFromRelationship function")
#EndOfFunction

#This function will save the current state of the data
#It includes theorem selected, attributes related to the theorem in the figure, input selected, expected output
def saveCurrentState(theorem, selectedSide, input_list, output_list):
	print("Inside saveCurrentState function")
	currentState_input = input_list
	currentState_output = output_list
	currentState_selectedSide = selectedSide
	current_State_theorem = theorem
	currentState_theorem_data = {currentState_selectedSide, currentState_input, currentState_output}
	cuurentState_theorem_dict = {current_State_theorem : currentState_theorem_data}
	print("theorem is "+ theorem)
	print(" selected side is " + selectedSide)
	print(" input_list is "+ input_list)
	print(" output_list is "+ output_list)
	print("Exiting saveCurrentState function")
#EOF

def getPreviousState():
	return currentState_data
#EOF
def check_theorem_object_map(theorem, objName, objType):
    print("inside check_theorem_object_map function ")
    # This function will check if the geom object can be used with the given theorem
    # For example if a line is checked with pythagoras theorem, so it will check if it is a output of pythagoras theorem 
    # Similarly for each theorem, a condition will be checked for each object
    # This function would be called when you have given one data( say input data) and now you have to give 
	# more data, first check if the input can be used in other theorem or not
	
	#Three cases need to handle in this function
	#1) Is there a available option of attribute selected in previous theorem
	#2) If not, is there are other theorems stored in stack
	#3) If not, is there are default theorems available
	#4) If not then return false
#EOF


# This is the main function of this component. It will perform the following operations
# 1) Pick the theorem given by the user or randomly from the database (if no theorem is given by the user)
# 2) Now depending on the theorem picked, get the required configuration (ex. right angle triangle in case of pythagorean theorem)
# 3) For pythogorean theorem, from the selected configuration, pick one triangle randomly
# 4) Pick one side randomly from the previously selected triangle 
# 5) Get the relationship of this side with the selected triangle (ex. base, perpendicular side or hypotenuse side)
# 6) Get the input and output from the KT
# 7) Subtract the number of questions and redo the whole process if the number of remaining questions are still > 0
# 8) Similar concept will be applied for other theorems
def generateData(graph_db, theorem_list = None, firstTime = 1):
    print("Inside generateData function and theorem_list is "+ theorem_list)

    if firstTime == 1 :	
		#If no theorem is given, pick randomly from the existing database
		if len(theorem_list) == 0 :
			theorem = random.sample(default_theoremList, 1)
		else :
			theorem = random.sample(theorem_list, 1)	
		if theorem_list == "Pythagoras" :
			
			#Get all right angle triangles in the figure and save it in a list
			list_right_triangles = getAllRightAngleTriangles(graph_db)
			
			#Generate a side - theorem mapping graph (This can be done in above function also..need to think)
			# TODO generateMap_side_theorem(graph_root, list_right_triangles)
			
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
			side = ''.join(side1) 
			print(side)

			#Query for getting all relationships of a selected side with other objects in the given figure
			print("Query for getting all relationships of a selected side with other objects in the given figure")
			query = "START a=node(*) MATCH a-[r:HAS]-b WHERE a.name = {A}  RETURN a,b,r"
			cypher.execute(graph_db, query, {"A" :side}, row_handler=handle_relationship)
			
			#Get the relations stored in data
			query = "START a=node(*) MATCH a-[r:HAS]-b WHERE a.name = {A}  RETURN r"
			data,metadata = cypher.execute(graph_db, query, {"A" :side})
			
			print(len(dict1))
			rel = random.choice(dict1.keys())
			print(rel)
			originalSide = dict1[rel]
			originalObject = dict2[rel]
			print("original side is " + originalSide)
			print("original object is " + originalObject)
			
			# It is deleted so that next selection should not select this again
			del dict1[rel]
		   
			#For input data...it means selecting side based on base, perpendicular or hypotenuse relationship
			selectedSide = str(getSideFromRelationship(theorem,rel,originalSide,originalObject))
			print("selected side is " + str(selectedSide))
			if selectedSide :
				getInput_OutputFromSide(theorem,selectedSide, originalSide, originalObject,1,0)
				saveCurrentState(theorem, selectedSide, input_list, output_list)
				return
		if theorem == "inequality" :
			print("going for inequality theorem ")	
    else:	
		#First time is not zero
		#Check for the previous state and pick the other options from the theorem selected last time
		previousState_data = getPreviousState()
		
		#while 1:
		#For checking if the selected side or angle can be used in other theorem
			#isAvailable_list = check_theorem_object_map(graph_root, theorem, objName, objType) 
			#if isAvailable_list[0] == true
			#	if isAvailable_list[1] == "pythagoras"
			#		break
			# 	else
			#		continue
				#End of inner if
			#End of outer if
		#End of while loop	 
	#End of outermost if
	
	
    print("Exiting generateData function")
#EndOfFunction

