'''
Title: Parse FC
Authors: Caitlin Hartig, Justine Jedlicka
Date: November 2024

This toolbox selects relevant layers within a geodatabase and parses them in preparation for uploading them into ArcGIS Enterprise SDE geodatabases (PostgreSQL).
The program projects the layers into NAD83 if necessary and then compares the schema from the new layer to the old layer that is stored the SDE in question.
The results of the schema comparison are exported into a .txt file for each layer, which is then saved in a specified folder pathway.

Libraries Utilized: arcpy, os, shutil, pathlib
'''

import arcpy, os, shutil, pathlib

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Parse_FC"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Parse_FC]


class Parse_FC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Parse_FC"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter - file directory pathway to the initial GDB
        param0 = arcpy.Parameter(
            displayName="Input GDB (Should contain the relevant feature classes)",
            name="input_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        master_gdb = r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'
        param0.value = master_gdb
        
        # Second parameter - user selected input feature classes / tables on which to run tool
        param1 = arcpy.Parameter(
            displayName="Input Feature Class / Table",
            name="input_fc",
            datatype=["DEFeatureClass", "DETable"],
            parameterType="Required",
            direction="Input",
            multiValue=True)

        # Third parameter - file directory pathway to the GDB utilized for schema check comparison
        param2 = arcpy.Parameter(
            displayName="Schema Comparison GDB (Should be either the Example1 SDE or the Example2 as viewer SDE)",
            name="schema_gdb",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        lst = []
        schema_folder1 = r'C:\Users\caitl\OneDrive\Documents\Tools\Example1.sde'
        lst.append(schema_folder1)
        
        schema_folder2 = r'C:\Users\caitl\OneDrive\Documents\Tools\Postgres\Example2 as viewer.sde'
        lst.append(schema_folder2)

        param2.filter.type = "ValueList"
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
        """The source code of the tool."""
        arcpy.env.overwriteOutput = 1

        # File Pathways
        initial_gdb = parameters[0].valueAsText
        input_fc = parameters[1]
        new_folder = str(pathlib.Path(initial_gdb).parent)
        lst_input = [] # This list holds all the user input feature classes / tables for which the program was also able to assess the projection information and/or project
        schema_folder = parameters[2].valueAsText

        # Part 1 - Project the coordinate system to NAD 83 for each feature class, if it is not already
        lst_input = set_coord(input_fc, new_folder, lst_input, initial_gdb)

        # Part 2 - Check for schema updates for each feature class / table
        compare_schema(new_folder, schema_folder, initial_gdb, lst_input)

##'''
##    Purpose - Function set_coord(input_fc, new_folder, lst_input, initial_gdb) projects a feature class into NAD83, if it is not already.
##    Inputs - input_fc: Input feature classes / tables defined by the user Ex) Hydro_NatFloodHaz_Comm_FEMA, Hydro_NatFloodHaz_HazArea_FEMA
##             new_folder: The parent folder of the initial_gdb Ex) r'C:\Users\caitl\OneDrive\Documents\Tools'.
##             lst_input: An empty list that holds all the user input feature classes / tables for which the program was also able to assess the projection information and/or project.
##             initial_gdb: The initial GDB that holds all the user input feature classes / tables Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
##    Outputs - lst_input: A list filled with user input feature classes / tables for which the program was also able to assess the projection information and/or project.
##'''
def set_coord(input_fc, new_folder, lst_input, initial_gdb):
    fcs = input_fc.valueAsText.split(';')
    staging_gdb = arcpy.management.CreateFileGDB(new_folder, 'Staging') # Necessary because projection cannot occur within the same folder

    # Define projection: NAD83
    wkt = 'GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]]'
    sr = arcpy.SpatialReference()
    sr.loadFromString(wkt)
    NAD83 = 'GCS_North_American_1983'

    arcpy.env.workspace = initial_gdb
    for dirpath_master, dirnames_master, fcs_master in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
        for filename in fcs:
            start_index = filename.rfind(chr(92))
            file = filename[start_index + 1:]
            if file[-1] == chr(39):
                file = file[:-1]
            if file not in fcs_master:
                arcpy.AddMessage('Error! {0} is not saved within the Input GDB. Please save layer into the Input GDB and try again.\n'.format(file))
            else:
                for fc_master in fcs_master:
                    if fc_master == file:
                        in_fc = os.path.join(initial_gdb, fc_master)
                        out_fc = os.path.join(str(staging_gdb), fc_master)

                        try:
                            if arcpy.Describe(fc_master).dataType == 'FeatureClass':
                                # Set the coordinate system to NAD 83 for the feature class if it is not already.
                                coord = arcpy.Describe(fc_master).spatialReference
                                arcpy.AddMessage("{0} : {1}".format(fc_master, coord.name))
                                
                                if coord.name == NAD83: # If the feature class is already in NAD83, it is not projected.
                                    arcpy.AddMessage('Not Projected\n\n')
                                else: # Otherwise, the feature class is projected into NAD83 and saved back into the Master GDB.
                                    arcpy.management.Project(in_fc, out_fc, wkt)
                                    arcpy.AddMessage('Projected to {0}\n\n'.format(NAD83))
                                    arcpy.management.Delete(fc_master, 'FeatureClass')
                                    arcpy.management.CopyFeatures(out_fc, in_fc)

                            lst_input.append(fc_master)

                        except:
                            arcpy.AddMessage('Error! Unable to assess and/or complete projection for {0} layer. This is due to possible network issues. Please try again later.\n\n'.format(fc_master))

    arcpy.management.Delete(staging_gdb) # Staging GDB is deleted

    return lst_input

##'''
##    Purpose - Function compare_schema(new_folder, schema_folder, initial_gdb, lst_input) compares the corresponding feature classes / tables between those in schema_folder and those in initial_gdb and generates a schema report for each layer.
##    Inputs - new_folder: The parent folder of the initial_gdb Ex) r'C:\Users\caitl\OneDrive\Documents\Tools'.
##             schema_folder: The comparison folder with already completed, older files Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Example1.sde'.
##             initial_gdb: The initial GDB that holds all the user input feature classes / tables Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
##             lst_input: A list filled with user input feature classes / tables for which the program was also able to assess the projection information and/or project (this is the output of function set_coord(input_fc, new_folder, lst_input, initial_gdb)).
##    Output - None
##'''
def compare_schema(new_folder, schema_folder, initial_gdb, lst_input):
    outfile_folder = os.path.join(new_folder, 'SchemaResults')
    arcpy.env.workspace = schema_folder

    fcs_old = [] # This list holds all the feature classes / tables in schema_folder
    fcs_new = [] # This list holds all the feature classes / tables in initial_gdb
    
    for dirpath_old, dcs_old, fcs in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']): # Find all the feature classes / tables in schema_folder
        if len(fcs) != 0:
            fcs_old += fcs
    
    if len(fcs_old) == 0:
        arcpy.AddMessage('Error! No feature classes or tables were found inside {0}. Unable to compare schema.\n'.format(schema_folder))
        quit()
    else:
        arcpy.env.workspace = initial_gdb
        for dirpath_new, dcs_new, fcs in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']): # Find all the feature classes / tables in initial_gdb
            if len(fcs) != 0:
                fcs_new += fcs
            
        if len(fcs_new) == 0:
            arcpy.AddMessage('Error! No feature classes or tables were found inside {0}. Unable to compare schema.\n'.format(initial_gdb))
            quit()
        else:
            for fc_new in fcs_new:
                if fc_new in lst_input:
                    flag_fc_new = 0
                
                    for fc_old in fcs_old:
                        if fc_new in fc_old: # Find the corresponding feature class / table in schema_folder and initial_gdb that is also in lst_input                     
                            flag_fc_new = 1
                            outfile_new = os.path.join(outfile_folder, fc_new + '.txt')
                            
                            if os.path.isdir(outfile_new):
                                shutil.rmtree(outfile_new)

                            if arcpy.Describe(fc_new).dataType == 'FeatureClass': # Compare the corresponding feature classes and generate a schema report
                                result = arcpy.management.FeatureCompare(
                                    in_base_features= fc_old,
                                    in_test_features= fc_new,
                                    sort_field= "OBJECTID",
                                    compare_type= "SCHEMA_ONLY",
                                    ignore_options= None,
                                    xy_tolerance= "0.000000008983 DecimalDegrees",
                                    m_tolerance= 0.001,
                                    z_tolerance= 0.001,
                                    attribute_tolerances= None,
                                    omit_field= None,
                                    continue_compare= "NO_CONTINUE_COMPARE",
                                    out_compare_file= outfile_new
                                )
                            elif arcpy.Describe(fc_new).dataType == 'Table': # Compare the corresponding tables and generate a schema report
                                result = arcpy.management.TableCompare(
                                    in_base_table= fc_old,
                                    in_test_table= fc_new,
                                    sort_field= "OBJECTID",
                                    compare_type= "SCHEMA_ONLY",
                                    ignore_options= None,
                                    attribute_tolerances= None,
                                    omit_field= None,
                                    continue_compare= "NO_CONTINUE_COMPARE",
                                    out_compare_file= outfile_new
                                )
                            else:
                                arcpy.AddMessage('Error! Invalid feature type. Feature type can only be either "FeatureClass" or "Table".')
                                quit()

                            if result[1] == 'false': # Print a message regarding whether or not a schema change exists for each layer
                                arcpy.AddMessage('Schema change exists for {0}. Please refer to output file {1}\n\n'.format(fc_new, outfile_new))
                            elif result[1] == 'true':
                                arcpy.AddMessage('No schema change exists for {0}.\n\n'.format(fc_new))

                    if flag_fc_new == 0:
                        arcpy.AddMessage('Error! Corresponding feature class / table for {0} not found in {1}.\n\tUnable to compare schema.\n\n'.format(fc_new, schema_folder))
