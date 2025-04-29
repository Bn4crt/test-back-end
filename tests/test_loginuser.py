import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_functions.LoginUser.login_user import lambda_handler

class TestLoginUserHandler(unittest.TestCase):
    @patch("lambda_functions.LoginUser.login_user.boto3")
    def test_invalid_credentials(self, mock_boto3):
        # Setup fake DynamoDB resource
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_table.get_item.return_value = {}  # Simulate no item found
        mock_dynamodb.resource.return_value.Table.return_value = mock_table
        mock_boto3.resource.return_value = mock_dynamodb

        event = {
            "body": json.dumps({
                "email": "fake@example.com",
                "password": "Fake123!"
            })
        }

        result = lambda_handler(event, None)

        self.assertIsInstance(result, dict)
        self.assertIn(result["statusCode"], [400, 401, 404])
        self.assertIn("body", result)
