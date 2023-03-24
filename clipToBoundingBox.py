#!/usr/bin/env python3
import csv
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument("--inputFile", help="The file to trim")
parser.add_argument("--outputFile", help="The file to output")
parser.add_argument("--north", help="The north point of the bounding box")
parser.add_argument("--east", help="The east point of the bounding box")
parser.add_argument("--south", help="The south point of the bounding box")
parser.add_argument("--west", help="The west point of the bounding box")

args=parser.parse_args()
print(args)
print(args.north)
north = float(args.north)
south = float(args.south)
east = float(args.east)
west = float(args.west)

with open(args.inputFile, newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(filereader)
    counter = 0
    for row in filereader:
       #print('LON ' + row[16])
       #print('LAT ' + row[17])
       lon = float(row[16])
       lat = float(row[17])
       print(str(lat) + " " + str(lon) + " " + str(north)+ " " + str(south)+ " " + str(east) + " " + str(west))
#      if lat < north:
#         print ("lat < north")
          
#      if lat > south:
#         print ("lat > south")

#      if lon < east:
#         print ("lon < east")

#      if lon > west:
#         print ("lon > west")
          
       if lat < north and lat > south and lon > west and lon < east:
          print ("row found")
          print (row)
       else:
          counter = counter + 1
         # if (counter == 100):
         #    sys.exit(0)
