# IJCAI-18-Adver-prediction

数据放在data目录下


编译
# make


生成tr.csv,te.csv, fc.trva.t10.txt, tr.gbdt.dense, tr.gbdt.sparse, te.gbdt.dense, te.gbdt.sparse文件
#python whole_deal.py



生成GBDT模型
#./gbdt -t 30 -s 1 ./output/te.gbdt.dense ./output/te.gbdt.sparse ./output/tr.gbdt.dense ./output/tr.gbdt.sparse ./output/te.gbdt.out ./output/tr.gbdt.out




