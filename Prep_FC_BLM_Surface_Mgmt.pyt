'''
Title: Prep FC BLM Surface Mgmt
Author: Caitlin Hartig
Date: March 2024

This program adds a definition query specifically to the BLM Surface Mgmt feature class specifically. It then dissolves the revised feature class based on the “ADMIN_UNIT_NAME” field.

Libraries Utilized: arcpy, os, shutil, datetime
'''

import arcpy, os, shutil, datetime

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Prep_FC_BLM_Surface_Mgmt"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Prep_FC_BLM_Surface_Mgmt]


class Prep_FC_BLM_Surface_Mgmt(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Prep_FC_BLM_Surface_Mgmt"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter - file directory pathway to initial GDB
        param0 = arcpy.Parameter(
            displayName="Input GDB (Should contain the relevant feature classes)",
            name="input_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        master_gdb = r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'
        param0.value = master_gdb
        
        # Second parameter - user selected input feature class on which to run tool
        param1 = arcpy.Parameter(
            displayName="Input Feature Class",
            name="input_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        
        # Third parameter - SQL query to select certain attributes
        param2 = arcpy.Parameter(
            displayName="SQL Query",
            name="sql_query",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        query = "ADMIN_UNIT_TYPE = 'American Indian Reservation'"
        param2.value = query

        # Fourth parameter - output file name for the queried and dissolved output feature class
        param3 = arcpy.Parameter(
            displayName="Feature Class Output Name",
            name="fc_output_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        date = datetime.date.today()
        date = str(date).replace('-', '')
        name_new = 'sma_blm_indian_area_dissolve_gtac_{0}'.format(date)
        param3.value = name_new
        
        params = [param0, param1, param2, param3]
    
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
        input_gdb = parameters[0].valueAsText
        input_fc = parameters[1].valueAsText
        query = parameters[2].valueAsText
        name_new = parameters[3].valueAsText

        arcpy.env.overwriteOutput = 1

        arcpy.env.workspace = input_gdb
        fcs_master = arcpy.ListFeatureClasses()

        start_index = input_fc.rfind(chr(92))
        file = input_fc[start_index + 1:]
        if file[-1:] == chr(39):
            file = file[:-1]
        if file not in fcs_master:
            arcpy.AddMessage('Error! {0} is not saved within the Input GDB. All selected feature classes must be saved within the Input GDB.'.format(file))
            quit()
        else:        
            # Select features with SQL query  
            fc_old_selected = os.path.join(input_gdb, file + "_selected")
            arcpy.analysis.Select(file, fc_old_selected, query)
            arcpy.AddMessage('New feature class created with certain features selected')

        fcs_master = arcpy.ListFeatureClasses()

        for fc in fcs_master:
            # Dissolve and Rename
            if '_selected' in fc:
                out_fc = os.path.join(input_gdb, name_new)
                arcpy.management.Dissolve(
                    in_features = fc,
                    out_feature_class = out_fc,
                    dissolve_field = "ADMIN_UNIT_NAME"
                )
                arcpy.management.Delete(fc)
                arcpy.AddMessage('Feature class renamed and dissolved')
