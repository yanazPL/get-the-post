from ..logic import send_request, ACTIONS_METHODS, handle_response
from .conftest import data_str_update, data_str_create
from unittest.mock import Mock
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager, QRestAccessManager
from PySide6.QtCore import QUrl, QByteArray
import pytest


def test_delete_request():
    rest_manager = Mock()
    callback = Mock()

    mock_reply = Mock(spec=QNetworkReply)
    mock_reply.error.return_value = QNetworkReply.NetworkError.NoError
    mock_reply.readAll.return_value = QByteArray(data_str_create.encode("utf-8"))
    rest_manager.deleteResource.return_value = mock_reply

    send_request(rest_manager, ACTIONS_METHODS.DELETE, QUrl("example.com/api/1"))
    handle_response(mock_reply, callback)
    rest_manager.deleteResource.assert_called_once()
    callback.assert_called_once()

@pytest.mark.parametrize("action_method, method_str", [[ACTIONS_METHODS.PUT, "put"], [ACTIONS_METHODS.PATCH, "patch"]])
def test_update_request(action_method, method_str):
    rest_manager = Mock()
    callback = Mock()
    rest_method = getattr(rest_manager, method_str)
    data = '{"id": 1, "title", "new_title"}'.encode("utf-8")
    reply = Mock(spec=QNetworkReply)
    reply.error.return_value = QNetworkReply.NetworkError.NoError
    reply.return_value = QByteArray(data)
    send_request(rest_manager, action_method, QUrl("example.com/api/1"), data)
    handle_response(reply, callback)
    rest_method.assert_called_once()


def test_post_request():
    rest_manager = Mock()
    callback = Mock()
    data = bytes(data_str_create, "utf-8")
    
    mock_reply = Mock(spec=QNetworkReply)
    mock_reply.error.return_value = QNetworkReply.NetworkError.NoError
    mock_reply.readAll.return_value = QByteArray(data)
    rest_manager.post.return_value = mock_reply

    send_request(rest_manager, ACTIONS_METHODS.POST, QUrl("example.com/api/1"), data)
    handle_response(mock_reply, callback)
    rest_manager.post.assert_called_once()
    callback.assert_called_once()

def test_get_request():
    rest_manager = Mock()
    callback = Mock()

    mock_reply = Mock(spec=QNetworkReply)
    mock_reply.error.return_value = QNetworkReply.NetworkError.NoError
    mock_reply.readAll.return_value = QByteArray(data_str_create.encode("utf-8"))
    rest_manager.get.return_value = mock_reply

    send_request(rest_manager, ACTIONS_METHODS.GET, QUrl("example.com/api/1"))
    handle_response(mock_reply, callback)
    rest_manager.get.assert_called_once()
    callback.assert_called_once()