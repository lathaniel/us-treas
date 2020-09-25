import re as _re
import pandas as _pd
import xml.etree.ElementTree as _ET

from . import utils

class Rate:
  ''' U.S. Treasury Rate data

  Can be one of many types available on treasury.gov

  '''
  def __init__(self):
    self.domain = 'https://www.treasury.gov'
    self.serverPath = 'resource-center/data-chart-center/interest-rates/pages'
    self.data = None # Not sure what to do here yet
    self._info = ''
  
  def history(self, period='current', term = 'all', viewStyle='xml'):
    '''Get the historical rates for the period.

    TODO: Allow for term selection

    Args:
      period: Specifies the period for which to request rates
      term: Specifies the desired term length, if applicable (e.g. 30)
      viewStyle: Specifies whether to grab from the TextView site or the XmlView site
        XmlView contains more data and can be retrieved slightly quicker.
        TextView represents the "standard" data one would see, and has more conventional column names.      

    Returns:
      Pandas Dataframe with requested rates

    '''
    if period.lower()=='current':
      q = ''
    
    elif _re.match('\d{4}', period):
      # User provided a year
      q = 'Year&year={}'.format(period)
    
    elif period.lower()=='all':
      # user wants  a l l  of the data
      q = 'All'
    
    assert viewStyle.lower() in ('xml', 'text'), "viewStyle must be one of 'xml' or 'text'"
    url = '{}/{}/{}View.aspx?data={}{}'.format(self.domain, self.serverPath, viewStyle, self.data, q)
    
    if viewStyle.lower()=='text':
      return _pd.read_html(url)[1] # not sure if it will always be index 1
    
    xml = utils.getPageText(url)
    parsed = __parseTreasuryXML(xml)

    return _pd.json_normalize(parsed)
  
  def __get_info(self):
    # TODO: also, print it prettier?
    url = '{}/{}/TextView.aspx?data={}'.format(self.domain, self.serverPath, self.data)
    txt = utils.getPageText(url)
    tbl = _re.search('<table>([\s\S]+?)</table>[\s]*?</div>', txt)[1]
    after = tbl.split('<div class="u_pdated"')[-1]
    info = ''.join(_re.findall('>([^>]+)</', after))
    self._info = info    

  def __parseTreasuryXML(self, s):
    l = []
    # I use list comprehension so I can ignore namespaces
    root = _ET.fromstring(s)
    entries = [x for x in root if 'entry' in x.tag]
    for entry in entries:
      content = [x for x in entry if 'content' in x.tag][0]
      prop = [x for x in content if 'properties' in x.tag][0]
      keys = [_re.search('\\{.*\\}(\w+)', x.tag)[1] for x in prop]
      vals = [x.text for x in prop]
      d = dict(zip(keys, vals))
      l.append(d.copy())
    
    return l

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