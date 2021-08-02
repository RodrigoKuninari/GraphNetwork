import pandas as pd
import glob
import logging
import logging.handlers
import os
import sys
from service import neo4j_processor

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("processor")
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)

SCHEME = "neo4j"
HOST_NAME = "localhost"
PORT = 7687
URL = "{scheme}://{host_name}:{port}".format(scheme=SCHEME, host_name=HOST_NAME, port=PORT)
USER = "neo4j"
PASSWORD = "test"


def read_and_process_files():
    df_properties = read_properties()
    df_properties = processing_properties(df_properties)
    df_relationships = read_relationships()
    df_relationships = processing_relationships(df_relationships)
    df_relationships_to_insert = create_relationships(df_properties, df_relationships)
    insert_relationships(df_relationships_to_insert)


def read_properties():
    try:
        logger.info("Reading Properties...")
        properties = glob.glob("resources/properties/*.txt")
        df_list = []
        for filename in properties:
            df = pd.read_csv(filename, index_col=None, header=0, sep="\t")
            df_list.append(df)
        df_properties = pd.concat(df_list, axis=0, ignore_index=True)
        logger.info("Properties Read!")
        return df_properties
    except Exception as e:
        logger.error("Error While Reading Properties. Error: {}".format(e))


def processing_properties(df_properties):
    try:
        logger.info("Processing Properties...")
        df_properties = df_properties.rename(columns=lambda x: x.strip())
        df_properties[df_properties.columns] = df_properties.apply(lambda x: x.str.strip())
        df_properties = df_properties[df_properties["Property"] == "Name"]
        print(df_properties)
        logger.info("Properties Processed!")
        return df_properties
    except Exception as e:
        logger.error("Error While Processing Properties. Error: {}".format(e))


def create_relationships(df_properties, df_relationships):
    try:
        logger.info("Creating Relationships...")
        df_to_insert = pd.merge(df_relationships, df_properties, left_on="ID1", right_on="ID", how="left")
        df_to_insert = pd.merge(df_to_insert, df_properties, left_on="ID2", right_on="ID", how="left", suffixes=("_Person", "_Friend"))
        logger.info("Relationships Created!")
        return df_to_insert
    except Exception as e:
        logger.error("Error While Creating Relationships. Error: {}".format(e))


def insert_relationships(df_relationships_to_insert):
    try:
        logger.info("Inserting Relationships...")
        app = neo4j_processor.App(URL, USER, PASSWORD)
        for index, row in df_relationships_to_insert.iterrows():
            app.create_friendship(row["Value_Person"], row["Value_Friend"])
        logger.info("Relationships Inserted!")
    except Exception as e:
        logger.error("Error While Inserting Relationships. Error: {}".format(e))


def read_relationships():
    try:
        logger.info("Reading Relationships...")
        relationships = glob.glob("resources/relationships/*.txt")
        df_list = []
        for filename in relationships:
            df = pd.read_csv(filename, index_col=None, header=0, sep="\t")
            df_list.append(df)
        df_relationships = pd.concat(df_list, axis=0, ignore_index=True)
        logger.info("Relationships Read!")
        return df_relationships
    except Exception as e:
        logger.error("Error While Reading Relationships. Error: {}".format(e))


def processing_relationships(df_relationships):
    try:
        logger.info("Processing Relationships...")
        df_relationships = df_relationships.rename(columns=lambda x: x.strip())
        df_relationships[df_relationships.columns] = df_relationships.apply(lambda x: x.str.strip())
        df_relationships = df_relationships[(df_relationships["Type1"] == "Person") & (df_relationships["Type2"] == "Person") & (df_relationships["Relationship"] == "FRIENDS_WITH")]
        print(df_relationships)
        logger.info("Relationships Processed!")
        return df_relationships
    except Exception as e:
        logger.error("Error While Processing Relationships. Error: {}".format(e))