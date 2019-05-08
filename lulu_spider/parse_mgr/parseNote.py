from abc import abstractmethod,ABCMeta
from lxml import etree
import numpy as np
import pandas as pd

class ParseBase(metaclass=ABCMeta):

    _tableLabel = ''

    def parse_page(self,page_source):
        try:
            race_info = self.parse_sole_info(page_source)
            df = self.parse_common_table(page_source,self._tableLabel)
            for key in race_info:
                df[key] = race_info[key]
            return df,True
        except TypeError:
            print('parse_page error!')
            return None,False


    @abstractmethod
    def getUrl(self, url_label):
        return

    @abstractmethod
    def parse_sole_info(self,page_source):
        pass

    def parse_common_table(self, page_source, table_label):
        try:
            xpath_str = '//table[@class="{}"]//tr'.format(table_label)

            html = etree.HTML(page_source)
            hs_history_trs = html.xpath(xpath_str)
            ele_num = len(hs_history_trs[0])
            data_pd = np.empty((0,ele_num))
            for one_tr in hs_history_trs:
                data_tr = np.array([])
                for one_td in one_tr:
                    data_td = one_td.xpath('string(.)').replace('\n','').replace(' ','').replace('\r','')
                    data_tr = np.append(data_tr, data_td)

                if len(data_tr) ==ele_num:
                    data_pd = np.vstack((data_pd, data_tr))

            df = pd.DataFrame(data_pd[1:], columns=data_pd[0])
            return df
        except IndexError:
            print('parse_common_table error!')
            return


