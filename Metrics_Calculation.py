import pandas as pd 
import numpy as np 
import warnings
import os
# from src.config import old_metrics_loc, sis_dataset_loc, herd_dataset_loc, config_dataset_loc, gss_dataset_loc,c_dataset_loc, cmap_dataset_loc, new_metrics_loc, old_metrics_new_name
warnings.filterwarnings("ignore")


Config_file_for_Datasets = pd.read_excel(r"Datasets\Config.xlsx", sheet_name="Config_file_for_Datasets")
Config_file_for_UnitId = pd.read_excel(r"Datasets\Config.xlsx", sheet_name="Config_file_for_UnitId")
old_metrics_loc = Config_file_for_Datasets['old_metrics_loc'].iloc[0]
sis_dataset_loc = Config_file_for_Datasets['sis_dataset_loc'].iloc[0]
herd_dataset_loc = Config_file_for_Datasets['herd_dataset_loc'].iloc[0]
gss_dataset_loc = Config_file_for_Datasets['gss_dataset_loc'].iloc[0]
c_dataset_loc = Config_file_for_Datasets['c_dataset_loc'].iloc[0]
cmap_dataset_loc = Config_file_for_Datasets['cmap_dataset_loc'].iloc[0]
new_metrics_loc = Config_file_for_Datasets['new_metrics_loc'].iloc[0]
old_metrics_new_name = Config_file_for_Datasets['old_metrics_new_name'].iloc[0]


old_metrics = pd.read_excel(old_metrics_loc)
print(old_metrics)

new_metrics = pd.DataFrame({'UNITID' : old_metrics['UNITID'],'NAME' : old_metrics["NAME"],'Peers' : old_metrics['Peers'] })
print("Created a new metrics basdic template")
### Loading the data from sis dataset, herd, config, gss, c2021 and CIPMap2021 
sis_dataset = pd.read_csv(sis_dataset_loc)
print("Loaded the sis dataset")
herd_dataset = pd.read_csv(herd_dataset_loc, encoding='latin1')
print("Ladd the herd dataset")
gss_dataset = pd.read_excel(gss_dataset_loc,sheet_name='PD_NFR')
print("Loaded the gss dataset")
c_dataset = pd.read_csv(c_dataset_loc)
print("Laoded the c dataset")
cmap_dataset = pd.read_excel(cmap_dataset_loc)
print("Loaded the cmap dataset")

    
for unit_id in new_metrics['UNITID']:
    print("Working with unit_id: ",unit_id)
    #For each unitid, need to sisprof(professor) + sisascp(associate professor) + sisastp(assistantprofessor) columns for Facnum column
    if unit_id in sis_dataset['UNITID'].unique():
        temp = sis_dataset[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==10)]
        temp_value = temp['SISPROF']+temp['SISASCP']+temp['SISASTP']
        temp_value = int(temp_value)
        new_metrics.loc[new_metrics['UNITID']==unit_id,'FACNUM'] = temp_value
    else:
        print("*****************************This unit id is not found in sis dataset**********:",unit_id)
        continue

    #From Herd dataset, Se total = need to 1.g, 09J09, 11J09 , row=Total and Non-se total = need to 1.g, 09J09, 11J09, column=Total
    if unit_id in herd_dataset['ipeds_unitid'].unique():
        se = herd_dataset[(herd_dataset['ipeds_unitid']==unit_id) & ((herd_dataset['questionnaire_no']=='01.g') | (herd_dataset['questionnaire_no']=='09J09') | (herd_dataset['questionnaire_no']=='11J09')) & (herd_dataset['row']=='Total')]
        non_se = herd_dataset[(herd_dataset['ipeds_unitid']==unit_id) & ((herd_dataset['questionnaire_no']=='01.g') | (herd_dataset['questionnaire_no']=='09J09') | (herd_dataset['questionnaire_no']=='11J09')) & (herd_dataset['column']=='Total')]
        se_total = sum(se['data'])
        non_se_total = sum(non_se['data'])
        new_metrics.loc[new_metrics['UNITID']==unit_id, 'S&ER&D'] = se_total-non_se_total
        new_metrics.loc[new_metrics['UNITID']==unit_id,'NONS&ER&D'] = non_se_total
    elif unit_id in Config_file_for_UnitId['UNITID'].values:
        inst_id = Config_file_for_UnitId.loc[Config_file_for_UnitId['UNITID']==unit_id,'inst_id'].values[0]
        se = herd_dataset[(herd_dataset['inst_id']==inst_id) & ((herd_dataset['questionnaire_no']=='01.g') | (herd_dataset['questionnaire_no']=='09J09') | (herd_dataset['questionnaire_no']=='11J09')) & (herd_dataset['row']=='Total')]
        non_se = herd_dataset[(herd_dataset['inst_id']==inst_id) & ((herd_dataset['questionnaire_no']=='01.g') | (herd_dataset['questionnaire_no']=='09J09') | (herd_dataset['questionnaire_no']=='11J09')) & (herd_dataset['column']=='Total')]
        se_total = sum(se['data'])
        non_se_total = sum(non_se['data'])
        new_metrics.loc[new_metrics['UNITID']==unit_id, 'S&ER&D'] = se_total-non_se_total
        new_metrics.loc[new_metrics['UNITID']==unit_id,'NONS&ER&D'] = non_se_total
        new_metrics.loc[new_metrics['UNITID']==unit_id,'NONS&ER&D'] = se_total
    else:
        new_metrics.loc[new_metrics['UNITID']==unit_id, 'S&ER&D'] = np.nan
        new_metrics.loc[new_metrics['UNITID']==unit_id,'NONS&ER&D'] = np.nan


    #Code to calculate the NFR Staff column from the Gss dataset with the PD_NFR sheet name and sum of pd_tot_all_races_v and nfr_tot_all_v columns
    temp = gss_dataset[(gss_dataset['UNITID']==unit_id) ]
    temp_value = sum(temp['pd_tot_all_races_v'])+sum(temp['nfr_tot_all_v'])
    # temp_value = sum(temp['pd_tot_all_races_v'])+sum(temp['nfr_tot_all_degr_v'])
    temp_value = int(temp_value)
    new_metrics.loc[new_metrics['UNITID']==unit_id,'PDNFRSTAFF'] = temp_value
    new_metrics.loc[new_metrics['UNITID']==unit_id,'PostDoc'] = int(sum(temp['pd_tot_all_races_v']))

    #Code to calculate the humanities, SOCSC, STEM and other columns for AWlevel=17
    temp = c_dataset[(c_dataset['UNITID']==unit_id) & (c_dataset['AWLEVEL']==17)]
    if not temp.empty:
        #For all the cipcodes, try to see the grad categories from cmap dataset and store this in the cip dataset
        for cip in temp['CIPCODE']:
            if not cmap_dataset.loc[( cmap_dataset['CIPCD'] == cip),'GradCat'].empty:
                dept_val = cmap_dataset.loc[( cmap_dataset['CIPCD'] == cip),'GradCat'].iloc[0]
                temp.loc[temp['CIPCODE']==cip,'Grad_Cat'] = dept_val
        # Now map all the same department category and try to find the sum of all the Ctotal column values
        for category in [1,2,3,4]:
            val = temp.loc[temp['Grad_Cat']==category,'CTOTALT']
            if not val.empty:
                val_sum = val.sum()
            else:
                val_sum = 0
            if category==1:
                new_metrics.loc[new_metrics['UNITID']==unit_id,'HUM_RSD'] = val_sum
            elif category==2:
                new_metrics.loc[new_metrics['UNITID']==unit_id,'SOCSC_RSD'] = val_sum
            elif category==3:
                new_metrics.loc[new_metrics['UNITID']==unit_id,'STEM_RSD'] = val_sum
            elif category==4:
                new_metrics.loc[new_metrics['UNITID']==unit_id,'OTHER_RSD'] = val_sum
    else:
        new_metrics.loc[new_metrics['UNITID']==unit_id,'HUM_RSD'] = 0
        new_metrics.loc[new_metrics['UNITID']==unit_id,'SOCSC_RSD'] = 0
        new_metrics.loc[new_metrics['UNITID']==unit_id,'STEM_RSD'] = 0
        new_metrics.loc[new_metrics['UNITID']==unit_id,'OTHER_RSD'] = 0
    


test = new_metrics['FACNUM']==old_metrics['FACNUM']
print(sum(test==True),sum(test==False))
test = new_metrics['NONS&ER&D']==old_metrics['NONS&ER&D']
print(sum(test==True),sum(test==False))
test = new_metrics['S&ER&D']==old_metrics['S&ER&D']
print(sum(test==True),sum(test==False))
test = new_metrics['PDNFRSTAFF']==old_metrics['PDNFRSTAFF']
print(sum(test==True),sum(test==False))
test = new_metrics['HUM_RSD']==old_metrics['HUM_RSD']
print(sum(test==True),sum(test==False))
test = new_metrics['SOCSC_RSD']==old_metrics['SOCSC_RSD']
print(sum(test==True),sum(test==False))
test = new_metrics['STEM_RSD']==old_metrics['STEM_RSD']
print(sum(test==True),sum(test==False))
test = new_metrics['OTHER_RSD']==old_metrics['OTHER_RSD']
print(sum(test==True),sum(test==False))
print(new_metrics)

### convert this and save to a csv file
new_metrics.to_csv(new_metrics_loc,index=None)
### Change the original carnegie file to source name
# os.rename(old_metrics_loc, old_metrics_new_name)