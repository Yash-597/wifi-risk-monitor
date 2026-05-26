import tempfile
import unittest
from pathlib import Path

from core.audit_log import clear_events, read_events, write_event
from core.models import AuditEvent


class AuditLogTests(unittest.TestCase):
    def test_read_events_returns_latest_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            for index in range(3):
                write_event(
                    AuditEvent(
                        timestamp=f"2026-05-20T00:00:0{index}",
                        ssid=f"ssid-{index}",
                        bssid=None,
                        authentication="WPA2-Personal",
                        cipher="CCMP",
                        risk_level="safe",
                        reason="test",
                    ),
                    path,
                )

            events = read_events(path, limit=2)

        self.assertEqual([event["ssid"] for event in events], ["ssid-1", "ssid-2"])

    def test_clear_events_empties_log(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            path.write_text('{"ssid": "x"}\n', encoding="utf-8")

            clear_events(path)

            self.assertEqual(path.read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
