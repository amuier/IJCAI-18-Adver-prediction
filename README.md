# IJCAI-18-Adver-prediction

data_re_get_target_cat_feats.ipynb ：该文件包含了data_pre.py代码，同时获取target_cat_feats值；

data_pre.py : 清洗数据，包括LabelEncoder、填充空值、修改列名、将修改后的数据保存为csv文件

get_target_cat_feats.py : 返回的是target_cat_feats，获取频数最高的C{i}, 用于OneHot，，，emmmm但是不知道为嘛读取csv文件有点问题，，所以事先
						  通过data_re_get_target_cat_feats.ipynb中的In[1]中获取target_cat_feats值，，然后直接在pre_a中写死该值。


count.py : 在kaggle的utils文件夹下，生成fc.trva.t10.txt文件，该文件中存储的是所有出现次数超过10次的字段属性值，
		   存储格式为：C{i},value,Neg,Pos,Total, Ratio   
		   其中，C{i},value 是一个整体(key)，Neg指该字段值出现时label为0的次数
		   Pos为label为1的次数，Total为该字段值总共出现的次数，Ratio为Pos/Ratio比值
		   
pre_a.py : 在kaggle的converters文件夹下， 生成sparse及dense文件，dense文件存储I1~I13的所有值，sparse文件存储的是
		   每个样本C1-C8字段的值出现在target_cat_feats中的索引。
		   