# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      start http server for handler
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import asyncio
import threading
from aiohttp import web

from common.log import log
from common.constant import *
from remote.handler.server_request_handler import ServerRequestHandler


# 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


class HttpHandlerStarter(object):

    def __init__(self):
        handler = ServerRequestHandler()
        self.app = web.Application()
        self.app.add_routes([
            web.post(WORKER_RECEIVE_SCHEDULE_PATH, handler.on_receive_server_schedule_job_req),
            web.post(WORKER_STOP_INSTANCE_PATH, handler.on_receive_server_stop_instance_req),
        ])
        self.runner = web.AppRunner(self.app)

    async def start_server(self, ip, port):
        await self.runner.setup()
        site = web.TCPSite(self.runner, ip, port)
        await site.start()

        # sleep forever
        while True:
            await asyncio.sleep(3600)

    def start(self, ip: str, port: int):

        log.info("[HttpHandler] start to listen %s:%d", ip, port)

        new_loop = asyncio.new_event_loop()
        # 通过当前线程开启新的线程去启动事件循环
        t = threading.Thread(target=start_loop, args=(new_loop,))
        t.start()
        asyncio.run_coroutine_threadsafe(self.start_server(ip, port), new_loop)

        log.info("[HttpHandler] start aio http server successfully")
