# PlotsAll.py
# Description: Create a query table from two OLE DB tables using a limited set of
#               fields and establishing an equal join.
 
# Import system modules   CSV version
import csv
import os
import xlrd
import arcpy
 
try:
    # Local variables...
    locationName = "CONUCPER"
    diskLocation="C:/Demo/"+locationName+"/"
    arcpy.env.overwriteOutput = True   
    # Set workspace
    arcpy.env.workspace = diskLocation+locationName+".gdb"
    out_gdb = diskLocation+locationName+".gdb"
    # Get and print a list of tables
    sheets = arcpy.ListTables()
    for sheet in sheets:    
        out_table = sheet        
        data = sheet.split("_") #split string into a list
        print('Converting {} to {}'.format(sheet, data[1]))         
        if not (data[1] == "Plots"):     
            inFc1 = out_gdb + "/" + sheet   
            outFc = data[1]
            arcpy.TableToTable_conversion(inFc1,out_gdb,outFc)
            arcpy.Delete_management(inFc1)
        fcs = [out_gdb + "/" + outFc]
        for fc in fcs:
                fields = arcpy.ListFields(fc)
                for field in fields:
                    #print field.name
                    fldss1 = field.name[:5]
                    fldss2 = field.name[:6]
                    if (fldss1 == "Field"):
                        if (fldss2 != "Field_"):
                            print "Deleting " + field.name
                            arcpy.DeleteField_management(fc, field.name)
    sheets = arcpy.ListTables()
    excelListpt = []
    excelList = []
    for sheet in sheets:    
        out_table = sheet
        print "Redoing columns for " + sheet        
        outFc = sheet        
        fcs = [out_gdb + "/" + outFc]   #sheet = data[1]
        fld2Base = []
        fld2New = []
        if sheet == "WeatherDaily": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1            
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Bad_Value") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Integer", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "WeatherStation": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 4):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1   
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Direction") > -1) or (fld2Base[i].find("Weather__1") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "Overview": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 8):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1   
            for fc in fcs:
                for i in range(0, len(fld2Base)):                
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])        
        elif sheet == "ExperUnits": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 9):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1   
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSoilPhys": #ok                       
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 3):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):                    
                    if (fld2Base[i].find("Model_if_s") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])            
        elif sheet == "MeasSoilChem": #ok                       
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 3):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Model_if_s") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSoilBiol": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 3):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("FAME") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("PLFA") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("DNA") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Model_if_s") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                        
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasResidueMgnt": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSoilCover": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasHarvestFraction": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasBiomassMinAn": #ok                       
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):                    
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")                    
                    arcpy.DeleteField_management(fc,fld2Base[i])
        elif sheet == "MgtAmendments": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
               for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Amend_Type") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Active_Ing") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Pest_Targe") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Pest_Place") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Irrigati_1") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MgtPlanting": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Planting_M") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MgtTillage": #ok            
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
               for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Tillage__2") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasGHGFlux": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MgtGrazing": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 4):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Animal_Spe") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Animal_Cla") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Other_Even") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif (fld2Base[i].find("Burn_Inten") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MeasGrazingPlants": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])        
        elif sheet == "MeasBiomassCHO":#ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasBiomassEnergy": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MgtResidue": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Stage_at_H") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSuppRes": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 4):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Measurem_1") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasARGenes": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 5):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Presence_o") > -1) or (fld2Base[i].find("Units") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasNutrEff": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 6):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasCropForageQuality": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 7):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Chemical_C") > -1) or (fld2Base[i].find("Unit") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasGasNutrientLoss": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 8):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasPlantMonitoring": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 3):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Crop_Monit") > -1) or (fld2Base[i].find("Test_Units") > -1) or (fld2Base[i].find("Growth_Sta") > -1) or (fld2Base[i].find("Crop") > -1) or (fld2Base[i].find("Model_if_s") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasYieldNutUptake": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 7):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasNutrientCycling": # test
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 7):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWaterQualityArea": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 9):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Losses_or") > -1) or (fld2Base[i].find("Erosion_Me") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWaterQualityConc": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 9):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i].find("Losses_or") > -1) or (fld2Base[i].find("Erosion_Me") > -1):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWindErosionArea": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 10):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWindErosionConc": #ok
            j = 0
            for fc in fcs:
                for fldOb in arcpy.ListFields (fc):
                    if (j > 10):
                        fld2Base.append(fldOb.name)
                        fld2New.append(fldOb.name + "1")
                    j = j + 1  
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        else:
            var = 1
        if ((sheet == "Overview") or (sheet == "FieldSites") or (sheet == "Citations") or (sheet == "Persons") or (sheet == "Treatments") or (sheet == "WeatherStation") or (sheet == "WeatherDaily") or (sheet == "AllCellComments")):
            excelListpt.append(sheet)
        else:
            excelList.append(sheet)    
        print sheet + " done"

    #for testing
    #for i in range(0, len(fld2Base)):
            #print fld2Base[i]
            #print fld2New[i]

    #for fc in fcs:
    #    for fldOb in arcpy.ListFields (fc):
    #        fld = fldOb.name
    #        print fld    
    #for i in range(0, len(excelListpt)):        
    #    print excelListpt[i]
    #for i in range(0, len(excelList)):        
    #    print excelList[i]

 
     

    overviewList= ["Site ID","Site ID Descriptor","Research Unit","Dataset Name","Dataset Descriptor","Funding Source","Start Date","End Date", "Duration of Dataset"]
    fieldsitesList= ["Site ID","Date","MLRA","Field ID","Country","State/Province","County","City", "Postal Code","Latitude decimal deg","Longitude decimal deg","Spatial Description","Elevation m","MAP mm","MAT degC","Native Veg","Site History"]
    personsList= ["Site ID","Last Name","First Name","Middle Name","Suffix","Role","Primary Contact","Department","Organization","Date Created","Profession","Email","Telephone","Web Site","Note"]
    citationsList= ["Site ID","Date Published","Type","Title","Is Part Of","Author","Correspond Author","Identifier USDA-ARS","Description","Citation"]    
    treatmentsList= ["Treatment ID","Start Date","Treatment Descriptor","Rotation Descriptor","Tillage Descriptor","N Treatment Descriptor","Project Scenario","Fert Ammend Class","Cover Crop","Residue Removal","Irrigation","Organic Management","Grazing Rate","Animal (Species)","Operation", "ARS Projects"]
    weatherstationList= ["Site ID", "Field ID","Date","Weather Station ID","Weather Latitude decimal deg","Weather Longitude decimal deg","Weather Elevation m","Distance from Field m","Direction from Field","Weather Station URL"]
    weatherdailyList= ["Site ID","Field ID","Weather Date","Weather Time","Weather Station ID","Temp Max degC","Temp Min degC","Precip mm/d","Bad Value Flag","RH %","Dew Point deg C","Wind Speed m/s","Solar Radiation Veg MJ/m2/d","Solar Radiation Bare MJ/m2/d","Soil Temp 5cm degC","Soil Temp 10cm degC","Wind Direction deg From N","Open Pan Evap mm/d","Closed Pan Evap mm/d", "Atmos N Deposition kgN/ha/d","Total Net Radiation MJ/m2/d","Snow mm/d"]    
    allcellcommentsList= ["Site ID","Date Entered","Sheet Name","Field Name","Reporting Person","Comment"]
    
    featureClassList = []
    for i in range(0, len(excelListpt)):
        featureClassList.append(locationName+"_"+excelListpt[i])
    baseLayer = locationName+"_Plots_Cntr"
    for i in range(0, len(excelListpt)):
        if arcpy.Exists(excelListpt[i]):
            tableList = [excelListpt[i],baseLayer]
            print tableList
            fieldList = '#'
            if excelListpt[i] == "Treatments":                
                whereClause = ""
            else:   
                whereClause = baseLayer+".LOCATIONID="+excelListpt[i]+".Site_ID"
            print whereClause
            keyField = '#'
            lyrName = excelListpt[i]+"_temp"
            # Make Query Table...
            arcpy.gp.MakeQueryTable_management(tableList, lyrName,"ADD_VIRTUAL_KEY_FIELD", keyField, fieldList, whereClause)
            print lyrName
            arcpy.Delete_management(featureClassList[i])
            arcpy.FeatureClassToFeatureClass_conversion(lyrName, arcpy.env.workspace, featureClassList[i])
            fieldList = arcpy.ListFields(featureClassList[i])  #get a list of fields for each feature class
            j = 0
            for field in fieldList: #loop through each field               
                # Split field name at _ symbol
                if field.name.find("_OBJECTID") > -1:
                    arcpy.DeleteField_management(featureClassList[i], field.name)
                elif field.name.find(baseLayer+"_County") > -1:
                    arcpy.DeleteField_management(featureClassList[i], field.name)
                elif field.name.find(baseLayer+"_Description") > -1:
                    arcpy.DeleteField_management(featureClassList[i], field.name)
                else:                     
                    if field.name.find(excelListpt[i]) > -1:
                        print field.name                        
                        indxb = len(excelListpt[i]) + 1
                        indxe = len(field.name)
                        nwstr = field.name[indxb:indxe]                        
                        if excelListpt[i] == "Persons":
                            arcpy.AlterField_management(featureClassList[i], field.name, personsList[j], personsList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "Citations":
                            arcpy.AlterField_management(featureClassList[i], field.name, citationsList[j], citationsList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "Treatments":
                            arcpy.AlterField_management(featureClassList[i], field.name, treatmentsList[j], treatmentsList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "WeatherStation":
                            arcpy.AlterField_management(featureClassList[i], field.name, weatherstationList[j], weatherstationList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "WeatherDaily":
                            arcpy.AlterField_management(featureClassList[i], field.name, weatherdailyList[j], weatherdailyList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "AllCellComments":
                            arcpy.AlterField_management(featureClassList[i], field.name, allcellcommentsList[j], allcellcommentsList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "Overview":
                            arcpy.AlterField_management(featureClassList[i], field.name, overviewList[j], overviewList[j])                            
                            j = j + 1
                        elif excelListpt[i] == "FieldSites":
                            arcpy.AlterField_management(featureClassList[i], field.name, fieldsitesList[j], fieldsitesList[j])                            
                            j = j + 1
                        else:
                            print "Table does not exist"
                    if field.name.find(baseLayer) > -1:
                        print field.name                        
                        j = 0
                        indxb = len(baseLayer) + 1
                        indxe = len(field.name)
                        nwstr = field.name[indxb:indxe]                        
                        arcpy.AlterField_management(featureClassList[i], field.name, nwstr, nwstr)
                        
    
                   
    if (len(excelList) != 0):             
        amendmentsList= ["Exp Unit ID","Date","Treatment ID","Crop"," Amend Placement","Amend Depth cm","Amend Type","Total Amend Amount kg/ha","Total N Amount kgN/ha","Total P Amount kgP/ha","Total K Amount kgK/ha","Total Pest Amount kg/ha","Active Ingredient Type","Pest Target","Pest Placement","Irrigation Amount cm","Irrigation Type","Irrigation N mg/l"]
        experunitsList= ["Exp Unit ID","Treatment ID","Field ID","Start Date","End Date","Change in Management","Soil Series","Soil Classification","Landscape Position","Latitude","Longitude","Slope %","Exp Unit Size m2"]            
        ghgfluxList = ["Exp Unit ID","Date","Treatment ID","Crop","Chamber Placement","N2O gN/ha","N2O Interp=0  Obs=1","CO2 gC/ha","CO2 Interp=0 Obs=1","CH4 gC/ha","CH4 Interp=0 Obs=1","Air Temp degC","Soil Temp degC","Soil Moisture %","Soil Moisture Depth cm","N2O STD gN/ha","CO2 STD gC/ha","CH4 STD gC/ha","Air Temp STD degC","Soil Temp STD degC","Soil Moisture STD %"]
        plantingList= ["Exp Unit ID","Date","Treatment ID","Crop","Cultivar","Planting Rate #seeds/ha","Planting Density kg/ha","Planting Method","Planting Depth cm","Row Width cm"]
        tillageList= ["Exp Unit ID","Date","Treatment ID","Crop","Tillage Event","Tillage Event Depth cm","Tillage Event Method"]
        growthstageList= ["Exp Unit ID","Date","Treatment ID","Crop","Growth Stage"]
        residueList= ["Exp Unit ID","Date","Treatment ID","Crop","Equipment Type","Cutting Ht/Material Harvested", "Rows Harvested %","Stand Age years","Stage at Harvest"]
        grazingList= ["Exp Unit ID","Start Date","End Date","Treatment ID","Stocking Rate #animals/ha","Animal Species","Animal Class","Other Events","Burn Frequency yrs btwn burns","Burn Intensity"]
        soilphysList= ["Exp Unit ID","Date","Treatment ID","Upper cm","Lower cm","Model if Simulated","Sand %","Silt %","Clay %", "Bulk Density g/cm3","Wilting Point % volume","Field Capacity % volume","Ksat cm/sec","Moisture Release Curve","Soil Heat Flux MJ/m2","Micro Aggregates %","H2O Stable Aggregate g/kg","Near-Infrared C g/kg","Bulk Density STD g/cm3","Wilting Point STD % volume","Field Capacity STD % volume","Ksat STD cm/sec","Soil Heat Flux STD MJ/m2","Micro Aggregates STD %","H2O Stable Aggregate STD g/kg","Near-Infrared C STD g/kg"]
        harvestremovList= ["Exp Unit ID", "Date", "Treatment ID", "Growth Stage", "Crop", "Harvested Frac", "Corn Ear Height cm", "Above G Biomass kg/ha", "Grain Weight mg", "Grain Dry Matt kg/ha", "Grain Moist %", "Grain C kgC/ha", "Grain N kgN/ha", "Harv Res Dry Matt kg/ha", "Harv Res Moist %", "Harv Res C kgC/ha", "Harv Res N kgN/ha", "Non Harv Res Dry Matt kg/ha", "Non Harv Res Moist %", "Non Harv Res C kgC/ha", "Non Harv Res N kgN/ha", "Root Dry Matt kg/ha", "Root Moist %", "Root C kgC/ha", "Root N kgN/ha", "Corn Ear Height STD cm", "Above G Biomass STD kg/ha", "Grain Weight STD mg", "Grain Dry Matt STD kg/ha", "Grain Moist STD %", "Grain C STD kgC/ha", "Grain N STD kgN/ha", "Har Res Dry Matt STD kg/ha", "Harv Res Moist STD %", "Harv Res C STD kgC/ha", "Harv Res N STD kgN/ha", "Non Harv Res DM STD kg/ha", "Non Harv Res Moist STD %", "Non Harv Res C STD kgC/ha", "Non Harv Res N STD kgN/ha", "Root Dry Matt STD kg/ha", "Root Moist STD %", "Root C STD kgC/ha", "Root N STD kgN/ha" ]
        soilchemList= ["Exp Unit ID", "Date", "Treatment ID", "Upper cm", "Lower cm","Model if Simulated", "pH", "TSC gC/kg", "TSN gN/kg", "Inorganic C gC/kg", "Organic C gC/kg", "Mineral C gC/kg", "CEC cmol/kg", "Electric Conduc siemens/m", "Soluble C mgC/kg", "NH4 mgN/kg", "NO3 mgN/kg", "P mgP/kg", "K mgK/kg", "Ca mgCa/kg", "Mg mgMg/kg", "Cu mgCu/kg", "Fe mgFe/kg", "Mn mgMn/kg", "Zn mgZn/kg", "Pot Mineralizable N gN/kg", "Nitirite mgN/kg","Cesium-137 Bq/m2","Lead-210 Bq/m2","Beryllium-7 Bq/m2", "pH STD", "TSC STD gC/kg", "TSN STD gN/kg", "Inorganic C STD gC/kg", "Organic C STD gC/kg", "Mineral C STD gC/kg", "CEC STD g/kg", "Electric Conduc STD siemens/m", "Soluble C STD mgC/kg", "NH4 STD mgN/kg", "NO3 STD mgN/kg", "P STD mgP/kg", "K STD mgK/kg", "Ca STD mgCa/kg", "Mg STD mgMg/kg", "Cu STD mgCu/kg", "Fe STD mgFe/kg", "Mn STD mgMn/kg", "Zn STD mgZn/kg", "Pot Mineralizable N STD gN/kg", "Nitrite STD mgN/kg","Cesium-137 STD Bq/m2","Lead-210 STD Bq/m2","Beryllium-7 STD Bq/m2"]
        soilbiolList= ["Exp Unit ID", "Date", "Treatment ID", "Upper cm", "Lower cm","Model if Simulated", "Glucosidase mg/kg/hr", "Glucosaminidase mg /kg/hr", "Acid Phosphotase mg/kg/hr", "Alk Phosphotase mg/kg/hr", " F D Hydrolysis mg/kg/hr", "Glomalin g/kg", "FAME", "PLFA", "DNA", "Iden Plant Mat gC/kg", "POM gC/kg", "Microbe Bio C mgC/kg", "Microbe Bio N mgN/kg", "Glucosidase STD mg/kg/hr", "Glucosaminidase STD mg/kg/hr", "Acid Phosphotase STD mg/kg/hr", "Alk Phosphotase STD mg/kg/hr", "F D Hydrolysis STD mg/kg/hr", "Glomalin STD g/kg", "Iden Plant Mat STD gC/kg", "POM STD gC/kg", "Microbe Bio C STD mgC/kg", "Microbe Bio N STD mgN/kg"]
        soilcoverlist=["Exp Unit ID", "Date", "Treatment ID", "Timing Descriptor", "Crop", "Soil w/ Residue %"]    
        plantfractionList= ["Exp Unit ID","Sampling Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Frac Dry Matt kg/ha","Frac Moist %","Frac C kgC/ha","FracN kgN/ha","Grain Weight mg","Frac Dry Matt STD kg/ha"," Frac Moist STD %","Frac C STD kgC/ha","FracN STD kgN/ha","Grain Weight STD mg"]
        biomasschoList= ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Glucan g/kg","Xylan g/kg","Galactan g/kg","Arabinan g/kg","Mannan g/kg","Lignin g/kg","Neutral Det Fiber g/kg","Acid Det Fiber g/kg","Acid Soluble Lignin g/kg","Acid Insoluble Lignin g/kg","Crude Protein g/kg","Non-fiber Carbs g/kg","Ash g/kg", "Glucan STD g/kg","Xylan STD g/kg","Galactan STD g/kg","Arabinan STD g/kg","Mannan STD g/kg","Lignin STD g/kg","Neutral Det Fiber STD g/kg","Acid Det Fiber STD g/kg","Acid Soluble Lignin STD g/kg","Acid Insoluble Lignin STD g/kg","Crude Protein STD g/kg","Non-fiber Carbs STD g/kg","Ash STD g/kg"]
        biomassenergyList= ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Volatile Matter g/kg","Ash g/kg","Gross Caloric Value MJ/kg","Volatile Matter STD g/kg","Ash STD g/kg","Gross Caloric Value STD MJ/k"]
        biomassminanList= ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Plant Fraction","C Concentration g/kg","N Concentration g/kg","P Concentration g/kg","K Concentration g/kg","Ca Concentration g/kg","Mg Concentration g/kg","S Concentration g/kg","Na Concentration g/kg","Cl Concentration g/kg","Al Concentration mg/kg","B Concentration mg/kg","Cu Concentration mg/kg","Fe Concentration mg/kg","Mn Concentration mg/kg","Zn Concentration mg/kg", "C Concentration STD g/kg","N Concentration STD g/kg","P Concentration STD g/kg","K Concentration STD g/kg","Ca Concentration STD g/kg","Mg Concentration STD g/kg","S Concentration STD g/kg","Na Concentration STD g/kg","Cl Concentration STD g/kg","Al Concentration STD mg/kg","B Concentration STD mg/kg","Cu Concentration STD mg/kg","Fe Concentration STD mg/kg","Mn Concentration STD mg/kg","Zn Concentration STD mg/kg"]
        grazingplantsList= ["Exp Unit ID","Date","Treatment ID","Species Mix","Growth Stage","Broadleaf vs Grass","AboveGr Bio kg/ha (dry)","Surface Litter kg/ha (dry)","Standing Dead kg/ha (dry)","LAI kg/ha (dry)","Biomass N %","Lignin N %","Ground Cover %","AboveGr Bio C kgC/ha","AboveGr Bio N kgN/ha","BelowGr Bio C kgC/ha","BelowGr Bio N kgN/ha","ANPP C kgC/ha/yr","ANPP N kgN/ha/yr","BNPP C kgC/ha/yr","BNPP N kgN/ha/yr","AboveGr Bio STD kg/ha","Surface Litter STD kg/ha","Standing Dead STD kg/ha (dry)","LAI STD kg/ha ","Biomass N STD %","Lignin N STD %","Ground Cover STD %","AboveGr Bio C STD kgC/ha","AboveGr Bio N STD kgN/ha","BelowGr Bio C STD kgC/ha","BelowGr Bio N STD kgN/ha","ANPP C STD kgC/ha/yr","ANPP N STD kgN/ha/yr","BNPP C STD kgC/ha/yr","BNPP N STD kgN/ha/yr"]
        suppresList= ["Exp Unit ID","Sampling Date","Treatment ID","What is Measured","Measurement Value","Measurement Units"]
        MeasNutrEffList = ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Fraction N kgN/ha","Nitrogen Use Efficiency %","Agronomic Efficiency kg/kg","Nutr effic ratio N kg/kg","Nitrogen15 Use Effic kgN/ha"]
        MeasARGenes = ["Exp Unit ID","Date","Treatment ID","Sample Type","Sample Details","Upper","Lower","Target","Presence or Absence of Target","Value","Units"]

        #NUOnet
        YieldNutUptake = ["Exp Unit ID","Sampling Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Model if simulated","Frac Dry Matt kg/ha YNU","Frac Moist % YNU","Frac C kgC/ha YNU","Frac N kgN/ha YNU","Frac P kgP/ha","Frac K kgK/ha","Frac S kgS/ha","Frac Ca kgCa/ha","Frac Mg kgMg/ha","Frac Cu gCu/ha","Frac Fe gFe/ha","Frac Mn gMn/ha","Frac Zn gZn/ha","Frac B gB/ha","Frac Mo gMo/ha","Grain Weight mg/kernel YNU","Frac Dry Matt STD kg/ha YNU","Frac Moist STD % YNU","Frac C  STD kgC/ha YNU","Frac N STD kgN/ha YNU","Frac P STD kgP/ha","Frac K STD kgK/ha","Frac S STD kgS/ha","Frac Ca STD kgCa/ha","Frac Mg STD kgMg/ha","Frac Cu STD gCu/ha","Frac Fe STD gFe/ha","Frac Mn STD gMn/ha","Frac Zn STD gZn/ha","Frac B STD gB/ha","Frac Mo STD gMo/ha","Grain Weight STD mg/kernel YNU"]
        GasNutrientLoss = ["Exp Unit ID","Start Date","Start time","End Date","End Time","Treatment ID","Growth Stage","Crop","Model if simulated GHG","NOx-N g/ha/day","Obs or sim Denitrified N gas","Model if sim Denitrified N gas","N2-N g/ha/day","N2O-N g/ha/day","Observed or simulated AmmVol","Model if simulated AmmVol","NH3-N kg/ha/day","NOx-N STD g/ha/day","N2-N STD g/ha/day","N2O-N STD g/ha/day","NH3-N STD kg/ha/day"]
        WaterQualityConc = ["Exp Unit ID","Date","Time","Treatment ID","Growth Stage","Crop","Sampling Start-Stop Interval","Model if simulated ","Surface or Leaching","Sampling Depth cm","Losses or Deposition","Erosion Method ","Erosion kg (sediment)","Erosion Tot susp solids kg","Erosion Total solids kg","Soil organic matter mg SOM/L","Soil organic carbon mg C/L","Water mm","mg total N/L","mg Total P/L","mg NH4-N/L","mg NO3-N/L","Total Dissolved N mg/L","Total Dissolved mg P/L","mg Cl/L","pH","EC mS/cm","Dissolved mg K/L","Dissolved mg S/L","Dissolved mg Ca/L","Dissolved mg Mg/L","Dissolved ug Cu/L","Dissolved ug Fe/L","Dissolved ug Mn/L","Dissolved ug Zn/L","Dissolved ug B/L","Dissolved ug Mo/L","Dissolved mg Al/L","Dissolved mg Na/L","Dissolved mg Si/L","Erosion kg (sediment) STD","Erosion Tot. susp solids kg STD","Erosion Total solids kg STD","Soil org matter mg SOM/L STD","Soil organic carbon mg C/L STD","Water mm STD","mg total N/L STD","mg total P/L STD","mg NH4-N/L STD","mg NO3-N/L STD","Total Dissolved N mg N/L STD","Total Dissolved P mg P/L STD","mg total Cl/L STD","pH STD","EC mS/cm STD","Dissolved mg K/L STD","Dissolved mg S/L STD","Dissolved mg Ca/L STD","Dissolved mg Mg/L STD","Dissolved ug Cu/L STD","Dissolved ug Fe/L STD","Dissolved ug Mn/L STD","Dissolved ug Zn/L STD","Dissolved ug B/L STD","Dissolved ug Mo/L STD","Dissolved mg Al/L STD","Dissolved mg Na/L STD","Dissolved mg Si/L STD"]
        WaterQualityArea = ["Exp Unit ID","Date","Time","Treatment ID","Growth Stage","Crop","Sampling Start-Stop Interval","Model if simulated ","Surface or Leaching","Sampling Depth cm","Losses or Deposition","Erosion Method ","Erosion t (sediment)/ha","Erosion tot susp solids t/ha","Erosion Total solids t/ha","Soil organic matter kg/ha","Soil organic carbon kg C/ha","Water mm","kg total N/ha","kg total P/ha","kg NH4-N/ha","kg NO3-N/ha","Total Dissolved N kg N/ha","Total Dissolved P kg P/ha","kg total Cl/ha","pH","EC mS/cm","Dissolved kg K/ha","Dissolved kg S/ha","Dissolved kg Ca/ha","Dissolved kg Mg/ha","Dissolved g Cu/ha","Dissolved g Fe/ha","Dissolved g Mn/ha","Dissolved g Zn/ha","Dissolved g B/ha","Dissolved g Mo/ha","Dissolved kg Al/ha","Dissolved kg Na/ha","Dissolved kg Si/ha"," Erosion t (sediment)/ha STD","Erosion tot sus solids t/ha STD","Erosion Total solids t/ha STD","Soil organic matter kg/ha STD","Soil organic carbon kg C/ha STD","Water mm STD","kg total N/ha STD","kg total P/ha STD","kg NH4-N/ha STD","kg NO3-N/ha STD","Total Dissolved N kg N/ha STD","Total Dissolved P kg P/ha STD","kg total Cl/ha STD","pH STD","EC mS/cm STD","Dissolved kg K/ha STD","Dissolved kg S/ha STD","Dissolved kg Ca/ha STD","Dissolved kg Mg/ha STD","Dissolved g Cu/ha STD","Dissolved g Fe/ha STD","Dissolved g Mn/ha STD","Dissolved g Zn/ha STD","Dissolved g B/ha STD","Dissolved g Mo/ha STD","Dissolved kg Al/ha STD","Dissolved kg Na/ha STD","Dissolved kg Si/ha STD"]
        PlantMonitoring = ["Exp Unit ID","Date","Treatment ID","Sample Depth Upper cm","Sample Depth Lower cm","Growth Stage","Crop","Model if Simulated","Test Value","Test Units","Crop Monitoring Test","Test Value STD"]
        CropForageQuality = ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Plant Fraction","Model if Simulated","Value","Unit","Chemical Compound","Value STD"]
        CropNutrientCycling = ["Exp Unit ID","Date","Treatment ID","Growth Stage","Crop","Harvested Fraction","Model if simulated","Corn Ear Height cm","Above G Biomass kg/ha","Unit Grain Weight mg","Grain Dry Matt kg/ha","Grain Moist %","Grain C kgC/ha","Grain N kgN/ha","Grain P kgP/ha","Grain K kgK/ha","Grain S kgS/ha","Grain Ca kgCa/ha","Grain Mg kgMg/ha","Grain Cu gCu/ha","Grain Fe gFe/ha","Grain Mn gMn/ha","Grain Zn gZn/ha","Grain B gB/ha","Grain Mo gMo/ha","Harv NonGrain Bio kg/ha","Harv Res Moist %","Harv Res C kgC/ha","Harv Res N kgN/ha","Harv Res P kgP/ha","Harv Res K kgK/ha","Harv Res S kgS/ha","Harv Res Ca kgCa/ha","Harv Res Mg kgMg/ha","Harv Res Cu gCu/ha","Harv Res Fe gFe/ha","Harv Res Mn gMn/ha","Harv Res Zn gZn/ha","Harv Res B gB/ha","Harv Res Mo gMo/ha","NonHarv NonGrain Bio kg/ha","NonHarv Res Moist %","NonHarv Res C kgC/ha","NonHarv Res N kgN/ha","nonHarv Res P kgP/ha","nonHarv Res K kgK/ha","nonHarv Res S kgS/ha","nonHarv Res Ca kgCa/ha","nonHarv Res Mg kgMg/ha","nonHarv Res Cu gCu/ha","nonHarv Res Fe gFe/ha","nonHarv Res Mn gMn/ha","nonHarv Res Zn gZn/ha","nonHarv Res B gB/ha","nonHarv Res Mo gMo/ha","Corn Ear Height STD","Above Ground Biomass STD","Unit Grain Weight STD","Grain DryMatter STD","Grain MoisturePct STD","Grain C STD","Grain N STD","Grain P STD","Grain K STD","Grain S STD","Grain Ca STD","Grain Mg STD","Grain Cu STD","Grain Fe STD","Grain Mn STD","Grain Zn STD","Grain B STD","Grain Mo STD","Harv Res DryMatter STD","HarvRes MoisturePct STD","Harv Res C STD","Harv Res N STD","Harv Res P STD","Harv Res K STD","Harv Res S STD","Harv Res Ca STD","Harv Res Mg STD","Harv Res Cu STD","Harv Res Fe STD","Harv Res Mn STD","Harv Res Zn STD","Harv Res B STD","Harv Res Mo STD","nonHarv Res DryMatter STD","nonHarv Res MoisturePct STD","nonHarv Res C STD","nonHarv Res N STD","nonHarv Res P STD","nonHarv Res K STD","nonHarv Res S STD","nonHarv Res Ca STD","nonHarv Res Mg STD","nonHarv Res Cu STD","nonHarv Res Fe STD","nonHarv Res Mn STD","nonHarv Res Zn STD","nonHarv Res B STD","nonHarv Res Mo STD"]
        WindErosionConc = ["Exp Unit ID","Date","Time","Treatment ID","Growth Stage","Crop","Sampling Start-Stop Interval","Model if simulated","Method","Losses or Deposition","Soil t","Soil org matter mg SOM/kg","Soil org carbon mg C/kg","pH","EC mS/cm","mg N/kg","mg NH4-N/kg","mg NO3-N/kg","mg P/kg","mg K/kg","mg S/kg","mg Ca/kg","mg Mg/kg","ug Cu/kg","ug Fe/kg","ug Mn/kg","ug Zn/kg","ug B/kg","ug Mo/kg","mg Al/kg","mg Na/kg","mg Si/kg","Soil t STD","Soil org matter mg SOM/kg STD","Soil org carbon mg C/kg STD","pH STD","EC mS/cm STD","mg N/kg STD","mg NH4-N/kg STD","mg NO3-N/kg STD","mg P/kg STD","mg K/kg STD","mg S/kg STD","mg Ca/kg STD","mg Mg/kg STD","ug Cu/kg STD","ug Fe/kg STD","ug Mn/kg STD","ug Zn/kg STD","ug B/kg STD","ug Mo/kg STD","mg Al/kg STD","mg Na/kg STD","mg Si/kg STD"]
        WindErosionArea = ["Exp Unit ID","Date","Time","Treatment ID","Growth Stage","Crop","Sampling Start-Stop Interval","Model if simulated","Method","Losses or Deposition","Soil t/ha","Soil org matter kg/ha","Soil org carbon kg C/ha","pH","EC mS/cm","kg total N/ha","kg NH4-N/ha","kg NO3-N/ha","kg total P/ha","kg K/ha","kg S/ha","kg Ca/ha","kg Mg/ha","g Cu/ha","g Fe/ha","g Mn/ha","g Zn/ha","g B/ha","g Mo/ha","kg Al/ha","kg Na/ha","kg Si/ha","Soil t/ha STD","Soil org matter kg/ha STD","Soil org carbon kg C/ha STD","pH STD","EC mS/cm STD","kg total N/ha STD","kg NH4-N/ha STD","kg NO3-N/ha STD","kg total P/ha STD","kg K/ha STD","kg S/ha STD","kg Ca/ha STD","kg Mg/ha STD","g Cu/ha STD","g Fe/ha STD","g Mn/ha STD","g Zn/ha STD","g B/ha STD","g Mo/ha STD","kg Al/ha STD","kg Na/ha STD","kg Si/ha STD"]
        joinTreat = locationName+"_Treatments"
        joinExp = locationName+"_ExperUnitsT1"
        featureClassList = []
        featureClassListOut = []
        featureClassListJ = []
        joinListOut = []
        for i in range(0, len(excelList)):
            featureClassListOut.append(locationName+"_"+excelList[i])
            featureClassList.append(locationName+"_"+excelList[i]+"T1")
            featureClassListJ.append(locationName+"_"+excelList[i]+"T2")
      
        baseLayer = locationName+"_Plots"
        for i in range(0, len(excelList)):
            if arcpy.Exists(excelList[i]):
                tableList = [excelList[i],baseLayer]
                print tableList
                fieldList = '#'        
                whereClause = baseLayer+".Exp_UnitID="+excelList[i]+".Exp_Unit_I"
                print whereClause
                keyField = '#'
                lyrName = excelList[i]+"_temp"
                # Make Query Table...
                arcpy.gp.MakeQueryTable_management(tableList, lyrName,"ADD_VIRTUAL_KEY_FIELD", keyField, fieldList, whereClause)
                print lyrName                
                arcpy.FeatureClassToFeatureClass_conversion(lyrName, arcpy.env.workspace, featureClassList[i])            
                fieldList = arcpy.ListFields(featureClassList[i])  #get a list of fields for each feature class
                j = 0
                for field in fieldList: #loop through each field               
                    # Split field name at _ symbol
                    if field.name.find("_OBJECTID") > -1:
                        arcpy.DeleteField_management(featureClassList[i], field.name)
                    elif field.name.find(baseLayer+"_Exp_UnitID") > -1:
                        arcpy.DeleteField_management(featureClassList[i], field.name)
                    else:                     
                        if field.name.find(excelList[i]) > -1:                           
                            indxb = len(excelList[i]) + 1
                            indxe = len(field.name)
                            nwstr = field.name[indxb:indxe]
                            print nwstr
                            #add NUOnet tables
                            if excelList[i] == "MeasGHGFlux":
                                arcpy.AlterField_management(featureClassList[i], field.name, ghgfluxList[j], ghgfluxList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasResidueMgnt":
                                arcpy.AlterField_management(featureClassList[i], field.name, harvestremovList[j], harvestremovList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasSoilPhys":
                                arcpy.AlterField_management(featureClassList[i], field.name, soilphysList[j], soilphysList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasSoilChem":
                                arcpy.AlterField_management(featureClassList[i], field.name, soilchemList[j], soilchemList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasSoilBiol":
                                arcpy.AlterField_management(featureClassList[i], field.name, soilbiolList[j], soilbiolList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasSoilCover":
                                arcpy.AlterField_management(featureClassList[i], field.name, soilcoverlist[j], soilcoverlist[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasHarvestFraction":
                                arcpy.AlterField_management(featureClassList[i], field.name, plantfractionList[j], plantfractionList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasBiomassCHO":
                                arcpy.AlterField_management(featureClassList[i], field.name, biomasschoList[j], biomasschoList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasBiomassEnergy":
                                arcpy.AlterField_management(featureClassList[i], field.name, biomassenergyList[j], biomassenergyList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasBiomassMinAn":
                                arcpy.AlterField_management(featureClassList[i], field.name, biomassminanList[j], biomassminanList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasGrazingPlants":
                                arcpy.AlterField_management(featureClassList[i], field.name, grazingplantsList[j], grazingplantsList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasSuppRes":
                                arcpy.AlterField_management(featureClassList[i], field.name, suppresList[j], suppresList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtAmendments":
                                arcpy.AlterField_management(featureClassList[i], field.name, amendmentsList[j], amendmentsList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtPlanting":
                                arcpy.AlterField_management(featureClassList[i], field.name, plantingList[j], plantingList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtTillage":
                                arcpy.AlterField_management(featureClassList[i], field.name, tillageList[j], tillageList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtGrowthStages":
                                arcpy.AlterField_management(featureClassList[i], field.name, growthstageList[j], growthstageList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtResidue":
                                arcpy.AlterField_management(featureClassList[i], field.name, residueList[j], residueList[j])                                
                                j = j + 1
                            elif excelList[i] == "MgtGrazing":
                                arcpy.AlterField_management(featureClassList[i], field.name, grazingList[j], grazingList[j])                                
                                j = j + 1
                            elif excelList[i] == "ExperUnits":
                                arcpy.AlterField_management(featureClassList[i], field.name, experunitsList[j], experunitsList[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasARGenes":
                                arcpy.AlterField_management(featureClassList[i], field.name, MeasARGenes[j], MeasARGenes[j])                                
                                j = j + 1 
                            elif excelList[i] == "MeasNutrEff":
                                arcpy.AlterField_management(featureClassList[i], field.name, MeasNutrEffList[j], MeasNutrEffList[j])                                
                                j = j + 1 
                            elif excelList[i] == "MeasYieldNutUptake":
                                arcpy.AlterField_management(featureClassList[i], field.name, YieldNutUptake[j], YieldNutUptake[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasGasNutrientLoss":
                                arcpy.AlterField_management(featureClassList[i], field.name, GasNutrientLoss[j], GasNutrientLoss[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasWaterQualityConc":
                                arcpy.AlterField_management(featureClassList[i], field.name, WaterQualityConc[j], WaterQualityConc[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasWaterQualityArea":
                                arcpy.AlterField_management(featureClassList[i], field.name, WaterQualityArea[j], WaterQualityArea[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasPlantMonitoring":
                                arcpy.AlterField_management(featureClassList[i], field.name, PlantMonitoring[j], PlantMonitoring[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasCropForageQuality":
                                arcpy.AlterField_management(featureClassList[i], field.name, CropForageQuality[j], CropForageQuality[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasNutrientCycling":
                                arcpy.AlterField_management(featureClassList[i], field.name, CropNutrientCycling[j], CropNutrientCycling[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasWindErosionConc":
                                arcpy.AlterField_management(featureClassList[i], field.name, WindErosionConc[j], WindErosionConc[j])                                
                                j = j + 1
                            elif excelList[i] == "MeasWindErosionArea":
                                arcpy.AlterField_management(featureClassList[i], field.name, WindErosionArea[j], WindErosionArea[j])                                
                                j = j + 1       
                            else:                            
                                print "Table does not exist"
                        if field.name.find(baseLayer) > -1:                                                   
                            j = 0
                            indxb = len(baseLayer) + 1
                            indxe = len(field.name)
                            nwstr = field.name[indxb:indxe]                                                
                            arcpy.AlterField_management(featureClassList[i], field.name, nwstr, nwstr)
                            
        for i in range(0, len(excelList)):
            if arcpy.Exists(excelList[i]):
               if excelList[i] != "ExperUnits":                
                    arcpy.MakeFeatureLayer_management(featureClassList[i], "temp")
                    arcpy.AddJoin_management("temp", "Treatment_ID", joinTreat, "Treatment_ID")
                    arcpy.AddJoin_management("temp", "Exp_Unit_ID", joinExp, "Exp_Unit_ID")
                    arcpy.CopyFeatures_management("temp", featureClassListOut[i])
                    dropFields = [joinTreat+"_OBJECTID", joinTreat+"_Treatment_ID",joinTreat+"_ORIG_FID", joinTreat+"_LOCATIONID",joinTreat+"_Full_Name", joinTreat+"_LocationName", joinExp+"_OBJECTID", joinExp+"_Exp_Unit_ID", joinExp+"_Treatment_ID", joinExp+"_Location", joinExp+"_LocationID", joinExp+"_County", joinExp+"_FullName", joinExp+"_Description", joinExp+"_LocationName", joinExp+"_State", joinExp+"_PLOT"]
                    arcpy.DeleteField_management(featureClassListOut[i], dropFields)
                    fieldList = arcpy.ListFields(featureClassListOut[i])  #get a list of fields for each feature class                
                    print featureClassListOut[i]
                    
        for i in range(0, len(excelList)):        
            arcpy.Delete_management(excelList[i])
            print excelList[i] + " deleted"
            if excelList[i] != "ExperUnits":            
                arcpy.Delete_management(featureClassList[i])
                print featureClassList[i] + " deleted"

        for i in range(0, len(excelListpt)):                
            arcpy.Delete_management(excelListpt[i])    
            print excelListpt[i] + " deleted"     

                 
except Exception as err:
    print(err.args[0])
