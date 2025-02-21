'''
Title: National Flood Hazard Layer (NFHL) Unzip
Author: Caitlin Hartig
Date: November 2024

This script takes a zip folder that has first been created using the NFHL Download States script and then unzips this folder into the same parent directory. Next, it goes through the unzipped folder that it just created, unzips the first layer of subfolders inside the same folder, and then deletes the zipped files that it has just unzipped.
Subsequently, the program goes through all the unzipped subfolders to find all the metadata.xml files contained within those subfolders. Once the program finds a working xml file, it returns the file pathway to the working metadata.xml file.
Next, the program goes through all the unzipped subfolders to find specific layers as outlined in the input dictionary. The program pulls feature classes / tables from each subfolder that have the same name as each key listed in the input dictionary (coming from each distinct state / territory) and projects them into NAD83 if necessary. Then the program merges together all the feature classes / tables with the same key into one national output layer for each key, the name of which is defined as the corresponding value in the input dictionary. Finally, the program imports the metadata file onto each national output layer.

Libraries Utilized: datetime, os, zipfile, arcpy, xml
'''

import datetime, os, zipfile, arcpy
import xml.etree.ElementTree as ET

# '''
# Purpose - unzip_folder(zip_folder) takes a zip folder that has first been created using the NFHL_Download_States.py script and unzips this folder into the same parent directory. 
#     It then goes through the unzipped folder that it just created, unzips the first layer of subfolders inside the same folder, and then finally deletes the zipped files that it has just unzipped.
# Inputs - file pathway for zip_folder Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data.zip'
# Outputs - unzip name - a file pathway to the unzipped folder created by the program
# '''
def unzip_folder(zip_folder):
    if os.path.exists(zip_folder): # Checks to see if the zip folder is a valid pathway
        if zip_folder[-4:] == '.zip': # Checks to see if the zip folder is a .zip
            unzip_name = zip_folder[:-4]
        else:
            print('Error! Not a zip folder.\n')
            quit()

        if os.path.isdir(unzip_name): # If the unzipped folder already exists, attempts to remove it and create a new one
            try:
                os.remove(unzip_name)
            except PermissionError: # If unable to remove the existing folder due to permissions, tacks on a number to create a distinct unzipped folder. Caution! Watch your disk space.
                flag_exists = 'y'
                count_folder = 0
                
                while flag_exists == 'y':
                    count_folder += 1
                    unzip_name += '_{0}'.format(count_folder)

                    if os.path.isdir(unzip_name):
                        unzip_name = unzip_name[:-2]
                    else:
                        flag_exists = 'n'            

        with zipfile.ZipFile(zip_folder, 'r') as myzip: # Extracts the main folder
            myzip.extractall(unzip_name)
        
        print('Main folder unzipped.\n')

        for root, dirs, files in os.walk(unzip_name): # Unzips a secondary layer of zipped files within the unzipped folder (subfolders)
            for file in files:
                file_pathway = os.path.join(root, file)

                if file_pathway[-4:] == '.zip': # Checks to see if the zip folder is a .zip
                    unzip_subfolder_name = file_pathway[:-4]

                    if os.path.isdir(unzip_subfolder_name): # If the unzipped folder already exists, attempts to remove it and create a new one
                        try:
                            os.remove(unzip_subfolder_name)
                        except PermissionError: # If unable to remove the existing folder due to permissions, tacks on a number to create a distinct unzipped folder
                            flag_exists_subfolder = 'y'
                            count_subfolder = 0
                            
                            while flag_exists_subfolder == 'y':
                                count_subfolder += 1
                                unzip_subfolder_name += '_{0}'.format(count_subfolder)

                                if os.path.isdir(unzip_subfolder_name):
                                    unzip_subfolder_name = unzip_subfolder_name[:-2]
                                else:
                                    flag_exists_subfolder = 'n'         

                    with zipfile.ZipFile(file_pathway, 'r') as myzip: # Extracts the subfolder
                        myzip.extractall(unzip_subfolder_name)

                    os.remove(file_pathway) # Removes the zipped file that was just extracted

        print('Subfolders unzipped.\n')

    else:
        print('Error! Folder directory does not exist.\n')
        quit()

    return unzip_name

# '''
# Purpose - obtain_metadata(folder) takes a folder that has first been unzipped using the unzip_folder(zip_folder) function and goes through all the subfolders to find all the metadata.xml files contained within those subfolders.
#     The program then checks each metadata.xml file to make sure that it can be opened/read, and that it is a valid xml file. 
#     Once the program finds a working xml file, it stops analyzing the rest of the metadata.xml files and returns the file pathway to the working metadata.xml file.
# Inputs - folder: a folder pathway for an unzipped NFHL data folder Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data'
# Outputs - metadata_filepath: the file pathway to the first working metadata file in the input folder
# '''
def obtain_metadata(folder):
    flag_meta = 0 # This counter remains 0 until the program finds a metadata file that functions
    dict_metadata = {} # This dictionary holds the file pathways to the metadata.xml for each state / territory

    for root, dirs, files in os.walk(folder):
        for dir_name in dirs:
            if dir_name[-4:] == '.gdb':
                arcpy.env.workspace = os.path.join(root, dir_name)

                start_index = dir_name.find('_')
                end_index = dir_name.rfind('_')
                dir_name_number = dir_name[start_index:end_index] # Find the state / territory number for the feature class being worked on

                if flag_meta == 0:
                    for file in files:
                        if 'metadata.xml' in file: # Pull the metadata.xml files
                            dict_metadata[dir_name_number] = os.path.join(root, file)

    metadata_items = list(dict_metadata.items())

    for metadata in metadata_items: # Find the first working metadata file to use for the metadata import for each national layer
        while flag_meta == 0:
            metadata_filepath = metadata[1]
            try:
                infile = open(metadata_filepath, 'r')
                file_contents = infile.read()
            except:
                if metadata == metadata_items[-1]:
                    print('Error! Unable to open/read any xml files for any state/territory. Please manually check all metadata files.')
                    quit()
            else:
                try:
                    ET.fromstring(file_contents)
                except ET.ParseError:
                    if metadata == metadata_items[-1]:
                        print('Error! Invalid xml files for all states/territories. Please manually check all metadata files.')
                        quit()
                else:
                    flag_meta = 1
    return metadata_filepath

# '''
# Purpose - create_national_layer(folder, dict_fcs, master_gdb, metadata_filepath) takes a folder that has first been unzipped using the unzip_folder(zip_folder) function and goes through all the subfolders to find specific layers as outlined in the input dictionary dict_fcs.
#     The program pulls feature classes / tables from each subfolder that have the same name as each key listed in dict_fcs, projects them into NAD83 if necessary, and then copies the feature classes / tables into the Master GDB. 
#     Once inside the Master GDB, the program then merges together all the feature classes with the same key (coming from each distinct state / territory) and merges them all together into one national output layer for each key, the name of which is defined as the corresponding value in dict_fcs.
#     Finally, the program then imports the metadata file (metadata_filepath) onto each national layer.
# Inputs - folder: a folder pathway for an unzipped NFHL data folder Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data'
#          dict_fcs: a dictionary with keys containing the NFHL feature class / table names in all uppercase, and corresponding values containing the EDW feature class names for the same layers
#               Ex) dict_fcs = {'S_FIRM_PAN':'Hydro_NatFloodHaz_Panel_FEMA', 'S_FLD_HAZ_AR':'Hydro_NatFloodHaz_HazArea_FEMA', 'S_BFE':'Hydro_NatFloodHaz_S_BFE_FEMA', 'S_XS':'Hydro_NatFloodHaz_XS_FEMA', 'S_GEN_STRUCT':'Hydro_NatFloodHaz_Struct_FEMA', 'S_LOMR':'Hydro_NatFloodHaz_LOMR_FEMA', 'S_PROFIL_BASLN':'Hydro_NatFloodHaz_PBas_FEMA', 'S_WTR_AR':'Hydro_NatFloodHaz_Wtr_FEMA', 'L_COMM_INFO':'Hydro_NatFloodHaz_Comm_FEMA', 'STUDY_INFO': 'Hydro_NatFloodHaz_Study_FEMA'}
#          master_gdb: a folder pathway to the Master GDB Ex) r'C:\Users\CaitlinHartig\Documents\Tools\Master_GDB.gdb'
#          metadata_filepath: a file pathway to the metadata.xml file that will be utilized to import metadata onto each national layer Ex) r'C:\Users\CaitlinHartig\Documents\NFHL\Data\NFHL_01_20241004\NFHL_01_20241004_metadata.xml'
# Outputs - None
# '''
def create_national_layer(folder, dict_fcs, master_gdb, metadata_filepath):
    arcpy.env.overwriteOutput = 1

    # Define projection: NAD83
    wkt = 'GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]]'
    sr = arcpy.SpatialReference()
    sr.loadFromString(wkt)
    NAD83 = 'GCS_North_American_1983'
    
    for item in dict_fcs:
        
        lst_names = [] # This list holds the feature classes / tables of the same key that will be combined into 1 national layer    
        lst_fcs = [] # This list holds the feature classes / tables of the same key that will be combined into 1 national layer. Necessary despite lst_names because there is an environment change and name change for all feature classes into the Master GDB before the merge occurs
        data_type = '' # This string holds the data type for the layer (should be either 'FeatureClass' or 'Table')
        data_type_fc = '' # This string holds the data type for the layer as pulled from the Master GDB (should be either 'FeatureClass' or 'Table')
        
        for root, dirs, files in os.walk(folder):
            for dir_name in dirs:
                if dir_name[-4:] == '.gdb':
                    arcpy.env.workspace = os.path.join(root, dir_name)

                    start_index = dir_name.find('_')
                    end_index = dir_name.rfind('_')
                    dir_name_number = dir_name[start_index:end_index] # Find the state / territory number for the feature class being worked on
                    
                    dss = arcpy.ListDatasets()
                    fcs = []

                    if len(dss) != 0: # Find the right feature class/table if the feature class/table is inside of a dataset
                        for ds in dss:
                            arcpy.env.workspace = ds
                            for dirpath_dss, dirnames_dss, fc_dss in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
                                for fc_ds in fc_dss:   
                                    if item in fc_ds.upper():
                                        fcs = fc_dss
                        if len(fcs) == 0: # Find the right feature class/table if there is a dataset but the feature class/table is inside of the main geodatabase
                            arcpy.env.workspace = os.path.join(root, dir_name)
                            for dirpath_fcs, dirnames_fcs, fc_fcs in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
                                fcs = fc_fcs
                    else: # Find the right feature class/table if there are no datasets and the feature class/table is inside of the main geodatabase
                        for dirpath_fcs, dirnames_fcs, fc_fcs in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
                            fcs = fc_fcs

                    flag_item = 0 # Tracks whether or not the right feature class/table is found for a specific state / territory
                    
                    if len(fcs) != 0:
                        for fc in fcs:
                            if item in fc.upper():
                                flag_item = 1
                                
                                in_fc = os.path.join(arcpy.env.workspace, fc)
                                out_name = fc.upper() + dir_name_number
                                lst_names.append(out_name)
                                out_fc = os.path.join(master_gdb, out_name)

                                try:
                                    if arcpy.Describe(fc).dataType == 'FeatureClass':
                                        # Set the coordinate system to NAD 83 for the feature class if not already. Copy or project the feature class into the Master_GDB
                                        coord = arcpy.Describe(fc).spatialReference
                                        
                                        if coord.name == NAD83: # If the feature class is already in NAD83, it is copied into the Master GDB
                                            arcpy.management.CopyFeatures(in_fc, out_fc)
                                        else: # Otherwise the feature class is projected into NAD83 and saved into the Master GDB
                                            arcpy.management.Project(in_fc, out_fc, wkt)

                                    elif arcpy.Describe(fc).dataType == 'Table': # Tables are copied into the Master GDB
                                        arcpy.management.Copy(in_fc, out_fc)
                                except:
                                    print('Error! Unable to move features into the Master GDB for {0} layer for state/territory # {1}. This is due to possible network issues. Please try again later.\n'.format(item, dir_name_number[1:]))
                                    quit()
                            
                    if flag_item == 0: # Prints a message if the right feature class/table is not found for a specific state / territory
                        print('{0} layer not present for state/territory # {1}.\n'.format(item, dir_name_number[1:]))
        
        arcpy.env.workspace = master_gdb    
        for dirpath_master, dirnames_master, fcs_master in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
            for fc_master in fcs_master:
                if fc_master in lst_names:
                    lst_fcs.append(fc_master) # Upload all relevant feature classes/tables into lst_fcs to be combined into 1 national layer
                    data_type = arcpy.Describe(fc_master).dataType

        if len(lst_fcs) == 0: # Prints an error message to alert the user if the program cannot find a certain key for any state/territory
            print('Error! {0} layer not present for any state/territory. Please check that {0} is a valid NFHL feature class/table.\n'.format(item))
            print('*****\n')
        else:
            # Merge the feature classes / tables of the same key together into one national output layer
            name_new = dict_fcs[item]
            merge_output = os.path.join(master_gdb, name_new)
            arcpy.management.Merge(lst_fcs, merge_output)
            names = '\t\n'.join(lst_fcs)
            print(names, '\n')
            print('{0}: {1} features merged together; {2} national {3} layer created.\n'.format(item, len(lst_fcs), name_new, data_type))

            for dirpath_master_final, dirnames_master_final, fcs_master_final in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
                for fc in fcs_master_final:
                    if fc in lst_fcs:
                        arcpy.management.Delete(fc) # Delete the individual feature classes / tables from the Master GDB to leave behind only the national layers
                    else:
                        if fc == name_new:
                            try: # Import the metadata.xml file onto the national feature class/table layer
                                data_type_fc = arcpy.Describe(fc).dataType
                                meta = arcpy.metadata.Metadata(fc)
                                print('Metadata Filepath:', metadata_filepath)
                                meta.importMetadata(metadata_filepath)
                                meta.save()
                                print('Successfully imported metadata for {0} national {1} layer.\n'.format(fc, data_type_fc))                      
                            except:
                                print('Error! Unable to import metadata for {0} national {1} layer. Please manually check metadata file:'.format(fc, data_type_fc))

            print('*****\n')
 
if __name__ == '__main__':
    print("Job starting!", datetime.datetime.now(), "\n")

    unzip_name = r'C:\Users\CaitlinHartig\Documents\NFHL\Data.zip'  # Update me!
    folder = unzip_folder(unzip_name)

    # If updating dict_fcs, all keys (the content to the left of the ':') MUST be written in all uppercase.
    dict_fcs = {'S_FIRM_PAN':'Hydro_NatFloodHaz_Panel_FEMA', 'S_FLD_HAZ_AR':'Hydro_NatFloodHaz_HazArea_FEMA', 'S_BFE':'Hydro_NatFloodHaz_S_BFE_FEMA', 'S_XS':'Hydro_NatFloodHaz_XS_FEMA', 'S_GEN_STRUCT':'Hydro_NatFloodHaz_Struct_FEMA', 'S_LOMR':'Hydro_NatFloodHaz_LOMR_FEMA', 'S_PROFIL_BASLN':'Hydro_NatFloodHaz_PBas_FEMA', 'S_WTR_LN':'Hydro_NatFloodHaz_Wtr_FEMA', 'S_WTR_AR':'Hydro_NatFloodHaz_Wtr_Ar_FEMA', 'L_COMM_INFO':'Hydro_NatFloodHaz_Comm_FEMA', 'STUDY_INFO': 'Hydro_NatFloodHaz_Study_FEMA'}
    master_gdb = r'C:\Users\CaitlinHartig\Documents\Tools\Master_GDB.gdb' # Update me!

    metadata_filepath = obtain_metadata(folder)
    create_national_layer(folder, dict_fcs, master_gdb, metadata_filepath)

    print("\nJob ending!", datetime.datetime.now(), "\n")
