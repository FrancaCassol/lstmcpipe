#!/usr//bin/env python3

# T. Vuillaume, 12/09/2019
# merge and copy DL1 data after 


# lstchain_dir="/home/thomas.vuillaume/software/cta-observatory/cta-lstchain"


# input_dir='/fefs/aswg/data/mc/DL1/20190822/gamma-diffuse/south_pointing/training/'
# output_file='/fefs/aswg/data/mc/DL1/20190822/gamma-diffuse/south_pointing/dl1_20190822_proton_training.h5'

# # input_dir=$1
# # output_file=$2

# python $lstchain_dir/scripts/merge_hdf5_files.py -d $input_dir -o $output_file




# 1. check job_logs
# 2. check that all files have been created in DL1 based on training and testing lists
# 3. move DL1 files in final place
# 4. merge DL1 files
# 5. move running_dir 


import os
import sys
from data_management import *


# input_dir = '/Users/thomasvuillaume/Work/CTA/Data/test_lst_script/running_analysis/70deg20deg/v00'
input_dir = sys.argv[1]

JOB_LOGS = os.path.join(input_dir, 'job_logs')
training_filelist = os.path.join(input_dir, 'training.list')
testing_filelist = os.path.join(input_dir, 'testing.list')
running_DL1_dir = os.path.join(input_dir, 'DL1')
DL1_training_dir = os.path.join(running_DL1_dir, 'training')
DL1_testing_dir = os.path.join(running_DL1_dir, 'testing')
final_DL1_dir = input_dir.replace('running_analysis', 'DL1')
logs_destination_dir = input_dir.replace('running_analysis', 'analysis_logs')



def check_files_in_dir_from_file(dir, file):
    """
    Check that a list of files from a file exist in a dir

    Parameters
    ----------
    dir
    file

    Returns
    -------

    """
    with open(file) as f:
        lines = f.readlines()

    files_in_dir = os.listdir(dir)
    files_not_in_dir = []
    for line in lines:
        filename = os.path.basename(line.rstrip('\n'))
        if filename not in files_in_dir:
            files_not_in_dir.append(filename)

    return files_not_in_dir


def readlines(file):
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def move_dir_content(src, dest):
    files = os.listdir(src)
    for f in files:
        shutil.move(os.path.join(src,f), dest)
    os.rmdir(src)
    

print("\n ==== START {} ==== \n".format(sys.argv[0]))

# 1. check job logs
check_job_logs(JOB_LOGS)


# 2. check that all files have been created in DL1 based on training and testing lists
## just check number of files first:
if not len(os.listdir(DL1_training_dir)) == len(readlines(training_filelist)):
    tf = check_files_in_dir_from_file(DL1_training_dir, training_filelist)
    if  tf != []:
        query_continue("{} files from the training list are not in the `DL1/training` directory:\n{} "
                     "Continue ?".format(len(tf),tf))
        
if not len(os.listdir(DL1_testing_dir)) == len(readlines(testing_filelist)):
    tf = check_files_in_dir_from_file(DL1_testing_dir, testing_filelist)
    if tf != []:
        query_continue("{} files from the testing list are not in the `DL1/training` directory:\n{} "
                     "Continue ?".format(len(tf), tf))

# 3. merge DL1 files
#TODO : after merging of DL1 files PR in lstchain

# 4. move DL1 files in final place
check_and_make_dir(final_DL1_dir)
# shutil.move(os.path.join(running_DL1_dir, "*"), final_DL1_dir)
move_dir_content(running_DL1_dir, final_DL1_dir)
print("DL1 files have been moved in {}".format(final_DL1_dir))

# 5. move running_dir as logs
check_and_make_dir(logs_destination_dir)
move_dir_content(input_dir, logs_destination_dir)
print("LOGS have been moved to {}".format(logs_destination_dir))

print("\n ==== END {} ==== \n".format(sys.argv[0]))