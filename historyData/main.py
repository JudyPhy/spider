# coding=gbk
from results_table import combine_results_tables_p
from horse_table import combine_horse_tables_p
from jockey_score import main as jockey_score
from trainer_score import main as trainer_score
from dragon import dragon
import datetime
from today_history import combine_history_today


start_time = datetime.datetime.now()


# 1. ��ԭʼ���ݺϲ��������ܱ�
# combine_results_tables_p.main()
# combine_horse_tables_p.main()

# 2.�����ܱ���㲿���ֶν���������ܱ��ϣ����ܵõ����������
dragon.main()

# elo����
# jockey_score.main()
# trainer_score.main()

# �ϲ����Ա�
# combine_history_today.main()

delta_time = datetime.datetime.now() - start_time
print('cost time:', delta_time)
