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

from apyum.service import Dispatcher, CeleryClient
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch


class DispatchTest(IsolatedAsyncioTestCase):

    @patch('celery.Celery')
    async def test_run_single_notify(self, mock):
        request = {"jsonrpc": "2.0", "method": "test", "params": ["1"]}
        celery_client = CeleryClient({})
        dispatcher = Dispatcher(celery_client)
        await dispatcher.run_single("", request)

    @patch('celery.Celery')
    async def test_run_single_result(self, mock):
        request = {"jsonrpc": "2.0", "method": "test", "params": ["1"], "id": "1"}
        celery_client = CeleryClient({})
        celery_client.celery.send_task.return_value.get.return_value = 3
        dispatcher = Dispatcher(celery_client)
        response = await dispatcher.run_single("", request)
        assert response['id'] is "1"
        assert response['result'] is 3

    @patch('celery.Celery')
    async def test_run_batch(self, mock):
        request = [
            {"jsonrpc": "2.0", "method": "test", "params": ["1"], "id": "1"},
            {"jsonrpc": "2.0", "method": "test", "params": ["2"], "id": "2"},
            {"jsonrpc": "2.0", "method": "test", "params": ["4"], "id": "3"},
            {"jsonrpc": "2.0", "method": "test", "params": ["4"]},
            {"jsonrpc": "2.0", "method": "test", "params": ["4"]}
        ]
        celery_client = CeleryClient({})
        dispatcher = Dispatcher(celery_client)
        response = await dispatcher.run_batch("", request)
        assert celery_client.celery.send_task.call_count is 5
        assert len(response) is 3

