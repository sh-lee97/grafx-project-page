from glob import glob
import os; opj = os.path.join
import random

def write_html(html_dir: str, task: str, sample_ids: list, valid_set: str, i: int):
    def replace(line, task, sample_id, valid_set, j):
        TASK = 'Singing Voice Effect Estimation' if task == 'singing' else 'Drum Mixing Estimation'
        dry = 'speaker' if task == 'singing' else 'kit'
        return line.replace('[TASK]', TASK)\
                   .replace('[task]', task)\
                   .replace('[DRY]', dry)\
                   .replace('[ID]', sample_id)\
                   .replace('[id]', str(j))\
                   .replace('[VALID-SET]', valid_set)\
                   .replace('[EX]', f'{i*10+1}-{(i+1)*10}')

    f = open(html_dir, 'w')

    head_f = open('head.html', 'r')
    headlines = head_f.readlines()
    for i in range(len(headlines)):
        headlines[i] = replace(headlines[i], task, '', valid_set, 0)
    f.writelines(headlines)

    j = 1
    for sample_id in sample_ids:
        sample_f = open('sample.html', 'r')
        samplelines = sample_f.readlines()
        for i in range(len(samplelines)):
            samplelines[i] = replace(samplelines[i], task, sample_id, valid_set, i*10+j)
        f.writelines(samplelines)
        j += 2

    tail_f = open('tail.html', 'r')
    taillines = tail_f.readlines()
    for i in range(len(taillines)):
        taillines[i] = replace(taillines[i], task, '', valid_set, 0)
    f.writelines(taillines)

if __name__ == '__main__':
    for task in ['singing', 'drum']:
        for valid_set in ['seen', 'unseen']:
            sample_dirs = glob(opj('samples', valid_set+'*', task, '*'))
            sample_ids = [d.split('/')[-1] for d in sample_dirs]
            random.shuffle(sample_ids)
            for i in range(5):
                _sample_ids = sample_ids[i*10:(i+1)*10]
                html_dir = f'sample-pages/{task}-{valid_set}-{i+1}.html'
                write_html(html_dir, task, _sample_ids, valid_set, i)
