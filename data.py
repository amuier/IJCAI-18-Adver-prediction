import numpy as np
import pandas as pd
from sklearn import preprocessing
from matplotlib import pyplot as plt

df = pd.DataFrame(pd.read_table('round1_ijcai_18_train_20180301.txt', header=0, delim_whitespace=True))

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
plt.show()
