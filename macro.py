from __future__ import print_function
import wx
# Import Neo4j modules
from py2neo import neo4j, cypher


theorem_list = ["pythagorus", "inequality"]
default_theoremList = ["pythagorus", "inequality"]

#######These lines insides hashes have been added to protect kd2 from entering here #########
# Attach to the graph db instance
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

graph_db.clear()
#Create root node
root = "Root"
node_root, = graph_db.create({"name":root,"type":"node"})
######################################################

