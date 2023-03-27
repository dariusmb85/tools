#!/usr/bin/env python3
# This code reads in an RTI synthetic population CSV file and outputs only the entries that
# are within the specified bounding box.
import csv
import argparse, sys

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

# Grab the output file name from the args and open it for writing
output = args.outputFile
outputFile = open(output, 'w')
filewriter = csv.writer(outputFile)

# Open the input file
with open(args.inputFile, newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # grab the header and add it to the output file
    header = next(filereader)
    filewriter.writerow(header)

    # for each row in the file, perform the bounding box test.
    for row in filereader:

       # I am unhappy that these fields have to be hard coded.  Either I should find a way to recode
       # this (maybe using pandas) or we should pass the LAT LON indices in as parameters.
       lon = float(row[16])
       lat = float(row[17])
       if lat < north and lat > south and lon > west and lon < east:
          filewriter.writerow(row)

    outputFile.close()     
