'''
Title: Woodland Tint
Authors: Caitlin Hartig, John Cuchta
Date: September 2023

This program reclassifies a raster and then converts it into a polygon. The area is calculated for each polygon.
Smaller clearings of 1 acre or less are then converted into canopy, and clearings greater than 1 acre are removed.
Then, the polygon numbers are streamlined, area is recalculated for the new larger polygons, and the polygons are smoothed out for a more polished look.

Libraries Utilized: arcpy, datetime
'''

import arcpy, datetime

'''
    Purpose - reclassifies a raster using raster 3D
    Inputs - input raster, reclass field, file pathway for output raster, data option
        remap option must be designated 1:1 and hand written in the Reclassify statement for function to work
    Outputs - reclassified raster
'''
def reclassify_raster(input_raster, RECLASS_FIELD, output_raster, DATA):
    # "Value" field 0-19 in attribute table for raster, and the value in the "Value" field gets updated
    # 0-19 become 0 (Clearings)
    # 20-100 become 1 (Canopy)
    return arcpy.ddd.Reclassify(
        in_raster=input_raster,
        reclass_field=RECLASS_FIELD,
        remap="0 0;1 0;2 0;3 0;4 0;5 0;6 0;7 0;8 0;9 0;10 0;11 1;12 1;13 1;14 1;15 1;16 1;17 1;18 1;19 1;20 21;21 22;22 23;23 24;24 25;25 26;26 27;27 28;28 29;29 30;30 31;31 32;32 33;33 34;34 35;35 36;36 37;37 38;38 39;39 40;40 41;41 42;42 43;43 44;44 45;45 46;46 47;47 48;48 49;49 50;50 51;51 52;52 53;53 54;54 55;55 56;56 57;57 58;58 59;59 60;60 61;61 62;62 63;63 64;64 65;65 66;66 67;67 68;68 69;69 70;70 71;71 72;72 73;73 74;74 75;75 76;76 77;77 78;78 79;79 80;80 81;81 82;82 83;83 84;84 85;85 86;86 87;87 88;88 89;89 90;90 91;91 92;92 93;93 94;94 95;95 96;96 97;97 98;98 99;99 100;100 101;101 102;102 103;103 104;104 105;105 106;106 107;107 108;108 109;109 110;110 111;111 112;112 113;113 114;114 115;115 116;116 117;117 118;118 119;119 120;120 121;121 122;122 123;123 124;124 125;125 126;126 127;127 128;128 129;129 130;130 131;131 132;132 133;133 134;134 135;135 136;136 137;137 138;138 139;139 140;140 141;141 142;142 143;143 144;144 145;145 146;146 147;147 148;148 149;149 150;150 151;151 152;152 153;153 154;154 155;155 156;156 157;157 158;158 159;159 160;160 161;161 162;162 163;163 164;164 165;165 166;166 167;167 168;168 169;169 170;170 171;171 172;172 173;173 174;174 175;175 176;176 177;177 178;178 179;179 180;180 181;181 182;182 183;183 184;184 185;185 186;186 187;187 188;188 189;189 190;190 191;191 192;192 193;193 194;194 195;195 196;196 197;197 198;198 199;199 200;200 201;201 202;202 203;203 204;204 205;205 206;206 207;207 208;208 209;209 210;210 211;211 212;212 213;213 214;214 215;215 216;216 217;217 218;218 219;219 220;220 221;221 222;222 223;223 224;224 225;225 226;226 227;227 228;228 229;229 230;230 231;231 232;232 233;233 234;234 235;235 236;236 237;237 238;238 239;239 240;240 241;241 242;242 243;243 244;244 245;245 246;246 247;247 248;248 249;249 250;250 251;251 252;252 253;253 254;254 255;255 256",
        out_raster=output_raster,
        missing_values=DATA
    )

'''
    Purpose - converts a raster to polygon
    Inputs - input raster, file pathway for output polygons, simplification option, reclass field
    Outputs - output polygons saved in designated file pathway
'''
def raster_to_polygon(input_raster, output_polygons, simplification, RECLASS_FIELD):
    return arcpy.conversion.RasterToPolygon(input_raster, output_polygons, simplification, RECLASS_FIELD)

'''
    Purpose - this program calculates the area in acres for a given field
    Inputs - input layer, new field name (to contain the calculated area in acres)
    Outputs - none
'''
def calculate_area(input_shape, new_field):
    expr = '!shape.area@acres!'
    LANGUAGE = "PYTHON3"
    arcpy.CalculateField_management(input_shape, new_field, expr, LANGUAGE)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\Users\CaitlinH\WoodlandTint", workspace=r"D:\Users\CaitlinH\WoodlandTint"): #Update Me!
        arcpy.env.overwriteOutput = True

        print("Job starting!", datetime.datetime.now(), "\n")

        # Step 1: Take tree canopy raster data and reclassify the 0 to 100 range

        # Must be written as below to obtain rasters in order for 3D Reclassify function to work
        rasters = arcpy.ListRasters()
        rasters = rasters if rasters is not None else []
        #print(rasters)

        input_raster = rasters[0] #Update Me!
        #print(input_raster)

        RECLASS_FIELD = "Value"
        output_raster = r"D:\Users\CaitlinH\WoodlandTint\WoodlandTint.gdb\raster_reclassified"
        DATA = "NODATA"

        arcpy.CheckOutExtension("3D")
        raster_reclassified = reclassify_raster(input_raster, RECLASS_FIELD, output_raster, DATA)
        
        print("Step 1 completed - tree canopy raster data reclassified.", datetime.datetime.now(), "\n")


        # Step 2: Convert the reclassified raster to polygon

        arcpy.env.workspace = r"D:\Users\CaitlinH\WoodlandTint\WoodlandTint.gdb"
        output_polygons = "raster_converted"
        simplification = "NO_SIMPLIFY"

        output_polygons = raster_to_polygon(raster_reclassified, output_polygons, simplification, RECLASS_FIELD)

        print("Step 2 completed - converted raster to polygon.", datetime.datetime.now(), "\n")


        # Step 3: Calculate area in acres for the polygons

        fieldName = "Area_Acres"
        calculate_area(output_polygons, fieldName)

        print("Step 3 completed - area in acres calculated for polygons.", datetime.datetime.now(), "\n")


        # Step 4: Convert smaller clearings (1 acre or less) to canopy. Where gridcode = 0 and area <= 1

        selection = arcpy.management.SelectLayerByAttribute(output_polygons, selection_type="NEW_SELECTION", where_clause="Area_Acres <= '1' And gridcode = 0", invert_where_clause=None)
        output_polygons = arcpy.management.CalculateField(selection, field="gridcode", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

        print("Step 4 completed - smaller clearings (1 acre or less) converted to canopy.", datetime.datetime.now(), "\n")
        

        # Step 5: Remove clearings greater than 1 acre. Where gridcode = 0 and area > 1
        
        selection = arcpy.management.SelectLayerByAttribute(output_polygons, selection_type="NEW_SELECTION", where_clause="Area_Acres > '1' And gridcode = 0", invert_where_clause=None)
        output_polygons = arcpy.management.DeleteRows(in_rows=str(selection))
        
        print("Step 5 completed - clearings greater than 1 acre removed.", datetime.datetime.now(), "\n")


        # Step 6: Run Dissolve to reduce polygon numbers
        dissolved = arcpy.env.workspace + r"\dissolved"
        dissolve_field = "gridcode"
        dissolved = arcpy.analysis.PairwiseDissolve(output_polygons, dissolved, dissolve_field, "", "MULTI_PART")
        
        print("Step 6 completed - polygon numbers reduced via Dissolve.", datetime.datetime.now(), "\n")


        # Step 7: Recalculate area in acres, as the dissolve tool forces the true areas to change
        fieldName = "Area_Acres_New"
        calculate_area(dissolved, fieldName)

        print("Step 7 completed - area recalculated in acres.", datetime.datetime.now(), "\n")


        # Step 8: Run Smooth Polygon tool
        smoothed = arcpy.env.workspace + r"\smoothed"
        ALGORITHM = "PAEK"
        TOLERANCE = 80
        ENDPOINT = "FIXED_ENDPOINT"
        ERROR_OPTION = "NO_CHECK"
        arcpy.cartography.SmoothPolygon(dissolved, smoothed, ALGORITHM, TOLERANCE, ENDPOINT, ERROR_OPTION)

        print("Step 8 completed - ran Smooth Polygon tool.", datetime.datetime.now(), "\n")

        print("Job ending!", datetime.datetime.now(), "\n")
