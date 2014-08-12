# Define a relationship handler...


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



#fo.close()

dict1 = {}
dict2 = {}
def handle_relationship(row):
    a, b,r = row
    tempStr = str(a["name"] + str(r.type) + str(b["name"]))
    dict1[tempStr] = a["name"]
    dict2[tempStr] = b["name"]
    print(a["name"] + " has relationship " + r.type + " with " + b["name"])
#End of function

# Define a new row handler...
dictLine_Point = []
countLine = []
def print_row_new(row):
    a, b = row
    global countLine
    countLine.append(1)
    dictLine_Point.append([str(a["name"]),str(b["name"])])
    print(a["name"] + " is not connected with the line " + b["name"])
#End of function

def handle_row(row):
    node = row[0]
    print (node)
#End of function


# Define a row handler...
def print_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])
#End of function


# Define a three non connected points handler...
def handle_three_points(row):
    a, b,c = row
    print(a["name"] + " and " +b["name"] + "and " + c["name"])
#End Of Function

# Define a row handler for file writing...
def print_file_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])
    writeToFile(a["name"], r.type, b["name"])
#End Of Function

count_row = 0
dict_three_point = []
def print_three_points_row(row):
	a ,b,c = row
	global count_row
	count_row = count_row+1
	dict_three_point.append(a["name"]+b["name"]+c["name"])
	print(a["name"] +" and "+ b["name"] + " and "+c["name"]) 
#End Of Function

dictPoint_Point = []
def handle_two_non_connecting_points(row):
    a,b = row
    dictPoint_Point.append([a,b])
    print(a["name"] + " with " + b["name"])
#End Of Function

# Define a row handle for handline line conatining two points...
line_container = []
def handle_line(row):
    p1, p2,line = row
    print(p1["name"] + " and " + p2["name"] + "belongs to the line "+ line["name"])
    line_container.append([p1,p2,line])
#EOF
