import unittest
from datetime import datetime, timezone

LICENSE_EXPIRES = datetime(2026, 10, 8, 15, 21, tzinfo=timezone.utc)


class LicenseTest(unittest.TestCase):
    def test_license_not_expired(self):
        self.assertLess(datetime.now(timezone.utc), LICENSE_EXPIRES, "sandbox license expired")
