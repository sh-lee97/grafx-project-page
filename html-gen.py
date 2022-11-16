from glob import glob
import os; opj = os.path.join
import random
import cv2
from tqdm import tqdm

def write_html(html_dir: str, task: str, sample_ids: list, valid_set: str, k: int):
    def replace(line, task, sample_id, valid_set, j, max_width_ref=50, max_width_pred=50):
        TASK = 'Singing Voice Effect Estimation' if task == 'singing' else 'Drum Mixing Estimation'
        DRY = 'speaker' if task == 'singing' else 'kit'
        dry = 'x' if task == 'singing' else 'x.sum'
        return line.replace('[TASK]', TASK)\
                   .replace('[task]', task)\
                   .replace('[DRY]', DRY)\
                   .replace('[dry]', dry)\
                   .replace('[ID]', sample_id)\
                   .replace('[id]', str(j))\
                   .replace('[VALID-SET]', valid_set)\
                   .replace('[EX]', f'{i*10+1}-{(i+1)*10}')\
                   .replace('[MAX-WIDTH-REF]', str(int(max_width_ref)))\
                   .replace('[MAX-WIDTH-PRED]', str(int(max_width_pred)))

    f = open(html_dir, 'w')

    head_f = open('head.html', 'r')
    headlines = head_f.readlines()
    for i in range(len(headlines)):
        headlines[i] = replace(headlines[i], task, '', valid_set, 0)
    f.writelines(headlines)

    j = 1
    for sample_id in tqdm(sample_ids):
        sample_f = open('sample.html', 'r')
        samplelines = sample_f.readlines()

        folder = opj('samples', valid_set+'-source-distribution', task, sample_id)
        ref_dir = opj(folder, 'token-2stage.png-1.png')
        ref_img = cv2.imread(ref_dir)
        ref_w = ref_img.shape[1]
        pred_dir = opj(folder, 'token-2stage.png-2.png')
        pred_img = cv2.imread(pred_dir)
        pred_w = pred_img.shape[1]

        max_width_ref = ref_w/2800*800
        max_width_pred = pred_w/2800*800

        for i in range(len(samplelines)):
            samplelines[i] = replace(samplelines[i], task, sample_id, valid_set, k*10+j, max_width_ref=max_width_ref, max_width_pred=max_width_pred)

        f.writelines(samplelines)
        j += 1

    tail_f = open('tail.html', 'r')
    taillines = tail_f.readlines()
    for i in range(len(taillines)):
        taillines[i] = replace(taillines[i], task, '', valid_set, 0)
    f.writelines(taillines)

if __name__ == '__main__':
    random.seed(2)
    for task in ['singing', 'drum']:
        for valid_set in ['seen', 'unseen']:
            sample_dirs = glob(opj('samples', valid_set+'*', task, '*'))
            sample_ids = [d.split('/')[-1] for d in sample_dirs]
            random.shuffle(sample_ids)
            for i in range(4):
                _sample_ids = sample_ids[i*10:(i+1)*10]
                html_dir = f'sample-pages/{task}-{valid_set}-{i+1}.html'
                write_html(html_dir, task, _sample_ids, valid_set, i)
