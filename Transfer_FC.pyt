import arcpy, os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Transfer_FC"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Transfer_FC]


class Transfer_FC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Transfer_FC"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # First parameter - file directory pathway to Input GDB
        param0 = arcpy.Parameter(
            displayName="Input GDB (Should contain the relevant feature classes)",
            name="input_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        master_gdb = r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\Automation_Repository\Tools\Master_GDB.gdb'
        param0.value = master_gdb
        
        # Second parameter - user selected input feature classes on which to run tool (must be contained within the Input GDB)
        param1 = arcpy.Parameter(
            displayName="Input Feature Class / Table",
            name="input_fc",
            datatype=["DEFeatureClass", "DETable"],
            parameterType="Required",
            direction="Input",
            multiValue=True)

        # Third parameter - user selected output GDB
        param2 = arcpy.Parameter(
            displayName="Output GDB -- Production SDE or EDW",
            name="output_gdb",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        lst = []
        folder_new1 = r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\SCHEMA\ProductionSDEstaging.gdb'
        lst.append(folder_new1)
        
        folder_new2 = r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\Workspace\chartig\Projects\Automation Repository\Test_Scripts\Oracle-SDE_EDW_DEV([S_USA]).sde'
        lst.append(folder_new2)

        param2.filter.type = "ValueList" # Remove specific links / dropdown menu. Change to a user populated field where the user inputs the correct link themselves.
        param2.filter.list = lst
        
        params = [param0, param1, param2]
        
        return params
    
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
            
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = 1

        # File Pathways
        folder_old = parameters[0].valueAsText
        input_fc = parameters[1]
        folder_new = parameters[2].valueAsText

        # Part 1 - Upload to Output GDB
        fcs_master_uploaded = upload(folder_old, input_fc, folder_new)

        # Part 2 - Grant Privileges to EDW Users
        #EDW = r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\Workspace\chartig\Projects\Automation Repository\Test_Scripts\Oracle-SDE_EDW_DEV([S_USA]).sde' # Since this will become its own separate user input, get rid of this variable and call the correct parameter instead
        #grant_permissions(folder_new, EDW, fcs_master_uploaded) # Not working - throws an error that states I do not have permission to grant privileges (even though I do)

##'''
##    Purpose - Function upload(folder_old, input_fc, folder_new)
##    Inputs - folder_old: File pathway to the Initial GDB, where the user input feature classes / tables are stored Ex) r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\Automation_Repository\Tools\Master_GDB.gdb'.
##             input_fc: Input feature classes / tables defined by the user Ex) Hydro_NatFloodHaz_Comm_FEMA, Hydro_NatFloodHaz_HazArea_FEMA
##             folder_new: File pathway to the Output GDB. Should either be the EDW (r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\Workspace\chartig\Projects\Automation Repository\Test_Scripts\Oracle-SDE_EDW_DEV([S_USA]).sde') or the SDE (r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\SCHEMA\ProductionSDEstaging.gdb').
##    Output - fcs_master_uploaded: A list filled with feature classes / tables that have been successfully uploaded into the Output GDB
##'''
def upload(folder_old, input_fc, folder_new):
    fcs_master_uploaded = []

    arcpy.env.workspace = folder_old

    fcs = input_fc.valueAsText.split(';')

    for filename in fcs:
        start_index = filename.rfind(chr(92))
        file = filename[start_index + 1:]
        if file[-1] == chr(39):
            file = file[:-1]
        for dirpath_master, dcs_master, fcs_master in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
            if file not in fcs_master:
                arcpy.AddMessage('Error! {0} is not saved within the Input GDB. File not exported. All selected feature classes / tables must be saved within the Input GDB.\n'.format(file))
            else:
                for fc_master in fcs_master:
                    if fc_master == file: # Take each feature class / table in the user's selection that is also located in the Input GDB and copy it into the Output GDB
                        fc_old = os.path.join(folder_old, fc_master)
                        fc_new = os.path.join(folder_new, fc_master)
                        arcpy.management.Copy(fc_old, fc_new)
                        fcs_master_uploaded.append(fc_master)

                        arcpy.AddMessage('{0} copied into {1}.'.format(fc_master, folder_new))

    return fcs_master_uploaded

##'''
##    Purpose - Function grant_permissions(folder_new, comparison_folder, fcs_master_uploaded) grants user privileges for SDE (Read Only), SDE_VIEW (Read Only), S_EDW_PUBLISH (Read/Write) and S_USA_EDW_EDIT (Read/Write).
##                This is especially important because the EDW metadata team needs to be able to look at the uploaded files to ensure metadata compliance. 
##    Inputs - folder_new: File pathway to the user selected Output GDB. Should either be the EDW (r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\Workspace\chartig\Projects\Automation Repository\Test_Scripts\Oracle-SDE_EDW_DEV([S_USA]).sde') or the SDE (r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\FSBaseMaps\SCHEMA\ProductionSDEstaging.gdb').
##             comparison_folder: File pathway to the comparison folder. Should be the EDW (r'T:\FS\NFS\WOEngineering\GMO-GTAC\Project\DDC\Workspace\chartig\Projects\Automation Repository\Test_Scripts\Oracle-SDE_EDW_DEV([S_USA]).sde')
##             fcs_master_uploaded: A list filled with feature classes / tables that have been successfully uploaded into the Output GDB (output of function upload(folder_old, input_fc, folder_new)).
##    Output - None
##'''
def grant_permissions(folder_new, comparison_folder, fcs_master_uploaded):      
    if folder_new == comparison_folder: # Grants permissions only if folder_new is the comparison folder
        arcpy.env.workspace = folder_new
        for dirpath_sde, dcs_sde, fcs_sde in arcpy.da.Walk(arcpy.env.workspace, datatype=['FeatureClass', 'Table']):
            for fc_sde in fcs_sde:
                for fc_master_uploaded in fcs_master_uploaded: # Grants permissions only if the feature class / table was just uploaded into folder_new
                    if fc_master_uploaded in fc_sde:
                        arcpy.AddMessage('Granting User Privileges for {0}:'.format(fc_sde))
                        
                        arcpy.AddMessage("\tGranting User: SDE Privileges = Read Only")
                        arcpy.management.ChangePrivileges(in_dataset=fc_sde, user="SDE", View="GRANT", Edit="AS_IS")

                        arcpy.AddMessage("\tGranting User: SDE_VIEW Privileges = Read Only")
                        arcpy.management.ChangePrivileges(in_dataset=fc_sde, user="SDE_VIEW", View="GRANT", Edit="AS_IS")

                        arcpy.AddMessage("\tGranting User: S_EDW_PUBLISH Privileges = Read/Write")
                        arcpy.management.ChangePrivileges(in_dataset=fc_sde, user="S_EDW_PUBLISH", View="GRANT", Edit="GRANT")

                        arcpy.AddMessage("\tGranting User: S_USA_EDW_EDIT Privileges = Read/Write")
                        arcpy.management.ChangePrivileges(in_dataset=fc_sde, user="S_USA_EDW_EDIT", View="GRANT", Edit="GRANT")
