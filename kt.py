#!/usr/bin/env python

"""
Simple example showing node and relationship creation plus
execution of Cypher queries
"""

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher

# Attach to the graph db instance
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

graph_db.clear()
#Create root node
root = "Root"
node_root, = graph_db.create({"name":root,"type":"node"})

node_kd2, = graph_db.create({"name": "THEOREM1","type":"node"})
node_root.create_relationship_to(node_kd2, "KD2")
node_triangle, = graph_db.create({"name": "ABC","type":"triangle"})
node_kd2.create_relationship_to(node_triangle, "Pythagorean")

# Create three nodes
node_a, node_b, node_c = graph_db.create(
    {"name": "AB","type":"line"},
    {"name": "BC","type":"line"},
    {"name": "CA","type":"line"}
)

# Join the nodes with a HAS relationship
rel_triangle_a = node_triangle.create_relationship_to(node_a, "HAS")
rel_triangle_b = node_triangle.create_relationship_to(node_b, "HAS")
rel_triangle_c = node_triangle.create_relationship_to(node_c, "HAS")

#Create input nodes
node_in1, = graph_db.create({"name":"in1","type":"node"})
node_in2, = graph_db.create({"name":"in2","type":"node"})
node_in3, = graph_db.create({"name":"in3","type":"node"})

node_out1, = graph_db.create({"name":"out1","type":"node"})
node_out2, = graph_db.create({"name":"out2","type":"node"})
node_out3, = graph_db.create({"name":"out3","type":"node"})

node_in11, = graph_db.create({"name":"in11","type":"node"})
node_in12, = graph_db.create({"name":"in12","type":"node"})
node_in21, = graph_db.create({"name":"in21","type":"node"})
node_out11, = graph_db.create({"name":"out11","type":"node"})
node_out21, = graph_db.create({"name":"out21","type":"node"})
node_out31, = graph_db.create({"name":"out31","type":"node"})

# Join the nodes with a  INPUT relationship
rel_a_in1 = node_a.create_relationship_to(node_in1, "INPUT")
#rel_a_in4 = node_a.create_relationship_to(node_in1, "MIDPOINT")
rel_b_in2 = node_b.create_relationship_to(node_in2, "INPUT")
rel_c_in3 = node_c.create_relationship_to(node_in3, "INPUT")

rel_a_out1 = node_a.create_relationship_to(node_out1, "OUTPUT")
rel_b_out2 = node_b.create_relationship_to(node_out2, "OUTPUT")
rel_c_out3 = node_c.create_relationship_to(node_out3, "OUTPUT")

rel_in1_in11 = node_in1.create_relationship_to(node_in11, "CONTAIN")
rel_in1_in12 = node_in1.create_relationship_to(node_in12, "CONTAIN")
rel_out1_out11 = node_out1.create_relationship_to(node_out11, "CONTAIN")

rel_in2_in21 = node_in2.create_relationship_to(node_in21, "CONTAIN")
rel_in2_in22 = node_in2.create_relationship_to(node_in12, "CONTAIN")
rel_out2_out21 = node_out2.create_relationship_to(node_out21, "CONTAIN")

rel_in3_in31 = node_in3.create_relationship_to(node_in21, "CONTAIN")
rel_in3_in32 = node_in3.create_relationship_to(node_in11, "CONTAIN")
rel_out3_out31 = node_out3.create_relationship_to(node_out31, "CONTAIN")

node_in11.create_relationship_to(node_b, "NEEDS")
node_in12.create_relationship_to(node_c, "NEEDS")

node_out11.create_relationship_to(node_b, "NEEDS")
node_out11.create_relationship_to(node_c, "NEEDS")

node_in21.create_relationship_to(node_a, "NEEDS")
node_out21.create_relationship_to(node_a, "NEEDS")
node_out21.create_relationship_to(node_c, "NEEDS")

node_out31.create_relationship_to(node_b, "NEEDS")
node_out31.create_relationship_to(node_a, "NEEDS")

#End of function

#Making KD2 for Trigonometry
node_kd2, = graph_db.create({"name": "THEOREM2","type":"node"})
node_root.create_relationship_to(node_kd2, "KD2")
node_triangle, = graph_db.create({"name": "ABC","type":"triangle"})
node_kd2.create_relationship_to(node_triangle, "Trigonometry")

# Create three nodes
node_a, node_b, node_c, node_alpha, node_beta = graph_db.create(
    {"name": "AB","type":"line"},
    {"name": "BC","type":"line"},
    {"name": "CA","type":"line"},
    {"name": "BAC","type":"angle"},
    {"name": "BCA","type":"angle"}
)

# Join the nodes with a HAS relationship
rel_triangle_a = node_triangle.create_relationship_to(node_a, "HAS")
rel_triangle_b = node_triangle.create_relationship_to(node_b, "HAS")
rel_triangle_c = node_triangle.create_relationship_to(node_c, "HAS")
rel_triangle_alpha = node_triangle.create_relationship_to(node_alpha, "HAS")
rel_triangle_beta = node_triangle.create_relationship_to(node_beta, "HAS")


#Create input nodes
node_in1, = graph_db.create({"name":"in1","type":"node"})
node_in2, = graph_db.create({"name":"in2","type":"node"})
node_in3, = graph_db.create({"name":"in3","type":"node"})
node_in4, = graph_db.create({"name":"in4","type":"node"})
node_in5, = graph_db.create({"name":"in5","type":"node"})

node_out1, = graph_db.create({"name":"out1","type":"node"})
node_out2, = graph_db.create({"name":"out2","type":"node"})
node_out3, = graph_db.create({"name":"out3","type":"node"})
node_out4, = graph_db.create({"name":"out4","type":"node"})
node_out5, = graph_db.create({"name":"out5","type":"node"})

#input for side1
node_in11, = graph_db.create({"name":"in11","type":"node"})
node_in12, = graph_db.create({"name":"in12","type":"node"})

#output for side1
node_out11, = graph_db.create({"name":"out11","type":"node"})
node_out12, = graph_db.create({"name":"out12","type":"node"})
node_out13, = graph_db.create({"name":"out13","type":"node"})
node_out14, = graph_db.create({"name":"out14","type":"node"})

#input for side2
node_in21, = graph_db.create({"name":"in21","type":"node"})
node_in22, = graph_db.create({"name":"in22","type":"node"})

#output for side2
node_out21, = graph_db.create({"name":"out21","type":"node"})
node_out22, = graph_db.create({"name":"out22","type":"node"})
node_out23, = graph_db.create({"name":"out23","type":"node"})
node_out24, = graph_db.create({"name":"out24","type":"node"})

#input for side3
node_in31, = graph_db.create({"name":"in31","type":"node"})
node_in32, = graph_db.create({"name":"in32","type":"node"})

#output for side3
node_out31, = graph_db.create({"name":"out31","type":"node"})
node_out32, = graph_db.create({"name":"out32","type":"node"})
node_out33, = graph_db.create({"name":"out33","type":"node"})
node_out34, = graph_db.create({"name":"out34","type":"node"})

#input for angle alpha
node_in41, = graph_db.create({"name":"in41","type":"node"})
node_in42, = graph_db.create({"name":"in42","type":"node"})
node_in43, = graph_db.create({"name":"in43","type":"node"})

#output for angle alpha
node_out41, = graph_db.create({"name":"out41","type":"node"})
node_out42, = graph_db.create({"name":"out42","type":"node"})
node_out43, = graph_db.create({"name":"out43","type":"node"})

#input for angle beta
node_in51, = graph_db.create({"name":"in51","type":"node"})
node_in52, = graph_db.create({"name":"in52","type":"node"})
node_in53, = graph_db.create({"name":"in53","type":"node"})

#output for angle beta
node_out51, = graph_db.create({"name":"out51","type":"node"})
node_out52, = graph_db.create({"name":"out52","type":"node"})
node_out53, = graph_db.create({"name":"out53","type":"node"})

# Join the nodes with a  INPUT relationship
rel_a_in1 = node_a.create_relationship_to(node_in1, "INPUT")
rel_b_in2 = node_b.create_relationship_to(node_in2, "INPUT")
rel_c_in3 = node_c.create_relationship_to(node_in3, "INPUT")

rel_a_out1 = node_a.create_relationship_to(node_out1, "OUTPUT")
rel_b_out2 = node_b.create_relationship_to(node_out2, "OUTPUT")
rel_c_out3 = node_c.create_relationship_to(node_out3, "OUTPUT")

rel_in1_in11 = node_in1.create_relationship_to(node_in11, "CONTAIN")
rel_in1_in12 = node_in1.create_relationship_to(node_in12, "CONTAIN")
rel_out1_out11 = node_out1.create_relationship_to(node_out11, "CONTAIN")
rel_out1_out12 = node_out1.create_relationship_to(node_out12, "CONTAIN")
rel_out1_out13 = node_out1.create_relationship_to(node_out13, "CONTAIN")
rel_out1_out14 = node_out1.create_relationship_to(node_out14, "CONTAIN")

rel_in1_in21 = node_in2.create_relationship_to(node_in21, "CONTAIN")
rel_in1_in22 = node_in2.create_relationship_to(node_in22, "CONTAIN")
rel_out1_out21 = node_out2.create_relationship_to(node_out21, "CONTAIN")
rel_out1_out22 = node_out2.create_relationship_to(node_out22, "CONTAIN")
rel_out1_out23 = node_out2.create_relationship_to(node_out23, "CONTAIN")
rel_out1_out24 = node_out2.create_relationship_to(node_out24, "CONTAIN")

rel_in1_in31 = node_in3.create_relationship_to(node_in31, "CONTAIN")
rel_in1_in32 = node_in3.create_relationship_to(node_in32, "CONTAIN")
rel_out1_out31 = node_out3.create_relationship_to(node_out31, "CONTAIN")
rel_out1_out32 = node_out3.create_relationship_to(node_out32, "CONTAIN")
rel_out1_out33 = node_out3.create_relationship_to(node_out33, "CONTAIN")
rel_out1_out34 = node_out3.create_relationship_to(node_out34, "CONTAIN")

rel_in1_in41 = node_in3.create_relationship_to(node_in41, "CONTAIN")
rel_in1_in42 = node_in3.create_relationship_to(node_in42, "CONTAIN")
rel_in1_in43 = node_in3.create_relationship_to(node_in43, "CONTAIN")
rel_out1_out41 = node_out3.create_relationship_to(node_out41, "CONTAIN")
rel_out1_out42 = node_out3.create_relationship_to(node_out42, "CONTAIN")
rel_out1_out43 = node_out3.create_relationship_to(node_out43, "CONTAIN")

rel_in1_in51 = node_in3.create_relationship_to(node_in51, "CONTAIN")
rel_in1_in52 = node_in3.create_relationship_to(node_in52, "CONTAIN")
rel_in1_in53 = node_in3.create_relationship_to(node_in53, "CONTAIN")
rel_out1_out51 = node_out3.create_relationship_to(node_out51, "CONTAIN")
rel_out1_out52 = node_out3.create_relationship_to(node_out52, "CONTAIN")
rel_out1_out53 = node_out3.create_relationship_to(node_out53, "CONTAIN")

#Connection for side1
node_in11.create_relationship_to(node_alpha, "NEEDS")
node_in12.create_relationship_to(node_beta, "NEEDS")

node_out11.create_relationship_to(node_b, "NEEDS")
node_out11.create_relationship_to(node_alpha, "NEEDS")

node_out12.create_relationship_to(node_b, "NEEDS")
node_out12.create_relationship_to(node_beta, "NEEDS")

node_out13.create_relationship_to(node_c, "NEEDS")
node_out13.create_relationship_to(node_alpha, "NEEDS")

node_out14.create_relationship_to(node_c, "NEEDS")
node_out14.create_relationship_to(node_beta, "NEEDS")

#Connection for side2
node_in21.create_relationship_to(node_alpha, "NEEDS")
node_in22.create_relationship_to(node_beta, "NEEDS")

node_out21.create_relationship_to(node_a, "NEEDS")
node_out21.create_relationship_to(node_alpha, "NEEDS")

node_out22.create_relationship_to(node_a, "NEEDS")
node_out22.create_relationship_to(node_beta, "NEEDS")

node_out23.create_relationship_to(node_c, "NEEDS")
node_out23.create_relationship_to(node_alpha, "NEEDS")

node_out24.create_relationship_to(node_c, "NEEDS")
node_out24.create_relationship_to(node_beta, "NEEDS")

#Connection for side3
node_in31.create_relationship_to(node_alpha, "NEEDS")
node_in32.create_relationship_to(node_beta, "NEEDS")

node_out31.create_relationship_to(node_b, "NEEDS")
node_out31.create_relationship_to(node_alpha, "NEEDS")

node_out32.create_relationship_to(node_b, "NEEDS")
node_out32.create_relationship_to(node_beta, "NEEDS")

node_out33.create_relationship_to(node_a, "NEEDS")
node_out33.create_relationship_to(node_alpha, "NEEDS")

node_out34.create_relationship_to(node_a, "NEEDS")
node_out34.create_relationship_to(node_beta, "NEEDS")

#Connection for angle alpha
node_in41.create_relationship_to(node_a, "NEEDS")
node_in42.create_relationship_to(node_b, "NEEDS")
node_in43.create_relationship_to(node_c, "NEEDS")


node_out41.create_relationship_to(node_b, "NEEDS")
node_out41.create_relationship_to(node_a, "NEEDS")

node_out42.create_relationship_to(node_c, "NEEDS")
node_out42.create_relationship_to(node_a, "NEEDS")

node_out43.create_relationship_to(node_b, "NEEDS")
node_out43.create_relationship_to(node_c, "NEEDS")

#Connection for angle beta
node_in51.create_relationship_to(node_a, "NEEDS")
node_in52.create_relationship_to(node_b, "NEEDS")
node_in53.create_relationship_to(node_c, "NEEDS")


node_out51.create_relationship_to(node_b, "NEEDS")
node_out51.create_relationship_to(node_a, "NEEDS")

node_out52.create_relationship_to(node_c, "NEEDS")
node_out52.create_relationship_to(node_a, "NEEDS")

node_out53.create_relationship_to(node_b, "NEEDS")
node_out53.create_relationship_to(node_c, "NEEDS")
#End of function


#This array contains the value of length of sides and values of angles between them
quesArray = [10,20,30,50,60,70]
#This array contains the coordinate values of each point
cordArray = [200,300,400,500,600,700]
triangleName = "ABC"

point1 = triangleName[0]
point2 = triangleName[1]
point3 = triangleName[2]

#Creating question for testing purpose
node_triangle, = graph_db.create({"name": "ABC","type":"triangle"})
node_root.create_relationship_to(node_triangle, "KD1")

node_triangle1, = graph_db.create({"name": "ABD","type":"triangle"})
node_root.create_relationship_to(node_triangle, "KD1")

node_triangle2, = graph_db.create({"name": "ACD","type":"triangle"})
node_root.create_relationship_to(node_triangle, "KD1")


# Create three nodes
node_a, node_b, node_c,node_d, node_e, node_f = graph_db.create(
    {"name": "AB", "value":quesArray[0],"type":"line"},
    {"name": "BC", "value":quesArray[1],"type":"line"},
    {"name": "AC", "value":quesArray[2],"type":"line"},
    {"name": "BD", "value":quesArray[0],"type":"line"},
    {"name": "CD", "value":quesArray[1],"type":"line"},
    {"name": "AD", "value":quesArray[2],"type":"line"}
)

# Join the nodes with a HAS relationship
rel_triangle_a = node_triangle.create_relationship_to(node_a, "HAS")
rel_triangle_b = node_triangle.create_relationship_to(node_b, "HAS")
rel_triangle_c = node_triangle.create_relationship_to(node_c, "HAS")

rel_triangle_a1 = node_triangle1.create_relationship_to(node_a, "HAS")
rel_triangle_b1 = node_triangle1.create_relationship_to(node_d, "HAS")
rel_triangle_c1 = node_triangle1.create_relationship_to(node_f, "HAS")

rel_triangle_a2 = node_triangle.create_relationship_to(node_c, "HAS")
rel_triangle_b2 = node_triangle.create_relationship_to(node_e, "HAS")
rel_triangle_c2 = node_triangle.create_relationship_to(node_f, "HAS")

rel_a_b, = graph_db.get_or_create_relationships((node_a, "ANGLE",node_b, {"value": quesArray[3]}))
rel_b_c, = graph_db.get_or_create_relationships((node_b, "ANGLE",node_c, {"value": quesArray[4]}))
rel_a_c, = graph_db.get_or_create_relationships((node_a, "ANGLE",node_c, {"value": quesArray[5]}))

#Create point nodes
node_point1, node_point2, node_point3= graph_db.create({"name":point1, "cordx":cordArray[0],"cordy":cordArray[1],"type":"point"},{"name":point2, "cordx":cordArray[2],"cordy":cordArray[3],"type":"point"},{"name":point3, "cordx":cordArray[4],"cordy":cordArray[5],"type":"point"})

# Join the nodes with a  CONTAIN relationship
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

#create a point node on one line 
node_point4= graph_db.create({"name":"D", "cordx":cordArray[0],"cordy":cordArray[1],"type":"point"})
rel_point4_point2_coll = node_point2.create_relationship_to(node_point4, "COLLINEAR")
rel_point4_point3_coll = node_point3.create_relationship_to(node_point4, "COLLINEAR")
rel_point4_point2 = node_point2.create_relationship_to(node_point4, "CONNECTED")
rel_point4_point3 = node_point3.create_relationship_to(node_point4, "CONNECTED")
rel_point4_point1 = node_point1.create_relationship_to(node_point4, "CONNECTED")

rel_node6_node2_perp = node_b.create_relationship_to(node_f, "PERPENDICULAR")
rel_node6_node4_perp = node_d.create_relationship_to(node_f, "PERPENDICULAR")
rel_node6_node5_perp = node_e.create_relationship_to(node_f, "PERPENDICULAR")
	
#End of fucntion

# Define a row handler...
def print_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])

def handle_row(row):
    node = row[0]
    print (node)
    #print (node["value"])

print(" inside kd2 file")
#Checking graph nodes by printing all nodes along with their relationship
query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
cypher.execute(graph_db, query, row_handler=print_row)


