import numpy as np
import pandas as pd
from sklearn import preprocessing
import csv, collections

df = pd.DataFrame(pd.read_table('./data/round1_ijcai_18_train_20180301.txt', header=0, delim_whitespace=True))

'''----------------将编号重新labelEncoder-------------------'''
le = preprocessing.LabelEncoder()
#item_id 数据转换
le.fit(df['item_id'])
df['item_id']=le.transform(df['item_id'])
#item_brand_id 数据转换
le.fit(df['item_brand_id'])
df['item_brand_id']=le.transform(df['item_brand_id'])
#item_city_id 数据转换
le.fit(df['item_city_id'])
df['item_city_id']=le.transform(df['item_city_id'])
#user_id 数据转换
le.fit(df['user_id'])
df['user_id']=le.transform(df['user_id'])
#context_id 数据转换
le.fit(df['context_id'])
df['context_id']=le.transform(df['context_id'])
#shop_id 数据转换
le.fit(df['shop_id'])
df['shop_id']=le.transform(df['shop_id'])
#instance_id 数据转换
le.fit(df['instance_id'])
df['instance_id']=le.transform(df['instance_id'])

'''
# 时间特征与点击率可视化,时间粒度为小时(可调),count里存放单位时间(小时)内点击数量的平均值,画出count和time的折线图
df['context_timestamp'] = pd.to_datetime(df['context_timestamp'], unit='s')
df['context_timestamp'].hist(bins=100)
df['time'] = df['context_timestamp'].dt.strftime('%Y-%m-%d-%H')

def mean_time(group):
    group['count'] = group['is_trade'].mean()
    return group

df = df.groupby('time').apply(mean_time)
df.plot(x='time', y='count', kind='line')
#plt.show()
'''

df['item_sales_level']=df['item_sales_level'].replace(-1, np.nan)
df['item_sales_level']=df['item_sales_level'].replace(np.nan, df['item_sales_level'].mean()) #设为均值

#类别数据，直接将-1值置为众数
df['user_gender_id']=df['user_gender_id'].replace(-1, df['user_gender_id'].mode()[0])
df['user_age_level']=df['user_age_level'].replace(-1, df['user_age_level'].mode()[0])
df['user_occupation_id']=df['user_occupation_id'].replace(-1, df['user_occupation_id'].mode()[0])
df['user_star_level']=df['user_star_level'].replace(-1, df['user_star_level'].mode()[0])


#先将-1置为空，然后求得各个值的均值
df['shop_review_positive_rate']=df['shop_review_positive_rate'].replace(-1, np.nan)
df['shop_score_service']=df['shop_score_service'].replace(-1, np.nan)
df['shop_score_delivery']=df['shop_score_delivery'].replace(-1, np.nan)
df['shop_score_description']=df['shop_score_description'].replace(-1, np.nan)

# 再将空值置为均值
df['shop_review_positive_rate']=df['shop_review_positive_rate'].replace(np.nan, df['shop_review_positive_rate'].mean())
df['shop_score_service']=df['shop_score_service'].replace(np.nan, df['shop_score_service'].mean())
df['shop_score_delivery']=df['shop_score_delivery'].replace(np.nan, df['shop_score_delivery'].mean())
df['shop_score_description']=df['shop_score_description'].replace(np.nan, df['shop_score_description'].mean())


#连续数据处理
df['user_age_level'] = df['user_age_level'].map(lambda x : x-1000)
df['user_star_level'] = df['user_star_level'].map(lambda x : x-3000)
df['context_page_id'] = df['context_page_id'].map(lambda x : x-4000)
df['shop_star_level'] = df['shop_star_level'].map(lambda x : x-4999)

#修改连续数据的列名
df.rename(columns={'item_price_level':'I1', 'item_sales_level':'I2','item_collected_level':'I3','item_pv_level':'I4','user_age_level':'I5',
                   'user_star_level':'I6','context_page_id':'I7','shop_review_num_level':'I8','shop_review_positive_rate':'I9','shop_star_level':'I10',
                   'shop_score_service':'I11','shop_score_delivery':'I12','shop_score_description':'I13',}, inplace = True)

#修改类别变量的列名
df.rename(columns={'item_id':'C1','item_category_list':'C2','item_brand_id':'C3','item_city_id':'C4',
                  'user_id':'C5','user_gender_id':'C6','user_occupation_id':'C7','shop_id':'C8','item_property_list':'C9','predict_category_property':'C10'}, inplace = True)

#修改is_trade列名为Label
df.rename(columns={'is_trade':'Label'}, inplace = True)

#item_category_list列 数据处理
'''
item_category_1 所有的的样本都是同一个值
item_category_2 一共有13个，我选N=10000,这样是取5个（N=5000的话,是取7个）
item_category_3 只有2个值，，而且出现频率太低，才几百，相对2的都太低了，不要了
'''
df['item_category_1'], df['item_category_2'], df['item_category_3'] = df['C2'].str.split(';', -1).str
df['C2'] = df['item_category_2']

#C2 数据转换
le.fit(df['C2'])
df['C2']=le.transform(df['C2'])

new_columns = ['Label','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','C1','C2','C3','C4','C5','C6','C7','C8']
df.sample(n=20000).to_csv("./output/tr.csv",index=False,columns=new_columns)
df.sample(n=8000).to_csv("./output/te.csv",index=False,columns=new_columns)

counts = collections.defaultdict(lambda : [0, 0, 0])        
for i in range(0, len(df)):
    row = df.loc[i]
    label = row['Label']
    for j in range(1, 9):
        field = 'C{0}'.format(j)
        value = row[field]
        if label == 0:
            counts[field+','+str(value)][0] += 1
        else:
            counts[field+','+str(value)][1] += 1
        counts[field+','+str(value)][2] += 1
with open('./output/fc.trva.t10.txt', 'w') as f_t10:
    f_t10.write('Field,Value,Neg,Pos,Total,Ratio' + '\n')
    for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
        if total < 10:
            continue
        ratio = round(float(pos)/total, 5)
        f_t10.write(key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio)+'\n')
        
        
target_cat_feats=['C6-0', 'C7-2005', 'C4-101', 'C2-11', 'C7-2002', 'C2-8', 'C6-1', 'C2-7', 
                  'C2-9','C3-1755', 'C4-99', 'C4-50', 'C2-10', 
                  'C4-78', 'C4-1','C4-38', 'C7-2004', 'C4-14', 'C4-60', 'C3-1594', 'C3-1144', 'C8-2802', 'C4-66', 'C6-2', 'C3-92','C8-788']

with open('./output/tr.gbdt.dense', 'w') as f_d, open('./output/tr.gbdt.sparse', 'w') as f_s:    
    for row in csv.DictReader(open('./output/tr.csv')):
        feats = []
        for j in range(1, 14):
            val = row['I{0}'.format(j)]
            feats.append('{0}'.format(val))
        f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        
        cat_feats = set()
        for j in range(1, 9):
            field = 'C{0}'.format(j)
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        
with open('./output/te.gbdt.dense', 'w') as f_d, open('./output/te.gbdt.sparse', 'w') as f_s:    
    for row in csv.DictReader(open('./output/te.csv')):
        feats = []
        for j in range(1, 14):
            val = row['I{0}'.format(j)]
            feats.append('{0}'.format(val))
        f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        
        cat_feats = set()
        for j in range(1, 9):
            field = 'C{0}'.format(j)
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')