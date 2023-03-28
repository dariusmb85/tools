#!/usr/bin/env python3
# This code reads in an RTI synthetic population CSV file and outputs only the entries that
# are within the specified bounding box.
import csv
import argparse, sys
import pandas as pd

parser=argparse.ArgumentParser()

parser.add_argument("--inputFile", help="The file to clip")
parser.add_argument("--outputFile", help="The file to output")
parser.add_argument("--boxFile", help="A file containing the bounding box as North, West, South, East")

args=parser.parse_args()

# Open the box file.  
for line in  open(args.boxFile):
   li=line.strip()
   # skip any comment lines
   if not li.startswith("#"):
      # The first non comment line is the bounding box
      # The bounding coordinates are "," separated
      coordList = li.split(",")
      north = float(coordList[0])
      west = float(coordList[1])
      south = float(coordList[2])
      east = float(coordList[3])

# Let's try this in pandas
# Read the input file
# Note that, strangely enough, the pandas csv implementation seems to round incorrectly sometimes.
# A discussion of this issue is at:
#
#    https://www.appsloveworld.com/pandas/100/5/pandas-read-csv-file-with-float-values-results-in-weird-rounding-and-decimal-digi
#
# We aren't going to deal with this at the moment, but we may need to eventually.
df = pd.read_csv(args.inputFile)

# Clip the data frame to the bounding box using the loc function
df_clipped = df.loc[(df['LAT'] < north) & (df['LAT'] > south) & (df['LON'] < east) & (df['LON'] > west)]

# Write the clipped csv to the output file
df_clipped.to_csv(args.outputFile, encoding='utf-8', index=False)
