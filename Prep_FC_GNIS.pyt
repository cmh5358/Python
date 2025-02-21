'''
Title: Prep FC GNIS
Author: Caitlin Hartig
Date: June 2024

This program takes two attribute fields from the older version of this data that have since been discontinued in the new data, and tacks them onto the attribute table for the new data.

Libraries Utilized: arcpy, os
'''

import arcpy, os

class Toolbox(object):
    def __init__(self):
        self.label = "Prep_FC_GNIS"
        self.alias = ""

        self.tools = [Prep_FC_GNIS]


class Prep_FC_GNIS(object):
    def __init__(self):
        self.label = "Prep_FC_GNIS"
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
        
        params = [param0, param1]
        
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        input_gdb = parameters[0].valueAsText
        input_fc = parameters[1]

        arcpy.env.overwriteOutput = 1

        arcpy.env.workspace = input_gdb
        fcs_master = arcpy.ListFeatureClasses()

        fcs = input_fc.valueAsText.split(';')

        flag_input_gdb = 0
        lst_join = []
        dict_final_join = {}

        for filename in fcs:
            start_index = filename.rfind(chr(92))
            file = filename[start_index + 1:]
            if file[-1:] == chr(39):
                file = file[:-1]
            if file not in fcs_master:
                arcpy.AddMessage('Error! {0} is not saved within the Input GDB. All selected feature classes must be saved within the Input GDB.'.format(file))
                flag_input_gdb = 1
            else:
                for fc in fcs_master:
                    if file == fc:
                        lst_join.append(fc)
                        if 'GNIS' in fc:
                            if 'S_USA_' in file:
                                dict_final_join[fc] = "FEATURE_ID"
                            else:
                                dict_final_join[fc] = "feature_id"

        if flag_input_gdb == 1:
            quit()
            
        # Join the elevation fields from the old layer into the new GNIS layer
        dict_items = list(dict_final_join.items())
        dict_items.sort()

        arcpy.management.JoinField(dict_items[0][0], dict_items[0][1], dict_items[1][0], dict_items[1][1])
        out_fc = os.path.join(input_gdb, "GNIS_final")

        fcs_master = arcpy.ListFeatureClasses()
        for fc in fcs_master:
            if 'GNIS' in fc:
                if 'S_USA_' in fc:
                    arcpy.management.Delete(fc)
                else:
                    fields = arcpy.ListFields(fc)
                    for field in fields:
                        if "_1" in field.name:
                            arcpy.management.DeleteField(fc, field.name)

        arcpy.AddMessage('Join completed for {0} and {1}'.format(dict_items[0][0], dict_items[1][0]))
                
        return
