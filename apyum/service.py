#
#    Copyright 2021 Alessio Pinna <alessio.pinna@aiselis.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from apyum.exceptions import *
from jsonschema import ValidationError
from functools import partial
import jsonschema
import logging
import asyncio
import celery
import celery.exceptions


class CeleryClient:

    def __init__(self, settings: dict, loop=None):
        self.celery = celery.Celery('celery-adapter')
        self.celery.conf.update(**settings)
        self.loop = loop if loop else asyncio.get_event_loop()

    async def call(self, id, method, params, executor=None):
        args = params if isinstance(params, list) else None
        kwargs = params if isinstance(params, dict) else None
        try:
            if not id:
                send_task_func = partial(self.celery.send_task, method, args, kwargs, ignore_result=True)
                await self.loop.run_in_executor(executor, send_task_func)
            else:
                send_task_func = partial(self.celery.send_task, method, args, kwargs, ignore_result=False)
                response = await self.loop.run_in_executor(executor, send_task_func)
                get_func = partial(response.get)
                return await self.loop.run_in_executor(executor, get_func)
        except celery.exceptions.NotRegistered:
            raise JsonRpcMethodNotFoundError(id)


class Dispatcher:
    schema = {
        'type': 'object',
        'properties': {
            'jsonrpc': {'const': '2.0'},
            'method': {'type': 'string'},
            'params': {'type': ['array', 'object']},
            'id': {'type': 'string'},
        },
        'required': ['jsonrpc', 'method', 'params']
    }

    def __init__(self, celery: CeleryClient, logger=logging.getLogger()):
        self.celery = celery
        self.logger = logger

    def validate(self, request):
        try:
            jsonschema.validate(request, self.schema)
        except ValidationError:
            raise JsonRpcInvalidRequestError()

    async def run_single(self, prefix, request):
        try:
            self.validate(request)
            self.logger.info(f"Sending request {request}")
            method = f"{prefix}.{request['method']}" if prefix else request['method']
            if 'id' in request:
                return dict(
                    jsonrpc='2.0',
                    result=await self.celery.call(request['id'], method, request['params']),
                    id=request['id']
                )
            else:
                await self.celery.call(None, method, request['params'])
        except JsonRpcError as error:
            self.logger.error(f"{error}")
            return error.to_dict()

    async def run_batch(self, prefix, request: list) -> list:
        result = list()
        for partial in asyncio.as_completed([self.run_single(prefix, row) for row in request]):
            item = await partial
            if item:
                result.append(item)
        return result

    async def execute(self, prefix, request):
        if isinstance(request, list):
            return await self.run_batch(prefix, request)
        else:
            return await self.run_single(prefix, request)
