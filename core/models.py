from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    SAFE = "safe"
    RISKY = "risky"
    PROTECTED = "protected"
    UNKNOWN = "unknown"
    TRUSTED = "trusted"
    PAUSED = "paused"


@dataclass(frozen=True)
class WifiNetwork:
    ssid: str | None
    bssid: str | None
    authentication: str | None
    cipher: str | None
    signal: str | None
    connected: bool


@dataclass(frozen=True)
class RiskAssessment:
    level: RiskLevel
    reason: str


@dataclass(frozen=True)
class AuditEvent:
    timestamp: str
    ssid: str | None
    bssid: str | None
    authentication: str | None
    cipher: str | None
    risk_level: str
    reason: str

    @classmethod
    def from_assessment(
        cls,
        network: WifiNetwork,
        assessment: RiskAssessment,
    ) -> "AuditEvent":
        return cls(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            ssid=network.ssid,
            bssid=network.bssid,
            authentication=network.authentication,
            cipher=network.cipher,
            risk_level=assessment.level.value,
            reason=assessment.reason,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
