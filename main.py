import os
from neomodel import config
# import data source classes

NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_URI = os.getenv("NEO4J_URI", "localhost:7687")

config.DATABASE_URL = f"bolt://{NEO4J_USER}:{NEO4J_PASSWORD}@{NEO4J_URI}"

#create soruce data

#Nulls report
# report on nulls