StyleFile.py

Purpose:
1. Create a new style file (.stylx) from scratch containing symbology from a map document!
2. Layers from multiple .aprx can be saved inside the same style file by running the script only once.

~*~

Instructions:
1. Open the desired .aprx and update all changes to symbology. Save and close .aprx.
2. Right click on the script and open it using "Edit with IDLE (ArcGIS Pro)"
3. At line 482 (# File paths), update:
	1. File pathway to the folder from which to pull the .aprx.
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\APRX\Pro
	2. File pathway to the folder in which to save files temporarily (does not need to already exist, but needs to be a valid file pathway).
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Export_Tool\LyrxOutput
	3. File pathway to the folder in which to save layer files permanently (also the .aprx will be copied into this location). Files are distributed into their respective subfolders "63,360" and "FSTopo" within this umbrella folder
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\LayerFiles
		***Note: Make sure that if using this option, the subfolder name in this directory either matches the .aprx name or contains the subfolder name within the .aprx name. Ex) "63,360" and "FSTopo".
			If the functionality to save .lyrx into distinct subfolders is not needed, simply comment out the move_files() function on line 148 and skip that part.***
	4. File pathway to the folder in which to save the style file.
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Style Files
	5. Style file name.
		Default is yyyymmdd_FSBasemapStyle.stylx
	6. List of .aprx names to copy.
		By default, saves the following .aprx: FSTopo_Continental, 63,360_FSBaseMap
	7. List of map names from which to pull .lyrx.
		By default, saves the following map names: 'FSTopo' and 'Main Map', for FSTopo_Continental and 63,360_FSBaseMap, respectively.
		If both map names or multiple maps of the same name (identical to the provided map_name) are present within an .aprx, the first map is selected.
	Caveat: The default setting is to overwrite output. Therefore if there are multiple .lyrx with the same name in the same map, the last is selected.
	Note: .lyrx of the same name from different maps are all saved. The map name is added to the end of the .lyrx name when saved. Ex) Airfield FAA_63360_FSBaseMap
4. Run code

Note: Code is designed not to save .lyrx without a symbology renderer. This is due to the fact that the arcpy command layer.saveACopy (line 72) fails (Attribute Error) without the layer having a symbology renderer.

~*~

Current limitations of code:
1. Code currently only works for map layers and not for layout elements or mesh symbols. Code works for both vector and raster layers.

   a. Therefore, code currently only works for the following map style classes:
	1. Colors
	2. Color schemes
	3. Point symbols
	4. Line symbols
	5. Polygon symbols

   b. Therefore, code currently does not work for the following style classes:
	6. Text symbols
	9. Standard Label Placement
	10. Maplex Label Placement
	7, 8, 11, 13, 14, 15, 17, 18. Layout elements
	12. Mesh symbols

-Caveat: Vector Field Symbology has not yet been tested, but should produce an error message when code is run.

~*~

How to load a completed style file into ArcGIS Pro:
1. Open the desired .aprx in ArcGIS Pro.
2. In ArcCatalog, right-click the Styles menu, select "Add" and then "Add Style".
3. Navigate to the folder directory containing the .stylx you wish to add and select the .stylx. Click "ok".
4. Your custom .stylx should now be listed at the bottom of the Styles drop-down menu and available for use.

~*~

For additional information, please see the Powerpoint:
   T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Export_Tool\1248 - Style File Automation Using ArcGIS Pro, Python, and SQL.pptx