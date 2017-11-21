print('***** import start const.py ****')

class _const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if name in self.__dict__.keys(): raise self.ConstError('readonly。再代入禁止。')
        self.__dict__[name]=value

import sys
sys.modules[__name__]=_const()

print('***** import end const.py ****')
