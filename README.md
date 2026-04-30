# pyside6-sliders

[![PyPI version](https://badge.fury.io/py/pyside6-sliders.svg)](https://pypi.org/project/pyside6-sliders/)

Reusable PySide6 slider widgets for scientific applications.

Built from real scientific software, these sliders are production-tested and
support float/int values, range selection, array editing, custom labels with
optional LaTeX rendering, right-click context menus, and configurable styling.

## Components

| Widget | Description |
|--------|-------------|
| `FloatSlider` | Single float-value slider with label, unit, and value display |
| `IntSlider` | Single integer-value slider |
| `ArraySlider` | Multi-value array slider |
| `FloatRangeSlider` | Dual-handle float range slider |
| `IntRangeSlider` | Dual-handle integer range slider |
| `MultiVariableSlider` | Array of float values sharing a single range |

## Installation

```bash
pip install pyside6-sliders
```

This package depends on `pyside6-widgets` which will be installed automatically.

## Quick Start

### FloatSlider

```python
from pyside6_sliders import FloatSlider

slider = FloatSlider(
    name=r"T_1",           # supports LaTeX math
    unit="s",
    val=1.0,
    val_min=0.0,
    val_max=10.0,
    val_fmt="{:.3g}",
)
slider.valueChanged.connect(lambda v: print(f"Value: {v}"))
```

### IntSlider

```python
from pyside6_sliders import IntSlider

slider = IntSlider(
    name="N",
    unit="",
    val=10,
    val_min=1,
    val_max=100,
)
```

### FloatRangeSlider

```python
from pyside6_sliders import FloatRangeSlider

slider = FloatRangeSlider(
    name=r"\nu",
    unit="MHz",
    val=(1.0, 5.0),
    val_min=0.0,
    val_max=10.0,
)
slider.valueChanged.connect(lambda v: print(f"Range: {v}"))
```

### MultiVariableSlider

```python
import numpy as np
from pyside6_sliders import MultiVariableSlider

slider = MultiVariableSlider(
    name=r"v",
    unit="km/s",
    val=np.array([1.0, 2.0, 3.0]),
    val_min=0.0,
    val_max=10.0,
)
```

## Features

- Float and integer single-value sliders
- Dual-handle range sliders
- Array/multi-variable sliders
- Math label rendering via Matplotlib (optional LaTeX)
- Right-click context menus for editing value, range, and config
- Configurable label sizes and display formats
- Out-of-range dialogs with clamp/extend options
- Clean signal API: `valueChanged`, `defaultChanged`, `configChanged`

## Requirements

- Python 3.10+
- PySide6 >= 6.5
- numpy >= 1.24
- pyside6-widgets >= 0.1.0

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

Vahid Anari —
[GitHub](https://github.com/vahid-anari) ·
[LinkedIn](https://www.linkedin.com/in/vahid-anari/)
