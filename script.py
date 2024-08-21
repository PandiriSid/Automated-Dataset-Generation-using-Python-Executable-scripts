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
effy_dataset_loc = Config_file_for_Datasets['effy_dataset_loc'].iloc[0]
new_metrics_loc = Config_file_for_Datasets['new_metrics_loc'].iloc[0]
old_metrics_new_name = Config_file_for_Datasets['old_metrics_new_name'].iloc[0]
year = Config_file_for_Datasets['Year'].iloc[0]


### Loading the data from sis dataset, herd, config, gss, c2021 and CIPMap2021 
sis_dataset = pd.read_csv(sis_dataset_loc)
print("Loaded the sis dataset")
herd_dataset = pd.read_csv(herd_dataset_loc, encoding='latin1')
print("Ladd the herd dataset")
gss_dataset = pd.read_excel(gss_dataset_loc, sheet_name='PD_NFR')
print("Loaded the gss dataset")
c_dataset = pd.read_csv(c_dataset_loc)
print("Laoded the c dataset")
cmap_dataset = pd.read_excel(cmap_dataset_loc)
print("Loaded the cmap dataset")
effy_dataset = pd.read_csv(effy_dataset_loc)
print("Loaded the effy dataset")



##### For calculating the Faculty & Sheet as per the formulas of the Readme.txt file
old_metrics_faculty = pd.read_excel(old_metrics_loc, sheet_name='Faculty & Staff')
print(old_metrics_faculty)

new_faculty_metrics = pd.DataFrame({'UNITID' : old_metrics_faculty['UNITID'],'NAME' : old_metrics_faculty["NAME"] })
print("Created a new metrics basdic template")
for unit_id in new_faculty_metrics['UNITID']:
    Professor = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==10), 'SISPROF'].values[0]
    Associate = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==10), 'SISASCP'].values[0]
    Assistant = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==10), 'SISASTP'].values[0]
    Total_Faculty = Professor + Associate + Assistant
    Tenured = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==20), 'SISTOTL'].values[0]
    Tenure_Track = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==30), 'SISTOTL'].values[0]
    Non_Tenure = sis_dataset.loc[(sis_dataset['UNITID']==unit_id) & (sis_dataset['FACSTAT']==40), 'SISTOTL'].values[0]

    temp = gss_dataset[(gss_dataset['UNITID']==unit_id) ]
    Post_Doctorates = sum(temp['pd_tot_all_races_v'])
    # Non_Faculty_Staff = sum(temp['nfr_tot_all_v'])
    Non_Faculty_Staff = sum(temp['nfr_tot_all_degr_v'])
    Total_Staff = Post_Doctorates + Non_Faculty_Staff

    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Fiscal Year'] = year
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Total Faculty'] = Total_Faculty
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Tenured'] = Tenured
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Tenure Track'] = Tenure_Track
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Non Tenure'] = Non_Tenure
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Professor'] = Professor
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Associate'] = Associate
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Assistant'] = Assistant
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Total Staff'] = Total_Staff
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Post Doctorates'] = Post_Doctorates
    new_faculty_metrics.loc[new_faculty_metrics['UNITID']==unit_id,'Non Faculty Staff'] = Non_Faculty_Staff
print(new_faculty_metrics)
new_faculty_metrics.to_csv(str(year)+'_Faculty_herd.csv', index=None)



###### For calculating the Enrollment sheet as per the formulas of the Readme.txt file
old_metrics_enrollment = pd.read_excel(old_metrics_loc, sheet_name='Enrollment')
print(old_metrics_enrollment)

new_enrollment_metrics = pd.DataFrame({'UNITID' : old_metrics_enrollment['UNITID'],'NAME' : old_metrics_enrollment["NAME"] })
print("Created a new Enrollment metrics basic template")
for unit_id in new_enrollment_metrics['UNITID']:
    #For Enrollment download EFFY2021:
    all_students = effy_dataset.loc[(effy_dataset['UNITID']==unit_id) & (effy_dataset['EFFYLEV']==1), 'EFYTOTLT'].values[0]
    Undergraduate = effy_dataset.loc[(effy_dataset['UNITID']==unit_id) & (effy_dataset['EFFYLEV']==2), 'EFYTOTLT'].values[0]
    graduate = effy_dataset.loc[(effy_dataset['UNITID']==unit_id) & (effy_dataset['EFFYLEV']==4), 'EFYTOTLT'].values[0]

    new_enrollment_metrics.loc[new_enrollment_metrics['UNITID']==unit_id,'Fiscal Year'] = year
    new_enrollment_metrics.loc[new_enrollment_metrics['UNITID']==unit_id,'All Students'] = all_students
    new_enrollment_metrics.loc[new_enrollment_metrics['UNITID']==unit_id,'Undergraduate'] = Undergraduate
    new_enrollment_metrics.loc[new_enrollment_metrics['UNITID']==unit_id,'Graduate'] = graduate

print(new_enrollment_metrics)
new_enrollment_metrics.to_csv(str(year)+'_enrollment_herd.csv', index=None)



###### For calculating the Completions sheet as per the formulas of the Readme.txt file
old_metrics_completions = pd.read_excel(old_metrics_loc, sheet_name='Completions')
print(old_metrics_completions)

new_completions_metrics = pd.DataFrame({'UNITID' : old_metrics_completions['UNITID'],'NAME' : old_metrics_completions["NAME"] })
print("Created a new Enrollment metrics basic template")
for unit_id in new_completions_metrics['UNITID']:
    bachelors_temp = c_dataset[(c_dataset['UNITID']==unit_id) & (c_dataset['AWLEVEL']==5) & (c_dataset['CIPCODE']==99)]
    bachelors = sum(bachelors_temp['CTOTALT'])
    masters_temp = c_dataset[(c_dataset['UNITID']==unit_id) & (c_dataset['AWLEVEL']==7) & (c_dataset['CIPCODE']==99)]
    masters = sum(masters_temp['CTOTALT'])
    total_research_doctorates_temp = c_dataset[(c_dataset['UNITID']==unit_id) & (c_dataset['AWLEVEL']==17) & (c_dataset['CIPCODE']==99)]
    total_research_doctorates = sum(total_research_doctorates_temp['CTOTALT'])

    new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'Fiscal Year'] = year
    new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,"Bachelor's Degree"] = bachelors
    new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,"Master's Degree"] = masters
    new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,"Total Research Doctorates"] = total_research_doctorates


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
                new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'Humanities (RD)'] = val_sum
            elif category==2:
                new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'Social Sciences (RD)'] = val_sum
            elif category==3:
                new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'STEM (RD)'] = val_sum
            elif category==4:
                new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'Other (RD)'] = val_sum
    else:
        new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'HUM_RSD'] = 0
        new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'SOCSC_RSD'] = 0
        new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'STEM_RSD'] = 0
        new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'OTHER_RSD'] = 0

    professional_doctorates_temp = c_dataset[(c_dataset['UNITID']==unit_id) & (c_dataset['AWLEVEL']==18) & (c_dataset['CIPCODE']==99)]
    professional_doctorates = sum(professional_doctorates_temp['CTOTALT'])
    new_completions_metrics.loc[new_completions_metrics['UNITID']==unit_id,'Professional Doctorate'] = professional_doctorates
new_completions_metrics.to_csv(str(year)+'_completions_herd.csv', index=None)




###### For calculating the Total R&D sheet as per the formulas of the Readme.txt file
old_metrics_total = pd.read_excel(old_metrics_loc, sheet_name='Total R&D')
print(old_metrics_total)

new_total_metrics = pd.DataFrame({'UNITID' : old_metrics_completions['UNITID'],'NAME' : old_metrics_completions["NAME"],'Fiscal Year': year })
print("Created a new Enrollment metrics basic template")
for unit_id in new_total_metrics['UNITID']:
    Total_Expenditures =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.g') & (herd_dataset['row']=='Total'), 'data'].iloc[0]    
    Extramural = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='03') & (herd_dataset['row']=='Total'), 'data'].iloc[0]
    Institutional = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.e') & (herd_dataset['row']=='Institution funds'), 'data'].iloc[0]
    Indirect_Cost_Recovery = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='12.f') & (herd_dataset['row']=='Indirect costs'), 'data'].iloc[0]

    new_total_metrics.loc[new_total_metrics['UNITID']==unit_id,'Total Expenditures(Thous)'] = Total_Expenditures
    new_total_metrics.loc[new_total_metrics['UNITID']==unit_id,'Extramural(Thous)'] = Extramural
    new_total_metrics.loc[new_total_metrics['UNITID']==unit_id,'Institutional(Thous)'] = Institutional
    new_total_metrics.loc[new_total_metrics['UNITID']==unit_id,'Indirect Cost Recovery(Thous)'] = Indirect_Cost_Recovery
new_total_metrics.to_csv(str(year)+'_total_R&D_herd.csv',index=None)



###### For calculating the Extramural R&D sheet as per the formulas of the Readme.txt file
old_metrics_extramural = pd.read_excel(old_metrics_loc, sheet_name='Extramural R&D')
print(old_metrics_extramural)

new_extramural_metrics = pd.DataFrame({'UNITID' : old_metrics_extramural['UNITID'],'NAME' : old_metrics_extramural["NAME"],'Fiscal Year': year })
print("Created a new Enrollment metrics basic template")
for unit_id in new_extramural_metrics['UNITID']:
    # Total_Expenditures =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.g') & (herd_dataset['row']=='Total'), 'data'].iloc[0]
    Federal_government =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.a') & (herd_dataset['row']=='Federal government'), 'data'].iloc[0]
    State_and_local_government =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.b') & (herd_dataset['row']=='State and local government'), 'data'].iloc[0]
    Business =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.c') & (herd_dataset['row']=='Business'), 'data'].iloc[0]
    Nonprofit_organizations =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.d') & (herd_dataset['row']=='Nonprofit organizations'), 'data'].iloc[0]
    All_other_sources =  herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='01.f') & (herd_dataset['row']=='All other sources'), 'data'].iloc[0]

    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'Total Expenditures(Thous)'] = Federal_government + State_and_local_government + Business + Nonprofit_organizations + All_other_sources
    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'Federal government'] = Federal_government
    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'State and local government(Thous)'] = State_and_local_government
    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'Business(Thous)'] = Business
    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'Nonprofit organizations(Thous)'] = Nonprofit_organizations
    new_extramural_metrics.loc[new_extramural_metrics['UNITID']==unit_id,'All other sources(Thous)'] = All_other_sources
new_extramural_metrics.to_csv(str(year)+'_extramural_herd.csv', index=None)



###### For calculating the Federal R&D sheet as per the formulas of the Readme.txt file
old_metrics_federal = pd.read_excel(old_metrics_loc, sheet_name='Federal R&D')
print(old_metrics_federal)

new_federal_metrics = pd.DataFrame({'UNITID' : old_metrics_federal['UNITID'],'NAME' : old_metrics_federal["NAME"], 'Fiscal Year': year, 'Federal R&D': old_metrics_federal['Federal R&D']})
print("Created a new Federal metrics basic template")
for unit_id in new_federal_metrics['UNITID'].unique():
    
    #Computer and information sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09A') & (herd_dataset['row']=='Computer and information sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Computer and information sciences'),'Other(Thous)'] = Other

    
    
    
    #Engineering:
    Total_Expenditures = herd_dataset.loc[((herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='Total')), 'data'].iloc[0]
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09B10') & (herd_dataset['row']=='Engineering, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Engineering'),'Other(Thous)'] = Other


    #Geosciences, atmospheric sciences, and ocean sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09C05') & (herd_dataset['row']=='Geosciences, atmospheric sciences, and ocean sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Geosciences, atmospheric sciences, and ocean sciences'),'Other(Thous)'] = Other


    #Life sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09D06') & (herd_dataset['row']=='Life sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Life sciences'),'Other(Thous)'] = Other


    #Mathematics and statistics:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09E') & (herd_dataset['row']=='Mathematics and statistics, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Mathematics and statistics'),'Other(Thous)'] = Other


    #Non-S&E:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09J09') & (herd_dataset['row']=='Non-S&E, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Non-S&E'),'Other(Thous)'] = Other


    #Other sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09I') & (herd_dataset['row']=='Other sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Other sciences'),'Other(Thous)'] = Other


    #Physical sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09F06') & (herd_dataset['row']=='Physical sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Physical sciences'),'Other(Thous)'] = Other


    #Psychology:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09G') & (herd_dataset['row']=='Psychology, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Psychology'),'Other(Thous)'] = Other


    #Social sciences:
    Total_Expenditures = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='Total'), 'data'].iloc[0]    
    USDA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='USDA'), 'data'].iloc[0]
    DoD = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='DOD'), 'data'].iloc[0]
    DoE = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='DOE'), 'data'].iloc[0]
    HHS = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='HHS'), 'data'].iloc[0]
    NASA = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='NASA'), 'data'].iloc[0]
    NSF = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='NSF'), 'data'].iloc[0]
    Other = herd_dataset.loc[(herd_dataset['ipeds_unitid']==unit_id) & (herd_dataset['questionnaire_no']=='09H06') & (herd_dataset['row']=='Social sciences, all') & (herd_dataset['column']=='Other agencies'), 'data'].iloc[0]

    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'Total Expenditures(Thous)'] = Total_Expenditures
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'USDA(Thous)'] = USDA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'DoD(Thous)'] = DoD
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'DoE(Thous)'] = DoE
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'HHS(Thous)'] = HHS
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'NASA(Thous)'] = NASA
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'NSF(Thous)'] = NSF
    new_federal_metrics.loc[(new_federal_metrics['UNITID']==unit_id) & (new_federal_metrics['Federal R&D']=='Social sciences'),'Other(Thous)'] = Other

new_federal_metrics.to_csv(str(year)+'_Federal_herd.csv', index=None)