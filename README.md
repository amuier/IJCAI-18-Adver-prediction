# IJCAI-18-Adver-prediction

data_re_get_target_cat_feats.ipynb ：该文件包含了data_pre.py代码，同时获取target_cat_feats值；

data_pre.py : 清洗数据，包括LabelEncoder、填充空值、修改列名、将修改后的数据保存为csv文件

get_target_cat_feats.py : 返回的是target_cat_feats，获取频数最高的C{i}, 用于OneHot，，，emmmm但是不知道为嘛读取csv文件有点问题，，所以事先
						  通过data_re_get_target_cat_feats.ipynb中的In[1]中获取target_cat_feats值，，然后直接在pre_a中写死该值。


#whole_deal.py
清洗数据，生成tr.csv,te.csv, fc.trva.t10.txt, tr.gbdt.dense, tr.gbdt.sparse, te.gbdt.dense, te.gbdt.sparse文件

#./gbdt -t 30 -s 1 ./output/te.gbdt.dense ./output/te.gbdt.sparse ./output/tr.gbdt.dense ./output/tr.gbdt.sparse ./output/te.gbdt.out ./output/tr.gbdt.out
生成GBDT模型


		   