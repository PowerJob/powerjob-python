# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      PowerJob Exception
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------


class PowerJobError(RuntimeError):

    def __init__(self, arg):
        self.args = arg
