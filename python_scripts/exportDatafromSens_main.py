import os
import glob
from multiprocessing import Pool
from multiprocessing import Process
import time

from myreader import reader as rdr

# input
Sens_dir = '/mnt/PURP8TB02/ScanNet/'
Sens_subset_format = 'scene*'
Sens_fileext = '.sens'

# output
Output_dir = '/mnt/PURP8TB02/ScanNet_images/'



def exportoneData(sens_subsetname, sens_fileext, output_dir):
    sens_fullname = os.path.join(sens_subsetname, os.path.basename(sens_subsetname)+sens_fileext)
    output_fullpath = os.path.join(output_dir, os.path.basename(sens_subsetname))

    # Export image, depth, pose, intrinsics
    rdr(sens_fullname, output_fullpath, \
    export_depth_images=True, export_color_images=True, export_poses=True, export_intrinsics=True)
    return 0

def wrapper_exportoneData(args):
    return exportoneData(**args)

def exportData_multi(subset_all, sens_fileext, output_dir):
    p = Pool(12)
    sts = p.map(wrapper_exportoneData, \
    [{'sens_subsetname':i, 'sens_fileext':sens_fileext, 'output_dir':output_dir} \
    for i in subset_all])

    return sts



    

if __name__ == '__main__':
    subset_all = glob.glob(os.path.join(Sens_dir, Sens_subset_format))
    print 'Number of scene: %d' %(len(subset_all))

    status = exportData_multi(subset_all, Sens_fileext, Output_dir)
    print status

