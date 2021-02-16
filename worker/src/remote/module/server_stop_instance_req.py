# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      ServerStopInstanceReq
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------


class ServerStopInstanceReq(object):

    def __init__(self, data=None):
        self.instanceId = None

        if data is not None:
            self.__dict__ = data
