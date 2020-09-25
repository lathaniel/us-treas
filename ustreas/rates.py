from .base import Rate

class YieldCurve(Rate):
  ''' Yield Curve Rate data

  Args:
    real (bool): Specifies whether to request "real" rates or not.

  '''
  def __init__(self, real = False):
    super().__init__()
    rateType = 'real' if real==True else ''
    self.data = '{}yield'.format(rateType)

class Bill(Rate):
  '''Bill Rate data

  '''
  def __init__(self):
    super().__init__()
    self.data = 'billrates'

class LongTerm(Rate):
  '''Long Term Rate data

  Args:
    real (bool): Specifies whether to request "real" rates or not.

  '''
  def __init__(self, real = False):
    super().__init__()
    rateType = 'real' if real else ''
    self.data = '{}longtermrate'.format(rateType)
