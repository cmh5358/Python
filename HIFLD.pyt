'''
Title: HIFLD
Authors: Caitlin Hartig, Justine Jedlicka
Date: December 2024

This program takes input data from the HERE Full Transportation Dataset and combines them together into an initial roads layer. Once this is completed, the Delete Identical tool is utilized to remove all records with identical shape and route type. Then roads with identical shape are removed in such a way that higher priority route types are kept and lesser priority route types are deleted.
Next, the initial roads layer is expanded to include certain fields that come from other HERE Full Transportation Data. The ThinRoadNetwork tool is utilized to populate a new “Generalization” field.
Subsequently, all roads are deleted that are inside the forest lands, except for state highways, US-routes, interstates, and corresponding ramps. Once this is completed, a new field called “Minus_ID” is added to the roads layer and marks which lands are inside the forest vs outside the forest.
Finally, a new field is created in the roads layer that contains updated labelling for the route type. With one or two exceptions, only the route numbers remain for high priority routes.

Note: This script is finished but has not been fully tested, as my contract with the client ended before that could take place. Consequently, there may be some bugs here and there that have not yet been resolved, and some of the functions might only work for smaller datasets and not for extremely large ones.

Libraries Utilized: arcpy, datetime, os
'''

import arcpy, datetime, os

#This script clips the data to a new buffered boundary called FS_Lands_dissolved & processes the HIFLD Labels. 
# #(This is a custom dataset )

class Toolbox(object):
    def __init__(self):

        self.label = "HIFLD"
        self.alias = ""

        self.tools = [HIFLD]


class HIFLD(object):
    def __init__(self):

        self.label = "HIFLD"
        self.description = "This is a tool that does something."
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
        
        # Second parameter - "Streets" feature class
        param1 = arcpy.Parameter(
            displayName='Input "Streets" Feature Class',
            name="input_streets",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        # Third parameter - "StreetAddress" table
        param2 = arcpy.Parameter(
            displayName='Input "StreetAddress" Table',
            name="input_streetaddress",
            datatype="DETable",
            parameterType="Required",
            direction="Input")

        # Fourth parameter - "Link" Feature Class
        param3 = arcpy.Parameter(
            displayName='Input "Link" Feature Class',
            name="input_link",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        # Fifth parameter - "LinkAttribute" Table
        param4 = arcpy.Parameter(
            displayName='Input "LinkAttribute" Table',
            name="input_linkattribute",
            datatype="DETable",
            parameterType="Required",
            direction="Input")
        
        # Sixth parameter - "Status" Table
        param5 = arcpy.Parameter(
            displayName='Input "Status" Table',
            name="input_status",
            datatype="DETable",
            parameterType="Required",
            direction="Input")    

        # Seventh parameter - "FS Lands" Feature Class
        param6 = arcpy.Parameter(
            displayName='Input "FS Lands" Feature Class',
            name="input_fslands",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
               
        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = 1

        start = datetime.datetime.now()
        arcpy.AddMessage(start)
        arcpy.AddMessage('\n')

        # Input parameters
        input_gdb = parameters[0].valueAsText
        streets = parameters[1].valueAsText
        street_address = parameters[2].valueAsText
        link = parameters[3].valueAsText
        link_attribute = parameters[4].valueAsText
        status = parameters[5].valueAsText
        fs_lands = parameters[6].valueAsText

        # Step 1 - Construct a list of input names to use in the delete_extraneous(lst_output, input_gdb, lst_input) function as the lst_input
        streets_name = display_name(streets, input_gdb)
        street_address_name = display_name(street_address, input_gdb)
        link_name = display_name(link, input_gdb)
        link_attribute_name = display_name(link_attribute, input_gdb)
        status_name = display_name(status, input_gdb)
        fs_lands_name = display_name(fs_lands, input_gdb)
        lst_input = [streets_name, street_address_name, link_name, link_attribute_name, status_name, fs_lands_name]

        lst_output = [] # Holds the output layers from each step, for use in the delete_extraneous(lst_output, input_gdb, lst_input) function as the lst_output

        # Step 2 - Create the initial_roads layer
        initial_roads = create_initial_roads(input_gdb, streets, street_address)
        lst_output.append(initial_roads)
        delete_extraneous(lst_output, input_gdb, lst_input)

        # Step 3 - Create the hifld_attributed layer
        hifld_attributed = add_attributes(input_gdb, initial_roads, link, link_attribute, status)
        lst_output.append(hifld_attributed)
        delete_extraneous(lst_output, input_gdb, lst_input)

        # Step 4 - Create the hifld_merged layer
        hifld_merged = mark_inside_outside(input_gdb, hifld_attributed, fs_lands)
        lst_output.append(hifld_merged)
        delete_extraneous(lst_output, input_gdb, lst_input)

        # Step 5 - Create the hifld_final layer
        hifld_plus_gtac = labels(input_gdb, hifld_merged)
        lst_output.append(hifld_plus_gtac)
        delete_extraneous(lst_output, input_gdb, lst_input)

        end = datetime.datetime.now()
        arcpy.AddMessage(end)

# '''
#     Purpose - Function display_name(feature_class, input_gdb) takes a feature class / table and the Input GDB in which it is saved. It then returns the display name for the same feature class / table.
#     Inputs - feature_class: The file pathway to the feature class / table for which to obtain a display name. Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb\hifld_final'.
#              input_gdb: The file pathway to the Input GDB that contains the feature class / table Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#     Outputs - feature_class_name: The display name for the feature class / table Ex) "hifld_final".
# '''
def display_name(feature_class, input_gdb):
    feature_class_name = ''

    for root, dss, lst_fcs in arcpy.da.Walk(input_gdb, datatype = ['FeatureClass', 'Table']):
        for fc in lst_fcs:
            if fc in feature_class:
                feature_class_name = fc

    return feature_class_name

# '''
#     Purpose - Function delete_extraneous(lst_output, input_gdb, lst_input) takes a list of output layers, an Input GDB, and a list of input layers. It deletes all feature classes / tables located in the Input GDB that are neither in the list of output layers nor in the list of input layers.
#     Inputs - lst_output: The list of output layers, or feature classes / tables, that should remain after all other files in the Input GDB have been deleted Ex) lst_output = [hifld_final].
#              input_gdb: The Input GDB containing the output_layer Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              lst_input: The list of input layers that should remain in the Input GDB Ex) lst_input = [streets_name, street_address_name, link_name, link_attribute_name, status_name, fs_lands_name].
#     Outputs - None
# '''
def delete_extraneous(lst_output, input_gdb, lst_input):
    output_names = []

    for output_layer in lst_output:
        output_layer_name = display_name(output_layer, input_gdb)
        output_names.append(output_layer_name)

    arcpy.env.workspace = input_gdb
    for root, dss, lst_fcs in arcpy.da.Walk(input_gdb, datatype = ['FeatureClass', 'Table']):
        for fc in lst_fcs:
            if fc not in output_names:
                if fc not in lst_input:
                    arcpy.management.Delete(fc)

    arcpy.AddMessage('Extraneous layers deleted.\n')

# '''
#     Purpose - Function create_new_gdb(input_gdb, name) takes an Input GDB and name, and then creates a new GDB in the parent folder directory of the Input GDB (one level up in the folder structure) with that name.
#     Inputs - input_gdb: The file pathway to the Input GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              name: The name of the new GDB Ex) r'Processing.gdb'
#     Outputs - new_gdb: The file pathway to the new GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Processing.gdb'.
# '''
def create_new_gdb(input_gdb, name):
    base_folder = os.path.dirname(input_gdb)    
    new_gdb = os.path.join(base_folder, name)

    if not os.path.isdir(new_gdb):
        arcpy.management.CreateFileGDB(base_folder, name, "CURRENT")

    return new_gdb

# '''
#     Purpose - Function create_initial_roads(input_gdb, streets, street_address) takes an Input GDB containing the streets layer and the street_address layer and then joins them together based on the Link_ID field, creating the initial_roads layer.
#                 Once this has been completed, the Delete Identical tool is utilized to remove all records from the initial_roads layer that have identical shape and route type.
#                 Next, overlapping route types of the same shape are removed, leaving route type 1 as the priority and so forth until route type 4, creating the initial_roads_final layer as output. Note: NULL route type values are left alone and are not deleted.
#     Inputs - input_gdb: a file pathway to the Input GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              streets: a file pathway to the "Streets" feature class (which comes from the 20230918_HERE_FullTransportationDataset.gdb or updated version and should be first copied into the Input GDB).
#              street_address: a file pathway to the "StreetAddress" table (which comes from the 20230918_HERE_FullTransportationDataset.gdb or updated version and should be first copied into the Input GDB).
#     Outputs - initial_roads: the initial roads layer which includes the StreetAddress table joined into the Streets feature class, with identical records of the same shape and route type removed, and with overlapping route types removed, leaving route type 1 as the priority and so forth until route type 4.
# '''
def create_initial_roads(input_gdb, streets, street_address):
    # New feature class file pathways
    initial_roads = os.path.join(input_gdb, 'initial_roads')
    initial_roads1a = os.path.join(input_gdb, 'initial_roads1a')
    initial_roads_sorted = os.path.join(input_gdb, 'initial_roads_sorted')

    # Step 1 - Join streets and street_address together. Create the initial_roads layer
    name = r'Processing.gdb'
    processing_gdb = create_new_gdb(input_gdb, name)
    arcpy.env.workspace = processing_gdb
    arcpy.env.qualifiedFieldNames = False
    JOIN_FIELD = 'Link_ID'
    JOIN_FIELD2 = 'LINK_ID'
    roads = arcpy.management.AddJoin(streets, JOIN_FIELD, street_address, JOIN_FIELD2, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY") # Located in the Processing GDB
    arcpy.management.CopyFeatures(roads, initial_roads) # The roads layer is then copied back into the Input GDB to solidify the join. The initial_roads layer is thus created as output.
    drop_field = JOIN_FIELD2 + '_1'
    arcpy.management.DeleteField(initial_roads, drop_field, 'DELETE_FIELDS') # Delete the duplicate LINK_ID_1 field

    # Obtain feature class / table names for program message display
    streets_name = display_name(streets, input_gdb)
    street_address_name = display_name(street_address, input_gdb)
    initial_roads_name = display_name(initial_roads, input_gdb)

    arcpy.AddMessage('{0} and {1} layers joined together; {2} layer created.\n'.format(streets_name, street_address_name, initial_roads_name))

    # Step 2 - Delete Identical based on the fields "Shape" and "ROUTE_TYPE". Removes all records from initial_roads that have identical shape and route type. 
    fields = ["Shape", "ROUTE_TYPE"]
    arcpy.management.DeleteIdentical(initial_roads, fields)
    arcpy.AddMessage('Records removed from {0} that have identical shape and route type.\n'.format(initial_roads_name))

    # Step 3 - Remove overlapping route types with 1 as the priority and so forth until 4
    arcpy.management.FindIdentical(initial_roads, initial_roads1a, "Shape") # Find records with identical shape in initial_roads. initial_roads1a output table is created.
    join_fc = arcpy.management.AddJoin(initial_roads, "OBJECTID", initial_roads1a, "IN_FID", "KEEP_ALL", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY") # Join the initial_roads1a output table into the initial_roads layer.
    arcpy.management.Sort(join_fc, initial_roads_sorted, 'FEAT_SEQ') # Sort the initial_roads layer based on the "FEAT_SEQ" field, creating the initial_roads_sorted layer as output.

    count = -999 # This count tracks the values in the field 'FEAT_SEQ', which shows the same number for records that the FindIdentical tool has deemed to have identical shape.
    lst_roads = [] # This list will hold tuples containing the route type and the OBJECTID for all features that have identical shape, as determined by the 'FEAT_SEQ' field. This list is reset whenever the value in the field 'FEAT_SEQ' changes to a different number.
    dict_roads = {} # This dictionary will hold each list created in lst_roads that has a length more than 1 (meaning, it only holds the lists created in lst_roads if they contain info for more than 1 identical feature/shape).
    lst_del = [] # This list will hold all the OBJECTIDs that need to be deleted from the initial_roads layer due to being duplicates of lower priority route types.

    with arcpy.da.SearchCursor(initial_roads_sorted, ['ROUTE_TYPE', 'FEAT_SEQ', 'OBJECTID']) as cursor:
        for row in cursor:
            if row[0] is not None: # Skip all ROUTE_TYPE IS NULL, since we want to save all these.
                if count == -999:
                        count = row[1]
                if row[1] == count:
                    lst_roads.append((row[0], row[2]))
                else:
                    if len(lst_roads) > 1:
                        dict_roads[count] = lst_roads

                    lst_roads = []
                    count = row[1]
                    lst_roads.append((row[0], row[2]))

    lst_dict_values = list(dict_roads.items())
    arcpy.AddMessage(len(lst_dict_values))

    for lst_dict_value in lst_dict_values:
        lst_dict_value = list(lst_dict_value)
        lst_tuple = list(lst_dict_value[1])
        lst_tuple.sort() # Sort the records in ascending order (and thus in order of priority with Route Type 1 being the most important and Route Type 4 being the least important).
        for tuple in lst_tuple:
            tuple = list(tuple) # tuple = ('ROUTE_TYPE', 'OBJECTID').
            if tuple != list(lst_tuple[0]): # Save the first tuple in the list, since this is the priority route type
                lst_del.append(tuple[1]) # Add the OBJECTID from all other tuples in the list to the lst_del (to be deleted from the initial_roads layer)

    with arcpy.da.UpdateCursor(initial_roads, ['OBJECTID']) as cursor: # ***Note: this step appears to work, but takes over 24 hours to run.
        for row in cursor:
            if row[0] in lst_del:
                cursor.deleteRow()

    arcpy.AddMessage('Overlapping route types removed from {0}.\n'.format(initial_roads_name))

    arcpy.management.Delete(processing_gdb)

    return initial_roads

# '''
#     Purpose - Function add_attributes(input_gdb, initial_roads, link, link_attribute, status) takes an Input GDB that contains the initial_roads, link, status, and link_attribute layers.
#                   First, the following fields are added: ACCESS_ID, STATUS_ID, POI_ACCESS, EXPANDED_INCLUSION, URBAN, Heirarchy, Generalization.
#                   Next, it joins the Link feature class and populates the ACCESS_ID, Status_ID, and POI_Access fields via the Link_ID. Once this has been completed, the join is removed.
#                   Then, it joins the LinkAttribute table and populates the Expanded Inclusion field via the Link_ID. Once this has been completed, the join is removed.
#                   Next, it joins the Status table and populates the URBAN field via the STATUS_ID. Once this has been completed, the join is removed.
#                   Next, the Hierarchy field values 0-5 are populated based on 5 distinct queries. Hierarchy = 0 indicates roads that are most important, while hierarchy = 5 indicates roads that are least important.
#                   Finally, the ThinRoadNetwork tool is utilized with the Hierarchy field to populate the "Generalization" field, utilizing a minimum distance of 3,000 m.
#     Inputs - input_gdb: the file pathway to the Input GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              initial_roads: the file pathway to the initial_roads layer to be worked on (should be called "initial_roads", the output of the create_initial_roads(input_gdb, streets, street_address) function, which is saved in the Input GDB).
#              link: the file pathway to the "Link" feature class (which comes from the 20230918_HERE_FullTransportationDataset.gdb or updated version and should be first copied into the Input GDB).
#              link_attribute: the file pathway to the "LinkAttribute" feature class (which comes from the 20230918_HERE_FullTransportationDataset.gdb or updated version and should be first copied into the Input GDB).
#              status: the file pathway to the "Status" table (which comes from the 20230918_HERE_FullTransportationDataset.gdb or updated version and should be first copied into the Input GDB).
#     Outputs - hifld_attributed: The HIFLD layer with all attributes added and populated.
# '''
def add_attributes(input_gdb, initial_roads, link, link_attribute, status):
    # New feature class file pathways
    hifld_query0 = os.path.join(input_gdb, 'hifld_query0')
    hifld_query1 = os.path.join(input_gdb, 'hifld_query1')
    hifld_query2 = os.path.join(input_gdb, 'hifld_query2')
    hifld_query3 = os.path.join(input_gdb, 'hifld_query3')
    hifld_query4 = os.path.join(input_gdb, 'hifld_query4')
    hifld_query5 = os.path.join(input_gdb, 'hifld_query5')
    hifld_attributed = os.path.join(input_gdb, 'hifld_attributed')

    # Step 1 - Add Fields- ACCESS_ID, STATUS_ID, POI_ACCESS, EXPANDED_INCLUSION, URBAN, Heirarchy, Generalization.
    ACCESS_ID = ['ACCESS_ID', 'Long']
    STATUS_ID = ['STATUS_ID', 'Short']
    POI_ACCESS = ['POI_ACCESS', 'Text', '', 1]
    EXPANDED_INCLUSION = ['EXPANDED_INCLUSION', 'Short']
    URBAN = ['URBAN', 'Text', '', 1]
    heirarchy = ['Heirarchy', 'Short']
    generalization = ['Generalization', 'Short']

    lst_fields = [ACCESS_ID, STATUS_ID, POI_ACCESS, EXPANDED_INCLUSION, URBAN, heirarchy, generalization]
    arcpy.management.AddFields(initial_roads, lst_fields)

    delim = ', '
    str_field_names = '' # This string will hold all the field names for program output display

    for lst_field in lst_fields:
        str_field_names += lst_field[0] + delim
    str_field_names = str_field_names[:-(len(delim))]

    arcpy.AddMessage('{0} fields added.\n'.format(str_field_names))

    # Step 2 - Obtain feature class / table names
    initial_roads_name = display_name(initial_roads, input_gdb)
    link_name = display_name(link, input_gdb)
    link_attribute_name = display_name(link_attribute, input_gdb)
    status_name = display_name(status, input_gdb)

    # Step 3 - Join the Link feature class into the initial_roads layer. Populate the ACCESS_ID, Status_ID, and POI_ACCESS fields via the Link_ID.
    name = r'Processing.gdb'
    processing_gdb = create_new_gdb(input_gdb, name)
    arcpy.env.workspace = processing_gdb
    arcpy.env.qualifiedFieldNames = True
    field_name = 'Link_ID'
    JOIN_FIELD = 'LINK_ID'
    roads1 = arcpy.management.AddJoin(initial_roads, field_name, link, JOIN_FIELD, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY")
    arcpy.management.CalculateField(roads1, '{0}.{1}'.format(initial_roads_name, ACCESS_ID[0]), '!{0}.{1}!'.format(link_name, ACCESS_ID[0])) # Fill the 'ACCESS_ID' field
    arcpy.management.CalculateField(roads1, '{0}.{1}'.format(initial_roads_name, STATUS_ID[0]), '!{0}.{1}!'.format(link_name, STATUS_ID[0])) # Fill the 'STATUS_ID' field
    arcpy.management.CalculateField(roads1, '{0}.{1}'.format(initial_roads_name, POI_ACCESS[0]), '!{0}.{1}!'.format(link_name, POI_ACCESS[0])) # Fill the 'POI_ACCESS' field
    arcpy.management.RemoveJoin(roads1)
    arcpy.AddMessage('{0}, {1}, and {2} fields populated.\n'.format(ACCESS_ID[0], STATUS_ID[0], POI_ACCESS[0]))
    
    # Step 4 - Join the LinkAttribute table into the initial_roads layer. Populate the EXPANDED_INCLUSION field via the Link_ID.
    roads2 = arcpy.management.AddJoin(initial_roads, field_name, link_attribute, JOIN_FIELD, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY")
    arcpy.management.CalculateField(roads2, '{0}.{1}'.format(initial_roads_name, EXPANDED_INCLUSION[0]), '!{0}.{1}!'.format(link_attribute_name, EXPANDED_INCLUSION[0])) # Fill the 'EXPANDED_INCLUSION' field
    arcpy.management.RemoveJoin(roads2)
    arcpy.AddMessage('{0} field populated.\n'.format(EXPANDED_INCLUSION[0]))

    # Step 5 - Join the Status table into the initial_roads layer. Populate the URBAN field via the STATUS_ID.
    JOIN_FIELD = 'STATUS_ID'
    roads3 = arcpy.management.AddJoin(initial_roads, JOIN_FIELD, status, JOIN_FIELD, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY")
    arcpy.management.CalculateField(roads3, '{0}.{1}'.format(initial_roads_name, URBAN[0]), '!{0}.{1}!'.format(status_name, URBAN[0])) # Fill the 'URBAN' field
    arcpy.management.RemoveJoin(roads3)
    arcpy.AddMessage('{0} field populated.\n'.format(URBAN[0]))

    # Step 6: Populate values 0-5 in the Hierarchy field
    hifld_queries = [hifld_query0, hifld_query1, hifld_query2, hifld_query3, hifld_query4, hifld_query5]

    query0 = "((ROUTE_TYPE IN (1, 2, 3, 4) AND FuncClass IN (1, 2, 3, 4, 5)) OR FuncClass IN (1, 2, 3, 4)) AND Paved = 'Y'"
    query1 = "((ROUTE_TYPE IN (1, 2, 3, 4) AND FuncClass IN (1, 2, 3, 4, 5)) OR FuncClass IN (1, 2, 3, 4)) AND Paved = 'N'"
    query2 = "FuncClass IN (5) AND Paved = 'Y' AND URBAN = 'N'"
    query3 = "FuncClass IN (5) AND Paved = 'N' AND URBAN = 'N'"
    query4 = "FuncClass IN (5) AND Paved = 'Y' AND URBAN = 'Y'"
    query5 = "FuncClass IN (5) AND Paved = 'N' AND URBAN = 'Y'"

    lst_queries = [query0, query1, query2, query3, query4, query5]

    for i in range(len(lst_queries), 0, -1): # Fill the Hierarchy field in reverse query order, as some records appear in multiple queries. Therefore, the record will be assigned the lower, or more important, hierarchy value by the end of the loop.
        for hifld_query in hifld_queries:
            for query in lst_queries:
                if hifld_query == hifld_queries[i-1]:
                    if (i-1) == lst_queries.index(query):
                        selection = arcpy.management.SelectLayerByAttribute(initial_roads, "NEW_SELECTION", query)
                        arcpy.management.CopyFeatures(selection, hifld_query)

                        arcpy.env.qualifiedFieldNames = True
                        JOIN_FIELD = 'Link_ID'
                        roads = arcpy.management.AddJoin(initial_roads, JOIN_FIELD, hifld_query, JOIN_FIELD, "KEEP_COMMON", "NO_INDEX_JOIN_FIELDS", "NO_REBUILD_INDEX", "JOIN_ONE_TO_MANY")
                        arcpy.management.CalculateField(roads, '{0}.{1}'.format(initial_roads_name, heirarchy[0]), (i-1), "PYTHON3") # Fill the 'Hierarchy' field with the correct number (i-1) based on the designated query
                        arcpy.management.RemoveJoin(roads)

    arcpy.AddMessage('{0} field populated.\n'.format(heirarchy[0]))

    # Step 7: Delete extraneous roads / features
    query = "(ACCESS_ID IN (290) AND STATUS_ID IN (41)) OR (ACCESS_ID IN (34, 623, 999) AND STATUS_ID IN (33, 37)) OR ACCESS_ID = 32 OR EXPANDED_INCLUSION IN (12, 9) OR POI_ACCESS = 'Y'"
    selection = arcpy.management.SelectLayerByAttribute(initial_roads, "NEW_SELECTION", query, "INVERT")
    arcpy.management.CopyFeatures(selection, hifld_attributed)

    hifld_attributed_name = display_name(hifld_attributed, input_gdb)

    arcpy.AddMessage('Extraneous roads and features deleted. {0} layer created.\n'.format(hifld_attributed_name))

    # Step 8: Run the Road Thin tool at 3,000 m with the Hierarchy and Generalization field
    MIN_LENGTH = 3000 # meters
    arcpy.cartography.ThinRoadNetwork(hifld_attributed, MIN_LENGTH, generalization[0], heirarchy[0])
    arcpy.AddMessage('{0} field populated.\n'.format(generalization[0]))

    arcpy.management.Delete(processing_gdb)

    return hifld_attributed

# '''
#     Purpose - Function mark_inside_outside(input_gdb, hifld_attributed, fs_lands) takes an Input GDB containing the hifld_attributed layer and the fs_lands layer. It then deletes all roads inside the forest from the hifld_attributed layer, except state highways, US-routes, interstates, and corresponding ramps.
#                 Once this has been completed, a field called 'Minus_ID' is added into the hifld_attributed layer, which tracks which roads are inside the FS lands and which are outside.
#                 Once the roads have been marked as either inside the FS lands (hifld_inside) or outside (hifld_outside), the hifld_inside and hifld_outside layers are then merged back together, creating the hifld_merged layer as output.
#     Inputs - input_gdb: the file pathway to the Input GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              hifld_attributed: the file pathway to the hifld_attributed layer to be worked on (should be called "hifld_attributed", the output of the add_attributes(input_gdb, initial_roads, link, link_attribute, status) function, which is saved in the Input GDB).
#              fs_lands: the file pathway to the fs_lands layer (C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb\FS_Lands_dissolved, which is saved in the Input GDB).
#     Output - hifld_merged: the HIFLD layer merged back together, with a new 'Minus_ID' field which indicates if a road is 'In FS' (in the forest) or 'Out FS' (outside of the forest).
# '''
def mark_inside_outside(input_gdb, hifld_attributed, fs_lands):
    # Lists
    lst_merge = [] # An empty list that will hold the hifld_inside and hifld_outside layers, which will be merged back together in the end into the hifld_merged layer
    
    # New feature class file pathways
    working_hifld = os.path.join(input_gdb, 'working_hifld')
    hifld_inside = os.path.join(input_gdb, 'hifld_inside')
    hifld_outside = os.path.join(input_gdb, 'hifld_outside')
    hifld_merged = os.path.join(input_gdb, 'hifld_merged')

    # Step 1 - Clip the hifld_attributed layer using the fs_lands layer. Create the working_hifld layer as output.
    arcpy.analysis.Clip(hifld_attributed, fs_lands, working_hifld)
    
    # Step 2 - In the working_hifld layer, delete all roads except state highways, US-routes, interstates, and corresponding ramps. Create the hifld_inside layer as output.
    query = "(ROUTE_TYPE IN (1,2,3) AND FuncClass IN (1,2,3,4,5)) OR (Paved = 'Y' AND FuncClass IN (1,2,3))" # Keep these roads, delete all else.
    selection = arcpy.management.SelectLayerByAttribute(working_hifld, "NEW_SELECTION", query)
    arcpy.management.CopyFeatures(selection, hifld_inside)
    arcpy.management.CalculateField(hifld_inside, 'Minus_ID', "'In FS'", "PYTHON3") # Adds a field in the hifld_inside layer called 'Minus_ID' and fills it with 'In FS' for each record.
    lst_merge.append(hifld_inside)
    hifld_inside_name = display_name(hifld_inside, input_gdb)
    arcpy.AddMessage('{0} layer created.\n'.format(hifld_inside_name))

    # Step 3 - Erase the hifld_attributed layer using the fs_lands layer (erases roads in the hifld_attributed layer that are from fs_lands). Create the hifld_outside layer as output.
    arcpy.analysis.Erase(hifld_attributed, fs_lands, hifld_outside)
    arcpy.management.CalculateField(hifld_outside, 'Minus_ID', "'Out FS'", "PYTHON3") # Adds a field in the hifld_outside layer called 'Minus_ID' and fills it with 'Out FS' for each record.
    lst_merge.append(hifld_outside)
    hifld_outside_name = display_name(hifld_outside, input_gdb)
    arcpy.AddMessage('{0} layer created.\n'.format(hifld_outside_name))

    # Step 4 - Merge hifld_inside and hifld_outside back together into 1 layer. Create the hifld_merged layer as output.
    arcpy.management.Merge(lst_merge, hifld_merged)
    delim = 'and '
    names = delim.join(lst_merge)
    names = names[:-len(delim)]

    hifld_merged_name = display_name(hifld_merged, input_gdb)

    arcpy.AddMessage('Merged together {0}. {1} layer created.\n'.format(names, hifld_merged_name))

    return hifld_merged

# '''
#     Purpose - Function labels(input_gdb, hifld_merged) takes the hifld_merged layer and saves a copy as the hifld_plus_gtac layer. Then it updates the labelling in the hifld_plus_gtac layer for the "BASENAME_ID" field, for route types 1-4 only.
#               First, the "BASENAME_ID" field is created. Then, a query is applied to an update cursor that shows results for route types 1-4 only in the hifld_final layer.
#               For each result, the route number is extracted from the "BASE_NAME" field and then is utilized to populate the "BASENAME_ID" field.
#               In special circumstances, such as when the row ends with '-ALT', then an 'A' is appended to the end of the new name.
#     Inputs - input_gdb: the file pathway to the Input GDB Ex) r'C:\Users\caitl\OneDrive\Documents\Tools\Master_GDB.gdb'.
#              hifld_merged: The file pathway to the hifld_merged layer (should be called "hifld_merged", the output of the mark_inside_outside(input_gdb, hifld_attributed, fs_lands) function, which is saved in the Input GDB).
#     Outputs - hifld_plus_gtac: The file pathway to the hifld_plus_gtac layer, with revised labelling, which is saved in the Input GDB.
# '''
def labels(input_gdb, hifld_merged):
    # New feature class file pathways
    hifld_plus_gtac = os.path.join(input_gdb, 'hifld_plus_gtac')

    # Step 1 - Create hifld_plus_gtac layer
    arcpy.management.CopyFeatures(hifld_merged, hifld_plus_gtac)
    hifld_plus_gtac_name = display_name(hifld_plus_gtac, input_gdb)
    arcpy.AddMessage('{0} layer created.'.format(hifld_plus_gtac_name))

    # Step 1 - Add "BASENAME_ID" field to hifld_merged
    arcpy.management.AddField(hifld_plus_gtac, "BASENAME_ID", "TEXT", "", "", "60","", "NULLABLE")

    # Step 2 - Fill the "BASENAME_ID" field with the modified route information from the "BASE_NAME" field
    fields = ["BASE_NAME", "BASENAME_ID"] # Revising the "BASENAME_ID" field based on the content of the "BASE_NAME" field
    query = 'ROUTE_TYPE IN (1, 2, 3, 4)' # Restrict results to route types 1-4 only

    with arcpy.da.UpdateCursor(hifld_plus_gtac, fields, query) as uc:
        for row in uc:
            if row[0] != None: # Skip rows where the "BASE_NAME" field IS NULL
                str_name = '' # This string holds the modified route information for the "BASENAME_ID" field

                for char in row[0]:
                    try: # Save each character in the row that is an integer
                        int(char)
                        str_name += char                         
                    except: # If the row ends with '-ALT', append an 'A' to the modified route name
                        ALT = '-ALT'
                        if row[0].endswith(ALT):
                            if char == row[0][-(len(ALT))]:
                                str_name += 'A'                     

                row[1] = str_name                            
                uc.updateRow(row) # Update the "BASENAME_ID" field with the modified route information

    arcpy.AddMessage('Labels updated for {0}'.format(hifld_plus_gtac_name))

    return hifld_plus_gtac