import numpy as np # Linear algebra

# Data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd
from pandas import DataFrame

import xml.etree.ElementTree as ET # Reading xml files

import os

                        
def csv_row(xml_file):

    tree = ET.parse(xml_file)

    root = tree.getroot()

    nct_text = ""
    sum_text = ""
    model_text = ""
    ph_text = ""
    title_text = ""
    year_text = ""
    condition_disease_text= ""
    description_text = ""
    failed_text_full=""
    
    if root.iter('drop_withdraw_reason'):
        # Only iterates through Phase 2 and 3 studies
        for ph in root.iter('phase'):
            ph_text = ph.text
        if (ph_text == "Phase 2" or ph_text == "Phase 3"):
            for date in root.iter('start_date'):
                    year_text = date.text
            if ('2016' or '2017' or '2018' or '2019' or '2020') in year_text:

                #This bit finds all roots with nct_id which is a sub_root to id_info
                for nct in root.findall('id_info'):
                    nctId_text = nct.find('nct_id').text
                    nct_text =nctId_text
                    #print(nct_text)

                # This bit finds the brief summary text
                for s in root.findall('brief_summary'):
                    summary_text = s.find('textblock').text
                    sum_text= summary_text
                    sum_text = sum_text.replace('\n', '') # Replaces newline with a whitespace
                    sum_text = re.sub(' +',' ',sum_text) # Compresses multiple whitespaces to only one
                    #print("Summary Text:", sum_text)

                # Get's the official title for the study
                for t in root.iter('brief_title'):
                    title_text = t.text

                # This get's the type of intervention_model
                for y in root.iter('intervention_model'):
                    model_text = y.text

                for date in root.iter('start_date'):
                    year_text = date.text
                    #print(year_text)

                for condition in root.iter('condition'):
                    condition_disease_text = condition.text
                    #print(condition_disease_text)


                for reason in root.iter('drop_withdraw_reason'):
                    failed_text_full= failed_text_full+', ' +f'{reason[0].text}'
                #print("withdraw reason", failed_text_full)


    total_text = "\"" + nct_text+ "\"" + ";" + "\""+ ph_text+ "\"" + ";" + "\"" + condition_disease_text+ "\"" + ";" + "\""+ sum_text + "\"" + ";"  + "\"" + title_text + "\"" + ";"  +  "\"" + model_text + "\"" + ";" + "\""+ year_text + "\"" + ";" + "\""+ 'NOT COMPLETED BECAUSE OF' + failed_text_full+ "\""

    # This functions returns a text with Nct_Id, brief_summary, title and type of intervention model on the form we intended

    return total_text

#csv_row("/groups/cherkasvgrp/share/progressive_docking/pd_python_pose/clinical_trials/NCT0126xxxx/NCT01266460.xml")# This is for checking that the function works



rdir = '/groups/cherkasvgrp/share/progressive_docking/pd_python_pose/clinical_trials' # Folders in directory where the all the xml files are placed

with open('all_clincal_trials.csv', 'w', encoding="utf-8") as csvfile: # Opens a blank csv file
    for _, dirs, _ in os.walk(rdir):
        for dir in dirs: # Looks at  all the xml folders
            for subdir, _, files in os.walk(os.path.join(rdir,dir)):
                for file in files:
                    name = os.path.join(subdir, file)
                    csvfile.write(csv_row(name)) #Writes total_text into a row in to all_clinical_trials.csv
                    csvfile.write("\n") # Skips to next line and do the same
