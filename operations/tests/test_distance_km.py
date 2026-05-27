from decimal import Decimal

from django.test import SimpleTestCase

from operations.services.distance_km import distance_km_str, round_distance_km


class DistanceKmRoundingTests(SimpleTestCase):
    def test_round_half_up(self):
        self.assertEqual(round_distance_km(Decimal("99.5")), 100)
        self.assertEqual(round_distance_km(Decimal("99.4")), 99)
        self.assertEqual(round_distance_km(Decimal("20.00")), 20)
        self.assertEqual(distance_km_str(Decimal("22.75")), "23")
        self.assertEqual(distance_km_str(None), "")
