import unittest
import GetWeatherByLocation as get_weather

class TestLambdaFunction(unittest.TestCase):
    def test_lambda_returns_error_without_location(self):
        event = {"queryStringParameters": {}}
        result = get_weather.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)

    def test_lambda_returns_success_for_city(self):
        event = {"queryStringParameters": {"location": "London"}}
        result = get_weather.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("temperature", result["body"])

if __name__ == '__main__':
    unittest.main()
