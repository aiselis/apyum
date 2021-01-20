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

class JsonRpcError(Exception):

    def __init__(self, id=None):
        self.id = id

    def __str__(self):
        return f'{self.code} -> {self.message} : {self.id}'

    def to_dict(self):
        return {"jsonrpc": "2.0", "error": {"code": self.code, "message": self.message}, "id": self.id}


class JsonRpcParseError(JsonRpcError):
    code = -32700
    message = "Parse error"


class JsonRpcInvalidRequestError(JsonRpcError):
    code = -32600
    message = "Invalid Request"


class JsonRpcMethodNotFoundError(JsonRpcError):
    code = -32601
    message = "Method not found"


class JsonRpcInvalidParamsError(JsonRpcError):
    code = -32602
    message = "Invalid params"


class JsonRpcInternalError(JsonRpcError):
    code = -32603
    message = "Internal error"
