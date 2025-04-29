import unittest
from unittest.mock import patch
from lambda_functions.LoginUser.login_user import lambda_handler

class TestLoginUserHandler(unittest.TestCase):
    @patch("lambda_functions.LoginUser.login_user.boto3.resource")
    def test_invalid_credentials(self, mock_boto_resource):
        # Setup the fake DynamoDB response
        mock_table = mock_boto_resource.return_value.Table.return_value
        mock_table.get_item.return_value = {}  # No Item returned

        event = {
            "body": "{\"email\": \"fake@example.com\", \"password\": \"Fake123!\"}"
        }

        result = lambda_handler(event, None)
        self.assertIn(result["statusCode"], [400, 401, 404])

if __name__ == '__main__':
    unittest.main()
