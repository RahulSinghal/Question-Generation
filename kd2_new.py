#!/usr/bin/env python

"""
Simple example showing node and relationship creation plus
execution of Cypher queries
"""

from __future__ import print_function

# Import Neo4j modules
from py2neo import neo4j, cypher
from macro import graph_db, node_root

# Attach to the graph db instance
#graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#graph_db.clear()
#Create root node
#root = "Root"
#node_root, = graph_db.create({"name":root,"type":"node"})

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

# Build a Cypher query
#query = "START a=node(*) MATCH a-[r:HAS|CONTAIN]->b RETURN a,b,r"

#Query for getting all relationships of a given Object through its name
#query = "START a=node(*) MATCH a-[r]-b WHERE a.name = {A} RETURN a,b,r"
#cypher.execute(graph_db, query, {"A" :""},row_handler=handle_row)

#Query for getting all relationships of a given Object with other objects
#query = "START a=node(*) MATCH a-[r]-b WHERE a.name = {A} RETURN b,a,r"

#query = "START z=node(50) MATCH z-[*]->b RETURN b"
#query = "START z=node(50) MATCH z-[r]->b RETURN r,b"

#Query for getting input for a given side
#query = "START a=node(*) MATCH a-[:INPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c"

#Query for getting output for a given side
#query = "START a=node(*) MATCH a-[:OUTPUT]->b-[:CONTAIN]->c WHERE a.name = {A} RETURN c"

#Query for getting exact input values from in11...
#query = "START a=node(*) MATCH a-[:NEEDS]->c WHERE a.name = {A} RETURN c"

#Query for getting exact output values from out11...
#query = "START a=node(*) MATCH a-[:NEEDS]->c WHERE a.name = {A} RETURN c"

# Define a row handler...
def print_row(row):
    a, b,r = row
    print(a["name"] + " has relationship " +r.type + " with " + b["name"])

def handle_row(row):
    node = row[0]
    print (node)
    #print (node["value"])

'''
# ...and execute the query
print("result from first query")
cypher.execute(graph_db, query, {"B": node_triangle.id,"A" :"AB"}, row_handler=print_row)
print("result from second query")
cypher.execute(graph_db, query, {"B": node_triangle.id,"A" :"AB"}, row_handler=handle_row)
print("result from third query")
data,metadata = cypher.execute(graph_db, query, {"B": node_triangle.id,"A" :"AB"})
for row in data:
    print(row[0][2]["name"])
    print(row[0]["name"])
'''

#AddPoint
#Pick an existing line not having a midPoint
#query = "START a=node(*) MATCH a-[r?:MIDPOINT]->b WHERE a.type = {A} AND r IS NULL  RETURN a,b,r"
#cypher.execute(graph_db, query, {"B": node_triangle.id,"A" :"line"}, row_handler=handle_row)

print(" inside kd2 file")
#Checking graph nodes by printing all nodes along with their relationship
query = "START a=node(*) MATCH a-[r]->b RETURN a,b,r"
#cypher.execute(graph_db, query, row_handler=print_row)

#################Making KD2 for similarity

node_kd2_new, = graph_db.create({"name": "THEOREM2","type":"node"})
node_root.create_relationship_to(node_kd2_new, "KD2")
node_triangle_root, = graph_db.create({"name": "TriangleRoot","type":"node"})
node_kd2_new.create_relationship_to(node_triangle_root, "SIMILARITY")

node_triangle1,node_triangle2 = graph_db.create({"name": "ABC","type":"triangle"},{"name": "PQR","type":"triangle"})
node_triangle_root.create_relationship_to(node_triangle1, "INVOLVES")
node_triangle_root.create_relationship_to(node_triangle2, "INVOLVES")

# Create three nodes for each side of a triangle
node_a, node_b, node_c,node_p, node_q, node_r = graph_db.create(
    {"name": "AB","type":"line"},
    {"name": "BC","type":"line"},
    {"name": "CA","type":"line"},
	{"name": "PQ","type":"line"},
    {"name": "QR","type":"line"},
    {"name": "RP","type":"line"}
)

# Join the side nodes with a HAS relationship
rel_triangle_a = node_triangle1.create_relationship_to(node_a, "HAS")
rel_triangle_b = node_triangle1.create_relationship_to(node_b, "HAS")
rel_triangle_c = node_triangle1.create_relationship_to(node_c, "HAS")

rel_triangle_p = node_triangle2.create_relationship_to(node_p, "HAS")
rel_triangle_q = node_triangle2.create_relationship_to(node_q, "HAS")
rel_triangle_r = node_triangle2.create_relationship_to(node_r, "HAS")

# Create three nodes for each angle of a triangle
node_ang_a, node_ang_b, node_ang_c,node_ang_p, node_ang_q, node_ang_r = graph_db.create(
    {"name": "Ang_A","type":"angle"},
    {"name": "Ang_B","type":"angle"},
    {"name": "Ang_C","type":"angle"},
	{"name": "Ang_P","type":"angle"},
    {"name": "Ang_Q","type":"angle"},
    {"name": "Ang_R","type":"angle"}
)

# Join the angle nodes with a HAS relationship
node_triangle1.create_relationship_to(node_ang_a, "HAS")
node_triangle1.create_relationship_to(node_ang_b, "HAS")
node_triangle1.create_relationship_to(node_ang_c, "HAS")
node_triangle1.create_relationship_to(node_ang_p, "HAS")
node_triangle1.create_relationship_to(node_ang_q, "HAS")
node_triangle1.create_relationship_to(node_ang_r, "HAS")

#Create input nodes
node_in1, = graph_db.create({"name":"in1","type":"node"})
node_in2, = graph_db.create({"name":"in2","type":"node"})
node_in3, = graph_db.create({"name":"in3","type":"node"})

node_ang_a.create_relationship_to(node_in1, "INPUT")
node_ang_a.create_relationship_to(node_in2, "INPUT")
node_ang_a.create_relationship_to(node_in3, "INPUT")

############### The above function is incomplete

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

