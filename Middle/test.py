from Worker import *

module = __import__('Worker')

class_ = getattr(module,'NET.Net')
obj = class_()

