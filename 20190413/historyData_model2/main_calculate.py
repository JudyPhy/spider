# coding=gbk
from jockey_score import main as jockey_score
from trainer_score import main as trainer_score
from dragon import dragon
import datetime
from today_history import combine_history_today

start_time = datetime.datetime.now()

dragon.main()

# elo����
# jockey_score.main()
# trainer_score.main()

# �ϲ����Ա�
# combine_history_today.main()

delta_time = datetime.datetime.now() - start_time
print('cost time:', delta_time)
