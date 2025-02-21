# -*- coding: utf-8 -*-
'''
Title: Pre Tool GNIS
Author: Caitlin Hartig
Date: May 2024

This program takes a .txt file that is downloaded specifically from the GNIS data and turns it into a feature class.

Libraries Utilized: arcpy
'''

import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Pre_Tool_GNIS"
        self.alias = "Pre_Tool_GNIS"

        # List of tool classes associated with this toolbox
        self.tools = [Pre_Tool_GNIS]


class Pre_Tool_GNIS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Pre_Tool_GNIS"
        self.description = "This tool converts the GNIS textfile into a NAD83 feature class."
        self.canRunInBackground = False
    
    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter - user selected input data text file
        param0 = arcpy.Parameter(
            displayName="Input Data TXT File",
            name="input_data_txt",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        param0.filter.list = ["txt"]
        param0.value = r'C:\Users\caitl\OneDrive\Documents\Tools\GNIS\Data\DomesticNames_National_Text\Text\DomesticNames_National.txt'

        # Second parameter - user selected output feature class
        param1 = arcpy.Parameter(
            displayName="Output Feature Class",
            name="output_fc_name",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output",
            multiValue=False)
        param1.value = r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb\GNIS_USGS'
        
        params = [param0, param1]
    
        return params
    
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        arcpy.env.overwriteOutput = 1

        txtfile = parameters[0].valueAsText
        gnis_fc = parameters[1].valueAsText
        SPATIAL_REFERENCE = 4269

        arcpy.management.MakeXYEventLayer(txtfile, 'prim_long_dec', 'prim_lat_dec', 'gnis_event', SPATIAL_REFERENCE)
        arcpy.management.CopyFeatures('gnis_event', gnis_fc)

        index_fc = gnis_fc.rfind(chr(92))
        name_fc = gnis_fc[index_fc + 1:]
        if name_fc[-1:] == chr(39):
            name_fc = name_fc[:-1]
        arcpy.AddMessage('GNIS shapefile created - {0}'.format(name_fc))

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
