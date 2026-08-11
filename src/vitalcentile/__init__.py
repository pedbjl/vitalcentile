from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal
import requests

Vital = Literal['sbp', 'dbp', 'mbp', 'hr', 'rr']

@dataclass(frozen=True)
class ZScoreResult:
    vital_name: str
    value: float
    zscore: float
    age_month: int
    percentile: int

class CentileClient:
    """Client for the official Centile pediatric vital-sign reference API."""
    def __init__(self, base_url: str = 'https://centile.research.or.kr', headers: dict[str, str] | None = None, timeout: float = 15):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout

    def calculate(self, vital: Vital, age_month: int, value: float) -> ZScoreResult:
        if vital not in {'sbp', 'dbp', 'mbp', 'hr', 'rr'}:
            raise ValueError('vital must be one of: sbp, dbp, mbp, hr, rr')
        if not 1 <= int(age_month) <= 217:
            raise ValueError('age_month must be in the supported range 1–217')
        response = requests.post(f'{self.base_url}/api/v1/centile/{vital}', headers={'Content-Type': 'application/json', **self.headers}, json={'age_month': int(age_month), 'value': float(value)}, timeout=self.timeout)
        response.raise_for_status()
        return ZScoreResult(**response.json())

    def zscore(self, vital: Vital, birth_day: str | date, measured_at: str | date | datetime, value: float) -> ZScoreResult:
        if vital not in {'sbp', 'dbp', 'mbp', 'hr', 'rr'}:
            raise ValueError('vital must be one of: sbp, dbp, mbp, hr, rr')
        birth = birth_day.isoformat() if isinstance(birth_day, date) else birth_day
        measured = measured_at.isoformat() if isinstance(measured_at, (date, datetime)) else measured_at
        response = requests.post(f'{self.base_url}/api/{vital}/zscore', headers={'Content-Type': 'application/json', **self.headers}, json={'birth_day': birth, 'measure_timerange': [measured, measured], 'value': float(value)}, timeout=self.timeout)
        response.raise_for_status()
        return ZScoreResult(**response.json())

    def centiles(self, vital: Vital, percentiles: list[int] = [3, 10, 25, 50, 75, 90, 97]) -> list[dict]:
        response = requests.get(f'{self.base_url}/api/{vital}/centiles', headers=self.headers, params=[('percent', str(p)) for p in percentiles], timeout=self.timeout)
        response.raise_for_status()
        return response.json()

def zscore(vital: Vital, birth_day: str | date, measured_at: str | date | datetime, value: float, *, timeout: float = 15) -> ZScoreResult:
    return CentileClient(timeout=timeout).zscore(vital, birth_day, measured_at, value)

def centiles(vital: Vital, percentiles: list[int] | None = None, *, timeout: float = 15) -> list[dict]:
    return CentileClient(timeout=timeout).centiles(vital, percentiles or [3, 10, 25, 50, 75, 90, 97])

__all__ = ['CentileClient', 'Vital', 'ZScoreResult', 'centiles', 'zscore']
