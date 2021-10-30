#!/usr/bin/env python
from xml.sax import parse
from xml.sax.handler import ContentHandler
import sys


class NodeHandler(ContentHandler):
    def __init__(self):
        self.element = None
        self.this_distance = None
        self.this_altitude = None
        self.last_distance = None
        self.last_altitude = None
        self.leg_distance = 0
        self.leg_up = 0
        self.leg_down = 0
        self.leg_time = 0
        self.seconds = 0
        
    def startElement(self, name, attrs):
        self.element = name
            
    def characters(self, content):
        content = content.strip()
        if content == "":
            return
        if self.element == "DistanceMeters":
            self.this_distance = float(content)
        elif self.element == "AltitudeMeters":
            self.this_altitude = int(content)
            
    def endElement(self, name):
        if name != "Trackpoint":
            return
        if self.seconds != 0:
            diff_distance = self.this_distance - self.last_distance
            diff_altitude = self.this_altitude - self.last_altitude
            self.leg_distance += diff_distance
            if diff_altitude > 0:
                self.leg_up += diff_altitude
            else:
                self.leg_down += diff_altitude
                    
        self.last_distance = self.this_distance
        self.last_altitude = self.this_altitude
        self.leg_time += +1
        self.seconds += 1
        
        if (self.leg_distance >= 100):
            outfile.write("%d\t%d\t%f\t%d\t%d\n"%(self.seconds, self.leg_time, self.leg_distance, self.leg_up, self.leg_down))
            self.leg_time = 0
            self.leg_distance = 0
            self.leg_up = 0
            self.leg_down = 0
        
handler = NodeHandler();
outfile = open("%s.tsv"%sys.argv[1], "w")
outfile.write("Total\tLap\tDistance\tUp\tDown\n")
parse(sys.argv[1], handler);

