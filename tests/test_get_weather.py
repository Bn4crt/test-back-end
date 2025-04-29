import unittest
import json
from unittest.mock import patch, MagicMock
from lambda_functions.GetWeatherByLocation.get_weather import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    @patch.dict('os.environ', {'WEATHER_API_KEY': 'dummy-key'})
    def test_lambda_returns_error_without_location(self, mock_requests_get):
        event = {"queryStringParameters": {}}
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertIn("error", body)
        self.assertEqual(body["error"], "No location or coordinates provided")
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
        body = json.loads(result["body"])
        self.assertEqual(body["location"], "London")
        self.assertEqual(body["temperature"], 20)
        self.assertEqual(body["condition"], "Cloudy")

    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    def test_lambda_returns_500_missing_api_key(self, mock_requests_get):
        event = {"queryStringParameters": {"location": "London"}}
        with patch.dict('os.environ', {}, clear=True):  # Clear all env vars
            result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Missing WEATHER_API_KEY in environment")
        mock_requests_get.assert_not_called()

    @patch('lambda_functions.GetWeatherByLocation.get_weather.requests.get')
    @patch.dict('os.environ', {'WEATHER_API_KEY': 'dummy-key'})
    def test_lambda_handles_weather_api_failure(self, mock_requests_get):
        mock_requests_get.side_effect = Exception("Simulated API crash")

        event = {"queryStringParameters": {"location": "Paris"}}
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertIn("error", body)
        self.assertTrue("Internal server error" in body["error"])

if __name__ == '__main__':
    unittest.main()
