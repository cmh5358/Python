# -*- coding: utf-8 -*-
'''
Title: PDF to GeoTiff 2023
Authors: Caitlin Hartig, Tyler Jones
Date: November 2023

This program pulls PDF names from a file directory and then updates the naming convention for the PDFs. It then creates a corresponding TIFF file for each PDF.
Finally, the program creates a GMS file and adds information for each tiff into the GMS.

Libraries Utilized: arcpy, os
'''

import arcpy, os

def get_all_pdfs_in_dir(in_dir):
##    Purpose: obtain file pathways to all PDFs contained in the folder.
##      Only returns the file, not the root + file, due to potential spacing issue in the in_dir:
##      C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Tyler\SampleInputPDFs\SampleInputPDFs
##      The spaces in the root cause errors in program processing if the root is also returned for each file.
##    
##
##    Input Example: "C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Tyler\SampleInputPDFs\SampleInputPDFs"
##    Output Example: "_ags__ags_20230525_180312_FSTopo_Indian Mountain_340008522.pdf" 
  
  output = [] 

  for root, dirs, files in os.walk(in_dir):
    for file in files: # for each .pdf
        output.append(file)

  return output

def parse_pdf_name(PDFFileName):
  '''
    Purpose: parse input pdf file name based on position of FSTopo substring.
      Joins remaining strings together with empty spaces.

    Input Example: "_ags__ags_20230525_180312_FSTopo_Indian Mountain_340008522.pdf"
    Output Example: "FSTopo Indian Mountain 340008522.pdf" 
  '''
  if "_" in PDFFileName:
    str_values = PDFFileName.split("_")
    topo_index = str_values.index("FSTopo")
    names = str_values[topo_index:]

    return " ".join(names)
  else:
    return PDFFileName

def create_new_batch(in_dir, batch_dir):
  '''
    Purpose: either create a new batch gms file (if the batch file name does not already exist in the input directory) or update an existing one (if it does already exist).
    Inputs: input directory, batch file name
    Outputs: prints whether or not a new batch file was created, or if an existing batch file is being appended
  '''
  lst = get_all_pdfs_in_dir(in_dir)
  str_values = batch_dir.split(os.sep)
  batch_name = str_values[-1]
          
  if batch_name not in lst:
    BatchFile = open(batch_dir, "w")
    BatchFile.write("GLOBAL_MAPPER_SCRIPT VERSION=1.0")
    BatchFile.close
    print("Created New Batch File\n")
  else:
    print("Appending to existing Batch File\n")

#This is test code to extract from a SECoord the component degree and minute values
# dlb 11/15/2016
 
def obtain_lat_long(SECoord):
  '''
    Purpose: obtains lat and long coordinates based on the SE coordinate of the map tile
    Inputs: SE coordinate
    Outputs: SE latitude, SE longitude, SW latitude, SW longitude
  '''
  #Latitude - North implied
  #first two characters represent degrees Latitude
  degLat = int(SECoord[:2])
  #third and fourth characters represent minutes Latitude
  minLat = int(SECoord[2:4])

  """
  minutes Latitude may have a fractional value, add if needed
  """

  if minLat % 15 == 11: # multiples of 15 (11.25, 26.25, 41.25, 56.25)
    minLat += 0.25
  elif minLat % 15 == 7: # multiples of 15 (7.5, 22.5, 37.5, 52.5)
    minLat += 0.5
  elif minLat % 15 == 3: # multiples of 15 (3.75, 18.75, 33.75, 48.75)
    minLat += 0.75

  #Longitude - West implied

  #fifth through seventh characters represent Degrees Longitude
  degLong = SECoord[4:7]
  #eighth and ninth characters represent Minutes Longitude
  minLong = SECoord[7:9]

  #add half a minute, as appropriate
  if float(minLong)%5 != 0:
   minLong = minLong + ".5"
  
  """
  Now, determine quadrangle size
  
  If below 50 degrees latitude
    size is 7.5 x 7.5 minutes
  Else
   size is 7.5 x 10 minutes (below 59 degrees)
     or
   size is 7.5 x 11.25 minutes (above 59 degrees)
   """
  
  if float(degLat) < 50:
    sizeLat = "7.5"
    sizeLong = "7.5"
  elif float(degLat) < 59:
    sizeLat = "7.5"
    sizeLong = "10"
  else:
    sizeLat = "7.5"
    sizeLong = "11.25"

  seLat = float(degLat) + float(minLat)/60
  seLong = float(degLong)*-1 - float(minLong)/60
  swLat = seLat + float(sizeLat)/60
  swLong = seLong - float(sizeLong)/60

  print(degLat, "degrees North", minLat, "minutes North,", degLong, "degrees West", minLong, "minutes West, quad size = ", sizeLat, "x", sizeLong)

  return seLat, seLong, swLat, swLong

def update_batch(batch_name, tiff_name, projection_name, raster_file_name, palette_name, seLat, seLong, swLat, swLong):
  '''
    Purpose: Appends information into an existing Batch File (GMS)
    Inputs: batch file path name, tiff file path name, projection file path name, raster file path name, palette file path name, SE latitude, SE longitude, SW latitude, SW longitude
    Outputs: None
  '''
  BatchFile = open(batch_name,"a")
  BatchFile.write (chr(10) + chr(13) + "IMPORT FILENAME=" + chr(34) + tiff_name + chr(34) + chr(10) + chr(13))
  BatchFile.write("LOAD_PROJECTION FILENAME="+ chr(34)+ projection_name + chr(34) + chr(10) + chr(13))
  BatchFile.write("EXPORT_RASTER FILENAME="+ chr(34) + raster_file_name + chr(34)  + " \\"+ chr(10) + chr(13))
  BatchFile.write("TYPE=GEOTIFF SAMPLING_METHOD=NEAREST_NEIGHBOR PALETTE=" + palette_name + " GEN_WORLD_FILE=NO LAT_LON_BOUNDS=" + str(swLong)+ "," + str(seLat) + ","  + str(seLong) + ","  + str(swLat) + chr(10) + chr(13))
  BatchFile.write("UNLOAD_ALL" + chr(10) + chr(13))
  BatchFile.write("RUN_COMMAND COMMAND_LINE=" + chr(34) + "CMD /C DEL '" + tiff_name[:-3] + '*' + chr(34))
  BatchFile.close
 
if __name__ == '__main__':

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    print("Program starting!\n")

    input_dir = input("Please enter the complete file pathway for the PDF folder directory:\n")
    gms_dir = input("Please enter the complete file pathway for the GMS folder directory:\n")
    GeoTiff_name = input("Please enter the file name for the GMS batch file. Ex: FirstBatch.gms\n")
    
    GeoTiffDir = os.path.join(gms_dir, GeoTiff_name)
    create_new_batch(gms_dir, GeoTiffDir)
    projection_name = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Tyler\geo.prj" #Update Me!
    palette_name = r"C:\Users\CaitlinHartig\OneDrive - USDA\Documents\Xentity\Code\Tyler\FStopoTIFF.pal" #Update Me!

    lst = get_all_pdfs_in_dir(input_dir)
    
    if lst == []:
      print("Error! PDF folder directory is empty.")
      quit()

    flag = 0
    
    for PDFFileName in lst: # .pdf's in the input directory
      
      original_pdf = os.path.join(input_dir, PDFFileName)
                         
      if ".pdf" in PDFFileName:
        flag = 1

      # Step 1: Rename PDF name starting at "FSTopo" and convert "_" to " ". Ex) "FSTopo Bradley 340008207.pdf"
        print(f"\nCurrently processing: {PDFFileName}")
        parsed_pdf_name = parse_pdf_name(PDFFileName) # "FSTopo Indian Mountain 340008522.pdf"
        renamed_pdf_file = os.path.join(input_dir, parsed_pdf_name)
        
        if parsed_pdf_name != PDFFileName:
          arcpy.management.Rename(original_pdf, renamed_pdf_file)

        
        # Step 2: Create tiff file from each PDF. Should just be the coordinate name: Ex) 340008207.tif
        str_values = renamed_pdf_file.split(" ")
        pdf_number = str_values[-1]
        renamed_pdf_as_tiff = pdf_number[:-4] + ".tif" # "340008522" + ".tif"
        final_tiff = os.path.join(input_dir, renamed_pdf_as_tiff)

        if renamed_pdf_as_tiff not in lst:
          arcpy.conversion.PDFToTIFF(in_pdf_file=renamed_pdf_file, out_tiff_file=final_tiff, resolution=500)


        # Step 3: Create a .gms file, which is the script that will run in the Global Mapper software.
        raster_name = parsed_pdf_name[:-4] + ".tiff" # "FSTopo Indian Mountain 340008522.tiff"
        raster_file_name = os.path.join(gms_dir, raster_name)
        
        seLat, seLong, swLat, swLong = obtain_lat_long(renamed_pdf_as_tiff)
        update_batch(GeoTiffDir, final_tiff, projection_name, raster_file_name, palette_name, seLat, seLong, swLat, swLong)

    if flag == 0:
      print("Error! PDF folder directory contains no PDFs.")
      quit()

    print("\nProgram ending!")
