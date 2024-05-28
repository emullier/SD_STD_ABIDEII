# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 17:25:36 2023

@author: emeli
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import subprocess
import os
import numpy as np
import shutil
import pandas as pd
import time


original_HD_dir = r'E:/RESEARCH_NEW/ABIDEII_BIDS'
local_dir = r'C:/Users/emeli/Documents/tmp_processing' 
fs_path = r'C:/Users/emeli/Documents/TOOLS/freesurfer'
final_dir = r'E:\RESEARCH_NEW\ABIDEII_BIDS_fmriprep'
info_path = r'E:\RESEARCH_NEW\PHENOTYPIC_ABIDEII\ABIDEII_Composite_Phenotypic.csv'


info = pd.read_csv(info_path)




ls_subs = info['SUB_ID']

for x in np.arange(len(ls_subs[1:5])):

    sub = 'sub-%d'%ls_subs[x]
    idx_sub = np.where(info['SUB_ID']==int(sub[4:]))[0][0]
    site = info['SITE_ID'].iloc[idx_sub]


    if not os.path.exists('%s/derivatives/fmriprep/%s'%(final_dir,sub)):
    
        #start = time.time()
    
        #### Copy locally the participant's data & keep only the run-1
        if not os.path.exists(os.path.join(local_dir,sub)):    
            shutil.copytree(os.path.join(original_HD_dir, sub), os.path.join(local_dir,sub))
        tmp_anat = os.listdir(os.path.join(local_dir,sub, 'ses-1','anat'))
        tmp_func = os.listdir(os.path.join(local_dir,sub, 'ses-1','func'))
        for a, anat in enumerate(tmp_anat):
            if not 'run-1' in anat:
                os.remove(os.path.join(local_dir,sub,'ses-1','anat',anat))
        for f, func in enumerate(tmp_func):
            if not 'run-1' in func:
                os.remove(os.path.join(local_dir,sub,'ses-1','func',func))
        
    
    
    ### Create the .json files for the different images required for fmriprep
    ### =========================================================================
    
    #T1_path = '%s/ses-1/anat/%s_ses-1_run-1_T1w.nii.gz'%(sub,sub)
   # func_path = '%s/ses-1/func/%s_ses-1_run-1_task-rest_bold.nii.gz'%(sub,sub)
    #new_func_path = '%s/ses-1/func/%s_ses-1_task-rest_bold_run-1.nii.gz'%(sub,sub)
    
    ### Convert the anatomical image run-1
   # cmd_convert_T1 = 'docker run --rm -it -v %s:/data mrtrix3/mrtrix3 mrconvert /data/%s /data/%s --json_export /data/%s --force'%(local_dir, T1_path, T1_path, T1_path[0:-6]+'json') 
   # print(cmd_convert_T1)
    #subprocess.call(cmd_convert_T1, shell=True)
    #docker.run("mrtrix3/mrtrix3", ["mrconvert /data/%s /data/%s --json_export /data/%s --force"%(T1_path, T1_path, T1_path[0:-6]+'json')], volumes=[("/data", local_dir)], detach=True)
    
    
    ### Convert the functional image run-1
    #cmd_convert_func = 'docker run --rm -it -v %s:/data mrtrix3/mrtrix3 mrconvert /data/%s /data/%s --json_export /data/%s --force'%(local_dir, func_path, func_path, func_path[0:-6]+'json') 
    #output = subprocess.call(cmd_convert_func, shell=True)
    ##print(output)
    #shutil.copyfile('%s/json_func_%s.json'%(func_json_path, site[8:]), '%s/%s'%(local_dir, func_path[0:-6]+'json'))
    
    
    
    ### Run fmriprep using docker
    ### ============================
   # cmd_fmriprep = 'docker run --rm -it -v %s:/data -v %s/derivatives/fmriprep:/out -v %s:/fs nipreps/fmriprep /data /out participant --skip-bids-validation --participant_label %s --fs-license-file /fs/license.txt' %(local_dir, local_dir, fs_path, sub)
   # print(cmd_fmriprep)
    #subprocess.call(cmd_fmriprep, shell=True)
    
    #shutil.copytree('%s/%s'%(local_dir, sub), '%s/%s'%(final_dir, sub))
    #shutil.copytree('%s/derivatives/fmriprep/%s'%(local_dir,sub),'%s/derivatives/fmriprep/%s'%(final_dir,sub))

   #end = time.time()

#    print('%s is done in %d s' % (sub, end-start))
    