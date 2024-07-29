import unittest
from unittest.mock import patch, MagicMock
import json
from main import app


class TestGroupAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('utils.utils.httpx.post')
    @patch('utils.utils.retry_operation')
    def test_create_group_api_success(self, mock_retry_operation,
                                      mock_httpx_post):
        # Mocking the post method to return a successful response
        mock_httpx_post.return_value = MagicMock(status_code=200, json=lambda: {'status': 200})
        mock_retry_operation.return_value = {'status': 200}

        response = self.client.post('/v1/create_groups', json={'groupId': 'test-group'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'creation completed in all nodes'})

    @patch('utils.utils.httpx.post')
    def test_create_group_api_failure(self, mock_httpx_post):
        # Mocking the post method to return a failure response
        mock_httpx_post.return_value = MagicMock(status_code=400, json=lambda: {'status': 400})

        response = self.client.post('/v1/create_groups', json={'groupId': 'test-group'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'failed to create in all nodes'})

    @patch('utils.utils.httpx.post')
    @patch('utils.utils.httpx.delete')
    def test_create_group_api_partial_success(self, mock_httpx_delete,
                                              mock_httpx_post):
        # Mocking the post method to return mixed responses
        mock_httpx_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=400, json=lambda: {"status": 400})
        ]
        mock_httpx_delete.return_value = MagicMock(status_code=200,
                                                   json=lambda: {
                                                       "status": 200})

        # Sending a POST request to the create_group_api
        response = self.client.post('/v1/create_groups',
                                    json={'groupId': 'test-group'})

        # Asserting that the status code is 500 and the expected message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'message': 'rollback success'})

    @patch('utils.utils.httpx.post')
    @patch('utils.utils.httpx.delete')
    def test_create_group_api_retry_failure(self, mock_httpx_delete,
                                            mock_httpx_post):
        # Mocking the post method to return mixed responses
        mock_httpx_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=400, json=lambda: {"status": 400})
        ]
        mock_httpx_delete.return_value = MagicMock(status_code=400,
                                                   json=lambda: {
                                                       "status": 400})

        # Sending a POST request to the create_group_api
        response = self.client.post('/v1/create_groups',
                                    json={'groupId': 'test-group'})

        # Asserting that the status code is 500 and the expected message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': 'max retry failed for url http://localhost:5001/v1/group/one'})


    #delete

    @patch('utils.utils.httpx.delete')
    def test_delete_group_api_success(self, mock_httpx_delete):
        # Mocking the delete method to return a successful response
        mock_httpx_delete.return_value = MagicMock(status_code=200, json=lambda: {"status": 200})

        # Sending a DELETE request to the delete_group_api with JSON payload
        response = self.client.delete('/v1/delete_groups', json={"groupId": "123"})

        # Printing response for debugging
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json)

        # Asserting that the status code is 200 and the expected message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'deletion completed in all nodes'})

    @patch('utils.utils.httpx.delete')
    def test_delete_group_api_failure(self, mock_delete_group):
        # Mocking the delete_group function to return a failure response
        mock_delete_group.return_value = {'status': 400}

        # Sending a DELETE request to the delete_group_api
        response = self.client.delete('/v1/delete_groups', json={'groupId': "123"})

        # Asserting that the status code is 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'failed to delete in all nodes'})

    @patch('utils.utils.httpx.delete')
    @patch('utils.utils.httpx.post')
    @patch('utils.utils.retry_operation')
    def test_delete_group_api_partial_success(self, mock_retry_operation, mock_create_group, mock_delete_group):
        # Mocking the delete_group function to return mixed responses
        mock_delete_group.side_effect = [
            {'status': 200}, {'status': 200}, {'status': 500}
        ]
        mock_create_group.return_value = {'status': 200}
        mock_retry_operation.return_value = {'status': 200}

        # Sending a DELETE request to the delete_group_api
        response = self.client.delete('/v1/delete_groups', json={'groupId': '123'})

        # Asserting that the status code is 500
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'failed to delete in all nodes'})

    @patch('utils.utils.httpx.delete')
    @patch('utils.utils.httpx.post')
    def test_delete_group_api_retry_failure(self, mock_httpx_post,
                                            mock_httpx_delete):
        # Mocking the delete method to return mixed responses
        mock_httpx_delete.side_effect = [
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=200, json=lambda: {"status": 200}),
            MagicMock(status_code=400, json=lambda: {"status": 400})
        ]

        # Mocking the post method to fail for the third URL
        def post_side_effect(url, *args, **kwargs):
            if "group/three" in url:
                return MagicMock(status_code=400, json=lambda: {"status": 400})
            return MagicMock(status_code=200, json=lambda: {"status": 200})

        mock_httpx_post.side_effect = post_side_effect

        # Sending a DELETE request to the delete_group_api
        response = self.client.delete('/v1/delete_groups',
                                      json={'groupId': 'test-group'})

        # Asserting that the status code is 500 and the expected message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': 'max retry failed for url http://localhost:5001/v1/group/one'})


if __name__ == '__main__':
    unittest.main()
