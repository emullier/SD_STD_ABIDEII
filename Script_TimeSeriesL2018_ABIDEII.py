
###########################################################################################################
### This script aims to generate the FC matrices from ABIDEI-preprocessed in space MNI152 SPM99 symmetric. 
###
### September 2020
### Emeline Mullier
### University of Geneva
###
### Script adapted by EM 28.05.2024 for ABIDEII for fmriprep output
############################################################################################################


import os
import numpy as np
import nibabel as nib
import nilearn as nl
import nilearn.plotting
from scipy.spatial.distance import squareform, pdist
import scipy.io as sio


### List of subjects
bids_dir = '/media/localadmin/Seagate/RESEARCH_NEW/PROJECT_ABIDEII/ABIDEII_BIDS/'
fmri_dir = '%s/derivatives/fmriprep' % bids_dir
conmat_dir = '%s/derivatives/STConn' % bids_dir
tmp = os.listdir(fmri_dir)
ls_subs = []
for sub in tmp:
    if  sub.startswith('sub') and not ('html' in sub):
        ls_subs.append(sub)
ls_subs = np.array(ls_subs)
print(ls_subs)
ses = 'ses-1'

# Load the parcellation
atlas_path = '/media/localadmin/Seagate/RESEARCH_NEW/PROJECT_ABIDEII/CODES/RegistrationLausanne2018Atlas/lausanne2018.scale4.sym.corrected_fmri_Nlin2099cAsym.nii.gz'
atlas = nib.load(atlas_path)
atlasVol = atlas.get_fdata()
atlasVol = atlasVol.reshape((np.shape(atlasVol)[0], np.shape(atlasVol)[1], np.shape(atlasVol)[2]))
nROIs = atlasVol.max()
nROIs = int(nROIs)
    

### Generate the time series and functional connectivity matrices
for s, sub in enumerate(ls_subs):
    
    print(sub)
    
    try:
    
        out_path = os.path.join(conmat_dir, sub, '%s_desc-ts-L2018.npy'% sub)
        if not os.path.exists(out_path):
    
                # Split the fmri volume
                fmri_path = os.path.join(fmri_dir, sub, ses, 'func/%s_%s_task-rest_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'%(sub,ses))

                if os.path.exists(fmri_path):
                    print(fmri_path)
                    
                    fmri4D = nib.load(fmri_path)
                    nbTR = np.shape(fmri4D)[3]
                    nbTR = int(nbTR)
                    fmriVol = fmri4D.get_fdata()

                    ts = np.zeros((nROIs, nbTR))
                    for r in np.arange(nROIs):
                        ts[r,:] = fmriVol[atlasVol==r+1].mean(axis=0)

            
                    FC = 1 - squareform(pdist(ts,metric='correlation'))
        
                    if not os.path.exists(os.path.join(conmat_dir, sub)):
                        os.makedirs(os.path.join(conmat_dir, sub))
            
                    out_path = os.path.join(conmat_dir, sub, '%s_desc-ts-L2018.npy'%(sub))
                    np.save(out_path, ts)   
                    out_path = os.path.join(conmat_dir, sub,  '%s_desc-FC-L2018.npy'%(sub))
                    np.save(out_path, FC)
                
                    out_path = os.path.join(conmat_dir, sub, '%s_desc-ts-L2018.mat'%(sub))
                    t = {'ts':ts}
                    sio.savemat(out_path, t)   
                    out_path = os.path.join(conmat_dir, sub,  '%s_desc-FC-L2018.mat'%(sub))
                    f = {'FC':FC}
                    sio.savemat(out_path, f)


    except:
        pass