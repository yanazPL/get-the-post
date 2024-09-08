from enum import StrEnum
from PyQt6.QtNetwork import QNetworkRequest, QNetworkReply


class ACTIONS_METHODS(StrEnum):
    POST = "POST"
    GET = "GET"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


def send_request(network_manager, action_method, url, data=None, params=None, headers=None):
    request = QNetworkRequest(url)
    request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
    if action_method == ACTIONS_METHODS.GET:
        network_manager.get(request)
    elif action_method == ACTIONS_METHODS.POST:
       network_manager.post(request, data)


def handle_response(reply, callback):
    error = reply.error()
    if error == QNetworkReply.NetworkError.NoError:
        print("success")
        data = reply.readAll()
        response_str = data.data().decode()
        callback(response_str)
