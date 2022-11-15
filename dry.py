import os; opj = os.path.join
from glob import glob
import shutil

#sample_dirs = glob('samples/*/singing/*/')
#for sample_dir in sample_dirs:
#    split = sample_dir.split('/')
#    valid, data_id = split[1], split[3]
#    batch_id, data_id = data_id[:2], data_id[3:]
#    dry_dir = opj('../2022_11_04_02_03_02/test/', valid, batch_id, data_id, 'x.wav')
#    dest_dir = opj(sample_dir, 'x.wav')
#    print(dry_dir)
#    print(dest_dir)
#    shutil.move(dry_dir, dest_dir)

sample_dirs = glob('samples/*/drum/*/')
for sample_dir in sample_dirs:
    split = sample_dir.split('/')
    valid, data_id = split[1], split[3]
    batch_id, data_id = data_id[:2], data_id[3:]
    dry_dir = opj('../2022_11_04_02_07_03/test/', valid, str(int(batch_id)), data_id, 'x_sum.wav')
    dest_dir = opj(sample_dir, 'x.wav')
    print(dry_dir)
    print(dest_dir)
    try:
        shutil.move(dry_dir, dest_dir)
    except:
        continue
