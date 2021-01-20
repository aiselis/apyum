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
from aiohttp.web import RouteTableDef, Request, Response

routes = RouteTableDef()


@routes.post('/{path:.*}')
async def json_rpc(request: Request) -> Response:
    dispatcher = request.app['dispatcher']
    prefix = request.match_info['path'].replace('/', '.')
    return web.json_response(await dispatcher.execute(prefix, await request.json()))
