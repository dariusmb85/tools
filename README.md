# tools


## Working repo for gfloat tool development
G-FLOAT tech status:
Link to jupyter notebook


All data files
NCDOT: Files are located at the following:
https://ncconnect.sharepoint.com/sites/NCDOTHydraulicsUnitAtlas/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FNCDOTHydraulicsUnitAtlas%2FShared%20Documents%2FGIS%5FData&p=true&ga=1

Contact Kurt Golembesky at kpgolembesky@ncdot.gov to obtain access. 

Synthetic Data files: 
Provided by James (Jay) Rineer at jrin@rti.org. These files can be access on the renci VM arcgis.renci.org or via hatteras server located at 
/projects/gfloat/data

All files that are in G-FLOAT Knowledge Graph
NC_schools_priv.csv.gz
NC_schools_pub.csv.gz
NC2019_Workplaces.csv.gz
NC2019_Persons.csv.gz
NC2019_Households.csv
coastalGages.dbf
Matthew.shp
Florence.shp

Building the Structure of a Knowledge Graph using Esri's ArcGIS Knowledge Framework

Establishing the ArcGIS Enterprise Server
To support the development and management of the G-FLOAT knowledge graph (KG), the first step involved setting up an ArcGIS Enterprise server. This server acts as a central repository for storing, managing, and sharing geospatial data and knowledge graphs. The ArcGIS Enterprise server provides a robust platform that ensures data integrity, security, and accessibility, which are crucial for the G-FLOAT project.

Setting up the ArcGIS Enterprise server included configuring the necessary components such as the ArcGIS Portal, ArcGIS Server, and the Data Store. The Data Store component is particularly important as it manages the hosted data layers that are integral to the KG. The configuration process also involved setting up user roles and permissions to ensure that only authorized personnel could access and manipulate the data, thereby maintaining data security and privacy.

Data Integration and Preparation

The next step was integrating various data sources into the ArcGIS Enterprise environment. The G-FLOAT project utilized RTI’s synthetic population data and the North Carolina Department of Transportation’s Flood Inundation Mapping Alert Network (FIMAN) data. These datasets provide crucial socio-economic and flood-related information necessary for creating a comprehensive KG.

Using the ArcGIS Python API, we automated the extraction, transformation, and loading (ETL) processes to ensure that the data was clean, consistent, and ready for analysis. The Python API facilitated seamless integration of the data into the ArcGIS environment, enabling us to manage and preprocess large datasets efficiently.

Constructing the Knowledge Graph
With the data prepared and integrated, the next phase was constructing the knowledge graph. The ArcGIS Knowledge framework allows for the creation of entities (nodes) and relationships (edges) that represent the various components and interactions within the data. For example, persons from RTI data were represented as nodes, and their relationships with workplaces or schools were depicted as edges.
We used the ArcGIS Python API to script the creation of these nodes and relationships. This approach allowed for the automation of KG construction, ensuring consistency and efficiency. The resulting KG provided a dynamic representation of flood-related data, facilitating complex queries and analyses.
Hosting and Managing the Knowledge Graph
Once the KG was constructed, it was hosted on the ArcGIS Enterprise server. This hosting environment provided a centralized platform for managing the KG and ensuring its availability to authorized users. The ArcGIS Enterprise server's robust capabilities allowed for efficient management of data stores and ensured the KG was scalable and secure.
By leveraging the server's capabilities, we could perform regular updates, maintain data integrity. In conclusion, developing the structure of the G-FLOAT knowledge graph involved setting up an ArcGIS Enterprise server, integrating and preparing data, constructing the KG, and managing it within the ArcGIS environment. This comprehensive approach ensured the creation of a robust and dynamic KG that supports effective flood response and recovery efforts.
