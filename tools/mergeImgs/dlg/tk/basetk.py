#coding: utf-8
import random

#获得随机数（整型）
#Sample: GetRandom(1, 100) #可获得1~100之间的随机整数
def GetRandom(begin, end):
    return random.randint(begin, end)