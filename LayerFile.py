'''
Title: Layer File
Author: Caitlin Hartig
Date: December 2023

This program copies .aprx files from a file directory and then saves the .aprx into a different folder.
It then exports the .lyrx files from selected .aprx in the copied folder and saves them into a specified location.

Libraries Utilized: arcpy, os, datetime, shutil
'''

import arcpy, os, datetime, shutil  

def copy_aprx(origin_location, lst_maps, save_location):
##  Purpose: Copy aprx from a given folder into another folder. Takes a list of aprx names to copy over
##  Input Example: origin_location = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Code\Pro"
##                 lst_maps = ['63,360_FSBaseMap', 'FSTopo_Continental'] # aprx names to copy to new destination
##                 save_location = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\CopyAprx"
##  Output Example: "C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\CopyAprx\FSTopo.aprx"  
  for root, dirs, files in os.walk(origin_location):
    if '.backups' not in root:
      for file in files:
        if '.aprx' in file:
          for element in lst_maps:
            if 'PuertoRico' not in file and 'Old' not in file: # Skipping the Puerto Rico aprx and the Old aprx
              if element.replace(',','') in file:
                input_location = os.path.join(root, file)
                output_location = os.path.join(save_location, file)

                if os.path.isfile(output_location): # Removes the aprx that exists so that a new one of the same name can be created
                  os.remove(output_location)
                  
                shutil.copy(input_location, output_location)

def select_map_and_save_lyrx(folder_path, lst_map_names):
##  Purpose: For each aprx in a given folder, function selects a map name from a map list and saves lyrx for all layers within that map. Calls helper function save_lyrx() to save lyrx for each map
##  Input Example: folder_path = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Layer Files"
##                 lst_map_names = ['FSTopo', 'Main Map'] # map names from which to save lyrx
##  Output Example: "FishnetLines1.lyrx", "FishnetLines2.lyrx", "FishnetLines3.lyrx", etc.
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        if '.aprx' in file:
          input_aprx = os.path.join(root, file)
          aprx = arcpy.mp.ArcGISProject(input_aprx)
          mxd = aprx.listMaps()

          for item in mxd:
            for lst_map_name in lst_map_names:
              if lst_map_name == item.name:
                map_name = lst_map_name

          save_lyrx(input_aprx, map_name, folder_path)

def save_lyrx(aprx_file_path, map_name, folder_path):
##  Purpose: save lyrx files for each layer in an aprx file. If multiple maps of the same name (identical to the provided map_name) are present within an aprx, the first map is selected. 
##  Input Example: aprx_file_path = "C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Projects\FSTopo.aprx"
##                 map_name = 'FSTopo_Continental'
##                 folder_path = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Layer Files"
##  Output Example: "FishnetLines1.lyrx", "FishnetLines2.lyrx", "FishnetLines3.lyrx", etc.

  # Open the MXD file
  aprx = arcpy.mp.ArcGISProject(aprx_file_path)

  head, tail = os.path.split(aprx_file_path)
  aprx_name = tail
  
  mxd = aprx.listMaps()

  for item in mxd:
    if item.name == map_name:
      map_index = mxd.index(item)
      break

  mxd = aprx.listMaps()[map_index]
  
  # Save map layers to .lyrx    
  layers = mxd.listLayers()
  for layer in layers:
    if 'REFERENCE' not in layer.name: # Skipping the REFERENCE layer
      if layer.isRasterLayer:
          feature_layer = os.path.join(folder_path, layer.name)
          feature_layer += '_{0}'.format(aprx_name)
          layer.saveACopy(feature_layer)
      else:
        try:
          renderer = layer.symbology.renderer
        except AttributeError: # A layer must contain a symbology renderer in order to save a lyrx file
          print("Warning! {0} layer object from {1} has no attribute 'renderer' and cannot be saved as a lyrx file.".format(layer, aprx_name))
        else:
          feature_layer = os.path.join(folder_path, layer.name)
          feature_layer += '_{0}'.format(aprx_name)
          
          if os.path.isfile(feature_layer): # Removes the lyrx that exists so that a new one of the same name can be created
            os.remove(feature_layer)

          layer.saveACopy(feature_layer)

def move_files(folder_path_new, folder_path_old):
##  Purpose: move lyrx files into a specific subfolder based on the aprx name 
##  Input Example: folder_path_new = r"C:\Users\CaitlinHartig\Documents\Xentity\Xentity\Code\Style File\Layer Files" - Umbrella folder that holds the subfolders for each map layer
##                 folder_path_old = r'C:\Users\CaitlinHartig\Documents\Xentity\Xentity\Code\Style File\Code\LyrxOutput' - Holding bucket for temporary storage of lyrx before they are distributed into subfolders within the folder_path_new
##  Output Example: "FishnetLines1.lyrx", "FishnetLines2.lyrx", "FishnetLines3.lyrx", etc. saved in either '63,360' or 'FSTopo' sub-folders within lyrx_folder_final
  lst = os.listdir(folder_path_new) # Lists all files and folders in the folder_path_new directory
  new_lst = [] # Contains the list of parsed folder names in the folder_path_new directory, without punctuation
  lst_copy = [] # Contains a copy of the list of parsed folder names in the folder_path_new directory, containing punctuation
  for lst_item in lst:
    if '.' not in lst_item:
      index = lst.index(lst_item)
      lst_copy.append(lst_item)
      lst_item = lst_item.replace(',','') # Removes comma punctuation in the folder name
      new_lst.append(lst_item)

  for root, dirs, files in os.walk(folder_path_old):
    for file in files:
      if '.' in file:
        feature_layer = os.path.join(root, file)
        for lst_item in new_lst:
          if lst_item in file:
            index = new_lst.index(lst_item)
            new_folder_path = os.path.join(folder_path_new, lst_copy[index])

            new_file_path = os.path.join(new_folder_path, file)

            if os.path.isfile(new_file_path): # Removes the file that exists so that a new one of the same name can be created
              os.remove(new_file_path)

            shutil.move(feature_layer, new_folder_path)

if __name__ == '__main__':
  arcpy.env.overwriteOutput = True
  
  print("Job starting!", datetime.datetime.now(), "\n")

  # File paths - update me!
  folder_path = r"C:\Users\CaitlinHartig\Documents\Projects\Style File\Pro" # Folder pathway to the aprx (or multiple aprx) from which you would like to pull styles
  lyrx_folder = r"C:\Users\CaitlinHartig\Documents\Projects\Style File\LyrxOutput" # Temporary holding bucket folder for .lyrx files (does not need to already exist, but needs to be a valid file pathway)
  lyrx_folder_final = r"C:\Users\CaitlinHartig\Documents\Projects\Style File\Layer Files" # Final folder in which to save and store .lyrx files

  # Lists of maps and map names from which you would like to pull styles - update me!
  lst_maps = ['FSTopo_Continental', '63,360_FSBaseMap'] # Saves copies of the following maps: FSTopo_Continental.arpx, 63,360_FSBaseMap.arpx
  lst_map_names = ['FSTopo', 'Main Map'] # Pulls .lyrx from the following map names within the above aprx

  # Creates the temporary holding bucket folder lyrx_folder if it does not already exist
  if not os.path.isdir(lyrx_folder):
    os.mkdir(lyrx_folder)

  
  # Step 1: Save copies of .aprx into a new folder (from folder_path into lyrx_folder)
  copy_aprx(folder_path, lst_maps, lyrx_folder)


  # Step 2: Pull copies of all .lyrx from each .aprx and save into lyrx_folder (temporary save)
  select_map_and_save_lyrx(lyrx_folder, lst_map_names)


  # Step 3: Organize .aprx and .lyrx into folder hierarchy for future use and storage
  
  # Move map layers from temporary holding bucket into corresponding folders for each map name ("63,360", "FSTopo") in lyrx_folder_final
  move_files(lyrx_folder_final, lyrx_folder)

  # Delete the temporary holding bucket folder
  shutil.rmtree(lyrx_folder)

  print("\n\nJob ending!", datetime.datetime.now(), "\n")
