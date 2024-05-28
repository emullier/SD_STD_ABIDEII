# -*- coding: utf-8 -*-
"""
Convert ABIDEII database in BIDS format.

EMU
09.11.2022
"""


import os
import shutil

path_abide = r'E:/RESEARCH_NEW\ABIDEII'
path_bids = r'E:/RESEARCH_NEW/ABIDEII_BIDS'
#json_template = 'E:\RESEARCH_NEW\PHENOTYPIC_ABIDEII\json_files\json_func_SDSU.json'
#info_path = r'E:\RESEARCH_NEW\PHENOTYPIC_ABIDEII\ABIDEII_Composite_Phenotypic.csv'
func_json_path= r'E:/RESEARCH_NEW/PHENOTYPIC_ABIDEII/json_files'

ls_sites = []
tmp = os.listdir(path_abide)
for t,tmp in enumerate(tmp):
    if tmp.startswith('ABIDEII'):
        ls_sites.append(tmp)

for s,site in enumerate(ls_sites):
    
    path_site = os.path.join(path_abide, site)
    tmp = os.listdir(path_site)
    ls_subs = [item for item in tmp if ((item.startswith('2') or item.startswith('3')))] 
    for s, sub in enumerate(ls_subs):
        path_sub = os.path.join(path_site, sub)
        #path_sub_bids = os.path.join(path_bids, 'sub-%s'%sub)
        path_sub_bids = '%s/sub-%s'%(path_bids, sub)
        if not os.path.exists(path_sub_bids):
            os.mkdir(path_sub_bids)
        tmp = os.listdir(path_sub)
        ls_ses = [item for item in tmp if (item.startswith('ses'))] 
        for e,ses in enumerate(ls_ses):
            path_ses = os.path.join(path_sub, ses)
            #path_ses_bids = os.path.join(path_sub_bids, 'ses-%d'%(e+1))
            path_ses_bids = '%s/ses-%d'%(path_sub_bids, (e+1))
            
            if not os.path.exists(os.path.join(path_ses_bids, 'func')):
                if not os.path.exists(path_ses_bids):
                    os.mkdir(path_ses_bids)
                ls_mod = []
                tmp = os.listdir(path_ses)
                ls_mod = [item for item in tmp if (item.startswith('a') or item.startswith('d') or item.startswith('rest'))] 
                for m,mod in enumerate(ls_mod):
                    path_mod = os.path.join(path_ses, mod)
                    tmp = os.listdir(path_mod)
                    ls_files = [item for item in tmp if item.endswith('.nii.gz')] 
                    if mod.startswith('anat'):
                        #path_anat_bids = os.path.join(path_ses_bids, 'anat')
                        path_anat_bids = '%s/anat'%(path_ses_bids)
                        if not os.path.exists(path_anat_bids):
                            os.mkdir(path_anat_bids)
                        for f,file in enumerate(ls_files):
                            T1_path = '%s/sub-%s_ses-%d_run-%s_T1w.nii.gz'%(path_anat_bids,sub,e+1,mod[-1])
                            shutil.copy(os.path.join(path_mod, file), T1_path)
                            shutil.copyfile('%s/json_anat.json'%(func_json_path), T1_path[0:-6]+'json')
                            #cmd_convert_T1 = 'docker run --rm -it -v %s:/data mrtrix3/mrtrix3 mrconvert /data/%s /data/%s --json_export /data/%s --force'%(path_anat_bids, T1_path, T1_path, T1_path[0:-6]+'json') 
                            #subprocess.call(cmd_convert_T1, shell=True)
                    elif mod.startswith('rest'):
                        path_func_bids = os.path.join(path_ses_bids, 'func')
                        if not os.path.exists(path_func_bids):
                            os.mkdir(path_func_bids)
                        for f,file in enumerate(ls_files):
                            shutil.copy(os.path.join(path_mod, file), os.path.join(path_func_bids, 'sub-%s_ses-%d_task-rest_run-%s_bold.nii.gz'%(sub,e+1,mod[-1])))
                            shutil.copyfile('%s/json_func_%s.json'%(func_json_path, site[8:]), '%s/sub-%s_ses-%d_task-rest_run-%s_bold.json'%(path_func_bids, sub,e+1,mod[-1]))
                    elif mod.startswith('dti'):
                        path_dwi_bids = os.path.join(path_ses_bids, 'dwi')
                        if not os.path.exists(path_dwi_bids):
                            os.mkdir(path_dwi_bids)
                        for f,file in enumerate(ls_files):
                            shutil.copy(os.path.join(path_mod, file), os.path.join(path_dwi_bids, 'sub-%s_ses-%d_run-%s_dwi.nii.gz'%(sub,e+1,mod[-1])))
                print('sub-%s copied'%sub)
            else:
                print('sub-%s already existant'%sub)
    print('Site %s copied'% site)
    
    
        