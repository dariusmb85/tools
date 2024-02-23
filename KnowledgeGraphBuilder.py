import sys
from arcgis.gis import GIS
from arcgis.graph import KnowledgeGraph
from arcgis.features import FeatureSet, Feature
from arcgis.geometry import Geometry
import pandas as pd
import numpy as np
import utils
import requests
from pprint import pprint
import time

# Connect to gis portal
gis = GIS("https://arcgis.edc.renci.org/portal",'dariusmb')


# result = gis.content.create_service(
#     name="Full_Upload_WIP",
#     capabilities="Query,Editing,Create,Update,Delete",
#     service_type="KnowledgeGraph",
# )

# Connect to existing knowledge graph (kg) on portal
kg = KnowledgeGraph("https://arcgis.edc.renci.org/portal/rest/services/Hosted/Full_Upload_WIP/KnowledgeGraphServer", gis=gis)

# Identify entities and relationships of graph
for types in kg.datamodel['entity_types']:
    print(types)
for types in kg.datamodel['relationship_types']:
    print(types)


entity_properties = {
    "Household": ["label", "serilno", "hh_age", "hh_income", "hh_race", "size","state", "county", "tract", "block_group"],
    "Person": ["label", "p_id", "serlino", "sproder", "relshipp", "rac1p", "agep", "sex", "school_id", "school_type", "grade_lvl", "income_bucket"],
    "Workplace": ["label","blkgrp_fips_workplace",]
}

entity_types = build_entity_types(entity_properties)

relationships = {
    "LivesIn", "Attends","WorksAt","Holds", "EvacPath", "Within"
}
relate_types = build_relationship_types(relationships)

res = kg.named_object_type_adds(entity_types, relate_types)
#print(res)

# entity_properties = {"Household": csv_headers[0:]}

# Read column headers from CSV
# hh_headers = read_csv_headers("2019_ver1_37/37/NC2019_Households.csv.gz")
# wp_headers = read_csv_headers("2019_ver1_37/37/NC2019_Workplaces.csv.gz")
# per_headers = read_csv_headers("2019_ver1_37/37/NC2019_Persons.csv.gz")


spatial_types = build_spatial_props()

spatial_types
kg.graph_property_adds(type_name='Household', graph_properties=spatial_types)
kg.graph_property_adds(type_name='Workplace', graph_properties=spatial_types)


#"esriFieldTypeString"
#"esriFieldTypeInteger"
#"esriFieldTypeGeometry"
#"esriFieldTypeDouble"

prop_types = build_props("hh_id","esriFieldTypeString")
kg.graph_property_adds(type_name='Person', graph_properties=prop_types)
kg.graph_property_adds(type_name='Household', graph_properties=prop_types)

prop_types = build_props("wp_id","esriFieldTypeString")
kg.graph_property_adds(type_name='Person', graph_properties=prop_types)
kg.graph_property_adds(type_name='Workplace', graph_properties=prop_types)

prop_types = build_props("NAICS","esriFieldTypeString")
kg.graph_property_adds(type_name='Workplace', graph_properties=prop_types)

prop_types = build_props("blkgrp_fips_wp","esriFieldTypeDouble")
kg.graph_property_adds(type_name='Workplace', graph_properties=prop_types)


# df_hh = pd.read_csv("2019_ver1_37/37/NC2019_Households.csv")
# df_Person = pd.read_csv("2019_ver1_37/37/NC2019_Persons.csv.gz")
# df_Work = pd.read_csv("2019_ver1_37/37/NC2019_Workplaces.csv.gz")
# merged_df = df_Person.merge(df_hh, on='hh_id', how='left').merge(df_Work, on='workplace_id', how='left')
# merged_df.to_csv("merged_synth_PerHouWor.csv", index = False)


merged_df = pd.read_csv("merged_synth_PerHouWor.csv")

# county_list = [37129, 37065, 37019, 37155, 37139]
# county_df = merged_df[merged_df['county_fips'].isin(county_list)]


county_list = [37129, 37065, 37019, 37155, 37139]
county_df = merged_df[(merged_df['county_fips'].isin(county_list))]
subset_nh = county_df.sample(frac=0.1)


kg.query("MATCH (n:Person) WHERE n.p_id = '" + subset_nh.iloc[0, subset_nh.columns.get_loc('person_id_numeric')].astype(str) + "' RETURN n.globalid")

# subset_nh.columns.get_loc('hh_id')
# subset_nh.columns.get_loc('person_id_numeric')
# subset_nh.columns.get_loc('workplace_id')


# Record the start time
start_time = time.time()

county_list = [37129, 37065, 37019, 37155, 37139]
county_list = [37065]

for county_fips in county_list:
    subset_nh = merged_df[merged_df['county_fips'] == county_fips]
    
    edits = []
    relates = []
    relates_counter = 0

    for per in subset_nh.itertuples():
        if not pd.isna(per.lon_workplace):
            person_edit = {
                "_objectType": "entity",
                "_typeName": "Person",
                "_properties": {
                    "hh_id": per.hh_id,
                    "p_id": per.person_id_numeric,
                    "sex": per.sex,
                    "agep": per.agep,
                    "rac1p": per.rac1p,
                    "wp_id": per.workplace_id,
                }
            }

            house_edit = {
                "_objectType": "entity",
                "_typeName": "Household",
                "_properties": {
                    "hh_id": per.hh_id,
                    "hh_age": per.hh_age,
                    "size": per.size,
                    "shape": {
                        'x': float(per.LON),
                        'y': float(per.LAT),
                        '_objectType': 'geometry'
                    }
                }
            }

            workplace_edit = {
                "_objectType": "entity",
                "_typeName": "Workplace",
                "_properties": {
                    "wp_id": per.workplace_id,
                    "NAICS": per.NAICS,
                    "shape": {
                        'x': float(per.lon_workplace),
                        'y': float(per.lat_workplace),
                        '_objectType': 'geometry'
                    }
                }
            }

            relates.extend([
                {
                    "_objectType": "relationship",
                    "_typeName": "LivesIn",
                    "_originEntityId": None,  # Placeholder for person_id
                    "_destinationEntityId": None,  # Placeholder for house_id
                    "_properties": {}
                },
                {
                    "_objectType": "relationship",
                    "_typeName": "WorksAt",
                    "_originEntityId": None,  # Placeholder for person_id
                    "_destinationEntityId": None,  # Placeholder for work_id
                    "_properties": {}
                }
            ])

            edits.extend([person_edit, house_edit, workplace_edit])
            relates_counter += 2
            
    # Apply batch edits for entities
    result = kg.apply_edits(adds=edits)

    # Update relationship placeholders with actual IDs
    for i in range(relates_counter):
        if "_originEntityId" in relates[i]:
            relates[i]["_originEntityId"] = result['editsResult']['Person']['addResults'][i // 2]['id']
        if "_destinationEntityId" in relates[i]:
            relates[i]["_destinationEntityId"] = result['editsResult']['Household' if i % 2 == 1 else 'Workplace']['addResults'][i // 2]['id']

    # Apply relationship edits
    kg.apply_edits(adds=relates)
    print(f"County: {county_fips} has completed")

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# In[46]:


county_list = [37129, 37065, 37019, 37155, 37139]
county_df = merged_df[(merged_df['county_fips'] == 37155)]
subset_nh = county_df
subset_nh.shape


# In[47]:


import time
# Record the start time
start_time = time.time()

# Convert columns to string
subset_nh['workplace_id'] = subset_nh['workplace_id'].astype(str)
subset_nh['NAICS'] = subset_nh['NAICS'].astype(str)

edits = []
relates = []

# Counter for relationship edits
relates_counter = 0

for per in subset_nh.itertuples():
    if not pd.isna(per.lon_workplace):
        person_edit = {
            "_objectType": "entity",
            "_typeName": "Person",
            "_properties": {
                "hh_id": per.hh_id,
                "p_id": per.person_id_numeric,
                "sex": per.sex,
                "agep": per.agep,
                "rac1p": per.rac1p,
                "wp_id": per.workplace_id,
            }
        }

        house_edit = {
            "_objectType": "entity",
            "_typeName": "Household",
            "_properties": {
                "hh_id": per.hh_id,
                "hh_age": per.hh_age,
                "size": per.size,
                "shape": {
                    'x': float(per.LON),
                    'y': float(per.LAT),
                    '_objectType': 'geometry'
                }
            }
        }

        workplace_edit = {
            "_objectType": "entity",
            "_typeName": "Workplace",
            "_properties": {
                "wp_id": per.workplace_id,
                "NAICS": per.NAICS,
                "shape": {
                    'x': float(per.lon_workplace),
                    'y': float(per.lat_workplace),
                    '_objectType': 'geometry'
                }
            }
        }

        relates.extend([
            {
                "_objectType": "relationship",
                "_typeName": "LivesIn",
                "_originEntityId": None,  # Placeholder for person_id
                "_destinationEntityId": None,  # Placeholder for house_id
                "_properties": {}
            },
            {
                "_objectType": "relationship",
                "_typeName": "WorksAt",
                "_originEntityId": None,  # Placeholder for person_id
                "_destinationEntityId": None,  # Placeholder for work_id
                "_properties": {}
            }
        ])

        edits.extend([person_edit, house_edit, workplace_edit])

        # Increment the counter for relationship edits
        relates_counter += 2

# Apply batch edits for entities
result = kg.apply_edits(adds=edits)

# Update relationship placeholders with actual IDs
for i in range(relates_counter):
    if "_originEntityId" in relates[i]:
        relates[i]["_originEntityId"] = result['editsResult']['Person']['addResults'][i // 2]['id']
    if "_destinationEntityId" in relates[i]:
        relates[i]["_destinationEntityId"] = result['editsResult']['Household' if i % 2 == 1 else 'Workplace']['addResults'][i // 2]['id']

# Apply relationship edits
kg.apply_edits(adds=relates)

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# In[ ]:


result = kg.apply_edits(adds=edits)


# In[28]:


query_results = kg.query("MATCH (n:Person) RETURN n")


kg.query("MATCH (person:Person) RETURN COUNT(person)") # 37155


# In[42]:


kg.query("MATCH (person:Person) RETURN COUNT(person)") # 37129


# In[45]:


kg.query("MATCH (person:Person) RETURN COUNT(person)") # 37019


# In[34]:


kg.query("MATCH (person:Person) RETURN COUNT(person)") # 37065


# In[39]:


kg.query("MATCH (person:Person) RETURN COUNT(person)") # 37139


# In[51]:


kg.query("MATCH (h:Household) RETURN COUNT(h)")



query_results = kg.query("MATCH (n:Household) RETURN n")
house_list = []

for house in query_results:
    geom = Geometry(house[0]['_properties']['shape'])
    house_feat = Feature(geometry=geom)
    house_list.append(house_feat)
    
house_fs = FeatureSet(features= house_list, geometry_type= 'Point', spatial_reference= kg.datamodel['spatial_reference'])
house_sdf = house_fs.sdf

new_map = gis.map()
#new_map.center
new_map.zoom = 6
new_map.basemap = 'gray-vector'
house_sdf.spatial.plot(map_widget = new_map, renderer_type = 's', markersize = 3, symbol_type = 'simple')

new_map
