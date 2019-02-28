from data_request.request import RequestData


requestData = RequestData()
TIME_FROM = 20180900
TIME_TO = 20181031

dataList = requestData.getDataList(TIME_FROM, TIME_TO)
print(len(dataList))