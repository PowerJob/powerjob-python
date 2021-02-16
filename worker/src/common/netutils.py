# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      NetUtils
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import socket


class NetUtils:

    @staticmethod
    def get_local_host() -> str:
        return socket.gethostbyname(socket.gethostname())
