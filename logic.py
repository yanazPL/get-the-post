from enum import StrEnum
from http import HTTPStatus
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
import time


request_start_time = None
# replace with Singleton?


class ACTIONS_METHODS(StrEnum):
    POST = "POST"
    GET = "GET"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


def send_request(manager, action_method, url, data=None, params=None, headers=None):
    request = QNetworkRequest(url)
    global request_start_time
    if action_method == ACTIONS_METHODS.GET:
        manager.get(request)
    elif action_method == ACTIONS_METHODS.POST:
        manager.post(request, data)
    elif action_method == ACTIONS_METHODS.PATCH:
        manager.patch(request, data)
    elif action_method == ACTIONS_METHODS.DELETE:
        manager.deleteResource(request)
    elif action_method == ACTIONS_METHODS.PUT:
        request.setHeader(
            QNetworkRequest.ContentTypeHeader, "application/json; charset=UTF-8"
        )
        manager.put(request, data)
    request_start_time = time.time()


def bytes_to_kb(bytes):
    kb = bytes / 1024
    return f"{kb:.1f} KB"


def float_time_to_ms(float_time):
    return round(float_time * 1000)


def get_status_message(status_code):
    try:
        # Get the status name from HTTPStatus
        status_message = HTTPStatus(status_code).phrase
        return f"{status_code} {status_message}"
    except ValueError:
        # If the status code is not found in HTTPStatus
        return f"{status_code} Unknown Status Code"


def handle_response(reply, callback):
    request_time = float_time_to_ms(time.time() - request_start_time)
    error = reply.error()
    if error == QNetworkReply.NetworkError.NoError:
        data = reply.readAll()
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        data_bytes = data.data()
        response_str = data_bytes.decode()
        callback(response_str, status_code, request_time)
