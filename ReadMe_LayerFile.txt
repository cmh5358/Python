Purpose: Save copies of .aprx. Then save .lyrx files for each layer in the copied .aprx file

Instructions:
1. Right click on the script and open it using "Edit with IDLE (ArcGIS Pro)"
2. At line 123 (# File paths), update:
	1. File pathway to the folder from which to pull the .aprx.
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\APRX\Pro
	2. File pathway to the folder in which to save files temporarily (does not need to already exist, but needs to be a valid file pathway).
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\Export_Tool\LyrxOutput
	3. File pathway to the folder in which to save layer files permanently (also the .aprx will be copied into this location). Files are distributed into their respective subfolders "63,360" and "FSTopo" within this umbrella folder
		Default location is: T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\LayerFile_StyleFile\LayerFiles
		***Note: Make sure that if using this option, the subfolder name in this directory either matches the .aprx name or contains the subfolder name within the .aprx name. Ex) "63,360" and "FSTopo".
			If the functionality to save .lyrx into distinct subfolders is not needed, simply comment out the move_files() function on line 148 and skip that part.***
	4. List of .aprx names to copy.
		By default, saves the following .aprx: FSTopo_Continental, 63,360_FSBaseMap
	5. List of map names from which to pull .lyrx.
		By default, saves the following map names: 'FSTopo' and 'Main Map', for FSTopo_Continental and 63,360_FSBaseMap, respectively.
		If both map names or multiple maps of the same name (identical to the provided map_name) are present within an .aprx, the first map is selected.
	Caveat: The default setting is to overwrite output. Therefore if there are multiple .lyrx with the same name in the same map, the last is selected.
	Note: .lyrx of the same name from different maps are all saved. The map name is added to the end of the .lyrx name when saved. Ex) Airfield FAA_63360_FSBaseMap
3. Run code

Note: Code is designed not to save .lyrx without a symbology renderer. This is due to the fact that the arcpy command layer.saveACopy (line 72) fails (Attribute Error) without the layer having a symbology renderer.