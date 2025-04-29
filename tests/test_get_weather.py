import unittest
from unittest.mock import patch, MagicMock
from lambda_functions.GetWeatherByLocation.get_weather import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    @patch.dict('os.environ', {'WEATHER_API_KEY': 'dummy-key'})
    def test_lambda_returns_error_without_location(self, mock_requests_get):
        event = {"queryStringParameters": {}}
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)
        mock_requests_get.assert_not_called()

    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    @patch.dict('os.environ', {'WEATHER_API_KEY': 'dummy-key'})
    def test_lambda_returns_success_for_city(self, mock_requests_get):
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
