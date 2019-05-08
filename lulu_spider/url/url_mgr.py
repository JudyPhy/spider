
class UrlMgr():

    def get_horseOrder_url(self,order):
        order_url = 'https://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype={}'.format(
            order)
        return order_url

    def get_raceCard_url(self,raceDate):
        raceCard_url = 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/{}'.format(raceDate)
        return raceCard_url

    def get_raceResult_url(self,raceDate):
        raceResult_url = 'https://racing.hkjc.com/racing/information/chinese/racing/LocalResults.aspx?RaceDate={}'.format(raceDate)
        return raceResult_url


