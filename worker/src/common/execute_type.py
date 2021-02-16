# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      ExecuteType
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
from enum import Enum


class ExecuteType(Enum):
    STANDALONE = 1
    BROADCAST = 2
    MAP_REDUCE = 3
    MAP = 4
