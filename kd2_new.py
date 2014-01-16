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

#Making KD2 for similarity

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

