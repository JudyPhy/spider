# coding=gbk
from results_table import combine_results_tables_p
from horse_table import combine_horse_tables_p
from jockey_score import main as jockey_score
from trainer_score import main as trainer_score
from dragon import dragon
import datetime
from today_history import combine_history_today


start_time = datetime.datetime.now()


# 1. 将原始数据合并成两张总表
# combine_results_tables_p.main()
# combine_horse_tables_p.main()

# 2.根据总表计算部分字段结果，并与总表结合，汇总得到最终所需表
dragon.main()

# elo计算
# jockey_score.main()
# trainer_score.main()

# 合并测试表
# combine_history_today.main()

delta_time = datetime.datetime.now() - start_time
print('cost time:', delta_time)
