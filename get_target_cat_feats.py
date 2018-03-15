import numpy as np
import pandas as pd

def get_ctg_feats():

    df = pd.DataFrame(pd.read_csv('tr.csv', header=0, delim_whitespace=True))

    #item_category_list列 数据处理
    df['item_category_1'], df['item_category_2'], df['item_category_3'] = df['C2'].str.split(';', -1).str

    #形成新类别特征
    cat_set=[]
    c1=df['C1'].value_counts()
    for i in c1[c1>2000].index:
        cat_set.append('C1-'+str(i))

    c2_2=df['item_category_2'].value_counts()
    for i in c2_2[c2_2>10000].index:
        cat_set.append('C2-'+str(i))

    c3=df['C3'].value_counts()
    for i in c3[c3>3000].index:
        cat_set.append('C3-'+str(i))

    c4=df['C4'].value_counts()
    for i in c4[c4>3000].index:
        cat_set.append('C4-'+str(i))

    c6=df['C5'].value_counts()
    for i in c5[c5>42].index:
        cat_set.append('C5-'+str(i))    

    cat_set.append('C6-0')
    cat_set.append('C6-1')
    cat_set.append('C7-2002')
    cat_set.append('C7-2005')

    c8=df['C8'].value_counts()
    for i in c8[c8>3000].index:
        cat_set.append('C8-'+str(i))

    return cat_set
	'''
	['C1-8268',
	 'C1-3295',
	 'C1-5927',
	 'C1-2279',
	 'C1-3026',
	 'C1-6272',
	 'C1-5985',
	 'C2-8277336076276184272',
	 'C2-5755694407684602296',
	 'C2-509660095530134768',
	 'C2-5799347067982556520',
	 'C2-7258015885215914736',
	 'C1-3040',
	 'C4-1755',
	 'C4-1594',
	 'C4-1144',
	 'C4-92',
	 'C4-160',
	 'C4-1533',
	 'C4-427',
	 'C4-1049',
	 'C4-1492',
	 'C4-1836',
	 'C4-1322',
	 'C4-844',
	 'C4-1584',
	 'C4-1609',
	 'C4-834',
	 'C4-261',
	 'C4-413',
	 'C5-101',
	 'C5-99',
	 'C5-50',
	 'C5-78',
	 'C5-1',
	 'C5-38',
	 'C5-14',
	 'C5-60',
	 'C5-66',
	 'C5-91',
	 'C5-25',
	 'C5-115',
	 'C5-48',
	 'C5-65',
	 'C5-90',
	 'C6-154495',
	 'C6-194672',
	 'C6-90249',
	 'C6-129548',
	 'C6-153329',
	 'C6-191015',
	 'C6-13650',
	 'C6-135894',
	 'C6-90445',
	 'C7-0',
	 'C7-1',
	 'C8-2002',
	 'C8-2005',
	 'C10-2802',
	 'C10-788',
	 'C10-3841',
	 'C10-829',
	 'C10-1750',
	 'C10-1791',
	 'C10-2477',
	 'C10-2124',
	 'C10-2549',
	 'C10-1856',
	 'C10-1071']
	 '''