"""pyside6-sliders — Reusable PySide6 slider widgets for scientific applications.

Modules
-------
base
    ParameterWidgetBase — common base class for all parameter widgets.
sliders
    FloatSlider, IntSlider, ArraySlider — single-value slider widgets.
range_sliders
    FloatRangeSlider, IntRangeSlider — dual-handle range slider widgets.
multi_slider
    MultiVariableSlider — array of float values in a single slider widget.
"""

from .base import ParameterWidgetBase
from .sliders import FloatSlider, IntSlider, ArraySlider
from .range_sliders import FloatRangeSlider, IntRangeSlider
from .multi_slider import MultiVariableSlider

__all__ = [
    "ParameterWidgetBase",
    "FloatSlider",
    "IntSlider",
    "ArraySlider",
    "FloatRangeSlider",
    "IntRangeSlider",
    "MultiVariableSlider",
]

__version__ = "0.1.0"
__author__ = "Vahid Anari"
__email__ = "vahid.anari8@gmail.com"
