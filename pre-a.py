#!/usr/bin/env python3

import argparse, csv, sys

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
parser.add_argument('dense_path', type=str)
parser.add_argument('sparse_path', type=str)
args = vars(parser.parse_args())

#These features are dense enough (they appear in the dataset more than 4 million times), so we include them in GBDT
#target_cat_feats = ['C9-a73ee510', 'C22-', 'C17-e5ba7672', 'C26-', 'C23-32c7478e', 'C6-7e0ccccf', 'C14-b28479f6', 'C19-21ddcdc9', 'C14-07d13a8f', 'C10-3b08e48b', 'C6-fbad5c96', 'C23-3a171ecb', 'C20-b1252a9d', 'C20-5840adea', 'C6-fe6b92e5', 'C20-a458ea53', 'C14-1adce6ef', 'C25-001f3601', 'C22-ad3062eb', 'C17-07c540c4', 'C6-', 'C23-423fab69', 'C17-d4bb7bd8', 'C2-38a947a1', 'C25-e8b83407', 'C9-7cc72ec2']
#target_cat_feats = get_ctg_feats()

target_cat_feats=['C1-8268', 'C1-3295', 'C1-5927', 'C1-2279', 'C1-3026', 'C1-6272', 'C1-5985', 'C1-3040', 
                  'C2-8277336076276184272', 'C2-5755694407684602296', 'C2-509660095530134768', 'C2-5799347067982556520', 'C2-7258015885215914736', 
                  'C3-1755', 'C3-1594', 'C3-1144', 'C3-92', 'C3-160', 'C3-1533', 'C3-427', 'C3-1049', 'C3-1492', 'C3-1836', 'C3-1322', 'C3-844', 'C3-1584', 'C3-1609', 'C3-834', 'C3-261', 'C3-413',
                  'C4-101', 'C4-99', 'C4-50', 'C4-78', 'C4-1', 'C4-38', 'C4-14', 'C4-60', 'C4-66', 'C4-91', 'C4-25', 'C4-115', 'C4-48', 'C4-65', 'C4-90',
                  'C5-154495', 'C5-194672', 'C5-90249', 'C5-129548', 'C5-153329', 'C5-191015', 'C5-13650', 'C5-135894', 'C5-90445',
                  'C6-0', 'C6-1',
                  'C7-2002', 'C7-2005',
                  'C8-2802', 'C8-788', 'C8-3841', 'C8-829', 'C8-1750', 'C8-1791', 'C8-2477', 'C8-2124', 'C8-2549', 'C8-1856', 'C8-1071']
with open(args['dense_path'], 'w') as f_d, open(args['sparse_path'], 'w') as f_s:
    for row in csv.DictReader(open(args['csv_path'])):
        feats = []
        for j in range(1, 14):
            val = row['I{0}'.format(j)]
            if val == '':
                val = -10 # ??not sure 
            feats.append('{0}'.format(val))
        f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        
        cat_feats = set()
        for j in range(1, 9):
            field = 'C{0}'.format(j)
            if j == 2:
                for i in row[field].split(';'):
                    key = 'C2-' + i
                    cat_feats.add(key)
            else:
                key = field + '-' + row[field]
                cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
