# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      ResultDTO from powerjob server
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import json


class ResultDTO(object):

    def __init__(self, d):
        # 声明属性
        self.success = None
        self.data = None
        self.message = None
        # 把json解析之后的dict直接赋值给对象的属性dict，然后就可以随心所欲的使用属性了
        self.__dict__ = d


def convert(data) -> ResultDTO:
    return json.loads(data, object_hook=ResultDTO)
