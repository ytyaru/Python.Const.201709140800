import sub
import const
print('const:', const, type(const))#<const._const object at 0xb7162f4c>

const.test = "Test1"
print(const.test)
#const.test = "Test2"
#print(const.test)

import const
#const.test = "Test2" #const.ConstError: readonly。再代入禁止。

