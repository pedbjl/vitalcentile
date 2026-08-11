# vitalcentile

`vitalcentile` provides Python access to age-specific pediatric vital-sign z-scores, percentiles, and reference curves from the official [Centile](https://centile.research.or.kr) service.

> **Research and educational use only.** This package is not medical advice, a medical device, or a substitute for clinical assessment, diagnosis, or treatment.

## Install

After the official PyPI release:

```bash
pip install vitalcentile
```

## Quick start

```python
from vitalcentile import zscore

result = zscore(
    "sbp",             # sbp, dbp, mbp, hr, or rr
    "2018-01-01",      # date of birth: YYYY-MM-DD
    "2024-01-01",      # measurement date: YYYY-MM-DD
    100,
)

print(result.percentile)
print(result.zscore)
```

The reference supports children aged 1–217 completed months.

## Reference curves

```python
from vitalcentile import centiles

curves = centiles("hr", [3, 50, 97])
```

## Advanced configuration

Most users do not need a client object. Use `CentileClient` only for a custom timeout, headers, or another compatible API deployment.

```python
from vitalcentile import CentileClient
client = CentileClient(timeout=30)
```

## Citation and license

Use of this package, its calculations, outputs, or reference methodology requires citation of:

> Goo S, Jang W, Kim YS, Ji S, Park T, Park JD, Lee B. *Streamlining pediatric vital sign assessment: innovations and insights.* Scientific Reports. 2024;14:22542. https://doi.org/10.1038/s41598-024-73148-7

The package is distributed under the [VitalCentile Research and Evaluation License 1.0](LICENSE). Non-commercial research, education, and internal evaluation are permitted under its terms. Commercial use, redistribution, bulk extraction, clinical decision-support use, and derivative distribution require prior written permission from Bongjin Lee.

For collaboration, validation, licensing, or permission requests: `pedbjl@snu.ac.kr`.
