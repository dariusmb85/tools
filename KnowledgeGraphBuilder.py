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

#### Connect to gis portal
gis = GIS("https://arcgis.edc.renci.org/portal",'dariusmb')

#### Create new KG
# result = gis.content.create_service(
#     name="Full_Upload_WIP",
#     capabilities="Query,Editing,Create,Update,Delete",
#     service_type="KnowledgeGraph",
# )

#### Connect to existing knowledge graph (kg) on portal
kg = KnowledgeGraph("https://arcgis.edc.renci.org/portal/rest/services/Hosted/Full_Upload_WIP/KnowledgeGraphServer", gis=gis)

#### Identify entities and relationships of graph
for types in kg.datamodel['entity_types']:
    print(types)
for types in kg.datamodel['relationship_types']:
    print(types)

#### Establish structure for datamodel entities and properties to add
entity_properties = {
    "Household": ["label", "logrecno", "hh_age", "hh_income", "hh_race", "ethnicity",
                  "size", "state_fips", "county_fips", "tract_fips", "blkgrp_fips",
                  "puma_fips","evelation"],
    "Person": ["label", "p_id", "sporder", "relshipp", "rac1p", "agep",
               "sex", "hisp"],
    "Workplace": ["label"]
}

entity_types = build_entity_types(entity_properties)

relationships = {
    "LivesIn", "Attends","WorksAt","Holds", "EvacPath", "Within"
}
relate_types = build_relationship_types(relationships)

res = kg.named_object_type_adds(entity_types, relate_types)

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
#### Define a list of properties for each type
person_properties = [
    ("hh_id", "esriFieldTypeString"),
    ("wp_id", "esriFieldTypeString"),
    ("job_income_bucket", "esriFieldTypeString"),
    ("school_id", "esriFieldTypeString"),
    ("school_type", "esriFieldTypeString"),
    ("grade_lvl", "esriFieldTypeString"),
    ("serlino", "esriFieldTypeString"),
]

workplace_properties = [
    ("x", "esriFieldTypeDouble"),
    ("y", "esriFieldTypeDouble"),
    ("wp_id", "esriFieldTypeString"),
    ("NAICS", "esriFieldTypeString"),
    ("blkgrp_fips_wp", "esriFieldTypeDouble"),
    ("elevation", "esriFieldTypeDouble"),
]

household_properties = [
    ("x", "esriFieldTypeDouble"),
    ("y", "esriFieldTypeDouble"),
    ("hh_id", "esriFieldTypeString"),
]
# Add properties for 'Person'
add_properties("Person", person_properties)

# Add properties for 'Workplace' and 'Household'
add_properties("Workplace", workplace_properties)
add_properties("Household", household_properties)

# df_hh = pd.read_csv("2019_ver1_37/37/NC2019_Households.csv")
# df_Person = pd.read_csv("2019_ver1_37/37/NC2019_Persons.csv.gz")
# df_Work = pd.read_csv("2019_ver1_37/37/NC2019_Workplaces.csv.gz")
# merged_df = df_Person.merge(df_hh, on='hh_id', how='left').merge(df_Work, on='workplace_id', how='left')
# merged_df.to_csv("merged_synth_PerHouWor.csv", index = False)


merged_df = pd.read_csv("merged_synth_PerHouWor.csv")

# subset_nh.columns.get_loc('hh_id')
# subset_nh.columns.get_loc('person_id_numeric')
# subset_nh.columns.get_loc('workplace_id')


################ Add data to KG ###############New Test KG.APPlY
import time

# Record the start time
start_time = time.time()

county_list = [37129, 37065, 37019, 37155, 37139]
#county_list = [37065]

for county_fips in county_list:
    subset_nh = merged_df[merged_df['county_fips'] == county_fips]
    subset_nh = subset_nh.sample(frac=0.5)
    edits_phw = []
    edits_ph = []
    relates = []
    #relates_counter = 0
    # Split merged_df into two halves
    half_len = len(subset_nh) // 2
    first_half = subset_nh.iloc[:half_len]
    second_half = subset_nh.iloc[half_len:]

    for per in first_half.itertuples():
        school_id, school_type, grade_lvl, income, serialno_y, workplace_id = convert_values_to_string(
            per.school_id, per.school_type, per.grade_level, per.job_income_bucket, per.serialno_y, per.workplace_id
        )
        
        person_edit = {
            "_objectType": "entity",
            "_typeName": "Person",
            "_properties": {
                "hh_id": per.hh_id,
                "p_id": per.person_id_numeric,
                "sex": per.sex,
                "agep": per.agep,
                "rac1p": per.rac1p,
                "wp_id": workplace_id,
                "hisp": per.hisp,
                "school_id": school_id,
                "school_type": school_type,
                "grade_lvl": grade_lvl,
                "job_income_bucket": income,
                "relshipp": per.relshipp,
                "sporder": per.sporder,
                "serlino": per.serialno_y
            }
        }
        
        house_edit = {
            "_objectType": "entity",
            "_typeName": "Household",
            "_properties": {
                "hh_id": per.hh_id,
                "hh_age": per.hh_age,
                "size": per.size,
                "hh_race": per.hh_race,
                "ethnicity": per.ethnicity,
                "hh_income": per.hh_income, 
                "state_fips": per.state_fips,
                "county_fips": per.county_fips,
                "tract_fips": per.tract_fips,
                "blkgrp_fips": per.blkgrp_fips,
                "evelation": per.elevation_x,
                "shape": {
                    'x': float(per.LON),
                    'y': float(per.LAT),
                    '_objectType': 'geometry'
                }
            }
        }
        
        # Check the condition only for workplace_edit
        if not pd.isna(per.lon_workplace):
            workplace_edit = {
                "_objectType": "entity",
                "_typeName": "Workplace",
                "_properties": {
                    "wp_id": workplace_id,
                    "NAICS": per.NAICS,
                    "blkgrp_fips_wp": per.blkgrp_fips_workplace,
                    "shape": {
                        'x': float(per.lon_workplace),
                        'y': float(per.lat_workplace),
                        '_objectType': 'geometry'
                    }
                }
            }
            edits_phw.extend([person_edit, house_edit, workplace_edit])
        else:
            edits_ph.extend([person_edit, house_edit])
            
    # Apply batch edits for entities
    result = kg.apply_edits(adds=edits_phw)
    result_noWork = kg.apply_edits(adds=edits_ph)
    print(f"County: {county_fips} has completed")
    
    for per in second_half.itertuples():
        school_id, school_type, grade_lvl, income, serialno_y, workplace_id = convert_values_to_string(
            per.school_id, per.school_type, per.grade_level, per.job_income_bucket, per.serialno_y, per.workplace_id
        )
        
        person_edit = {
            "_objectType": "entity",
            "_typeName": "Person",
            "_properties": {
                "hh_id": per.hh_id,
                "p_id": per.person_id_numeric,
                "sex": per.sex,
                "agep": per.agep,
                "rac1p": per.rac1p,
                "wp_id": workplace_id,
                "hisp": per.hisp,
                "school_id": school_id,
                "school_type": school_type,
                "grade_lvl": grade_lvl,
                "job_income_bucket": income,
                "relshipp": per.relshipp,
                "sporder": per.sporder,
                "serlino": per.serialno_y
            }
        }
        
        house_edit = {
            "_objectType": "entity",
            "_typeName": "Household",
            "_properties": {
                "hh_id": per.hh_id,
                "hh_age": per.hh_age,
                "size": per.size,
                "hh_race": per.hh_race,
                "ethnicity": per.ethnicity,
                "hh_income": per.hh_income, 
                "state_fips": per.state_fips,
                "county_fips": per.county_fips,
                "tract_fips": per.tract_fips,
                "blkgrp_fips": per.blkgrp_fips,
                "evelation": per.elevation_x,
                "shape": {
                    'x': float(per.LON),
                    'y': float(per.LAT),
                    '_objectType': 'geometry'
                }
            }
        }
        
        # Check the condition only for workplace_edit
        if not pd.isna(per.lon_workplace):
            workplace_edit = {
                "_objectType": "entity",
                "_typeName": "Workplace",
                "_properties": {
                    "wp_id": workplace_id,
                    "NAICS": per.NAICS,
                    "blkgrp_fips_wp": per.blkgrp_fips_workplace,
                    "shape": {
                        'x': float(per.lon_workplace),
                        'y': float(per.lat_workplace),
                        '_objectType': 'geometry'
                    }
                }
            }
            edits_phw.extend([person_edit, house_edit, workplace_edit])
        else:
            edits_ph.extend([person_edit, house_edit])
            
    # Apply batch edits for entities
    result = kg.apply_edits(adds=edits_phw)
    result_noWork = kg.apply_edits(adds=edits_ph)
    print(f"County: {county_fips} has completed")

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


######## Add Relationships ###########################
start_time = time.time()
relates = []
# Update relationship placeholders with actual IDs
for i in range(len(edits_phw)// 3):
    relationship = [{
        "_objectType": "relationship",
        "_typeName": "LivesIn",
        "_originEntityId": result['editsResult']['Person']['addResults'][i]['id'],
        "_destinationEntityId": result['editsResult']['Household']['addResults'][i]['id'],
        "_properties":{}
    },{
        "_objectType": "relationship",
        "_typeName": "WorksAt",
        "_originEntityId": result['editsResult']['Person']['addResults'][i]['id'],
        "_destinationEntityId": result['editsResult']['Workplace']['addResults'][i]['id'],
        "_properties":{}
    }]
    relates.extend(relationship)
    # Apply relationship edits
kg.apply_edits(adds=relates)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

start_time = time.time()
relates_noWork = []
# Update relationship placeholders with actual IDs
for i in range(len(edits_ph)// 2):
    relationship_noWork = [{
        "_objectType": "relationship",
        "_typeName": "LivesIn",
        "_originEntityId": result_noWork['editsResult']['Person']['addResults'][i]['id'],
        "_destinationEntityId": result_noWork['editsResult']['Household']['addResults'][i]['id'],
        "_properties":{}
    }]
    relates_noWork.extend(relationship_noWork)
    # Apply relationship edits
kg.apply_edits(adds=relates_noWork)
# Record the end time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

######## Create Map with Households from KG #####################

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
