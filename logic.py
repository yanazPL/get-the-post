from enum import StrEnum
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply


class ACTIONS_METHODS(StrEnum):
    POST = "POST"
    GET = "GET"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


def send_request(manager, action_method, url, data=None, params=None, headers=None):
    request = QNetworkRequest(url)
    if action_method == ACTIONS_METHODS.GET:
        manager.get(request)
    elif action_method == ACTIONS_METHODS.POST:
       manager.post(request, data)
    elif action_method == ACTIONS_METHODS.PATCH:
        manager.patch(request, data)
    elif action_method == ACTIONS_METHODS.DELETE:
        manager.deleteResource(request)
    elif action_method == ACTIONS_METHODS.PUT:
        request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json; charset=UTF-8')
        manager.put(request, data)
        

def handle_response(reply, callback):
    error = reply.error()
    if error == QNetworkReply.NetworkError.NoError:
        data = reply.readAll()
        response_str = data.data().decode()
        callback(response_str)
