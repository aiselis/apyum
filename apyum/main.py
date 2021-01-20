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

from apyum.starter import Application
from argparse import ArgumentParser
import yaml
import apyum
import os
import aiohttp


async def create(settings_file=None):
    if not settings_file:
        settings_file = os.environ.get('APYUM_SETTINGS')
    with open(settings_file, 'r') as file:
        settings = yaml.load(file, Loader=yaml.Loader)
        application = Application(settings)
        return application.start()


def run():
    print(apyum.__banner__.format(apyum.__version__))
    parser = ArgumentParser(description='Apyum adapter')
    parser.add_argument('settings', type=str, help='setting file')
    parser.add_argument('--port', '-p', type=int, nargs='?', help='port listener')
    parser.add_argument('--path', '-s', type=str, nargs='?', help='unix socket path')
    args = parser.parse_args()
    aiohttp.web.run_app(create(args.settings), path=args.path, port=args.port)


if __name__ == '__main__':
    run()
