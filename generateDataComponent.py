#!/usr/bin/env python

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher
#from kd2_new import graph_db, node_root

# Define a relationship handler...
dict1 = {}
dict2 = {}
def handle_relationship(row):
    a, b,r = row
    tempStr = str(a["name"] + str(r.type) + str(b["name"]))
    dict1[tempStr] = a["name"]
    dict2[tempStr] = b["name"]
    print(a["name"] + " has relationship " + r.type + " with " + b["name"])
#End of function

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



#Get 
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
    if rel == "PERP" :
    	query = "START a=node(*) MATCH a-[r:PERPENDICULAR]-b WHERE a.name = {A}  RETURN r"
    elif rel == "HAS": 
    	query = "START a=node(*) MATCH a-[r:HAS]-b WHERE a.name = {A}  RETURN r"
    else :
	print("given relationship not found ")
    data,metadata = cypher.execute(graph_db, query, {"A" :originalSide})
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
    return sideName
    print("Exiting getSideFromRelationship function")
#EndOfFunction


theoremList = ["pythagorus", "inequality"]
def generateData(theorem = None, num_questions = 1):
    print("Inside generateData function")

    #If no theorem is given, pick randomly from the existing database
    theorem = random.sample(theoremList, 1)
    while 1 :	
	if theorem == "pythagorus" :
		
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

		#side2 = "PS"

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

		#We have different options here, currently I am taking num_of_questions > 1 . WE can have options such as complex questions, interesting questions, For output data
		num_questions = num_questions - 1
		if num_questions == 0 :
			break
		elif dict1.len() == 0:
			theorem = random.sample(theoremList, 1)
			continue
		else:
			rel1 = random.choice(dict1.keys())
			print(rel1)
			originalSide = dict1[rel1]
			originalObject = dict2[rel1]
			selectedSide = str(getSideFromRelationship(rel1,originalSide, originalObject))
			print("selected side is " + str(selectedSide))
			if selectedSide :
				getInput_OutputFromSide(selectedSide, originalSide,originalObject,0,1)
				num_questions = num_questions - 1
				if num_questions == 0 :
					break
			else: 
				print(" no side can be selected now ")
				theorem = random.sample(theoremList, 1)
	#End of outer if
	if theorem == "inequality" :
		print("going for inequality theorem ")
    #End of while loop
    print("Exiting generateData function")
#EndOfFunction

