'''
Title: Backup Geodatabase
Authors: Caitlin Hartig, Steve Schultz
Date: 7/20/23

This program creates a function “dataSubmittal()” which pulls data from either a local machine or from an Enterprise geodatabase (GDB).
A new backup folder is created containing new GDBs, new feature datasets (DS), and new feature classes (FC).
A function “remove_field_name(folder)” subsequently removes all fields with a given field name from each FC within a
   given folder. A timestamp is printed for completion of each step in the process.
Helper functions select the most recently modified backup GDB in a given file directory, return the file path of a FC
   within a given GDB, create a new folder, create a new GDB, create a new DS, convert FC to GDB, clip a file, and rename a file.

Libraries Utilized: arcpy, datetime
'''

import arcpy, datetime

'''
Function select_backup returns the most recently modified backup GDB in a given file directory (local machine).
Inputs - initial folder / file directory
Outputs - file pathway to the most recently modified backup GDB
'''
def select_backup(folder):
    
    arcpy.env.workspace = str(folder)

    from pathlib import Path
    import os

    p = Path(arcpy.env.workspace)
    return max(p.glob('*/'), key=os.path.getmtime)

'''
Function fc_filepath returns the file path of a given feature class within a given GDB
Inputs - GDB name, feature class name
Outputs - file pathway to the given feature class within the given GDB
'''
def fc_filepath(GDB_name, in_data):
    
    arcpy.env.workspace = str(GDB_name)
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []

    for ds in datasets:
        feature_classes = arcpy.ListFeatureClasses(feature_dataset=ds)
        feature_classes = [''] + feature_classes if feature_classes is not None else []
        
        for fc in feature_classes:
            if in_data == fc:
                result = str(GDB_name) + "\\" + str(ds) + "\\" + str(fc)
                return result

'''
Function create_folder creates a new folder in a given file directory.
Inputs - existing folder path, name of output folder
Outputs - file path to new output folder
'''
def create_folder(name_folder_path, name_ouput_folder):
    return arcpy.management.CreateFolder(out_folder_path=name_folder_path, out_name=name_ouput_folder)[0]

'''
Function create_file_GDB creates a new geodatabase (GDB) in an existing folder.
Inputs - existing folder, name of GDB
Outputs - file path to new GDB
'''
def create_file_GDB(name_ouput_folder, name_GDB):
    return arcpy.management.CreateFileGDB(out_folder_path=name_ouput_folder, out_name=str(name_GDB), out_version="CURRENT")[0]

'''
Function create_feature_dataset creates a new feature dataset in an existing GDB.
Inputs - existing GDB, name of feature dataset
Outputs - file path to new feature dataset
'''
def create_feature_dataset(name_GDB, output_name):
    return arcpy.management.CreateFeatureDataset(out_dataset_path=name_GDB, out_name=str(output_name), spatial_reference="PROJCS[\"WGS_1984_UTM_Zone_10N\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-123.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")[0]

'''
Function convert_FC_to_GDB creates a new feature class in an existing feature dataset.
Inputs - list of layers to be input into the new feature class, existing feature dataset
Outputs - file path to new feature class
'''
def convert_FC_to_GDB(lst, name_dataset):
    return arcpy.conversion.FeatureClassToGeodatabase(Input_Features=lst, Output_Geodatabase=name_dataset)[0]

'''
Function clip_file clips another layer to the boundaries of another layer.
Inputs - layer to be clipped, boundary layer, name of new clipped file
Outputs - clipped file
'''
def clip_file(clip_layer, clip_boundary_layer, name_feature_class):
    return arcpy.analysis.Clip(in_features=clip_layer, clip_features=clip_boundary_layer, out_feature_class=name_feature_class, cluster_tolerance="")

'''
Function remove_field_name removes all fields with the given field name from each feature class within each GDB, including clipped layers, within a given folder.
Inputs - folder name
Outputs - none
'''
def remove_field_name(folder_name):

    import os

    arcpy.env.workspace = folder_name

    geodatabases = arcpy.ListWorkspaces()

    for geodatabase in geodatabases:

        arcpy.env.workspace = geodatabase
    
        datasets = arcpy.ListDatasets(feature_type='feature')
        datasets = [''] + datasets if datasets is not None else []

        for ds in datasets:
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                path = os.path.join(arcpy.env.workspace, ds, fc)

                for f in arcpy.ListFields(path):
                    field = f.name

                    if field.startswith("LM"):
                        arcpy.DeleteField_management(fc, field)

    print("Field names removed.", datetime.datetime.now(), "\n")

'''
Function Rename changes the name of a datum in a feature class
Inputs - GDB where the fc is contained, input data name to be renamed, output data name
Outputs - the renamed datum
'''
def Rename(GDB_name, in_data, out_data):

    arcpy.env.workspace = GDB_name
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []

    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            if in_data == fc:
                arcpy.env.workspace = str(GDB_name) + "\\" + str(ds) + "\\"

    return arcpy.management.Rename(in_data, out_data)


def dataSubmittal():  # Data Submittal

    # To allow overwriting outputs change overwriteOutput option to True. Set to true so that clipped data may be sent to the project GDB before creation of the destination folders/GDB/FD.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")

    
    # Step 1: Create folders and select backup GDB. Obtain file pathways for feature classes from the selected GDB

    # Starting Folder Filepath -- pulls from a local machine. Can also be utilized to pull from an Enterprise GDB (if pulling from an Enterprise GDB, make sure to delete the "Select Backup GDB" section!)
    folder = "C:\\Backups"

    # Process: Create Folder (Create Folder) (management)
    currentBackup = create_folder(folder, "currentBackup")

    # Process: Create Folder (2) (Create Sub Folder) (management)
    global Backup1
    Backup1 = create_folder(currentBackup, "Backup1")

    #Select Backup GDB. If pulling from an Enterprise GDB, not a local machine, delete only this section!
    folder_GDB = str(folder) + "\\GDBs\\"
    backup_GDB = select_backup(folder_GDB)
    
    # GDB1 Feature Dataset 1 Classes (Feature_Dataset1) = lst_Feature_Dataset1
    Layer1 = fc_filepath(backup_GDB, "Layer1")
    Layer2 = fc_filepath(backup_GDB, "Layer2")
    Layer3 = fc_filepath(backup_GDB, "Layer3")
    Layer4 = fc_filepath(backup_GDB, "Layer4")
    
    # Clip 1
    Layer5 = fc_filepath(backup_GDB, "Layer5")
    Layer_Boundary = fc_filepath(backup_GDB, "Layer_Boundary")
 
    # GDB1 Feature Dataset 2 Classes (Feature_Dataset2) = lst_Feature_Dataset2
    Layer5 = fc_filepath(backup_GDB, "Layer5") # From Clip 1
    Layer6 = fc_filepath(backup_GDB, "Layer6")
    Layer7 = fc_filepath(backup_GDB, "Layer7")
    
    # GDB2 Feature Dataset 1 Classes (Feature_Dataset1) = lst_Feature_Dataset1
    Layer8 = fc_filepath(backup_GDB, "Layer8")
    Layer9 = fc_filepath(backup_GDB, "Layer9")
    
    # Clip 2
    Layer10 = fc_filepath(backup_GDB, "Layer10")
    
    # Clip 3
    Layer11 = fc_filepath(backup_GDB, "Layer11")
    
    # GDB2 Feature Dataset 2 Classes (Feature_Dataset2) = lst_Feature_Dataset2
    Layer10 = fc_filepath(backup_GDB, "Layer10") # From Clip 2
    Layer11 = fc_filepath(backup_GDB, "Layer11") # From Clip 3
    Layer12 = fc_filepath(backup_GDB, "Layer12")
    Layer13 = fc_filepath(backup_GDB, "Layer13")
    Layer14 = fc_filepath(backup_GDB, "Layer14")

    # GDB3 Feature Dataset 1 Classes (Feature_Dataset1) = lst_Feature_Dataset1
    Layer15 = fc_filepath(backup_GDB, "Layer15")
    Layer16 = fc_filepath(backup_GDB, "Layer16")
    Layer17 = fc_filepath(backup_GDB, "Layer17_2022_new")
    Layer18 = fc_filepath(backup_GDB, "Layer18")

    # GDB3 Feature Dataset 2 Classes (Feature_Dataset2) = lst_Feature_Dataset2
    Layer19 = fc_filepath(backup_GDB, "Layer19")
    Layer20 = fc_filepath(backup_GDB, "Layer20")


    # Step 2: Create GDB1 (GDB1) in Backup1 folder, containing Feature Datasets 1 and 2 (Feature_Dataset1 and Feature_Dataset2), containing respectively Feature Classes 1 and 2 out of 6 (GDB1_Feature_Dataset1 and GDB1_Feature_Dataset2)
    
    # Process: Create File Geodatabase (Create File Geodatabase) (management)
    GDB1 = create_file_GDB(Backup1, "GDB1")

    # Process: Create GDB1 Feature Dataset (Create Feature Dataset) (management)
    Feature_Dataset1 = create_feature_dataset(GDB1, "Feature_Dataset1")

    # Process: Feature Class To Geodatabase (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset1 = [Layer1, Layer2, Layer3, Layer4]
    GDB1_Feature_Dataset1 = convert_FC_to_GDB(lst_Feature_Dataset1, Feature_Dataset1)

    print("Feature class to geodatabase # 1 of 6 completed.", datetime.datetime.now())



    # Process: Clip (Clip) (analysis)
    clip_file(Layer5, Layer_Boundary, Layer5)

    # Process: Create GDB1 Feature Dataset (2) (Create Feature Dataset) (management)
    Feature_Dataset2 = create_feature_dataset(GDB1, "Feature_Dataset2")

    # Process: Feature Class To Geodatabase (2) (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset2 = [Layer5, Layer6, Layer7]
    GDB1_Feature_Dataset2 = convert_FC_to_GDB(lst_Feature_Dataset2, Feature_Dataset2)

    print("Feature class to geodatabase #2 of 6 completed.", datetime.datetime.now())
    


    # Step 3: Create GDB2 (GDB2) in Backup1 folder, containing Feature Datasets 1 and 2 (Feature_Dataset1 and Feature_Dataset2), containing respectively Feature Classes 3 and 4 out of 6 (GDB2_Feature_Dataset1 and GDB2_Feature_Dataset2)

    # Process: Create File Geodatabase (2) (Create File Geodatabase) (management)
    GDB2 = create_file_GDB(Backup1, "GDB2")

    # Process: Create GDB2 Feature Dataset (3) (Create Feature Dataset) (management)
    Feature_Dataset1 = create_feature_dataset(GDB2, "Feature_Dataset1")

    # Process: Feature Class To Geodatabase (3) (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset1 = [Layer8, Layer9]
    GDB2_Feature_Dataset1 = convert_FC_to_GDB(lst_Feature_Dataset1, Feature_Dataset1)

    print("Feature class to geodatabase #3 of 6 completed.", datetime.datetime.now())

    
    # Process: Clip (2) (Clip) (analysis)
    clip_file(Layer10, Layer_Boundary, Layer10)

    # Process: Clip (3) (Clip) (analysis)
    clip_file(Layer11, Layer_Boundary, Layer11)


    # Process: Create GDB2 Feature Dataset (4) (Create Feature Dataset) (management)
    Feature_Dataset2 = create_feature_dataset(GDB2, "Feature_Dataset2")

    # Process: Feature Class To Geodatabase (4) (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset2 = [Layer10, Layer11, Layer12, Layer13, Layer14]
    GDB2_Feature_Dataset2 = convert_FC_to_GDB(lst_Feature_Dataset2, Feature_Dataset2)

    print("Feature class to geodatabase #4 of 6 completed.", datetime.datetime.now())
    
    

    # Step 3: Create GDB3 (GDB3) in Backup1 folder, containing Feature Datasets 1 and 2 (Feature_Dataset1 and Feature_Dataset2), containing respectively Feature Classes 5 and 6 out of 6 (GDB3_Feature_Dataset1 and GDB3_Feature_Dataset2)

    # Process: Create File Geodatabase (3) (Create File Geodatabase) (management)
    GDB3 = create_file_GDB(Backup1, "GDB3")

    # Process: Create GDB3 Feature Dataset (5) (Create Feature Dataset) (management)
    Feature_Dataset1 = create_feature_dataset(GDB3, "Feature_Dataset1")

    # Process: Feature Class To Geodatabase (5) (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset1 = [Layer15, Layer16, Layer17, Layer18]
    GDB3_Feature_Dataset1 = convert_FC_to_GDB(lst_Feature_Dataset1, Feature_Dataset1)

    #Rename Layer17 feature class
    Layer17_L = Rename(GDB3, "Layer17_2022_new", "Layer17_L")

    print("Feature class to geodatabase #5 of 6 completed.", datetime.datetime.now())


    # Process: Create GDB3 Feature Dataset (6) (Create Feature Dataset) (management)
    Feature_Dataset2 = create_feature_dataset(GDB3, "Feature_Dataset2")

    # Process: Feature Class To Geodatabase (6) (Feature Class To Geodatabase) (conversion)
    lst_Feature_Dataset2 = [Layer19, Layer20]
    GDB3_Feature_Dataset2 = convert_FC_to_GDB(lst_Feature_Dataset2, Feature_Dataset2)

    print("Feature class to geodatabase #6 of 6 completed.\n", datetime.datetime.now())
    
    
if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Projects.gdb", workspace=r"C:\Projects.gdb"):

        print("Job starting!", datetime.datetime.now(), "\n")

        dataSubmittal()

        # Remove field names from within the Backup1 folder
        remove_field_name(Backup1)
        
        print("Job ending!", datetime.datetime.now(), "\n")
