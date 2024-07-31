'''
Title: Style File
Author: Caitlin Hartig
Date: July 2024

This program creates a new custom style file (.stylx) from scratch, utilizing symbology from map layers (.lyrx) from a map document (.aprx).
First, this program copies .aprx files from a file directory and then saves the .aprx into a different folder.
It then exports the .lyrx files from the .aprx in the copied folder and saves them into a specified location.
From there, the program extracts style information (JSON format) from each .lyrx file and uploads that style information into a new style file.
Presentation titled “Style File Automation Using ArcGIS Pro, Python, and SQL” at ESRI User Conference, July 2024.

For more information, please see:
-ReadMe_StyleFile.txt
-1248 - Style File Automation Using ArcGIS Pro, Python, and SQL.pptx

Libraries Utilized: arcpy, sqlite3, os, datetime, shutil
'''

import arcpy, sqlite3, os, datetime, shutil

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
            
def get_all_lyrx_in_dir(in_dir):
##    Purpose: obtain file pathways to all .lyrx contained in the folder.
##      Only returns the file, not the root + file, due to potential spacing issue in the in_dir:
##      C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Layer Files
##      The spaces in the root cause errors in program processing if the root is also returned for each file.
##    
##    Input Example: in_dir = "C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Style File\Layer Files"
##    Output Example: "FishnetLines.lyrx" (a lyrx that is saved within the in_dir)
  
  output = []

  for root, dirs, files in os.walk(in_dir):
    for file in files: # for each .lyrx
      output.append(file)

  return output

def add_label(lst_maps, lyrx, symbol_type, content_string, value_string, flag_label):
##  Purpose: Adds a label for each map layer / sublayer present in each lyrx. The default is to grab the sublayer name to label each content string.
##          -If the map layer contains no sublayer name, the umbrella name for the map layer is added.
##          -Also tacks on the layer umbrella name for sublayers with sublayer name "<all other values>", for clarity in analyzing results, particularly with sublayers that have identical sublabels but differing content.
##          -Tacks on the aprx name to the end of the label, for clarity in analyzing results, particularly with sublayers that have identical sublabels but differing content.
##          flag_label is a boolean which tracks whether or not a map layer has multiple sublayers. The purpose of including flag_label is to utilize and update the variable from both within the main script and this function.
##          value_string is added in the event that some sublayers contain labels while others do not. value_string therefore represents the end of the current sublayer / beginning of the next sublayer.
##  Input Example:
##          -lst_maps = ['FSTopo_Continental', '63,360_FSBaseMap']
##          -lyrx = 'Airfield FAA_63360_FSBaseMap.lyrx'
##          -symbol_type = 'Unique'
##          -content_string (unformatted and with spaces) = '{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Butt","joinStyle":"Miter","lineStyle3D":"Strip","miterLimit":4,"width":0.40000000000000002,"height3D":1,"anchor3D":"Center","color":{"type":"CIMRGBColor","values":[110,110,110,100]}}],"angleAlignment":"Map"}'
##          -value_string = '"symbol" : {'
##          -flag_label = 0
##  Output Example: ("<all other values>_Airfield FAA_63360_FSBaseMap", 1)
##                  A tuple is returned with content_string (the sublayer name label) and flag_label.

  index = -600

  for map_name in lst_maps:
    map_name = map_name.replace(',','')
    if map_name in lyrx:
      index = lyrx.rfind(map_name)

  if index == -600:
    print('Error! {0} does not contain map name in {1}.'.format(lyrx, lst_maps))
    quit()
    
  else:
    aprx_name = lyrx[index - 1:-5]

    lst_symbols = ['Graduated', 'Point Line Polygon Dictionary', 'Raster Classify', 'Raster Unique']

    if symbol_type == 'Unique': # Unique Values
      if '"defaultLabel" : "' in content_string:
        start_string = '"defaultLabel" : "'
        start_index = content_string.index(start_string)
        if start_index < content_string.index(value_string):
          start = start_index + len(start_string)
          content_string = content_string[start:]

          end_string = '",'
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]

          if '<all other values>' or '<null>' in content_string:
            content_string += '_' + lyrx[:-5]
          else:
            content_string += aprx_name
        else:
          content_string = lyrx[:-5]
          
      elif '"label" : "' in content_string:
        start_string = '"label" : "'
        start_index = content_string.index(start_string)
        if start_index < content_string.index(value_string):
          start = start_index + len(start_string)
          content_string = content_string[start:]

          end_string = '",'
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]
          content_string += aprx_name
        else:
          content_string = lyrx[:-5]
          
      else:
        flag_label = 1
        content_string = lyrx[:-5]

    elif symbol_type == 'Proportional': # Proportional Symbol
      if '"size" : ' in content_string:
        value_string = value_string # Not used
        
        start_string = '"size" : '
        start_index = content_string.index(start_string)
        start = start_index + len(start_string)
        content_string = content_string[start:]

        end_string = ','
        end_index = content_string.find(end_string)
        content_string = content_string[:end_index]
        content_string += aprx_name

      else:
        flag_label = 1
        content_string = lyrx[:-5]

    elif symbol_type in lst_symbols: # Graduated Color, Graduated Symbol, Point / Line / Polygon / Dictionary, Raster Classify, and Raster Unique
      if '"label" : "' in content_string:
        start_string = '"label" : "'
        start_index = content_string.index(start_string)
        if start_index < content_string.index(value_string):
          start = start_index + len(start_string)
          content_string = content_string[start:]

          end_string = '",'
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]
          content_string += aprx_name
        else:
          content_string = lyrx[:-5]
        
      elif '"defaultLabel" : "' in content_string:
        start_string = '"defaultLabel" : "'
        start_index = content_string.index(start_string)
        if start_index < content_string.index(value_string):
          start = start_index + len(start_string)
          content_string = content_string[start:]

          end_string = '",'
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]

          if '<all other values>' or '<null>' in content_string:
            content_string += '_' + lyrx[:-5]
          else:
            content_string += aprx_name
        else:
          content_string = lyrx[:-5]
             
      else:
        flag_label = 1
        content_string = lyrx[:-5]

    elif symbol_type == 'Raster ColorMap': # Raster ColorMap
      start_string = '"'
      if start_string in content_string:
        start_index = content_string.find(start_string) + len(start_string)
        content_string = content_string[start_index:]
        
        if value_string in content_string:
          end_string = value_string
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]
        else:
          end_string = start_string
          end_index = content_string.find(end_string)
          content_string = content_string[:end_index]

        if content_string == '':
          content_string = lyrx[:-5]
      else:
        content_string = lyrx[:-5]
          
    else: # Bivariate, Unclassed, and Raster
      content_string = lyrx[:-5]
      
  return content_string, flag_label

def parse_string(content_string):
##  Purpose: Each content string obtained from the lyrx file needs to be parsed so that it will become a functional JSON string.
##    This function removes spaces and newlines that were present in the content string (part or all of a lyrx file), as well as adds spaces back into the font name and the url name if applicable.
##  Input Example: content_string (unformatted and with spaces) = "{"type":"CIMPointSymbol","symbolLayers":[{"type":"CIMCharacterMarker","enable":true,"colorLocked":true,"anchorPoint":{"x":0,"y":0},"anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":16,"billboardMode3D":"FaceNearPlane","characterIndex":40,"fontFamilyName":"ESRIDefaultMarker","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMRGBColor","values":[0,0,0,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true},{"type":"CIMCharacterMarker","enable":true,"anchorPoint":{"x":-1,"y":0},"anchorPointUnits":"Absolute","dominantSizeAxis3D":"Y","size":12.280000000000001,"billboardMode3D":"FaceNearPlane","characterIndex":94,"fontFamilyName":"USDAFS3","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMCMYKColor","values":[0,0,0,100,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true},{"type":"CIMCharacterMarker","enable":true,"anchorPoint":{"x":0,"y":0},"anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":18,"billboardMode3D":"FaceNearPlane","characterIndex":33,"fontFamilyName":"ESRIDefaultMarker","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMRGBColor","values":[255,255,255,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true}],"haloSize":1,"scaleX":1,"angleAlignment":"Map"}"
##  Output Example: symbology_json (content_string formatted; only contains spaces in the font name and url name if applicable) = "{"type":"CIMPointSymbol","symbolLayers":[{"type":"CIMCharacterMarker","enable":true,"colorLocked":true,"anchorPoint":{"x":0,"y":0},"anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":16,"billboardMode3D":"FaceNearPlane","characterIndex":40,"fontFamilyName":"ESRI Default Marker","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMRGBColor","values":[0,0,0,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true},{"type":"CIMCharacterMarker","enable":true,"anchorPoint":{"x":-1,"y":0},"anchorPointUnits":"Absolute","dominantSizeAxis3D":"Y","size":12.280000000000001,"billboardMode3D":"FaceNearPlane","characterIndex":94,"fontFamilyName":"USDAFS3","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMCMYKColor","values":[0,0,0,100,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true},{"type":"CIMCharacterMarker","enable":true,"anchorPoint":{"x":0,"y":0},"anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":18,"billboardMode3D":"FaceNearPlane","characterIndex":33,"fontFamilyName":"ESRI Default Marker","fontStyleName":"Regular","fontType":"Unspecified","scaleX":1,"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMRGBColor","values":[255,255,255,100]}}],"angleAlignment":"Map"},"scaleSymbolsProportionally":true,"respectFrame":true}],"haloSize":1,"scaleX":1,"angleAlignment":"Map"}"
  lst = []
  for line in content_string:
    lst.append(line)

  new_lst = []
  for element in lst:
    if element != ' ' and element != '\n':
      new_lst.append(element)

  symbology_json = ""
  symbology_json = symbology_json.join(new_lst)
  if symbology_json[-1:] == ',':
    symbology_json = symbology_json[:-1]    

  # Add spaces back into the font name if applicable
  font_string = '"fontFamilyName" : "'
  flag_font = 0
  while flag_font == 0:
    if font_string not in content_string:
      flag_font = 1
    else:
      start_index = content_string.index(font_string)
      start = start_index + len(font_string) - 1
      font_contents = content_string[start:]
      content_string = font_contents
      end_string = '",'
      end_index = font_contents.index(end_string) + 1
      font_contents = font_contents[:end_index]

      font_json = font_contents.replace(' ', '')
      symbology_json = symbology_json.replace(font_json, font_contents)

  # Add spaces back into the URL name if applicable
  url_string = '"url" : "'
  flag_url = 0
  while flag_url == 0:
    if url_string not in content_string:
      flag_url = 1
    else:
      start_index = content_string.index(url_string)
      start = start_index + len(url_string)
      url_contents = content_string[start:]
      content_string = url_contents
      end_string = '"'
      end_index = url_contents.index(end_string)
      url_contents = url_contents[:end_index]

      url_json = url_contents.replace(' ', '')
      symbology_json = symbology_json.replace(url_json, url_contents)

  return symbology_json

def create_sym_name_lst(flag_multi, symbology_json, flag_multi_raster, flag_background, background_contents):
##  Purpose: This function determines the correct location to split the JSON string, if there are multiple sublayers per lyrx.
##           A list, sym_name_lst, is returned with the symbology_json string separated into distinct styles for each sublayer, to upload separately into the style file.
##           The background contents, if applicable, are also appended to the sym_name_lst as the last step. This is so that the background label can be applied to the correct sublayer.
##  Input Example: -flag_multi = 1
##                 -symbology_json = '{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Round","joinStyle":"Round","lineStyle3D":"Strip","miterLimit":10,"width":0.40000000000000002,"height3D":1,"anchor3D":"Center","color":{"type":"CIMHSVColor","values":[240,0,57,100]}}],"angleAlignment":"Map"}{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Round","joinStyle":"Round","lineStyle3D":"Strip","miterLimit":10,"width":0.40000000000000002,"height3D":1,"anchor3D":"Center","color":{"type":"CIMCMYKColor","values":[100,41,0,0,100]}}],"angleAlignment":"Map"}'
##                 -flag_multi_raster = 0
##                 -flag_background = 0
##                 -background_contents = ''
##  Output Example: sym_name_lst = ['{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Round","joinStyle":"Round","lineStyle3D":"Strip","miterLimit":10,"width":0.40000000000000002,"height3D":1,"anchor3D":"Center","color":{"type":"CIMHSVColor","values":[240,0,57,100]}}],"angleAlignment":"Map"}', '{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Round","joinStyle":"Round","lineStyle3D":"Strip","miterLimit":10,"width":0.40000000000000002,"height3D":1,"anchor3D":"Center","color":{"type":"CIMCMYKColor","values":[100,41,0,0,100]}}],"angleAlignment":"Map"}']
  sym_name_lst = []              

  if flag_multi == 1:
    point = '{"type":"CIMPointSymbol"'
    line = '{"type":"CIMLineSymbol"'
    polygon = '{"type":"CIMPolygonSymbol"'
    middle = ',"symbol":'

    if point in symbology_json:
      if symbology_json.index(point) == 0:
        symbology_json = symbology_json.replace('{"type":"CIMPointSymbol"', '****{"type":"CIMPointSymbol"')

    if line in symbology_json:
      if symbology_json.index(line) == 0:
        symbology_json = symbology_json.replace('{"type":"CIMLineSymbol"', '****{"type":"CIMLineSymbol"')

    if polygon in symbology_json:
      if symbology_json.index(polygon) == 0:
        symbology_json = symbology_json.replace('{"type":"CIMPolygonSymbol"', '****{"type":"CIMPolygonSymbol"')
        
    if ',"symbol":****' in symbology_json:
      symbology_json = symbology_json.replace(',"symbol":****', middle)

    sym_name_lst = symbology_json.split('****')
    if sym_name_lst[0] == '':
      del sym_name_lst[0]

  elif flag_multi_raster == 1:
    symbology_json = symbology_json.replace('{"type":', '****{"type":')
    sym_name_lst = symbology_json.split('****')
    if sym_name_lst[0] == '':
      del sym_name_lst[0]          
      
  else:
    sym_name_lst.append(symbology_json)
    
  if flag_background == 1:
    sym_name_lst.append(background_contents)

  return sym_name_lst

def get_new_content(new_item):
##  Purpose: For color styles, saves the outline color, fill color, and and/or picture fill color if present.
##          -new_item is the JSON string
##  Input Example: new_item = "{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMVectorMarker","enable":true,"name":"Level_47","anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":1,"billboardMode3D":"FaceNearPlane","markerPlacement":{"type":"CIMMarkerPlacementInsidePolygon","gridType":"Random","randomness":100,"seed":13,"stepX":1.5,"stepY":1.5,"clipping":"ClipAtBoundary"},"frame":{"xmin":-4.8399999999999999,"ymin":-4.8399999999999999,"xmax":4.8399999999999999,"ymax":4.8399999999999999},"markerGraphics":[{"type":"CIMMarkerGraphic","geometry":{"x":0,"y":0},"symbol":{"type":"CIMPointSymbol","symbolLayers":[{"type":"CIMVectorMarker","enable":true,"anchorPoint":{"x":4.6891343603761019e-06,"y":4.7063696006451513e-06,"z":0},"anchorPointUnits":"Relative","dominantSizeAxis3D":"Y","size":7,"billboardMode3D":"FaceNearPlane","frame":{"xmin":0,"ymin":0,"xmax":17,"ymax":17},"markerGraphics":[{"type":"CIMMarkerGraphic","geometry":{"curveRings":[[[8.4000000000000004,0.28000000000000003],{"c":[[10.33,0.94999999999999996],[9.4085666286281295,0.48950209962344982]]},{"c":[[12,2.5699999999999998],[11.2905707812443747,1.6305535773591937]]},{"a":[[13.9,1.8999999999999999],[13.98,5.1600000000000001],1,0,1.5707963267948966,3.2609828262898262,0.99929813358716424]},{"c":[[16,3],[15.0911211473561035,2.1805869005019844]]},{"c":[[16.7199999999999989,5.2999999999999998],[16.5410427285346842,4.0933257545456634]]},{"a":[[16.3500000000000014,7],[13.32,5.4500000000000002],1,0,1.5707963267948966,3.4039496298062444,0.9998109064915669]},{"c":[[14.98,8.0899999999999999],[15.7578553713744292,7.6617081273238217]]},{"c":[[16.6499999999999986,10.9499999999999993],[16.1519124614968277,9.3232713948602441]]},{"a":[[16.1499999999999986,12.3800000000000008],[13.66,10.7100000000000009],1,0,0,2.9996472247701766,0.99841114653145224]},{"a":[[15.15,13.52],[13.81,11.34],1,0,0,2.5612322770382128,0.99874921777190973]},[14.15,13.81],[13.8800000000000008,13.81],[12.9600000000000009,13.81],{"c":[[12.2200000000000006,15.81],[12.72941453930526,14.8615833795429459]]},{"c":[[10.41,16.7199999999999989],[11.4285008537223316,16.4907544453158472]]},{"c":[[7.9000000000000004,15.3800000000000008],[9.0106665495228633,16.3203559408191161]]},[7.4500000000000002,14.8699999999999992],[7.1200000000000001,14.48],{"a":[[5.1900000000000004,15.58],[5.0700000000000003,13.1199999999999992],1,0,1.5707963267948966,2.462934792590965,0.99834465561953767]},{"c":[[3.2599999999999998,14.2200000000000006],[3.9916439357889621,15.2311597087700772]]},[2.8500000000000001,12.48],[2.8500000000000001,12.31],[2.0699999999999998,12.41],{"b":[[0.28000000000000003,10.93],[0.88,12.41],[0.28000000000000003,11.91]]},{"c":[[0.84999999999999998,9.5],[0.45891613306696133,10.1727148222714447]]},[1.8100000000000001,8.2599999999999998],{"c":[[0.70999999999999996,6.8099999999999996],[1.1890865988076249,7.5887963733183526]]},{"a":[[0.29999999999999999,5.1900000000000004],[4.0300000000000002,5.1100000000000003],1,0,0,3.7308598625773386,0.99880572172255633]},{"c":[[1.23,3.0699999999999998],[0.531135289873506,4.0274084054633779]]},{"a":[[3.5600000000000001,2.21],[3.4700000000000002,5.5599999999999996],1,0,1.5707963267948966,3.3512118492224716,0.99871492771927439]},[4.5599999999999996,2.5],[4.8600000000000003,2.73],[5.3700000000000001,3.1899999999999999],[5.5599999999999996,3.3799999999999999],{"c":[[6.4900000000000002,1.21],[5.8789648073350778,2.2324134888578921]]},{"a":[[8.4000000000000004,0.28000000000000003],[8.4000000000000004,2.7000000000000002],1,0,0,2.4239233384280405,0.99838140985490698]}]]},"symbol":{"type":"CIMPolygonSymbol","symbolLayers":[{"type":"CIMSolidStroke","enable":true,"capStyle":"Round","joinStyle":"Round","lineStyle3D":"Strip","miterLimit":10,"width":0,"height3D":1,"anchor3D":"Center","color":{"type":"CIMRGBColor","values":[51,51,51,100]}},{"type":"CIMSolidFill","enable":true,"color":{"type":"CIMCMYKColor","values":[100,45,0,0,100]}}],"angleAlignment":"Map"}}],"scaleSymbolsProportionally":true,"respectFrame":true,"clippingPath":{"type":"CIMClippingPath","clippingType":"Intersect","path":{"rings":[[[0,0],[17,0],[17,17],[0,17],[0,0]]]}}}],"haloSize":0,"scaleX":1,"angleAlignment":"Display"}}],"scaleSymbolsProportionally":true,"respectFrame":true}],"angleAlignment":"Map"}"
##  Output Example: new_content_colors = [{"type":"CIMCMYKColor","values":[100,45,0,0,100]}, {"type":"CIMRGBColor","values":[51,51,51,100]}] # A list containing content strings for both Rapids_63360_FSBaseMap_SolidFill and Rapids_63360_FSBaseMap_SolidStroke
##                  label_types = ['SolidFill', 'SolidStroke'] # A list containing labels for the corresponding content strings as outline color, fill color, or picture fill color as applicable
  # Lists
  new_content_colors = [] # Holds the content strings for each color string
  label_types = [] # Holds the corresponding labels for each content string in new_content_colors
  lst_colors = ['{"type":"CIMPictureFill"', '{"type":"CIMSolidFill"', '{"type":"CIMSolidStroke"']
  
  for value_string in lst_colors: # Saves both the fill color and the outline color into the style file, as well as picture fill color, if applicable
    if value_string in new_item:
      start_index = new_item.index(value_string)
      label_type = new_item[start_index:]
      start_string = '{"type":"CIM'
      start_index = label_type.index(start_string)
      start = start_index + len(start_string)
      label_type = label_type[start:]
      end_string = '"'
      end_index = label_type.index(end_string)
      label_type = label_type[:end_index]
      label_types.append(label_type)

      new_item_copy = new_item
      start_index = new_item_copy.index(value_string)
      new_item_copy = new_item_copy[start_index:]

      if value_string == lst_colors[0]:
        value_string = '"newColor":{'
      else:
        value_string = '"color":{'

      start_index = new_item_copy.index(value_string)
      start = start_index + len(value_string) - 1 #Starting point of the JSON string
      new_item_copy = new_item_copy[start:]
      end_string = '}' #Ending point of the JSON string
      end_index = new_item_copy.index(end_string) + 1
      new_item_copy = new_item_copy[:end_index]

      new_content_colors.append(new_item_copy)

  return new_content_colors, label_types

def add_tags(content_string):
##    Purpose: Creates custom tags for each style (excluding color schemes). Saves the color mode and the color levels into the style file as unique style tags.
##              Works for color, point, line, and polygon class types.
##    Input Example: content_string = '{"type":"CIMHSVColor","values":[240,0,57,100]}'
##    Output Example: tag_name = "HSV;[240,0,57,100]"
  tag_name = ''
  value_string = '{"type":"CIM'
  start_string = content_string.index(value_string)
  start = start_string + len(value_string)
  tag_color_name = content_string[start:]
  value_string = 'Color"'
  end_string = tag_color_name.index(value_string)
  tag_color_name = tag_color_name[:end_string]
  tag_name += tag_color_name + ';'

  value_string = '['
  start_string = content_string.index(value_string)
  tag_color_code = content_string[start_string:]
  value_string = ']'
  end_string = tag_color_code.index(value_string)
  tag_color_code = tag_color_code[:end_string + 1]
  tag_name += tag_color_code
  
  return tag_name

def add_tags_color_scheme(content_string):
##    Purpose: Creates custom tags for each style (for color schemes only). Saves the color scheme type as a unique style tag.
##    Input Example: content_string = '{"type":"CIMMultipartColorRamp","colorRamps":[{"type":"CIMPolarContinuousColorRamp","fromColor":{"type":"CIMHSVColor","values":[270,0,100,100]},"toColor":{"type":"CIMHSVColor","values":[270,100,100,100]},"interpolationSpace":"HSV","polarDirection":"Counterclockwise"},{"type":"CIMFixedColorRamp","colors":[{"type":"CIMRGBColor","values":[166,38,57,100]},{"type":"CIMRGBColor","values":[71,121,152,100]},{"type":"CIMRGBColor","values":[255,196,130,100]},{"type":"CIMRGBColor","values":[196,144,209,100]},{"type":"CIMRGBColor","values":[182,238,166,100]}],"arrangement":"Default"},{"type":"CIMPolarContinuousColorRamp","fromColor":{"type":"CIMHSVColor","values":[270,0,100,100]},"toColor":{"type":"CIMHSVColor","values":[270,100,100,100]},"interpolationSpace":"HSV","polarDirection":"Counterclockwise"}],"weights":[1,1,1]}'
##    Output Example: tag_name = "Multipart"
  tag_name = ''
  value_string = '{"type":"CIM'
  start_string = content_string.index(value_string)
  start = start_string + len(value_string)
  tag_color_name = content_string[start:]
  value_string = 'ColorRamp'
  end_string = tag_color_name.index(value_string)
  tag_name = tag_color_name[:end_string]

  return tag_name

if __name__ == '__main__':
  arcpy.env.overwriteOutput = True
  
  print("Job starting!", datetime.datetime.now(), "\n")

  # File paths - update me!
  folder_path = r"T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\APRX\Pro" # Folder pathway to the aprx (or multiple aprx) from which you would like to pull styles
  lyrx_folder = r"T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Export_Tool\LyrxOutput" # Temporary holding bucket folder for .lyrx files (does not need to already exist, but needs to be a valid file pathway)
  lyrx_folder_final = r"T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\LayerFiles" # Final folder in which to save and store .lyrx files
  style_file_folder = r"T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Style Files" # Folder in which to save and store the .stylx file created in this script

  # Style file base name (script later tacks on the date as well) - update me!
  style_name = "FSBasemapStyle"

  # Lists of maps and map names from which you would like to pull styles - update me!
  lst_maps = ['FSTopo_Continental', '63,360_FSBaseMap'] # Saves copies of the following maps: FSTopo_Continental.arpx, 63,360_FSBaseMap.arpx
  lst_map_names = ['FSTopo', 'Main Map'] # Pulls .lyrx from the following map names within the above aprx

  # Other Lists
  sql_lst = [] # Holds styles and colors in this batch that have already been saved into the style file

  # Creates the temporary holding bucket folder lyrx_folder if it does not already exist
  if not os.path.isdir(lyrx_folder):
    os.mkdir(lyrx_folder)
    
  # Dictionaries
  class_dict = {1:'Color', 2:'Color Scheme', 3:'Point Symbol', 4:'Line Symbol', 5:'Polygon Symbol', 6:'Text Symbol', 7:'North Arrow', 8:'Scale Bar', 9:'Standard Label Placement', 10:'Maplex Label Placement',
                11:'Grid', 12:'Mesh Symbol', 13:'Legend', 14:'Table Frame', 15:'Map Surround', 17:'Legend Item', 18:'Table Frame Field'}
  
  meta_dict = {'version':'1.0', 'cim_version':'3.1.0', 'build':'41833', 'content':'json', 'colorModel':'RGB', 'RGBColorProfile':'sRGB IEC61966-2.1', 'CMYKColorProfile':'U.S. Web Coated (SWOP) v2'}


  # Step 1: Save copies of .aprx into a new folder (from folder_path into lyrx_folder)
  copy_aprx(folder_path, lst_maps, lyrx_folder)


  # Step 2: Pull copies of all .lyrx from each .aprx and save into lyrx_folder (temporary save)
  select_map_and_save_lyrx(lyrx_folder, lst_map_names)


  # Step 3: Create a new .stylx using the sqlite3 library
  
  # 3a. Create the style file name
  date = datetime.date.today()
  date = str(date).replace('-', '')

  style_file  = os.path.join(style_file_folder, "{0}_{1}.stylx".format(date, style_name)) #yyyymmdd_StyleName.stylx

  # 3b. Removes the style file that exists so that a new one of the same name can be created
  if os.path.isfile(style_file): 
    os.remove(style_file)

  # 3c. Set up the SQLite database connection
  conn = sqlite3.connect(style_file)
  cursor = conn.cursor()


  # Step 4: Insert new styles into the new .stylx using the sqlite3 library
  
  # 4a i. Create the BINARIES table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS BINARIES (ID, MD5, CLASS, CONTENT)')

  # 4a ii. Create the BINARY_CLASSES table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS BINARY_CLASSES (ID, NAME)')

  ID_binary_classes = 1
  name_binary_classes = 'GLB'

  row_binary_classes = (ID_binary_classes, name_binary_classes)
  cursor.execute('INSERT INTO BINARY_CLASSES(ID, NAME) VALUES(?,?)', row_binary_classes)

  # 4a iii. Create the CLASSES table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS CLASSES (ID, NAME)')

  lst_classes = class_dict.items()
  for element in lst_classes:
    row_classes = element      
    cursor.execute('INSERT INTO CLASSES(ID, NAME) VALUES(?,?)', row_classes)

  # 4b. Create the ITEMS table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS ITEMS (ID INTEGER PRIMARY KEY, CLASS INTEGER, CATEGORY TEXT, NAME TEXT, TAGS TEXT, CONTENT TEXT, KEY TEXT)')

  # 4b i. Go through each .lyrx saved in the folder and pull the JSON string
  lst_lyrx = get_all_lyrx_in_dir(lyrx_folder)
  
  if lst_lyrx == []:
    print("Error! Lyrx folder directory is empty.")
    quit()

  flag_lyrx = 0
  count = 1

  for lyrx in lst_lyrx:
    if ".lyrx" in lyrx:
      flag_lyrx = 1
      print(f"\nCurrently processing: {lyrx}")

      lyrx_file = os.path.join(lyrx_folder, lyrx) # Obtain the JSON string from the .lyrx file
      infile = open(lyrx_file, 'r')

      try:
        file_contents = infile.read()
      except UnicodeDecodeError: # Unicode error is produced when trying to read some lyrx
        print("Warning! Error reading {0} and therefore cannot add it into the style file.".format(lyrx))
      else:
        # Flags
        flag_is_vector = 0 # Determines if a style is a vector (for the purpose of saving both the fill color and outline color into the style file if present)
        flag_vector = 0 # Filters out vector symbology that cannot be added to the style file at this time (dot density, chart)
        flag_proportional = 0 # Determines if a vector symbology layer is a proportional symbol. Necessary because this distinction occurs earlier in the code than "symbol", as is the cutoff for other symbol types
        flag_multi = 0 # Used for unique values and graduated colors to add all sublayers
        flag_multi_raster = 0 # Used for rasters to add all sublayers
        flag_raster = 0 # Filters out raster symbology that cannot be added to the style file at this time (vector field)
        flag_unique = 0 # Determines if a vector symbology layer is unique values. Necessary because sometimes this distinction occurs earlier in the code than "symbol", as is the cutoff for other symbol types
        flag_only_default = 0 # Determines whether or not only the default value is used for unique values
        flag_default_plus = 0 # Determines whether or not the default value is used as well as other values for unique values
        flag_background = 0 # Determines whether or not a style has a separate background color (applies to proportional symbol and graduated symbol styles)
        flag_label = 0 # Determines whether or not a style has sublabels
        symbol_type = '' # Used to assign proper labelling based on the symbol type

        # Lists
        name_labels = [] # Stores the names of each sub layer within each lyrx

        # Vectors
        if "renderer" in file_contents:
          flag_is_vector = 1

          start_string = '"renderer" : {'
          start_index = file_contents.index(start_string) + len(start_string) + 1

          # Dot density lyrx does not follow the same protocol; it does not go in order and contains elements that are not listed inside the JSON string
          if '"CIMDotDensityRenderer"' in file_contents:
            print("Error! Dot density symbology cannot be added to style file at this time.")
            flag_vector = 1
            del file_contents
            
          # Chart lyrx does not follow the same protocol; it is in order, but contains elements that are not listed inside the JSON string
          elif '"CIMChartRenderer"' in file_contents:
            print("Error! Chart symbology cannot be added to style file at this time.")
            flag_vector = 1
            del file_contents

          # Bivariate Colors
          elif '"arrangement" : "Bivariate"' in file_contents:
            flag_is_vector = 0
            symbol_type = 'Bivariate'
            new_contents = ''

            start_string = '"renderer" : {'
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]
            label_contents = file_contents
            start_string = '"colorRamp" : {'
            start_index = file_contents.index(start_string)
            start = start_index + len(start_string) - 1 # Starting point of the JSON string
            mid_contents = file_contents[start:]

            mid_index = mid_contents.index('"arrangement" : "Bivariate"')
            end_contents = mid_contents[mid_index:]
            end_string = '},'
            end_index = end_contents.index(end_string)
            end = mid_index + (end_index + 1) # Ending point of the JSON string
            value_contents = mid_contents[:end]
            
            new_contents = value_contents
            value_string = '"arrangement" : "Bivariate"'

            label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, label_contents, value_string, flag_label)

            name_labels.append(label_contents)
              
            del mid_contents
              
          else: # Works for Simple Renderer (point, line, polygon, and dictionary symbology). Also is the starting point for other vector symbology types

            # Determine the symbol type
            if '"type" : "CIMProportionalRenderer"' in file_contents: # Proportional Symbols
              flag_proportional = 1
              symbol_type = 'Proportional'
            elif '"type" : "CIMUniqueValueRenderer"' in file_contents: # Unique Values
              flag_unique = 1
              symbol_type = 'Unique'
            elif '"type" : "CIMClassBreak"' in file_contents: # Graduated Colors, Graduated Symbols
              symbol_type = 'Graduated'
            elif '"type" : "CIMSimpleRenderer"' in file_contents: # Point, Line, Polygon, Dictionary
              symbol_type = 'Point Line Polygon Dictionary'

            # Restrict the JSON string to start after '"renderer" : {'
            start_string = '"renderer" : {'
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]
            file_contents_only_default = file_contents

            label_contents = file_contents
            value_string = '"scaleSymbols"'

            label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, label_contents, value_string, flag_label) # Proportional Symbols and Point, Line, Polygon, Dictionary, as well as starting points for Unique Values and Graduated Colors/Symbols (because the label comes before the beginning of the first symbol)

            name_labels.append(label_contents)

            # If it exists, capture the background symbol JSON string (proportional symbol and graduated symbol styles)
            if '"backgroundSymbol" : {' in file_contents:
              flag_background = 1
              
              start_string = '"backgroundSymbol" : {'
              start_index = file_contents.index(start_string) + len(start_string) + 1
              background_contents = file_contents[start_index:]
              start_string = '"symbol" : {'
              start_index = background_contents.index(start_string)
              start = start_index + len(start_string) - 1 # Starting point of the JSON string - background symbol
              background_contents = background_contents[start:]

              if '"angleAlignment" : ' in background_contents:
                end_string = '"angleAlignment" : '
              else:
                end_string = ']'                  
              end_index = background_contents.find(end_string)
              true_end = '}'
              index = background_contents.find(true_end, end_index)
              background_contents = background_contents[:index + 1]

              file_contents = file_contents[index + 1:]
            
            start_string = '"type" : "CIMSymbolReference"'
            start_index = file_contents.index(start_string)
            start = start_index + len(start_string) + 1
            file_contents = file_contents[start:]
            start_string = '"symbol" : {'
            start_index = file_contents.index(start_string)
            start = start_index + len(start_string) - 1 # Starting point of the JSON string - point, line, polygon, and dictionary symbology
            file_contents = file_contents[start:]
            
            end_index = file_contents.index('"scaleSymbols"') # The end of the JSON string appears somewhere before '"scaleSymbols"'
            end = end_index
            mid_contents = file_contents[:end]

            if flag_unique == 1:
              true_end = '}'
              index = mid_contents.rfind(true_end)
              mid_contents = mid_contents[:index + 1]
              if '"useDefaultSymbol" : true' in mid_contents:
                if '"type" : "CIMSymbolReference"' not in mid_contents: # Unique Values. Only the default symbol is utilized
                    flag_only_default = 1
                    if '"angleAlignment" : ' in mid_contents:
                      end_string = '"angleAlignment" : '
                    else:
                      end_string = ']'                  
                    end_index = mid_contents.rfind(end_string)
                    true_end = '}'
                    index = mid_contents.find(true_end, end_index)
                    mid_contents = mid_contents[:index + 1]
                    new_contents = mid_contents

                    value_string = end_string
                    label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, file_contents_only_default, value_string, flag_label)

                    name_labels.append(label_contents)
                  
                else: # Unique Values, when a default value and other values are utilized
                  flag_default_plus = 1
                  
            else:
              if '"angleAlignment" : ' in mid_contents:
                end_string = '"angleAlignment" : '
              else:
                end_string = ']'
              end_index = mid_contents.rfind(end_string)
              true_end = '}' # Ending point of the JSON string - point, line, polygon, and dictionary symbology
              index = mid_contents.find(true_end, end_index)
              new_contents = mid_contents[:index + 1]

            if flag_proportional == 1: # Proportional Symbols. Does not save the default symbol.
              new_contents = ''
              
              end_string = '"defaultSymbolPatch" : '

              end_index = mid_contents.index(end_string)
              end = end_index - 20 #Ending point of the JSON string
              mid_contents = mid_contents[:end]

              end_string = '"defaultSymbol" : {' # Default symbol is not saved
              
              if end_string in mid_contents:
                end_index = mid_contents.index(end_string)
                end = end_index - 20 #Ending point of the JSON string
                mid_contents = mid_contents[:end]
                  
              new_contents += mid_contents + '\n'
                
              del mid_contents

            elif flag_default_plus == 1: # Unique Values. Saves the default symbol.
              start_string = '"type" : "CIMSymbolReference"'
              new_contents = ''
              while flag_multi == 0:
                if start_string not in mid_contents:
                  flag_multi = 1
                else:
                    if '"defaultSymbolPatch" :' in mid_contents: #Saves the default symbol                     
                      end_string = '"defaultSymbolPatch" :'
                      end_index = mid_contents.index(end_string)
                      end = end_index - 20 #Ending point of the JSON string (starting point of JSON string same as for basic point, line, and polygon symbology) - default symbol
                      value_contents = mid_contents[:end]
                      mid_contents = mid_contents[end_index + len(end_string):]
                      new_contents += value_contents + '\n'

                    value_string = '"symbol" : {'
                    
                    label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

                    name_labels.append(label_contents)
                    
                    start_index = mid_contents.index(start_string)
                    start = start_index + len(start_string) + 1
                    mid_contents = mid_contents[start:]
                    start_string = '"symbol" : {'
                    start_index = mid_contents.index(start_string)
                    start = start_index + len(start_string) - 1 #Starting point of the JSON string
                    mid_contents = mid_contents[start:]

                    end_index = mid_contents.index('"type" : "CIMUniqueValue"')
                    end = end_index - 89 #Ending point of the JSON string
                    value_contents = mid_contents[:end]
                    mid_contents = mid_contents[end_index:]
                    
                    new_contents += value_contents + '\n'
              del mid_contents
              
            elif flag_unique == 1 and flag_only_default != 1: # Unique Values. Does not save the default symbol.
              start_string = '"type" : "CIMSymbolReference"'
              new_contents = ''
              while flag_multi == 0:
                if start_string not in mid_contents:
                  flag_multi = 1
                else:
                  if '"defaultSymbolPatch" :' in mid_contents: #Removes the default symbol
                    start_after_string = '"defaultSymbolPatch" :'
                    start_after_index = mid_contents.index(start_after_string)
                    mid_contents = mid_contents[start_after_index + len(start_after_string) + 1:]

                  value_string = '"symbol" : {'
                  
                  label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

                  name_labels.append(label_contents)

                  start_index = mid_contents.index(start_string)
                  start = start_index + len(start_string) + 1
                  mid_contents = mid_contents[start:]
                  start_string = '"symbol" : {'
                  start_index = mid_contents.index(start_string)
                  start = start_index + len(start_string) - 1 #Starting point of the JSON string
                  mid_contents = mid_contents[start:]

                  end_index = mid_contents.index('"type" : "CIMUniqueValue"')
                  end = end_index - 89 #Ending point of the JSON string
                  value_contents = mid_contents[:end]
                  mid_contents = mid_contents[end_index:]
                  
                  new_contents += value_contents + '\n'
              del mid_contents
              del name_labels[0] # Deletes the default symbol label

            elif '"type" : "CIMClassBreak"' in mid_contents: # Graduated colors and graduated symbols. Does not save the default symbol
              symbol_type = 'Graduated'

              new_contents = ''

              end_string = '"upperBound" :'
              end_index = mid_contents.index(end_string)
              value_contents = mid_contents[:end_index]
              mid_contents = mid_contents[end_index + len(end_string):]
                                             
              end_index = value_contents.rfind('},')
              value_contents = value_contents[:end_index]
                  
              new_contents += value_contents + '\n'

              start_string = '"type" : "CIMSymbolReference"'
              end_string = '"upperBound" :'

              value_string = end_string

              while flag_multi == 0:
                if end_string not in mid_contents:
                  flag_multi = 1
                else:
                  label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

                  name_labels.append(label_contents)
                  
                  start_index = mid_contents.index(start_string)
                  start = start_index + len(start_string) + 1
                  mid_contents = mid_contents[start:]
                  start_string = '"symbol" : {'
                  start_index = mid_contents.index(start_string)
                  start = start_index + len(start_string) - 1 # Starting point of the JSON string
                  mid_contents = mid_contents[start:]

                  end_index = mid_contents.index(end_string)
                  end = end_index - 28 # Ending point of the JSON string
                  value_contents = mid_contents[:end]
                  mid_contents = mid_contents[end_index + len(end_string):]
                  
                  new_contents += value_contents + '\n'
              del mid_contents
                
            elif '"weights" : [' in mid_contents: # Unclassed Colors.
              flag_is_vector = 0
              new_contents = ''

              start_string = '"colorRamp" : {'
              start_index = mid_contents.index(start_string)
              start = start_index + len(start_string) - 1 # Starting point of the JSON string
              mid_contents = mid_contents[start:]

              symbol_type = "Unclassed"

              mid_index = mid_contents.index('"weights" : [')
              end_contents = mid_contents[mid_index:]
              end_string = '},'
              end_index = end_contents.index(end_string)
              end = mid_index + (end_index + 1) # Ending point of the JSON string
              value_contents = mid_contents[:end]
              
              new_contents = value_contents

              if len(name_labels) == 1:
                del name_labels[0]

              label_contents = mid_contents
              value_string = end_string
              label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, label_contents, value_string, flag_label)

              name_labels.append(label_contents)
              del mid_contents

        # Rasters
        elif "CIMRasterLayer" in file_contents:
          
          if '"type" : "CIMRasterStretchColorizer"' in file_contents: # Raster Stretch
            start_string = '"colorRamp" : {'
            start_index = file_contents.index(start_string)
            start = start_index + len(start_string) - 1 # Starting point of the JSON string
            mid_contents = file_contents[start:]

            symbol_type = "Raster"
            value_string = '"colorScheme" : '

            label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

            name_labels.append(label_contents)
            
            end_string = '"colorScheme" : '
            end_index = mid_contents.index(end_string)
            end = end_index - 10 # Ending point of the JSON string
            new_contents = mid_contents[:end]

          elif '"type" : "CIMRasterDiscreteColorColorizer"' in file_contents: # Raster Discrete
            start_string = '"colorRamp" : {'
            start_index = file_contents.index(start_string)
            start = start_index + len(start_string) - 1 # Starting point of the JSON string
            mid_contents = file_contents[start:]
            
            symbol_type = "Raster"
            value_string = '"attributeTable" : {'

            label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

            name_labels.append(label_contents)
              
            end_string = '"attributeTable" : {'
            end_index = mid_contents.index(end_string) # Ending point of the JSON string
            end = end_index + len(end_string) - 36
            new_contents = mid_contents[:end]

          elif '"type" : "CIMRasterColorMapColorizer"' in file_contents: # Raster Colormap
            start_string = '"type" : "CIMRasterColorMapColorizer"'
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]
            start_string = '"colors" : ['
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]

            end_string = '"bandID" : '
            end_index = file_contents.index(end_string)

            labels_string = file_contents[end_index + len(end_string):]
            labels_start = '"labels" : ['
            labels_start_index = labels_string.index(labels_start) + len(labels_start)
            labels_string = labels_string[labels_start_index:]
            labels_end = '],'
            labels_end_index = labels_string.index(labels_end)
            labels_string = labels_string[:labels_end_index]
            
            mid_contents = file_contents[:end_index]

            symbol_type = "Raster ColorMap"

            value_string = '{'
            new_contents = ''
            while flag_multi_raster == 0:
              if value_string not in mid_contents:
                flag_multi_raster = 1
              else:
                value_string_labels = '",'
                label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, labels_string, value_string_labels, flag_label)

                name_labels.append(label_contents)

                if value_string_labels in labels_string:
                  labels_end_index = labels_string.find(value_string_labels) + len(value_string_labels)
                elif '""' in labels_string:
                  value_string_labels = '""'
                  labels_end_index = labels_string.find(value_string_labels) + len(value_string_labels)
                  
                labels_string = labels_string[labels_end_index:]

                start_index = mid_contents.index(value_string) # Starting point of the JSON string
                value_contents = mid_contents[start_index:]
                end_string = '}' # Ending point of the JSON string
                end_index = value_contents.index(end_string) + 1
                mid_contents = value_contents[end_index:]
                
                value_contents = value_contents[:end_index]
                new_contents += value_contents + '\n'
                
          elif '"type" : "CIMRasterClassifyColorizer"' in file_contents: # Raster Classify
            start_string = '"type" : "CIMRasterClassifyColorizer"'
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]
            end_index = file_contents.index('],')
            mid_contents = file_contents[:end_index]

            symbol_type = "Raster Classify"
            
            value_string = '"color" : {'
            new_contents = ''
            while flag_multi_raster == 0:
              if value_string not in mid_contents:
                flag_multi_raster = 1
              else:
                label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

                name_labels.append(label_contents)

                start_index = mid_contents.index(value_string)
                start = start_index + len(value_string) - 1 # Starting point of the JSON string
                value_contents = mid_contents[start:]
                mid_contents = value_contents
                  
                end_string = '}' # Ending point of the JSON string
                end_index = value_contents.index(end_string) + 1
                value_contents = value_contents[:end_index]
                new_contents += value_contents + '\n'
                
          elif '"type" : "CIMRasterUniqueValueColorizer"' in file_contents: # Raster Unique Values
            start_string = '"type" : "CIMRasterUniqueValueGroup"'
            start_index = file_contents.index(start_string)
            file_contents = file_contents[start_index:]
            end_index = file_contents.index('"heading" : ')
            mid_contents = file_contents[:end_index]

            symbol_type = "Raster Unique"
            
            value_string = '"color" : {'
            new_contents = ''
            while flag_multi_raster == 0:
              if value_string not in mid_contents:
                flag_multi_raster = 1
              else:
                label_contents, flag_label = add_label(lst_maps, lyrx, symbol_type, mid_contents, value_string, flag_label)

                name_labels.append(label_contents)

                start_index = mid_contents.index(value_string)
                start = start_index + len(value_string) - 1 # Starting point of the JSON string
                value_contents = mid_contents[start:]
                mid_contents = value_contents
                    
                end_string = '}' # Ending point of the JSON string
                end_index = value_contents.index(end_string) + 1
                value_contents = value_contents[:end_index]
                new_contents += value_contents + '\n'
                             
          else:
            print("Error! Vector field symbology cannot be added to style file at this time.")
            flag_raster = 1

        infile.close()

        if flag_vector != 1 and flag_raster != 1:          

          # Remove all spaces. Adds spaces back only for fonts and URLs
          symbology_json = parse_string(new_contents)

          if flag_background == 1:
            background_contents = parse_string(background_contents)
          else:
            background_contents = ''

          # Create symbology name list
          sym_name_lst = create_sym_name_lst(flag_multi, symbology_json, flag_multi_raster, flag_background, background_contents)

          for item in sym_name_lst:              
            symbol_class = 0
            
            # Determine symbol class type
            symbol_string_start = '{"type":"CIM'
            start_index = symbology_json.index(symbol_string_start)
            start = start_index + len(symbol_string_start)
            symbol_string_end = '",'
            end_index = symbology_json.index(symbol_string_end)
            symbol_name = symbology_json[start:end_index]
            
            if symbol_name[-5:] == "Color":
              symbol_name = symbol_name[-5:]
            elif symbol_name[-9:] == "ColorRamp":
              symbol_name = "ColorScheme"

            for key in class_dict:
              value = class_dict.get(key)
              value = value.replace(' ', '')
              if value in symbol_name:
                symbol_class = key

            if symbol_class == 0:
              print("Error! Unable to obtain symbol class for layer.")
            else:
              # 4b ii. Assign the ID to each style
              new_id = count

              # 4b iii. Pull the CLASS, NAME, TAGS, CONTENT, and KEY for each style from the JSON string
              new_class = symbol_class
              new_category = ''

              # Obtain tags for color type and color code
              if flag_is_vector != 1 and new_class == 1:
                tag_name = add_tags(item)
              elif new_class != 2:
                new_content_colors, label_types = get_new_content(item)
                tag_name = add_tags(new_content_colors[0])
              else:
                tag_name = add_tags_color_scheme(item)

              if flag_background == 1:
                name_background = lyrx[:-5] + "_background"
                if name_background != name_labels[-1]:
                  name_labels.append(name_background)
              
              if flag_label == 1:
                new_name = label_contents
              else:
                index = sym_name_lst.index(item)
                new_name = name_labels[index]

              new_tags = tag_name
              new_content = item
              new_key = new_name

              # 4b iv. Insert the symbology information into the ITEMS table
              if new_content not in sql_lst: # Prevents duplicate styles from being uploaded into the style file
                new_row = (new_id, new_class, new_category, new_name, new_tags, new_content, new_key)
                cursor.execute('INSERT INTO ITEMS(ID, CLASS, CATEGORY, NAME, TAGS, CONTENT, KEY) VALUES(?,?,?,?,?,?,?)', new_row)
                sql_lst.append(new_content)
                count += 1
                
                if symbol_class > 2 and symbol_class < 6:
                  new_item = item
                  symbol_class = 1
                  
                  new_content_colors, label_types = get_new_content(new_item)
          
                  for i in range(len(new_content_colors)):
                    for j in range(len(label_types)):
                      new_content_color = new_content_colors[i]
                      label_type = label_types[j]
                      if i == j:
                        # Obtain tags for color type and color code
                        tag_name = add_tags(new_content_color)
                        
                        # 4b ii. Assign ID to each style
                        new_id = count
                        # 4b iii. Pull the CLASS, NAME, TAGS, CONTENT, and KEY for each style from the JSON string
                        new_class = symbol_class
                        new_category = ''
                        new_name += '_' + label_type
                        new_tags = tag_name
                        new_content_item = new_content_color
                        new_key = new_name

                        # 4b iv. Insert the symbology information into the ITEMS table as color styles, if applicable
                        if new_content_item not in sql_lst: # Prevents duplicate color styles from being uploaded into the style file
                          new_row = (new_id, new_class, new_category, new_name, new_tags, new_content_item, new_key)
                          cursor.execute('INSERT INTO ITEMS(ID, CLASS, CATEGORY, NAME, TAGS, CONTENT, KEY) VALUES(?,?,?,?,?,?,?)', new_row)
                          sql_lst.append(new_content_item)
                          count += 1
                      
                    end_dash = new_name.rfind('_')
                    new_name = new_name[:end_dash]

  if flag_lyrx == 0:
    print("Error! lyrx folder directory contains no lyrx.")
    quit()

  # 4c i. Create the STYLE_ITEM_BINARY_REFERENCES table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS STYLE_ITEM_BINARY_REFERENCES (ID, ITEMS_ID, BINARIES_ID)')

  # 4c ii.Create the meta table if it doesn't already exist
  cursor.execute('CREATE TABLE IF NOT EXISTS meta (key, value)')

  lst_meta = meta_dict.items()
  for element in lst_meta:
    row_meta = element      
    cursor.execute('INSERT INTO meta(key, value) VALUES(?,?)', row_meta)

  # 4d. Commit the changes to the database and close the connection
  conn.commit()
  conn.close()


  # Step 5: Organize .aprx and .lyrx into folder hierarchy for future use and storage
  
  # Move map layers from temporary holding bucket into corresponding folders for each map name ("63,360", "FSTopo") in lyrx_folder_final
  move_files(lyrx_folder_final, lyrx_folder)

  # Delete the temporary holding bucket folder
  shutil.rmtree(lyrx_folder)

  print("\n\nJob ending!", datetime.datetime.now(), "\n")
