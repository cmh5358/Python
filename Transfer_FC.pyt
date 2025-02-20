'''
Title: Transfer FC
Author: Caitlin Hartig
Date: November 2024

This toolbox takes layers that have first gone through the Parse FC toolbox and then uploads them into ArcGIS Enterprise SDE geodatabases (PostgreSQL). The user selects an upload destination via drop-down menu.

Libraries Utilized: arcpy, os
'''

import arcpy, os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Transfer_FC"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Transfer_FC]


class Transfer_FC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Transfer_FC"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter - file directory pathway to Input GDB
        param0 = arcpy.Parameter(
            displayName="Input GDB (Should contain the relevant feature classes)",
            name="input_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        master_gdb = r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'
        param0.value = master_gdb
        
        # Second parameter - user selected input feature classes on which to run tool (must be contained within the Input GDB)
        param1 = arcpy.Parameter(
            displayName="Input Feature Class / Table",
            name="input_fc",
            datatype=["DEFeatureClass", "DETable"],
            parameterType="Required",
            direction="Input",
            multiValue=True)

        # Third parameter - user selected output GDB
        param2 = arcpy.Parameter(
            displayName="Output GDB -- Example1 or Example2",
            name="output_gdb",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        lst = []
        folder_new1 = r'C:\Users\caitl\OneDrive\Documents\Tools\Example1.gdb'
        lst.append(folder_new1)
        
        folder_new2 = r'C:\Users\caitl\OneDrive\Documents\Tools\Example2.sde'
        lst.append(folder_new2)

        param2.filter.type = "ValueList" # Remove specific links / dropdown menu. Change to a user populated field where the user inputs the correct link themselves.
        param2.filter.list = lst
        
        params = [param0, param1, param2]
        
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
        arcpy.env.overwriteOutput = 1

        # File Pathways
        folder_old = parameters[0].valueAsText
        input_fc = parameters[1]
        folder_new = parameters[2].valueAsText

        # Upload to Output GDB
        fcs_master_uploaded = upload(folder_old, input_fc, folder_new)

##'''
##    Purpose - Function upload(folder_old, input_fc, folder_new)
##    Inputs - folder_old: File pathway to the Initial GDB, where the user input feature classes / tables are stored Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
##             input_fc: Input feature classes / tables defined by the user Ex) Hydro_NatFloodHaz_Comm_FEMA, Hydro_NatFloodHaz_HazArea_FEMA
##             folder_new: File pathway to the Output GDB. Should either be Example1 (r'C:\Users\caitl\OneDrive\Documents\Tools\Example1.gdb') or Example2 (r'C:\Users\caitl\OneDrive\Documents\Tools\Example2.sde').
##    Output - fcs_master_uploaded: A list filled with feature classes / tables that have been successfully uploaded into the Output GDB
##'''
def upload(folder_old, input_fc, folder_new):
    fcs_master_uploaded = []

    arcpy.env.workspace = folder_old

    fcs = input_fc.valueAsText.split(';')

    for filename in fcs:
        start_index = filename.rfind(chr(92))
        file = filename[start_index + 1:]
        if file[-1] == chr(39):
            file = file[:-1]
        for dirpath_master, dcs_master, fcs_master in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
            if file not in fcs_master:
                arcpy.AddMessage('Error! {0} is not saved within the Input GDB. File not exported. All selected feature classes / tables must be saved within the Input GDB.\n'.format(file))
            else:
                for fc_master in fcs_master:
                    if fc_master == file: # Take each feature class / table in the user's selection that is also located in the Input GDB and copy it into the Output GDB
                        fc_old = os.path.join(folder_old, fc_master)
                        fc_new = os.path.join(folder_new, fc_master)
                        arcpy.management.Copy(fc_old, fc_new)
                        fcs_master_uploaded.append(fc_master)

                        arcpy.AddMessage('{0} copied into {1}.'.format(fc_master, folder_new))

    return fcs_master_uploaded
