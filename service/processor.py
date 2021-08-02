import pandas as pd
import glob
import logging
import logging.handlers
import os
import sys

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("processor")
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)


def read_properties():
    try:
        logger.info("Reading Properties...")
        properties = glob.glob("resources/properties/*.txt")
        df_list = []
        for filename in properties:
            df = pd.read_csv(filename, index_col=None, header=0, sep="\t")
            df_list.append(df)

        df_properties = pd.concat(df_list, axis=0, ignore_index=True)
        df_properties = df_properties.rename(columns=lambda x: x.strip())
        df_properties[df_properties.columns] = df_properties.apply(lambda x: x.str.strip())
        df_properties = df_properties[df_properties["Property"] == "Name"]
        print(df_properties)
        logger.info("Properties Read!")
    except Exception as e:
        logger.error("Error While Reading Properties. Error: {}".format(e))


def read_relationships():
    try:
        logger.info("Reading Relationships...")
        relationships = glob.glob("resources/relationships/*.txt")
        df_list = []
        for filename in relationships:
            df = pd.read_csv(filename, index_col=None, header=0, sep="\t")
            df_list.append(df)

        df_relationships = pd.concat(df_list, axis=0, ignore_index=True)
        df_relationships = df_relationships.rename(columns=lambda x: x.strip())
        df_relationships[df_relationships.columns] = df_relationships.apply(lambda x: x.str.strip())
        df_relationships = df_relationships[(df_relationships["Type1"] == "Person") & (df_relationships["Type2"] == "Person") & (df_relationships["Relationship"] == "FRIENDS_WITH")]
        print(df_relationships)
        logger.info("Relationships Read!")
    except Exception as e:
        logger.error("Error While Reading Relationships. Error: {}".format(e))
