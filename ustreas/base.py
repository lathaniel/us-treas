import re as _re
import pandas as _pd
import xml.etree.ElementTree as _ET
import warnings

from . import utils


class Rate:
    ''' U.S. Treasury Rate data

    Can be one of many types available on treasury.gov

    '''

    def __init__(self):
        self.domain = 'https://www.treasury.gov'
        self.serverPath = 'resource-center/'\
            'data-chart-center/interest-rates/pages'
        self.data = None  # Not sure what to do here yet
        self._info = ''

    def history(self, period='current', term='all', viewStyle='xml'):
        '''Get the historical rates for the period.

        TODO: Allow for term selection

        Args:
          period (str or int): Specifies the period for which to request rates.
            Can be one of 'current' or 'YYYY'

            * *current* will return all available rates for the current month.
            * *2020* would return all available rates for the year 2020.

          term (str): Specifies the desired term length, if applicable
            (e.g. 30). Logic for this is not yet built in.
          viewStyle (str):
            Specifies whether to grab data from the TextView site
            or the XmlView site.

            * XmlView site usually contains more data attributes.
            * TextView represents the "standard" data, i.e. most comparable\
            to what one would see on the website.

        Returns:
          Pandas Dataframe with requested rates.

        '''
        if not isinstance(period, (str, int)):
            raise TypeError("period must be of type str or int")

        # Convert period to string, in case user provided int
        period = str(period)

        if period.lower() == 'current':
            q = ''

        elif _re.match(r'\d{4}', period):
            # User provided a year
            q = 'Year&year={}'.format(period)

        elif period.lower() == 'all':
            # user wants  a l l  of the data
            q = 'All'

        assert viewStyle.lower() in ('xml', 'text'), "viewStyle must be"\
            "one of 'xml' or 'text'"
        url = '{}/{}/{}View.aspx?data={}{}'.format(
            self.domain, self.serverPath, viewStyle, self.data, q)

        if viewStyle.lower() == 'text':
            # not sure if it will always be index 1
            return _pd.read_html(url)[1]

        xml = utils.getPageText(url)
        parsed = self.__parseTreasuryXML(xml)
        df = _pd.json_normalize(parsed)
        if not len(df):
            warnings.warn(
                "No data found for {}. There may not be available"
                "treasury data for that period.".format(period))

        return df

    def __get_info(self):
        # TODO: also, print it prettier?
        url = '{}/{}/TextView.aspx?data={}'.format(
            self.domain, self.serverPath, self.data)
        txt = utils.getPageText(url)
        tbl = _re.search(r'<table>([\s\S]+?)</table>[\s]*?</div>', txt)[1]
        after = tbl.split('<div class="u_pdated"')[-1]
        info = ''.join(_re.findall('>([^>]+)</', after))
        self._info = info

    def __parseTreasuryXML(self, s):
        list_data = []
        # I use list comprehension so I can ignore namespaces
        root = _ET.fromstring(s)
        entries = [x for x in root if 'entry' in x.tag]
        for entry in entries:
            content = [x for x in entry if 'content' in x.tag][0]
            prop = [x for x in content if 'properties' in x.tag][0]
            keys = [_re.search(r'\\{.*\\}(\w+)', x.tag)[1] for x in prop]
            vals = [x.text for x in prop]
            d = dict(zip(keys, vals))
            list_data.append(d.copy())

        return list_data

    @property
    def info(self):
        '''Information from U.S. Treasury site for the specified rates'''
        if self._info == '':
            # Retrieve it
            self.__get_info()

        print(utils.unescape(self._info))

    @info.setter
    def info(self, val):
        self._info = val
