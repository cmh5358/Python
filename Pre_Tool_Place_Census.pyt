'''
Title: Pre Tool Place Census
Authors: Caitlin Hartig, Justine Jedlicka
Date: August 2024

This program takes two specific feature classes from the Census data, sets the coordinate system to NAD83 if necessary, and then merges together the two feature classes into one combined layer.

Libraries Utilized: arcpy, os, pathlib
'''

import arcpy, os, pathlib

class Toolbox(object):
    def __init__(self):
        self.label = "Pre_Tool_Place_Census"
        self.alias = ""

        self.tools = [Pre_Tool_Place_Census]


class Pre_Tool_Place_Census(object):
    def __init__(self):
        self.label = "Pre_Tool_Place_Census"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        # First parameter - file directory pathway to the initial GDB
        param0 = arcpy.Parameter(
            displayName="Input GDB (Should contain the relevant feature classes)",
            name="input_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        master_gdb = r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'
        param0.value = master_gdb
        
        # Second parameter - user selected input feature classes on which to run tool
        param1 = arcpy.Parameter(
            displayName="Input Feature Classes",
            name="input_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        # Third parameter - output file name for the queried feature class with joined table
        param2 = arcpy.Parameter(
            displayName="Feature Class Output Name (fc name will become tacked onto the beginning)",
            name="fc_output_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        name_new = 'BdyPol_Place_Census'
        param2.value = name_new
        
        params = [param0, param1, param2]
        
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = 1

        # File Pathways
        initial_gdb = parameters[0].valueAsText
        input_fc = parameters[1]
        name_new = parameters[2].valueAsText

        new_folder = str(pathlib.Path(initial_gdb).parent)
        staging_gdb = arcpy.management.CreateFileGDB(new_folder, 'Staging') # Necessary because projection cannot occur within the same folder
        
        wkt = 'GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]]'
        sr = arcpy.SpatialReference()
        sr.loadFromString(wkt)
        NAD83 = 'GCS_North_American_1983'

        arcpy.env.workspace = initial_gdb
        fcs_master = arcpy.ListFeatureClasses()
        
        # Set the coordinate system to NAD83 for each feature class
        flag_input_gdb = 0
        fcs = input_fc.valueAsText.split(';')
        lst_merge = []

        for filename in fcs:
            start_index = filename.rfind(chr(92))
            file = filename[start_index + 1:]
            if file[-1] == chr(39):
                file = file[:-1]
            if file not in fcs_master:
                arcpy.AddMessage('Error! {0} is not saved within the Input GDB. All selected feature classes must be saved within the Input GDB.'.format(file))
                flag_input_gdb = 1            
            else:
                for fc_master in fcs_master:
                    if fc_master == file:
                        coord = arcpy.Describe(fc_master).spatialReference
                        arcpy.AddMessage("{0} : {1}".format(fc_master, coord.name))
                        if coord.name == NAD83:
                            arcpy.AddMessage('Not Projected\n')
                        else:
                            out_fc = os.path.join(str(staging_gdb), fc_master)
                            arcpy.management.Project(fc_master, out_fc, wkt)
                            arcpy.AddMessage('Projected to {0}\n'.format(NAD83))
                            arcpy.management.Delete(fc_master, 'FeatureClass')
                            in_fc = os.path.join(initial_gdb, fc_master)
                            arcpy.management.CopyFeatures(out_fc, in_fc)
                        lst_merge.append(fc_master)

        if flag_input_gdb == 1:
            quit()
            
        arcpy.management.Delete(staging_gdb)
            
        # Merge together Incorporated_Place and Census_Designated_Place
        merge_output = os.path.join(initial_gdb, name_new)
        arcpy.management.Merge(lst_merge, merge_output)
        names = ', '.join(lst_merge)
        arcpy.AddMessage('{0} features merged together'.format(names))
        for fc in fcs_master:
            if fc in lst_merge:
                arcpy.management.Delete(fc, "FeatureClass")
                
        return
