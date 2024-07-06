'''
Title: SmallScaleMapsPDFExport
Authors: Caitlin Hartig, Clay Williams
Date: February 2024

This program exports PDF(s) of the user's choosing from an existing map series that has been created in ArcGIS Pro.
The user can either choose to export a single PDF or can choose to export PDFs for an entire region of their choosing.

Libraries Utilized: arcpy, os, datetime, shutil
'''

import arcpy, os, datetime, shutil

print("Program starting!", datetime.datetime.now())

# Update Me!
arcpy.env.workspace = r'C:\Users\caitl\OneDrive\Documents\APRX'
featureclass = r'C:\Users\caitl\OneDrive\Documents\APRX\Map_Index_Data_Driven_Pages.gdb\Map_Index'
pdfNEW = r'C:\Users\caitl\OneDrive\Documents\APRX\Maps'

# List all aprx in folder. Select desired aprx from menu option
count = 0
dict_aprx = {}
for aprx in arcpy.ListFiles('*.aprx'):
    count += 1
    print(count, '-', aprx)
    dict_aprx[count] = aprx

case_aprx = 'n'
while case_aprx == 'n':
    input_aprx_number = input('Which aprx would you like to select? Enter the number as listed above\n')
    if not input_aprx_number.lstrip("-").isdigit():
        print('Error! Invalid entry. Please enter a valid numerical digit.')
    elif int(input_aprx_number) not in dict_aprx.keys():
        print('Error! Invalid entry.')
    else:
        case_aprx = 'y'
        
        input_aprx = dict_aprx[int(input_aprx_number)]
        input_aprx = os.path.join(arcpy.env.workspace, input_aprx)
        aprx = arcpy.mp.ArcGISProject(input_aprx)

        layout = aprx.listLayouts()[0]
        ms = layout.mapSeries

        # Select the desired region number for processing
        case_region_or_singlePDF = 'n'
        lst_region_or_singlePDF = [1, 2]
        case_region = 'n'
        lst_region_numbers = [1, 2, 3, 4, 5, 6, 8, 9, 10]
        case_singlePDF = 'n'
        dict_singlePDFs = {}
        case_PDF_name = 'n'

        while case_region_or_singlePDF == 'n':
            region_or_singlePDF = input('Would you like to process a whole region or a single PDF? Enter 1 for whole region, 2 for single PDF.\n')
            if not region_or_singlePDF.lstrip("-").isdigit():
                print('Error! Invalid entry. Please enter a valid numerical digit.')
            elif int(region_or_singlePDF) not in lst_region_or_singlePDF:
                print('Error! Invalid entry.')
            else:
                case_region_or_singlePDF = 'y'
                
                if int(region_or_singlePDF) == lst_region_or_singlePDF[0]:
                    while case_region == 'n':
                        region_number = input('Which region number would you like to process? Enter 1, 2, 3, 4, 5, 6, 8, 9, 10\n')
                        if not region_number.lstrip("-").isdigit():
                            print('Error! Invalid entry. Please enter a valid numerical digit.')
                        elif int(region_number) not in lst_region_numbers:
                            print('Error! Invalid entry.')
                        else:
                            case_region = 'y'
                            
                            if int(region_number) < 10:
                                region_number_zero = '0' + region_number
                                folder_pathway_new = os.path.join(pdfNEW, 'Region_' + region_number_zero)
                            else:
                                folder_pathway_new = os.path.join(pdfNEW, 'Region_' + region_number)

                            # Obtain PDF name
                            with arcpy.da.SearchCursor(featureclass, ['REGION', 'CODE', 'PageName']) as cursor:
                                for row in cursor:
                                    region = row[0]
                                    if region == 'Region {0}'.format(str(region_number)):
                                        orgCode = row[1]
                                        name = row[2]
                                        pdfName = orgCode + '_' + name + '.pdf'
                                        pdfName = os.path.join(folder_pathway_new, pdfName)

                                        while os.path.exists(pdfName):
                                            pdfName = pdfName[:-4] + '(1)' + '.pdf'
                                        print("\n", pdfName)

                                        # Export PDF for corresponding map series page that matches PDF name
                                        pageNumber = ms.getPageNumberFromName(name)

                                        ms.exportToPDF(out_pdf = pdfName, 
                                                       page_range_type = "RANGE", 
                                                       page_range_string = pageNumber,
                                                       multiple_files = "PDF_SINGLE_FILE")

                elif int(region_or_singlePDF) == lst_region_or_singlePDF[1]:
                    while case_singlePDF == 'n':
                        with arcpy.da.SearchCursor(featureclass, ['CODE', 'PageName']) as cursor:
                            for row in cursor:
                                dict_singlePDFs[row[1]] = row[0]
                            print(dict_singlePDFs.values())
                            
                            singlePDF_number = input('Which single PDF number would you like to process?\n')
                            if not singlePDF_number.lstrip("-").isdigit():
                                print('Error! Invalid entry. Please enter a valid numerical digit.')
                            elif singlePDF_number not in dict_singlePDFs.values():
                                print('Error! Invalid entry.')
                            else:
                                case_singlePDF = 'y'

                                lst_dict = dict_singlePDFs.items()
                                count = 0
                                dict_new = {}
                                for item in lst_dict:
                                    if item[1] == singlePDF_number:
                                        count += 1
                                        dict_new[count] = item[0]
                                        print(count, ":", item[0])

                                while case_PDF_name == 'n': 
                                    PDF_name_number = input('Which PDF name would you like to process? Enter the corresponding number listed above.\n')
                                    if not PDF_name_number.lstrip("-").isdigit():
                                        print('Error! Invalid entry. Please enter a valid numerical digit.')
                                    elif int(PDF_name_number) not in dict_new.keys():
                                        print('Error! Invalid entry.')
                                    else:
                                        case_PDF_name = 'y'
                                        
                                        with arcpy.da.SearchCursor(featureclass, ['REGION', 'CODE', 'PageName']) as cursor:
                                            for row in cursor:
                                                if row[1] == singlePDF_number:
                                                    if row[2] == dict_new[int(PDF_name_number)]:
                                                        orgCode = row[1]
                                                        name = row[2]
                                                        
                                                        region_number = row[0][-1:]
                                                        
                                                        if int(region_number) < 10:
                                                            region_number_zero = '0' + region_number
                                                            folder_pathway_new = os.path.join(pdfNEW, 'Region_' + region_number_zero)
                                                        else:
                                                            folder_pathway_new = os.path.join(pdfNEW, 'Region_' + region_number)
                                                
                                                        pdfName = orgCode + '_' + name + '.pdf'
                                                        pdfName = os.path.join(folder_pathway_new, pdfName)

                                                        while os.path.exists(pdfName):
                                                            pdfName = pdfName[:-4] + '(1)' + '.pdf'
                                                        print("\n", pdfName)

                                                        # Export PDF for corresponding map series page that matches PDF name
                                                        pageNumber = ms.getPageNumberFromName(name)

                                                        ms.exportToPDF(out_pdf = pdfName, 
                                                                       page_range_type = "RANGE", 
                                                                       page_range_string = pageNumber,
                                                                       multiple_files = "PDF_SINGLE_FILE")          

        print("\nEnd of program!", datetime.datetime.now())
