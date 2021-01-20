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

from aiohttp import web
from apyum.middleware import validator_handler
from apyum.service import CeleryClient, Dispatcher
from apyum.endpoint import routes
import logging


class Application:

    def __init__(self, settings: dict):
        self.settings = settings
        self.app = None
        self.logger = logging.getLogger('apyum')
        if 'logging' in settings:
            logging.config.dictConfig(self.settings['logging'])
        else:
            logging.basicConfig(format="%(asctime)s - %(name)s [%(levelname)s] - %(message)s", level=logging.INFO)

    def start(self):
        self.app = web.Application(middlewares=[validator_handler], logger=self.logger)
        celery = CeleryClient(self.settings['celery'])
        self.app['dispatcher'] = Dispatcher(celery, self.logger)
        self.app.add_routes(routes)
        return self.app
