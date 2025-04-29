import unittest
from unittest.mock import patch, MagicMock
from lambda_functions.GetWeatherByLocation.get_weather import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    def test_lambda_returns_error_without_location(self, mock_requests_get):
        # No location or lat/lon -> should return 400 directly without calling requests.get
        event = {"queryStringParameters": {}}
        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        mock_requests_get.assert_not_called()  # ✅ Make sure no external API call happens

    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    def test_lambda_returns_success_for_city(self, mock_requests_get):
        # Setup mock for requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "main": {"temp": 20},
            "weather": [{"main": "Cloudy"}],
            "name": "London"
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        event = {"queryStringParameters": {"location": "London"}}
        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("temperature", result["body"])

if __name__ == '__main__':
    unittest.main()
