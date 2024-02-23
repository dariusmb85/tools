import csv
import gzip

def read_csv_headers(file_path):
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the first row (headers)
    else:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the first row (headers)
    # Read the first few rows to infer data types using pandas
    sample_data = pd.read_csv(file_path, nrows=5)
    dtypes = sample_data.dtypes.tolist()

    return ['label'] + headers, dtypes


def build_entity_types(entity_properties):
    entity_types = []
    
    for entity, properties in entity_properties.items():
        entity_dict = {
            "name": entity,
            "alias": entity,
            "role": "esriGraphNamedObjectRegular",
            "strict": False,
            "properties": {}
        }
        
        for prop in properties:
            prop_dict = {
                "name": prop,
                "alias": prop,
                "fieldType": "esriFieldTypeInteger",
                "editable": True,
                "visible": True,
                "required": False,
                "IsSystemMaintained": False,
                "role": "esriGraphPropertyRegular"
            }
            
            entity_dict["properties"][prop] = prop_dict
        
        entity_types.append(entity_dict)
    
    return entity_types

def build_props(name, fieldType):
    prop_types = []
    prop_dict = {
        "name": name,
        "alias": name,
        "fieldType": fieldType,
        "editable": True,
        "visible": True,
        "required": False,
        "IsSystemMaintained": False,
        "role": "esriGraphPropertyRegular"
    }
    prop_types.append(prop_dict)
    return prop_types

def build_relationship_types(relationships):
    relationship_types = []
    
    for relate in relationships:
        relate_dict = {
            "name": relate,
            "alias": relate,
            "role": "esriGraphNamedObjectRegular",
            "strict": False

        }
        relationship_types.append(relate_dict)
    
    return relationship_types

def build_spatial_props():
    space_types = []
    space_dict = {
        "name": "shape",
        "alias": "shape",
        "fieldType": "esriFieldTypeGeometry",
        "geometryType": "esriGeometryPoint",
        "hasZ": False,
        "hasM": False,
        "editable": True,
        "visible": True,
        "required": False,
        "IsSystemMaintained": False,
        "role": "esriGraphPropertyRegular"
    }
    space_types.append(space_dict)
    return space_types
