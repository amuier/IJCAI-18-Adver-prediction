import numpy as np
import pandas as pd
from sklearn import preprocessing
from matplotlib import pyplot as plt

df = pd.DataFrame(pd.read_table('round1_ijcai_18_train_20180301.txt', header=0, delim_whitespace=True))

'''----------------将编号重新labelEncoder-------------------'''
le = preprocessing.LabelEncoder()
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

'''-----------------广告商品信息处理--------------- '''
fig = plt.figure(figsize=(40,40))
#item_price_level直方图
plt.subplot(231)
plt.title('item_price_level')
df['item_price_level'].hist(bins=20)

#item_sales_level直方图
plt.subplot(232)
plt.title('item_sales_level')
df['item_sales_level'].hist(bins=20)

#item_collected_level直方图
plt.subplot(233)
plt.title('item_collected_level')
df['item_collected_level'].hist(bins=20)

#item_pv_level直方图
plt.subplot(234)
plt.title('item_pv_level')
df['item_pv_level'].hist(bins=20)

#item_id直方图(不能直接这样画直方图，item_id就是编号，感觉无特殊意义，如果以item_id为横坐标，知道落在某段编号范围内的频数意义不大)
#plt.subplot(335)
#plt.title('item_id')
#df['item_id'].hist(bins=20)

#item_id图 以频数为横轴，画出每个频数段的商品数
plt.subplot(235)
plt.title('item_id')
#(df.groupby('item_id').count().sort_values(by='instance_id',ascending=False))['instance_id'].plot.hist(bins=10,grid=True)
df.groupby('item_id').count()['instance_id'].plot.hist(bins=50,grid=True)

#样本中商品出现频数大于1000的商品数和出现频数小于500的商品数（应该就是长尾分布）
print(len((np.where(df.groupby('item_id').count()['instance_id']>1000))[0]))#45
print(len((np.where(df.groupby('item_id').count()['instance_id']<500))[0]))#9908

#plt.tight_layout() #设置默认的间距
plt.subplots_adjust(wspace=0.2, hspace=0.3)
#plt.show()

''' 上下文信息'''
fig1 = plt.figure()
#context_page_id直方图
plt.subplot(111)
plt.title('context_page_id')
df['context_page_id'].hist(bins=50)
print('这个字段很奇怪，数据低于4001的数量为0，但是这不是页数么 ',len(np.where(df["context_page_id"]>4002)[0]))



''' -------------- 用户信息数据处理 ------------------'''
print('-----------user_gender_id--------------')
print(df['user_gender_id'].describe())
print('-----------user_age_level--------------')
print(df['user_age_level'].describe())
print('-----------user_occupation_id--------------')
print(df['user_occupation_id'].describe())
print('-----------user_star_level--------------')
print(df['user_star_level'].describe())

#类别数据，直接将-1值置为众数
df['user_gender_id']=df['user_gender_id'].replace(-1, 0)
df['user_age_level']=df['user_age_level'].replace(-1, 1004)
df['user_occupation_id']=df['user_occupation_id'].replace(-1, 2005)
df['user_star_level']=df['user_star_level'].replace(-1, 3006)


fig2 = plt.figure(figsize=(40,40))
#user_gender_id直方图
plt.subplot(221)
plt.title('user_gender_id')
df['user_gender_id'].hist(bins=10)

#user_age_level直方图
plt.subplot(222)
plt.title('user_age_level')
df['user_age_level'].hist(bins=20)

#user_occupation_id直方图
plt.subplot(223)
plt.title('user_occupation_id')
df['user_occupation_id'].hist(bins=20)

#user_star_level直方图
plt.subplot(224)
plt.title('user_star_level')
df['user_star_level'].hist(bins=20)



'''--------------------店铺信息处理-------------------'''
print('-----------shop_review_num_level--------------')
print(df['shop_review_num_level'].describe())
print('-----------shop_review_positive_rate--------------')
print(df['shop_review_positive_rate'].describe())
print('-----------shop_star_level--------------')
print(df['shop_star_level'].describe())
print('-----------shop_score_service--------------')
print(df['shop_score_service'].describe())
print('-----------shop_score_delivery--------------')
print(df['shop_score_delivery'].describe())
print('-----------shop_score_description--------------')
print(df['shop_score_description'].describe())

#先将-1置为空，然后求得各个值的均值
df['shop_review_positive_rate']=df['shop_review_positive_rate'].replace(-1, np.nan)
df['shop_score_service']=df['shop_score_service'].replace(-1, np.nan)
df['shop_score_delivery']=df['shop_score_delivery'].replace(-1, np.nan)
df['shop_score_description']=df['shop_score_description'].replace(-1, np.nan)

# 再将空值置为均值
df['shop_review_positive_rate']=df['shop_review_positive_rate'].replace(np.nan, 0.994859)
df['shop_score_service']=df['shop_score_service'].replace(np.nan, 0.971367)
df['shop_score_delivery']=df['shop_score_delivery'].replace(np.nan, 0.970740)
df['shop_score_description']=df['shop_score_description'].replace(np.nan, 0.975107)

fig2 = plt.figure(figsize=(40,40))
#shop_review_num_level直方图
plt.subplot(231)
plt.title('shop_review_num_level')
df['shop_review_num_level'].hist(bins=10)

#shop_review_positive_rate直方图
plt.subplot(232)
plt.title('shop_review_positive_rate')
df['shop_review_positive_rate'].hist(bins=20)

#shop_star_level直方图
plt.subplot(233)
plt.title('shop_star_level')
df['shop_star_level'].hist(bins=20)

#shop_score_service直方图
plt.subplot(234)
plt.title('shop_score_service')
df['shop_score_service'].hist(bins=40)

#shop_score_delivery直方图
plt.subplot(235)
plt.title('shop_score_delivery')
df['shop_score_delivery'].hist(bins=40)

#shop_score_description直方图
plt.subplot(236)
plt.title('shop_score_description')
df['shop_score_description'].hist(bins=40)


plt.show()