import unittest
from unittest.mock import patch, Mock
import httpx

# Assuming the create_group function is defined in a module named group_utils.utils
from utils.utils import create_group, delete_group


class TestDeleteGroup(unittest.TestCase):
    @patch('utils.utils.httpx.delete')
    def test_delete_group_success(self, mock_delete):
        mock_response = httpx.Response(200, json={"status": "success"})
        mock_delete.return_value = mock_response

        url = "http://example.com/delete"
        payload = {"groupId": "123"}

        response = delete_group(url, payload)
        self.assertEqual(response, {"status": "success"})
        mock_delete.assert_called_once_with(url, params=payload)

    @patch('utils.utils.httpx.delete')
    def test_delete_group_failure(self, mock_delete):
        mock_response = httpx.Response(400, json={'message': 'Request failed', 'status': 400})
        mock_delete.return_value = mock_response

        url = "http://example.com/delete"
        payload = {"groupId": "123"}

        response = delete_group(url, payload)
        self.assertEqual(response, {'message': 'Request failed', 'status': 400})
        mock_delete.assert_called_once_with(url, params=payload)

    @patch('utils.utils.httpx.delete')
    def test_delete_group_exception(self, mock_delete):
        mock_delete.side_effect = httpx.RequestError("Connection error")

        url = "http://example.com/delete"
        payload = {"groupId": "123"}

        response = delete_group(url, payload)
        self.assertEqual(response, {'message': 'Connection error', 'status': 'error'})
        mock_delete.assert_called_once_with(url, params=payload)


class TestCreateGroup(unittest.TestCase):
    @patch('utils.utils.httpx.post')
    def test_create_group_success(self, mock_post):
        mock_response = httpx.Response(201, json={"status": "success"})
        mock_post.return_value = mock_response

        url = "http://example.com/create"
        payload = {"name": "Test Group"}

        response = create_group(url, payload)
        self.assertEqual(response, {"status": "success"})
        mock_post.assert_called_once_with(url, json=payload)

    @patch('utils.utils.httpx.post')
    def test_create_group_failure(self, mock_post):
        mock_response = httpx.Response(400, json={"error": "Bad Request"})
        mock_post.return_value = mock_response

        url = "http://example.com/create"
        payload = {"name": "Test Group"}

        response = create_group(url, payload)
        self.assertEqual(response, {"error": "Bad Request"})
        mock_post.assert_called_once_with(url, json=payload)

    @patch('utils.utils.httpx.post')
    def test_create_group_exception(self, mock_post):
        mock_post.side_effect = httpx.RequestError("Connection error")

        url = "http://example.com/create"
        payload = {"name": "Test Group"}

        response = create_group(url, payload)
        self.assertEqual(response, {})
        mock_post.assert_called_once_with(url, json=payload)


if __name__ == '__main__':
    unittest.main()

