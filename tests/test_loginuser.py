import json
import unittest
from unittest.mock import patch
from lambda_functions.LoginUser.login_user import lambda_handler

class TestLoginUserHandler(unittest.TestCase):
    @patch("lambda_functions.LoginUser.login_user.boto3.resource")
    def test_invalid_credentials(self, mock_boto_resource):
        # Arrange: Setup fake DynamoDB table returning no item
        mock_table = mock_boto_resource.return_value.Table.return_value
        mock_table.get_item.return_value = {}  # No item simulates invalid credentials

        event = {
            "body": json.dumps({
                "email": "fake@example.com",
                "password": "Fake123!"
            })
        }

        # Act: Call Lambda function
        result = lambda_handler(event, None)

        # Assert: Expecting client error status code
        self.assertIsInstance(result, dict)
        self.assertIn(result["statusCode"], [400, 401, 404])
        self.assertIn("body", result)
