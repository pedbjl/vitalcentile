from unittest.mock import Mock, patch
import unittest

from vitalcentile import CentileClient, centiles, zscore

class VitalCentileTests(unittest.TestCase):
    @patch("vitalcentile.requests.post")
    def test_zscore_convenience_uses_official_api(self, post):
        response = Mock()
        response.json.return_value = {"vital_name": "sbp", "value": 100.0, "zscore": -0.605, "age_month": 72, "percentile": 28}
        post.return_value = response
        result = zscore("sbp", "2018-01-01", "2024-01-01", 100)
        self.assertEqual(result.percentile, 28)
        post.assert_called_once_with(
            "https://centile.research.or.kr/api/sbp/zscore",
            headers={"Content-Type": "application/json"},
            json={"birth_day": "2018-01-01", "measure_timerange": ["2024-01-01", "2024-01-01"], "value": 100.0},
            timeout=15,
        )
        response.raise_for_status.assert_called_once()

    @patch("vitalcentile.requests.get")
    def test_centiles_passes_selected_percentiles(self, get):
        response = Mock(); response.json.return_value = []; get.return_value = response
        self.assertEqual(centiles("hr", [3, 50, 97]), [])
        self.assertEqual(get.call_args.kwargs["params"], [("percent", "3"), ("percent", "50"), ("percent", "97")])

    def test_rejects_unknown_vital(self):
        with self.assertRaisesRegex(ValueError, "vital must be one of"):
            CentileClient().zscore("temperature", "2018-01-01", "2024-01-01", 100)

    def test_rejects_out_of_range_direct_age(self):
        with self.assertRaisesRegex(ValueError, "1–217"):
            CentileClient().calculate("sbp", 218, 100)

if __name__ == "__main__":
    unittest.main()
