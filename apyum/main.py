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
from argparse import ArgumentParser, FileType
import yaml
import apyum


def run():
    parser = ArgumentParser(description='Apyum adapter')
    parser.add_argument('settings', type=FileType('r'), help='setting file')
    parser.add_argument('--port', '-p', type=int, nargs='?', help='port listener')
    parser.add_argument('--path', '-s', type=str, nargs='?', help='unix socket path')
    args = parser.parse_args()
    settings = yaml.load(args.settings, Loader=yaml.Loader)
    print(apyum.__banner__.format(apyum.__version__))
    app = Application(settings)
    app.run(args.path, args.port)


if __name__ == '__main__':
    run()
