'''
Title: Layer File
Authors: Caitlin Hartig
Date: December 2023

This program copies aprx files from a file directory and then saves the aprx into a different folder.
It then exports the lyrx files from selected aprx in the copied folder and saves them into a specified location.

Libraries Utilized: arcpy, os, datetime, shutil
'''

import arcpy, os, datetime, shutil  

def copy_aprx(origin_location, lst_maps, save_location):
##  Purpose: Copy aprx from a given folder into another folder. Takes a list of aprx names to copy over
##  Input Example: origin_location = r"C:\Users\CaitlinHartig\OneDrive - Home\Pro_Originals"
##                 lst_maps = ['1000', 'Sample States', 'PRO'] # aprx names to copy to new destination
##                 save_location = r"C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx"
##  Output Example: "C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx\Map.aprx"
  for root, dirs, files in os.walk(folder_path):
    if '.backups' not in root:
      for file in files:
        if '.aprx' in file:
          for element in lst_maps:
            if element in file:
              input_location = os.path.join(root, file)
              output_location = os.path.join(lyrx_folder, file)

              if os.path.isfile(output_location): # Removes the aprx that exists so that a new one of the same name can be created
                os.remove(output_location)
                
              shutil.copy(input_location, output_location)

def select_map_and_save_lyrx(folder_path, lst_map_names):
##  Purpose: For each aprx in a given folder, function selects a map name from a map list and saves lyrx for all layers within that map. Calls helper function save_lyrx() to save lyrx for each map
##  Input Example: folder_path = r"C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx"
##                 lst_map_names = ['Map', 'Main Map'] # Map names from which to save lyrx
##  Output Example: "Lyrx1.lyrx", "Lyrx2.lyrx", "Lyrx3.lyrx", etc
    for root, dirs, files in os.walk(lyrx_folder):
      for file in files:
        if '.aprx' in file:
          input_aprx = os.path.join(root, file)
          #print(input_aprx)
          aprx = arcpy.mp.ArcGISProject(input_aprx)
          mxd = aprx.listMaps()

          for item in mxd:
            #print(item.name)
            for lst_map_name in lst_map_names:
              if lst_map_name == item.name:
                map_name = lst_map_name

          #print(map_name)
          aprx_file_path = os.path.join(root, file)
          save_lyrx(input_aprx, lyrx_folder, map_name)

def save_lyrx(aprx_file_path, folder_path, map_name):
##  Purpose: save lyrx files for each layer in an aprx file. If multiple maps of the same name (identical to the provided map_name) are present within an aprx, the first map is selected. 
##  Input Example: aprx_file_path = "C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx\Map.aprx"
##                 folder_path = r"C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx"
##                 map_name = 'Main Map'
##  Output Example: "Lyrx1.lyrx", "Lyrx2.lyrx", "Lyrx3.lyrx", etc

  # Open the MXD file
  aprx = arcpy.mp.ArcGISProject(aprx_file_path)

  head, tail = os.path.split(aprx_file_path)
  aprx_name = tail
  #print(aprx_name)
  
  mxd = aprx.listMaps()

  for item in mxd:
    if item.name == map_name:
      map_index = mxd.index(item)
      #print(map_index)
      break

  mxd = aprx.listMaps()[map_index]
  
  # Save map layers to .lyrx    
  layers = mxd.listLayers()
  for layer in layers:
    #print(layer.name)
    if layer.isRasterLayer:
        feature_layer = os.path.join(lyrx_folder, layer.name)
        feature_layer += '_{0}'.format(aprx_name)
        layer.saveACopy(feature_layer)
    else:
      try:
        renderer = layer.symbology.renderer
      except AttributeError: # Prevents certain lyrx from being exported into the folder
        print("Warning! {0} layer object from {1} has no attribute 'renderer' and cannot saved.".format(layer, aprx_name))
      else:
        feature_layer = os.path.join(lyrx_folder, layer.name)
        feature_layer += '_{0}'.format(aprx_name)
        
        if os.path.isfile(feature_layer): # Removes the lyrx that exists so that a new one of the same name can be created
          os.remove(feature_layer)
          
        layer.saveACopy(feature_layer)

if __name__ == '__main__':
  # Global Environment settings - update me!
  arcpy.env.overwriteOutput = True
  
  print("Job starting!", datetime.datetime.now(), "\n")

  # File paths - update me!
  folder_path = r"C:\Users\CaitlinHartig\OneDrive - Home\Pro_Originals"
  lyrx_folder = r"C:\Users\CaitlinHartig\OneDrive - Home\CopyAprx"

  # Lists
  lst_maps = ['1000', 'Sample States', 'PRO'] # Saves copies of aprx containing '1000', 'Sample States', or 'PRO' in the title
  lst_map_names = ['Map', 'Main Map'] # Map names within the aprx from which to save lyrx
  
  # Save copies of selected maps in folder_path to lyrx_folder.
  copy_aprx(folder_path, lst_maps, lyrx_folder)

  # Save map layers from each aprx copy to .lyrx into lyrx_folder
  select_map_and_save_lyrx(lyrx_folder, lst_map_names)

  print("\n\nJob ending!", datetime.datetime.now(), "\n")
