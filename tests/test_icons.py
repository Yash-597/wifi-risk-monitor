import unittest

from app.icons import build_icon
from core.models import RiskLevel


class IconTests(unittest.TestCase):
    def test_builds_paused_icon(self) -> None:
        icon = build_icon(RiskLevel.PAUSED)

        self.assertEqual(icon.size, (64, 64))


if __name__ == "__main__":
    unittest.main()
