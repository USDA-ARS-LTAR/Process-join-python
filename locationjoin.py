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
                            #print "Deleting " + field.name
                            arcpy.DeleteField_management(fc, field.name)
    sheets = arcpy.ListTables()
    excelListpt = []
    excelList = []
    for sheet in sheets:    
        out_table = sheet
        print "Redoing columns for " + sheet        
        outFc = sheet
        fcs = [out_gdb + "/" + outFc]   #sheet = data[1]                            
        if sheet == "WeatherDaily": #ok
            fld2Base = ["Temp_Max_d","Temp_Min_d","Precip_mm_","Bad_Value","RH__","Dew_Point","Wind_Speed","Solar_Radi","Solar_Ra_1","Soil_Temp","Soil_Tem_1","Wind_Direc","Open_Pan_E","Closed_Pan","Atmos_N_De","Total_Net","Snow_mm_d"]
            fld2New  = ["Temp_Max_d_1","Temp_Min_d_1","Precip_mm__1","Bad_Value_1","RH___1","Dew_Point_1","Wind_Speed_1","Solar_Radi_1","Solar_Ra_1_1","Soil_Temp_1","Soil_Tem_1_1","Wind_Direc_1","Open_Pan_E_1","Closed_Pan_1","Atmos_N_De_1","Total_Net_1","Snow_mm_d_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Bad_Value":
                        arcpy.AddField_management(fc,fld2New[i], "Integer", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "WeatherStation": #ok
            fld2Base = ["Weather_La","Weather_Lo","Weather_El","Distance_f","Direction","Weather__1"]
            fld2New  = ["Weather_La_1","Weather_Lo_1","Weather_El_1","Distance_f_1","Direction_1","Weather__1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Direction") or (fld2Base[i] == "Weather__1"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "Overview": #ok
            fld2Base = ["Duration_o"]
            fld2New  = ["Duration_o_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):                
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])        
        elif sheet == "ExperUnits": #ok
            fld2Base = ["Latitude","Longitude","Slope__","Exp_Unit_S"]
            fld2New  = ["Latitude_1","Longitude_1","Slope___1","Exp_Unit_S_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])                          
        elif sheet == "MeasSoilPhys": #ok           
            fld2Base = ["Upper_cm","Lower_cm","Model_if_s","Sand__","Silt__","Clay__","Bulk_Densi","Wilting_Po","Field_Capa","Ksat_cm_se","Moisture_R","Soil_Heat","Aggregatio","H2O_Stable","Near_Infra","Bulk_Den_1","Wilting__1","Field_Ca_1","Ksat_STD_c","Soil_Hea_1","Macro_Aggr","H2O_Stab_1","Near_Inf_1"]
            fld2New  = ["Upper_cm_1","Lower_cm_1","Model_if_s_1","Sand___1","Silt___1","Clay___1","Bulk_Densi_1","Wilting_Po_1","Field_Capa_1","Ksat_cm_se_1","Moisture_R_1","Soil_Heat_1","Aggregatio_1","H2O_Stable_1","Near_Infra_1","Bulk_Den_1_1","Wilting__1_1","Field_Ca_1_1","Ksat_STD_c_1","Soil_Hea_1_1","Macro_Aggr_1","H2O_Stab_1_1","Near_Inf_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Model_if_s":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])            
        elif sheet == "MeasSoilChem": #ok           
            fld2Base = ["Upper_cm","Lower_cm","Model_if_s","pH","TSC_gC_kg","TSN_gN_kg","Inorganic","Organic_C","Mineral_C","CEC_cmol_k","Electric_C","Soluble_C","NH4_mgN_kg","NO3_mgN_kg","P_mgP_kg","K_mgK_kg","Ca_mgCa_kg","Mg_mgMg_kg","Cu_mgCu_kg","Fe_mgFe_kg","Mn_mgMN_kg","Zn_mgZn_kg","Mineraliza","Nitrite_mg","Cesium_137","Lead_210_B","Beryllium_","pH_STD","TSC_STD_gC","TSN_STD_gN","Inorgani_1","Organic_ST","Mineral__1","CEC_STD_cm","Electric_1","Soluble__1","NH4_STD_mg","NO3_STD_mg","P_STD_mgP_","K_STD_mgK_","Ca_STD_mgC","Mg_STD_mgM","Cu_STD_mgC","Fe_STD_mgF","Mn_STD_mgM","Zn_STD_mgZ","Minerali_1","Nitrite_ST","Cesium_138","Lead_210_S","Beryllium1"]
            fld2New  = ["Upper_cm_1","Lower_cm_1","Model_if_s_1","pH_1","TSC_gC_kg_1","TSN_gN_kg_1","Inorganic_1","Organic_C_1","Mineral_C_1","CEC_cmol_k_1","Electric_C_1","Soluble_C_1","NH4_mgN_kg_1","NO3_mgN_kg_1","P_mgP_kg_1","K_mgK_kg_1","Ca_mgCa_kg_1","Mg_mgMg_kg_1","Cu_mgCu_kg_1","Fe_mgFe_kg_1","Mn_mgMN_kg_1","Zn_mgZn_kg_1","Mineraliza_1","Nitrite_mg_1","Cesium_137_1","Lead_210_B_1","Beryllium__1","pH_STD_1","TSC_STD_gC_1","TSN_STD_gN_1","Inorgani_1_1","Organic_ST_1","Mineral__1_1","CEC_STD_cm_1","Electric_1_1","Soluble__1_1","NH4_STD_mg_1","NO3_STD_mg_1","P_STD_mgP__1","K_STD_mgK__1","Ca_STD_mgC_1","Mg_STD_mgM_1","Cu_STD_mgC_1","Fe_STD_mgF_1","Mn_STD_mgM_1","Zn_STD_mgZ_1","Minerali_1_1","Nitrite_ST_1","Cesium_138_1","Lead_210_S_1","Beryllium1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Model_if_s":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSoilBiol": #ok
            fld2Base = ["Upper_cm","Lower_cm","Model_if_s","Glucosidas","Glucosamin","Acid_Phosp","Alk_Phosph","Fluorescei","Glomalin_g","FAME","PLFA","DNA","Iden_Plant","POM_gC_kg","Microbe_Bi","Microbe__1","Glucosid_1","Glucosam_1","Acid_Pho_1","Alk_Phos_1","Fluoresc_1","Glomalin_S","Iden_Pla_1","POM_STD_gC","Microbe__2","Microbe__3"]
            fld2New  = ["Upper_cm_1","Lower_cm_1","Model_if_s_1","Glucosidas_1","Glucosamin_1","Acid_Phosp_1","Alk_Phosph_1","Fluorescei_1","Glomalin_g_1","FAME_1","PLFA_1","DNA_1","Iden_Plant_1","POM_gC_kg_1","Microbe_Bi_1","Microbe__1_1","Glucosid_1_1","Glucosam_1_1","Acid_Pho_1_1","Alk_Phos_1_1","Fluoresc_1_1","Glomalin_S_1","Iden_Pla_1_1","POM_STD_gC_1","Microbe__2_1","Microbe__3_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "FAME":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "PLFA":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "DNA":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Model_if_s":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                        
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])                    
        elif sheet == "MeasResidueMgnt": #ok
            fld2Base = ["Corn_Ear_H","Above_G_Bi","Unit_Grain","Grain_Dry","Grain_Mois","Grain_C_kg","Grain_N_kg","Harv_NonGr","Harv_Res_M","Harv_Res_C","Harv_Res_N","NonHarv_No","NonHarv_Re","NonHarv__1","NonHarv__2","Root_Dry_M","Root_Moist","Root_C_kgC","Root_N_kgN","Corn_Ear_1","Above_G__1","Unit_Gra_1","Grain_Dr_1","Grain_Mo_1","Grain_C_ST","Grain_N_ST","Harv_Non_1","Harv_Res_1","Harv_Res_2","Harv_Res_3","NonHarv__3","NonHarv__4","NonHarv__5","NonHarv__6","Root_Dry_1","Root_Moi_1","Root_C_STD","Root_N_STD"]
            fld2New  = ["Corn_Ear_H_1","Above_G_Bi_1","Unit_Grain_1","Grain_Dry_1","Grain_Mois_1","Grain_C_kg_1","Grain_N_kg_1","Harv_NonGr_1","Harv_Res_M_1","Harv_Res_C_1","Harv_Res_N_1","NonHarv_No_1","NonHarv_Re_1","NonHarv__1_1","NonHarv__2_1","Root_Dry_M_1","Root_Moist_1","Root_C_kgC_1","Root_N_kgN_1","Corn_Ear_1_1","Above_G__1_1","Unit_Gra_1_1","Grain_Dr_1_1","Grain_Mo_1_1","Grain_C_ST_1","Grain_N_ST_1","Harv_Non_1_1","Harv_Res_1_1","Harv_Res_2_1","Harv_Res_3_1","NonHarv__3_1","NonHarv__4_1","NonHarv__5_1","NonHarv__6_1","Root_Dry_1_1","Root_Moi_1_1","Root_C_STD_1","Root_N_STD_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSoilCover": #ok
            fld2Base = ["Soil_w_Res"]
            fld2New  = ["Soil_w_Res_1"]          
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasHarvestFraction": #ok
            fld2Base = ["Frac_Dry_M","Frac_Moist","Frac_C_kgC","Frac_N_kgN","Grain_Weig","Frac_Dry_1","Frac_Moi_1","Frac_C_STD","Frac_N_STD","Frac_Dry_M","Frac_Moist","Frac_C_kgC","Frac_N_kgN","Grain_Weig","Frac_Dry_1","Frac_Moi_1","Frac_C_STD","Frac_N_STD","Frac_Dry_M","Frac_Moist","Frac_C_kgC","Frac_N_kgN","Grain_Weig","Frac_Dry_1","Frac_Moi_1","Frac_C_STD","Frac_N_STD","Grain_We_1"]
            fld2New  = ["Frac_Dry_M_1","Frac_Moist_1","Frac_C_kgC_1","Frac_N_kgN_1","Grain_Weig_1","Frac_Dry_1_1","Frac_Moi_1_1","Frac_C_STD_1","Frac_N_STD_1","Frac_Dry_M_1","Frac_Moist_1","Frac_C_kgC_1","Frac_N_kgN_1","Grain_Weig_1","Frac_Dry_1_1","Frac_Moi_1_1","Frac_C_STD_1","Frac_N_STD_1","Frac_Dry_M_1","Frac_Moist_1","Frac_C_kgC_1","Frac_N_kgN_1","Grain_Weig_1","Frac_Dry_1_1","Frac_Moi_1_1","Frac_C_STD_1","Frac_N_STD_1","Grain_We_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasBiomassMinAn": #ok           
            fld2Base = ["C_Concentr","N_Concentr","P_Concentr","K_Concentr","Ca_Concent","Mg_Concent","S_Concentr","Na_Concent","Cl_Concent","Al_Concent","B_Concentr","Cu_Concent","Fe_Concent","Mn_Concent","Zn_Concent","C_Concen_1","N_Concen_1","P_Concen_1","K_Concen_1","Ca_Conce_1","Mg_Conce_1","S_Concen_1","Na_Conce_1","Cl_Conce_1","Al_Conce_1","B_Concen_1","Cu_Conce_1","Fe_Conce_1","Mn_Conce_1","Zn_Conce_1"]
            fld2New  = ["C_Concentr_1","N_Concentr_1","P_Concentr_1","K_Concentr_1","Ca_Concent_1","Mg_Concent_1","S_Concentr_1","Na_Concent_1","Cl_Concent_1","Al_Concent_1","B_Concentr_1","Cu_Concent_1","Fe_Concent_1","Mn_Concent_1","Zn_Concent_1","C_Concen_1_1","N_Concen_1_1","P_Concen_1_1","K_Concen_1_1","Ca_Conce_1_1","Mg_Conce_1_1","S_Concen_1_1","Na_Conce_1_1","Cl_Conce_1_1","Al_Conce_1_1","B_Concen_1_1","Cu_Conce_1_1","Fe_Conce_1_1","Mn_Conce_1_1","Zn_Conce_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):                    
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")                    
                    arcpy.DeleteField_management(fc,fld2Base[i])
        elif sheet == "MgtAmendments": #ok
            fld2Base = ["Amend_Dept","Amend_Type","Total_Amen","Total_N_Am","Total_P_Am","Total_K_Am","Total_Pest","Active_Ing","Pest_Targe","Pest_Place","Irrigation","Irrigati_1","Irrigati_2"]
            fld2New  = ["Amend_Dept_1","Amend_Type_1","Total_Amen_1","Total_N_Am_1","Total_P_Am_1","Total_K_Am_1","Total_Pest_1","Active_Ing_1","Pest_Targe_1","Pest_Place_1","Irrigation_1","Irrigati_1_1","Irrigati_2_1"]
            for fc in fcs:
               for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Amend_Type":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Active_Ing":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Pest_Targe":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Pest_Place":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Irrigati_1":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MgtPlanting": #ok
            fld2Base = ["Planting_R","Planting_D","Planting_M","Planting_1","Row_Width"]
            fld2New  = ["Planting_R_1","Planting_D_1","Planting_M_1","Planting_1_1","Row_Width_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Planting_M":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MgtTillage": #ok
            fld2Base = ["Tillage__1","Tillage__2"]
            fld2New  = ["Tillage__1_1","Tillage__2_1"]
            for fc in fcs:
               for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Tillage__2":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasGHGFlux": #ok
            fld2Base = ["N2O_gN_ha_","N2O_Interp","CO2_gC_ha_","CO2_Interp","CH4_gC_ha_","CH4_Interp","Air_Temp_d","Soil_Temp","Soil_Moist","Soil_Moi_1","N2O_STD_gN","CO2_STD_gC","CH4_STD_gC","Air_Temp_S","Soil_Tem_1","Soil_Moi_2"]
            fld2New  = ["N2O_gN_ha__1","N2O_Interp_1","CO2_gC_ha__1","CO2_Interp_1","CH4_gC_ha__1","CH4_Interp_1","Air_Temp_d_1","Soil_Temp_1","Soil_Moist_1","Soil_Moi_1_1","N2O_STD_gN_1","CO2_STD_gC_1","CH4_STD_gC_1","Air_Temp_S_1","Soil_Tem_1_1","Soil_Moi_2_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MgtGrazing": #ok
            fld2Base = ["Stocking_R","Animal_Spe","Animal_Cla","Other_Even","Burn_Frequ","Burn_Inten"]
            fld2New  = ["Stocking_R_1","Animal_Spe_1","Animal_Cla_1","Other_Even_1","Burn_Frequ_1","Burn_Inten_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Animal_Spe":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Animal_Cla":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Other_Even":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")
                    elif fld2Base[i] == "Burn_Inten":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                    
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])   
        elif sheet == "MeasGrazingPlants": #ok
            fld2Base = ["AboveGr_Bi","Surface_Li","Standing_D","LAI_kg_ha","Biomass_N","Lignin__","Ground_Cov","AboveGr__1","AboveGr__2","BelowGr_Bi","BelowGr__1","ANPP_C_kgC","ANPP_N_kgN","BNPP_C_kgC","BNPP_N_kgN","AboveGr__3","Surface__1","Standing_1","LAI_STD_kg","Biomass__1","Lignin_STD","Ground_C_1","AboveGr__4","AboveGr__5","BelowGr__2","BelowGr__3","ANPP_C_STD","ANPP_N_STD","BNPP_C_STD","BNPP_N_STD"]
            fld2New  = ["AboveGr_Bi_1","Surface_Li_1","Standing_D_1","LAI_kg_ha_1","Biomass_N_1","Lignin___1","Ground_Cov_1","AboveGr__1_1","AboveGr__2_1","BelowGr_Bi_1","BelowGr__1_1","ANPP_C_kgC_1","ANPP_N_kgN_1","BNPP_C_kgC_1","BNPP_N_kgN_1","AboveGr__3_1","Surface__1_1","Standing_1_1","LAI_STD_kg_1","Biomass__1_1","Lignin_STD_1","Ground_C_1_1","AboveGr__4_1","AboveGr__5_1","BelowGr__2_1","BelowGr__3_1","ANPP_C_STD_1","ANPP_N_STD_1","BNPP_C_STD_1","BNPP_N_STD_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])        
        elif sheet == "MeasBiomassCHO":#ok
            fld2Base = ["Glucan_g_k","Xylan_g_kg","Galactan_g","Arabinan_g","Mannan_g_k","Lignin_g_k","Neutral_De","Acid_Det_F","Acid_Solub","Acid_Insol","Crude_Prot","Non_fiber","Ash_g_kg","Glucan_STD","Xylan_STD","Galactan_S","Arabinan_S","Mannan_STD","Lignin_STD","Neutral__1","Acid_Det_1","Acid_Sol_1","Acid_Ins_1","Crude_Pr_1","Non_fibe_1","Ash_STD_g_"]
            fld2New  = ["Glucan_g_k_1","Xylan_g_kg_1","Galactan_g_1","Arabinan_g_1","Mannan_g_k_1","Lignin_g_k_1","Neutral_De_1","Acid_Det_F_1","Acid_Solub_1","Acid_Insol_1","Crude_Prot_1","Non_fiber_1","Ash_g_kg_1","Glucan_STD_1","Xylan_STD_1","Galactan_S_1","Arabinan_S_1","Mannan_STD_1","Lignin_STD_1","Neutral__1_1","Acid_Det_1_1","Acid_Sol_1_1","Acid_Ins_1_1","Crude_Pr_1_1","Non_fibe_1_1","Ash_STD_g__1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])

        elif sheet == "MeasBiomassEnergy": #ok
            fld2Base = ["Volatile_M","Mineral_Ma","Gross_Calo","Volatile_1","Ash_STD_g_","Gross_Ca_1"]
            fld2New  = ["Volatile_M_1","Mineral_Ma_1","Gross_Calo_1","Volatile_1_1","Ash_STD_g__1","Gross_Ca_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MgtResidue": #ok
            fld2Base = ["Cutting_He","Rows_Harve","Stand_Age","Stage_at_H"]
            fld2New  = ["Cutting_He_1","Rows_Harve_1","Stand_Age_1","Stage_at_H_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Stage_at_H":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasSuppRes": #ok
            fld2Base = ["Measuremen","Measurem_1"]
            fld2New  = ["Measuremen_1","Measurem_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if fld2Base[i] == "Measurem_1":
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasARGenes": #ok
            fld2Base = ["Upper","Lower","Target","Presence_o","Value","Units"]
            fld2New  = ["Upper_1","Lower_1","Target_1","Presence_o_1","Value_1","Units_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Presence_o") or (fld2Base[i] == "Units"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasNutrEff": #ok
            fld2Base = ["Fraction_N","Nitrogen_U","Agronomic","Nutrient_e","Nitrogen15"]
            fld2New  = ["Fraction_N_1","Nitrogen_U_1","Agronomic_1","Nutrient_e_1","Nitrogen15_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasCropForageQuality": #ok
            fld2Base = ["Value","Unit","Chemical_C","Value_STD"]
            fld2New  = ["Value_1","Unit_1","Chemical_C_1","Value_STD_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Chemical_C") or (fld2Base[i] == "Unit"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasGasNutrientLoss": #ok
            fld2Base = ["NOx_N_g_ha","N2_N_g_ha_","N2O_N_g_ha","NH3_N_kg_h","NOx_N_STD","N2_N_STD_g","N2O_N_STD","NH3_N_STD"]
            fld2New  = ["NOx_N_g_ha_1","N2_N_g_ha__1","N2O_N_g_ha_1","NH3_N_kg_h_1","NOx_N_STD_1","N2_N_STD_g_1","N2O_N_STD_1","NH3_N_STD_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasPlantMonitoring": #ok
            fld2Base = ["Test_Value","Test_Units","Crop_Monit","Test_Val_1"]
            fld2New  = ["Test_Value_1","Test_Units_1","Crop_Monit_1","Test_Val_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Crop_Monit") or (fld2Base[i] == "Test_Units"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasYieldNutUptake": #ok
            fld2Base = ["Frac_Dry_M","Frac_Moist","Frac_C_kgC","Frac_N_kgN","Frac_P_kgP","Frac_K_kgK","Frac_S_kgS","Frac_Ca_kg","Frac_Mg_kg","Frac_Cu_gC","Frac_Fe_gF","Frac_Mn_gM","Frac_Zn_gZ","Frac_B_gB_","Frac_Mo_gM","Grain_Weig","Frac_Dry_1","Frac_Moi_1","Frac_C_STD","Frac_N_STD","Frac_P_STD","Frac_K_STD","Frac_S_STD","Frac_Ca_ST","Frac_Mg_ST","Frac_Cu_ST","Frac_Fe_ST","Frac_Mn_ST","Frac_Zn_ST","Frac_B_STD","Frac_Mo_ST","Grain_We_1"]
            fld2New  = ["Frac_Dry_M_1","Frac_Moist_1","Frac_C_kgC_1","Frac_N_kgN_1","Frac_P_kgP_1","Frac_K_kgK_1","Frac_S_kgS_1","Frac_Ca_kg_1","Frac_Mg_kg_1","Frac_Cu_gC_1","Frac_Fe_gF_1","Frac_Mn_gM_1","Frac_Zn_gZ_1","Frac_B_gB__1","Frac_Mo_gM_1","Grain_Weig_1","Frac_Dry_1_1","Frac_Moi_1_1","Frac_C_STD_1","Frac_N_STD_1","Frac_P_STD_1","Frac_K_STD_1","Frac_S_STD_1","Frac_Ca_ST_1","Frac_Mg_ST_1","Frac_Cu_ST_1","Frac_Fe_ST_1","Frac_Mn_ST_1","Frac_Zn_ST_1","Frac_B_STD_1","Frac_Mo_ST_1","Grain_We_1_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasNutrientCycling": # test
            fld2Base = ["Corn_Ear_H","Above_G_Bi","Unit_Grain","Grain_Dry","Grain_Mois","Grain_C_kg","Grain_N_kg","Grain_P_kg","Grain_K_kg","Grain_S_kg","Grain_Ca_k","Grain_Mg_k","Grain_Cu_g","Grain_Fe_g","Grain_Mn_g","Grain_Zn_g","Grain_B_gB","Grain_Mo_g","Harv_NonGr","Harv_Res_M","Harv_Res_C","Harv_Res_N","Harv_Res_P","Harv_Res_K","Harv_Res_S","Harv_Res_1","Harv_Res_2","Harv_Res_3","Harv_Res_F","Harv_Res_4","Harv_Res_Z","Harv_Res_B","Harv_Res_5","NonHarv_No","NonHarv_Re","NonHarv__1","NonHarv__2","nonHarv__3","nonHarv__4","nonHarv__5","nonHarv__6","nonHarv__7","nonHarv__8","nonHarv__9","nonHarv_10","nonHarv_11","nonHarv_12","nonHarv_13","Corn_Ear_1","Above_Grou","Unit_Gra_1","Grain_DryM","Grain_Mo_1","Grain_C_ST","Grain_N_ST","Grain_P_ST","Grain_K_ST","Grain_S_ST","Grain_Ca_S","Grain_Mg_S","Grain_Cu_S","Grain_Fe_S","Grain_Mn_S","Grain_Zn_S","Grain_B_ST","Grain_Mo_S","Harv_Res_D","HarvRes_Mo","Harv_Res_6","Harv_Res_7","Harv_Res_8","Harv_Res_9","Harv_Re_10","Harv_Re_11","Harv_Re_12","Harv_Re_13","Harv_Re_14","Harv_Re_15","Harv_Re_16","Harv_Re_17","Harv_Re_18","nonHarv_14","nonHarv_15","nonHarv_16","nonHarv_17","nonHarv_18","nonHarv_19","nonHarv_20","nonHarv_21","nonHarv_22","nonHarv_23","nonHarv_24","nonHarv_25","nonHarv_26","nonHarv_27","nonHarv_28"]
            fld2New  = ["Corn_Ear_H_1","Above_G_Bi_1","Unit_Grain_1","Grain_Dry_1","Grain_Mois_1","Grain_C_kg_1","Grain_N_kg_1","Grain_P_kg_1","Grain_K_kg_1","Grain_S_kg_1","Grain_Ca_k_1","Grain_Mg_k_1","Grain_Cu_g_1","Grain_Fe_g_1","Grain_Mn_g_1","Grain_Zn_g_1","Grain_B_gB_1","Grain_Mo_g_1","Harv_NonGr_1","Harv_Res_M_1","Harv_Res_C_1","Harv_Res_N_1","Harv_Res_P_1","Harv_Res_K_1","Harv_Res_S_1","Harv_Res_1_1","Harv_Res_2_1","Harv_Res_3_1","Harv_Res_F_1","Harv_Res_4_1","Harv_Res_Z_1","Harv_Res_B_1","Harv_Res_5_1","NonHarv_No_1","NonHarv_Re_1","NonHarv__1_1","NonHarv__2_1","nonHarv__3_1","nonHarv__4_1","nonHarv__5_1","nonHarv__6_1","nonHarv__7_1","nonHarv__8_1","nonHarv__9_1","nonHarv_10_1","nonHarv_11_1","nonHarv_12_1","nonHarv_13_1","Corn_Ear_1_1","Above_Grou_1","Unit_Gra_1_1","Grain_DryM_1","Grain_Mo_1_1","Grain_C_ST_1","Grain_N_ST_1","Grain_P_ST_1","Grain_K_ST_1","Grain_S_ST_1","Grain_Ca_S_1","Grain_Mg_S_1","Grain_Cu_S_1","Grain_Fe_S_1","Grain_Mn_S_1","Grain_Zn_S_1","Grain_B_ST_1","Grain_Mo_S_1","Harv_Res_D_1","HarvRes_Mo_1","Harv_Res_6_1","Harv_Res_7_1","Harv_Res_8_1","Harv_Res_9_1","Harv_Re_10_1","Harv_Re_11_1","Harv_Re_12_1","Harv_Re_13_1","Harv_Re_14_1","Harv_Re_15_1","Harv_Re_16_1","Harv_Re_17_1","Harv_Re_18_1","nonHarv_14_1","nonHarv_15_1","nonHarv_16_1","nonHarv_17_1","nonHarv_18_1","nonHarv_19_1","nonHarv_20_1","nonHarv_21_1","nonHarv_22_1","nonHarv_23_1","nonHarv_24_1","nonHarv_25_1","nonHarv_26_1","nonHarv_27_1","nonHarv_28_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWaterQualityArea": #ok
            fld2Base = ["Sampling_D","Losses_or","Erosion_Me","Erosion_t","Erosion_To","Erosion__1","Soil_organ","Soil_org_1","Water_mm","kg_total_N","kg_total_P","kg_NH4_N_h","kg_NO3_N_h","Total_Diss","Total_Di_1","kg_total_C","pH","EC_mS_cm","Dissolved","Dissolve_1","Dissolve_2","Dissolve_3","Dissolve_4","Dissolve_5","Dissolve_6","Dissolve_7","Dissolve_8","Dissolve_9","Dissolv_10","Dissolv_11","Dissolv_12","Erosion__2","Erosion__3","Erosion__4","Soil_org_2","Soil_org_3","Water_mm_S","kg_total_1","kg_total_2","kg_NH4_N_1","kg_NO3_N_1","Total_Di_2","Total_Di_3","kg_total_3","pH_STD","EC_mS_cm_S","Dissolv_13","Dissolv_14","Dissolv_15","Dissolv_16","Dissolv_17","Dissolv_18","Dissolv_19","Dissolv_20","Dissolv_21","Dissolv_22","Dissolv_23","Dissolv_24","Dissolv_25"]
            fld2New  = ["Sampling_D_1","Losses_or_1","Erosion_Me_1","Erosion_t_1","Erosion_To_1","Erosion__1_1","Soil_organ_1","Soil_org_1_1","Water_mm_1","kg_total_N_1","kg_total_P_1","kg_NH4_N_h_1","kg_NO3_N_h_1","Total_Diss_1","Total_Di_1_1","kg_total_C_1","pH_1","EC_mS_cm_1","Dissolved_1","Dissolve_1_1","Dissolve_2_1","Dissolve_3_1","Dissolve_4_1","Dissolve_5_1","Dissolve_6_1","Dissolve_7_1","Dissolve_8_1","Dissolve_9_1","Dissolv_10_1","Dissolv_11_1","Dissolv_12_1","Erosion__2_1","Erosion__3_1","Erosion__4_1","Soil_org_2_1","Soil_org_3_1","Water_mm_S_1","kg_total_1_1","kg_total_2_1","kg_NH4_N_1_1","kg_NO3_N_1_1","Total_Di_2_1","Total_Di_3_1","kg_total_3_1","pH_STD_1","EC_mS_cm_S_1","Dissolv_13_1","Dissolv_14_1","Dissolv_15_1","Dissolv_16_1","Dissolv_17_1","Dissolv_18_1","Dissolv_19_1","Dissolv_20_1","Dissolv_21_1","Dissolv_22_1","Dissolv_23_1","Dissolv_24_1","Dissolv_25_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Losses_or") or (fld2Base[i] == "Erosion_Me"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWaterQualityConc": #ok
            fld2Base = ["Sampling_D","Losses_or","Erosion_Me","Erosion_kg","Erosion_To","Erosion__1","Soil_organ","Soil_org_1","Water_mm","mg_total_N","mg_Total_P","mg_NH4_N_L","mg_NO3_N_L","Total_Diss","Total_Di_1","mg_Cl_L","pH","EC_mS_cm","Dissolved","Dissolve_1","Dissolve_2","Dissolve_3","Dissolve_4","Dissolve_5","Dissolve_6","Dissolve_7","Dissolve_8","Dissolve_9","Dissolv_10","Dissolv_11","Dissolv_12","Erosion__2","Erosion__3","Erosion__4","Soil_org_2","Soil_org_3","Water_mm_S","mg_total_1","mg_total_2","mg_NH4_N_1","mg_NO3_N_1","Total_Di_2","Total_Di_3","mg_total_C","pH_STD","EC_mS_cm_S","Dissolv_13","Dissolv_14","Dissolv_15","Dissolv_16","Dissolv_17","Dissolv_18","Dissolv_19","Dissolv_20","Dissolv_21","Dissolv_22","Dissolv_23","Dissolv_24","Dissolv_25"]
            fld2New  = ["Sampling_D_1","Losses_or_1","Erosion_Me_1","Erosion_kg_1","Erosion_To_1","Erosion__1_1","Soil_organ_1","Soil_org_1_1","Water_mm_1","mg_total_N_1","mg_Total_P_1","mg_NH4_N_L_1","mg_NO3_N_L_1","Total_Diss_1","Total_Di_1_1","mg_Cl_L_1","pH_1","EC_mS_cm_1","Dissolved_1","Dissolve_1_1","Dissolve_2_1","Dissolve_3_1","Dissolve_4_1","Dissolve_5_1","Dissolve_6_1","Dissolve_7_1","Dissolve_8_1","Dissolve_9_1","Dissolv_10_1","Dissolv_11_1","Dissolv_12_1","Erosion__2_1","Erosion__3_1","Erosion__4_1","Soil_org_2_1","Soil_org_3_1","Water_mm_S_1","mg_total_1_1","mg_total_2_1","mg_NH4_N_1_1","mg_NO3_N_1_1","Total_Di_2_1","Total_Di_3_1","mg_total_C_1","pH_STD_1","EC_mS_cm_S_1","Dissolv_13_1","Dissolv_14_1","Dissolv_15_1","Dissolv_16_1","Dissolv_17_1","Dissolv_18_1","Dissolv_19_1","Dissolv_20_1","Dissolv_21_1","Dissolv_22_1","Dissolv_23_1","Dissolv_24_1","Dissolv_25_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):
                    if (fld2Base[i] == "Losses_or") or (fld2Base[i] == "Erosion_Me"):
                        arcpy.AddField_management(fc,fld2New[i], "Text", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")                                  
                    else:
                        arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWindErosionArea": #ok
            fld2Base = ["Soil_t_ha","Soil_organ","Soil_org_1","pH","EC_mS_cm","kg_total_N","kg_NH4_N_h","kg_NO3_N_h","kg_total_P","kg_K_ha","kg_S_ha","kg_Ca_ha","kg_Mg_ha","g_Cu_ha","g_Fe_ha","g_Mn_ha","g_Zn_ha","g_B_ha","g_Mo_ha","kg_Al_ha","kg_Na_ha","kg_Si_ha","Soil_t_h_1","Soil_org_2","Soil_org_3","pH_STD","EC_mS_cm_S","kg_total_1","kg_NH4_N_1","kg_NO3_N_1","kg_total_2","kg_K_ha_ST","kg_S_ha_ST","kg_Ca_ha_S","kg_Mg_ha_S","g_Cu_ha_ST","g_Fe_ha_ST","g_Mn_ha_ST","g_Zn_ha_ST","g_B_ha_STD","g_Mo_ha_ST","kg_Al_ha_S","kg_Na_ha_S","kg_Si_ha_S"]
            fld2New  = ["Soil_t_ha_1","Soil_organ_1","Soil_org_1_1","pH_1","EC_mS_cm_1","kg_total_N_1","kg_NH4_N_h_1","kg_NO3_N_h_1","kg_total_P_1","kg_K_ha_1","kg_S_ha_1","kg_Ca_ha_1","kg_Mg_ha_1","g_Cu_ha_1","g_Fe_ha_1","g_Mn_ha_1","g_Zn_ha_1","g_B_ha_1","g_Mo_ha_1","kg_Al_ha_1","kg_Na_ha_1","kg_Si_ha_1","Soil_t_h_1_1","Soil_org_2_1","Soil_org_3_1","pH_STD_1","EC_mS_cm_S_1","kg_total_1_1","kg_NH4_N_1_1","kg_NO3_N_1_1","kg_total_2_1","kg_K_ha_ST_1","kg_S_ha_ST_1","kg_Ca_ha_S_1","kg_Mg_ha_S_1","g_Cu_ha_ST_1","g_Fe_ha_ST_1","g_Mn_ha_ST_1","g_Zn_ha_ST_1","g_B_ha_STD_1","g_Mo_ha_ST_1","kg_Al_ha_S_1","kg_Na_ha_S_1","kg_Si_ha_S_1"]
            for fc in fcs:
                for i in range(0, len(fld2Base)):            
                    arcpy.AddField_management(fc,fld2New[i], "Double", "", "", "", fld2New[i], "NULLABLE", "NON_REQUIRED")         
                    arcpy.CalculateField_management(fc,fld2New[i],"["+fld2Base[i]+"]")
                    arcpy.DeleteField_management(fc, fld2Base[i])
        elif sheet == "MeasWindErosionConc": #ok
            fld2Base = ["Soil_t","Soil_organ","Soil_org_1","pH","EC_mS_cm","mg_N_kg","mg_NH4_N_k","mg_NO3_N_k","mg_P_kg","mg_K_kg","mg_S_kg","mg_Ca_kg","mg_Mg_kg","ug_Cu_kg","ug_Fe_kg","ug_Mn_kg","ug_Zn_kg","ug_B_kg","ug_Mo_kg","mg_Al_kg","mg_Na_kg","mg_Si_kg","Soil_t_STD","Soil_org_2","Soil_org_3","pH_STD","EC_mS_cm_S","mg_N_kg_ST","mg_NH4_N_1","mg_NO3_N_1","mg_P_kg_ST","mg_K_kg_ST","mg_S_kg_ST","mg_Ca_kg_S","mg_Mg_kg_S","ug_Cu_kg_S","ug_Fe_kg_S","ug_Mn_kg_S","ug_Zn_kg_S","ug_B_kg_ST","ug_Mo_kg_S","mg_Al_kg_S","mg_Na_kg_S","mg_Si_kg_S"]
            fld2New  = ["Soil_t_1","Soil_organ_1","Soil_org_1_1","pH_1","EC_mS_cm_1","mg_N_kg_1","mg_NH4_N_k_1","mg_NO3_N_k_1","mg_P_kg_1","mg_K_kg_1","mg_S_kg_1","mg_Ca_kg_1","mg_Mg_kg_1","ug_Cu_kg_1","ug_Fe_kg_1","ug_Mn_kg_1","ug_Zn_kg_1","ug_B_kg_1","ug_Mo_kg_1","mg_Al_kg_1","mg_Na_kg_1","mg_Si_kg_1","Soil_t_STD_1","Soil_org_2_1","Soil_org_3_1","pH_STD_1","EC_mS_cm_S_1","mg_N_kg_ST_1","mg_NH4_N_1_1","mg_NO3_N_1_1","mg_P_kg_ST_1","mg_K_kg_ST_1","mg_S_kg_ST_1","mg_Ca_kg_S_1","mg_Mg_kg_S_1","ug_Cu_kg_S_1","ug_Fe_kg_S_1","ug_Mn_kg_S_1","ug_Zn_kg_S_1","ug_B_kg_ST_1","ug_Mo_kg_S_1","mg_Al_kg_S_1","mg_Na_kg_S_1","mg_Si_kg_S_1"]
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
