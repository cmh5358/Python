'''
Title: Prep FC PLSS
Author: Caitlin Hartig
Date: April 2024

This program merges together two existing waterbody layers into a single layer that defines the whole waterbody area. It then runs the tabulate intersection tool to create a table for each PLSS layer and then joins the table into each existing PLSS layer, respectively. Null values are removed from the joined table and are replaced with 0. Extraneous and temporary layers are deleted.

Libraries Utilized: arcpy, os, datetime
'''

import arcpy, os, datetime

class Toolbox(object):
    def __init__(self):
        self.label = "Prep_FC_PLSS"
        self.alias = ""

        self.tools = [Prep_FC_PLSS]


class Prep_FC_PLSS(object):
    def __init__(self):
        self.label = "Prep_FC_PLSS"
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

        date = datetime.date.today()
        date = str(date).replace('-', '')
        name_new = '_{0}'.format(date)
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
        input_gdb = parameters[0].valueAsText
        input_fc = parameters[1]
        name_new = parameters[2].valueAsText

        arcpy.env.overwriteOutput = 1

        arcpy.env.workspace = input_gdb
        fcs_master = arcpy.ListFeatureClasses()

        fcs = input_fc.valueAsText.split(';')
        fcs.sort(reverse = True)

        flag_input_gdb = 0
        lst_merge = []
        dict_plss = {}

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
                        if 'PLSS' in file:
                            if 'FirstDivision' in file:
                                dict_plss[fc] = "FRSTDIVID"
                            elif 'Township' in file:
                                dict_plss[fc] = "PLSSID"
                        else:
                            lst_merge.append(fc)

        if flag_input_gdb == 1:
            quit()
            
        # Merge queried results of nhd_waterbody together with nhd_area
        merge_output = os.path.join(input_gdb, "nhd_waterbody_area_merged")
        arcpy.management.Merge(lst_merge, merge_output)
        names = ', '.join(lst_merge)
        arcpy.AddMessage('{0} features merged together'.format(names))
        for fc in fcs_master:
            if fc in lst_merge:
                arcpy.management.Delete(fc, "FeatureClass")

        # Run tabulate intersect on the merged layer for both PLSSFirstDivision and PLSSTownship
        fcs_master = arcpy.ListFeatureClasses()
        
        for fc in fcs_master:
            if "merged" in fc:
                for plss in dict_plss:
                    identifier = dict_plss[plss]
                    ti_output = os.path.join(input_gdb, "ti_output_{0}".format(plss))
                    arcpy.analysis.TabulateIntersection(plss, identifier, fc, ti_output)
                    arcpy.AddMessage('Tabulate Intersection completed for {0} and {1}'.format(fc, plss))
                arcpy.management.Delete(fc, "FeatureClass")

        # Join the table to PLSS layer
        dict_final_join = {}
        fcs_master = arcpy.ListFeatureClasses()
        tables = arcpy.ListTables()
        
        for fc in fcs_master:
            for table in tables:
                if fc in table:
                    if fc in dict_plss:
                        dict_final_join[fc] = table

        dict_items = dict_final_join.items()

        for dict_item in dict_items:
            drop_field = dict_plss[dict_item[0]] + "_1"
            arcpy.management.JoinField(dict_item[0], dict_plss[dict_item[0]], dict_item[1], dict_plss[dict_item[0]])
            arcpy.management.DeleteField(dict_item[0], drop_field)
            arcpy.management.Delete(dict_item[1])
            arcpy.AddMessage('\n')
            arcpy.AddMessage('Table join completed for {0} and {1}'.format(dict_item[0], dict_item[1]))

        # Convert NULL values to 0 in the AREA or PERCENTAGE fields (NULL values come as a result of the table join). Rename the final output layers
        fcs_master = arcpy.ListFeatureClasses()
        for fc in fcs_master:
            if fc in dict_plss:
                selected_null_prcnt = os.path.join(input_gdb, "selected_null_prcnt_{0}".format(fc))
                arcpy.analysis.Select(fc, selected_null_prcnt, "AREA IS NULL OR PERCENTAGE IS NULL")
                arcpy.management.CalculateField(selected_null_prcnt, "AREA", '0', "PYTHON3")
                arcpy.management.CalculateField(selected_null_prcnt, "PERCENTAGE", '0', "PYTHON3")
                selected_output = os.path.join(input_gdb, "selected_{0}".format(fc))
                arcpy.analysis.Select(fc, selected_output, "AREA IS NOT NULL OR PERCENTAGE IS NOT NULL")

        lst_merge_township = []
        lst_merge_firstdiv = []

        fcs_master = arcpy.ListFeatureClasses()
        string = "selected_BdySur_PLSS"
        index = len(string)
        for fc in fcs_master:
            if "selected_" in fc:
                if "Township" in fc:
                    lst_merge_township.append(fc)
                    if "null_prcnt_" not in fc:
                        name_final_township = "PLSS_" + fc[index:] + name_new
                elif "FirstDivision" in fc:
                    lst_merge_firstdiv.append(fc)
                    if "null_prcnt_" not in fc:
                        name_final_firstdiv = "PLSS_" + fc[index:] + name_new

        output_final_township = os.path.join(input_gdb, name_final_township)
        arcpy.management.Merge(lst_merge_township, output_final_township)
        arcpy.AddMessage('{0} created'.format(name_final_township))

        output_final_firstdiv = os.path.join(input_gdb, name_final_firstdiv)
        arcpy.management.Merge(lst_merge_firstdiv, output_final_firstdiv)
        arcpy.AddMessage('{0} created'.format(name_final_firstdiv))

        fcs_master = arcpy.ListFeatureClasses()
        for fc in fcs_master:
            if fc in dict_plss or "selected_" in fc:
                arcpy.management.Delete(fc, "FeatureClass")
                
        return
