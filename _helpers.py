"""Internal helper functions for slider widgets."""

from __future__ import annotations

import re
from typing import Literal, Optional

from PySide6.QtWidgets import QWidget

from pyside6_widgets.dialogs import AskResult, ask_question


# ---------------------------------------------------------------------------
# Numeric formatting helpers
# ---------------------------------------------------------------------------

def pretty_sci_text(
    value: float,
    sig_digits: int = 3,
    notation: Literal["plain", "html", "latex"] = "html",
) -> str:
    """Format a float using scientific notation when appropriate.

    Args:
        value: Numeric value to format.
        sig_digits: Number of significant digits. Must be at least 1.
        notation: Output style. Supported values are ``"plain"``, ``"html"``,
            and ``"latex"``.

    Returns:
        Formatted numeric string.
    """
    if sig_digits < 1:
        raise ValueError("sig_digits must be >= 1")

    if notation not in {"plain", "html", "latex"}:
        raise ValueError("notation must be 'plain', 'html', or 'latex'")

    if value == 0:
        return "0"

    av = abs(value)

    if 1 <= av < 10 ** sig_digits:
        s = f"{value:.{sig_digits}g}"
        if "e" not in s and "E" not in s:
            if "." in s:
                int_part, frac_part = s.split(".", 1)
                return f"{int(int_part):,d}.{frac_part}"
            return f"{int(s):,d}"

    s = f"{value:.{sig_digits - 1}e}"
    mant_str, exp_str = s.split("e", 1)
    exp = int(exp_str)

    if notation == "html":
        return f"{mant_str}×10<sup>{exp}</sup>"
    if notation == "latex":
        return rf"{mant_str}\times 10^{{{exp}}}"
    return f"{mant_str}×10^{exp}"


def get_numeric_format_field(fmt: str) -> str:
    """Return a Python-compatible numeric replacement field derived from ``fmt``.

    Args:
        fmt: Original format string.

    Returns:
        Full replacement field such as ``"{:.3f}"`` or ``"{:}"``.
    """
    m = re.search(r"\{[^{}]*:([^{}]*)\}", fmt)
    if not m:
        return "{:}"
    spec = m.group(1).replace("S", "g")
    spec = spec.replace(",", "")
    return f"{{:{spec}}}"


def value_to_text(value: int | float, fmt: str) -> str:
    """Format a numeric value for display.

    Args:
        value: Numeric value to format.
        fmt: Format string, which may use ordinary Python formatting or the
            custom ``"S"`` scientific marker.

    Returns:
        Formatted text. Falls back to ``str(value)`` if formatting fails.
    """
    sci_pat = r"\{:[0-9]*\.(\d+)S\}"

    if not re.search(sci_pat, fmt):
        try:
            return fmt.format(value)
        except Exception:
            return str(value)

    def repl(m: re.Match) -> str:
        prec = int(m.group(1))
        return pretty_sci_text(float(value), sig_digits=prec)

    try:
        return re.sub(sci_pat, repl, fmt)
    except Exception:
        return str(value)


# ---------------------------------------------------------------------------
# Slider-specific dialog helpers
# ---------------------------------------------------------------------------

def slider_ask_clamp_value(
    proposed_range: str,
    old_cur: str,
    new_cur: str,
    old_dft: str,
    new_dft: str,
    parent: Optional[QWidget] = None,
) -> AskResult:
    """Ask whether a slider value should be clamped to a proposed range.

    Args:
        proposed_range: Proposed allowed range.
        old_cur: Previous current value.
        new_cur: Clamped current value.
        old_dft: Previous default value.
        new_dft: Clamped default value.
        parent: Optional parent widget.

    Returns:
        User's selected answer.
    """
    return ask_question(
        "Out of range",
        "<b>Current</b>/<b>default</b> value is outside the proposed range.",
        f"<b>Proposed range:</b> <code>{proposed_range}</code><br>"
        f"<b>Current:</b> <code>{old_cur}</code> → <code>{new_cur}</code><br>"
        f"<b>Default:</b> <code>{old_dft}</code> → <code>{new_dft}</code><br><br>"
        "Press <b>OK</b> to clamp values to the proposed range, or <b>Cancel</b> to abort.",
        yes_btn_label="OK",
        cancel_btn_label="Cancel",
        parent=parent,
    )


def range_slider_ask_clamp_value(
    proposed_range: str,
    old_cur: str,
    new_cur: str,
    old_dft: str,
    new_dft: str,
    parent: Optional[QWidget] = None,
) -> AskResult:
    """Ask whether range-slider values should be clamped to proposed limits.

    Args:
        proposed_range: Proposed allowed range limits.
        old_cur: Previous current range.
        new_cur: Clamped current range.
        old_dft: Previous default range.
        new_dft: Clamped default range.
        parent: Optional parent widget.

    Returns:
        User's selected answer.
    """
    return ask_question(
        "Out of range",
        "<b>Current</b>/<b>default</b> values are outside the proposed range limits.",
        f"<b>Proposed range limits:</b> <code>{proposed_range}</code><br>"
        f"<b>Current:</b> <code>{old_cur}</code> → <code>{new_cur}</code><br>"
        f"<b>Default:</b> <code>{old_dft}</code> → <code>{new_dft}</code><br><br>"
        "Press <b>OK</b> to clamp values to the proposed range, or <b>Cancel</b> to abort.",
        yes_btn_label="OK",
        cancel_btn_label="Cancel",
        parent=parent,
    )


def multi_slider_ask_clamp_value(
    proposed_range: str,
    cur_min: str,
    cur_max: str,
    dft_min: str,
    dft_max: str,
    parent: Optional[QWidget] = None,
) -> AskResult:
    """Ask whether array-slider values should be clamped to a proposed range.

    Args:
        proposed_range: Proposed allowed range.
        cur_min: Minimum current value.
        cur_max: Maximum current value.
        dft_min: Minimum default value.
        dft_max: Maximum default value.
        parent: Optional parent widget.

    Returns:
        User's selected answer.
    """
    return ask_question(
        "Out of range",
        "<b>Current</b>/<b>default</b> values are outside the proposed range.",
        f"<b>Proposed range:</b> <code>{proposed_range}</code><br>"
        f"<b>Current values range:</b> <code>[{cur_min}, {cur_max}]</code><br>"
        f"<b>Default values range:</b> <code>[{dft_min}, {dft_max}]</code><br><br>"
        "Press <b>OK</b> to clamp values to the proposed range, or <b>Cancel</b> to abort.",
        yes_btn_label="OK",
        cancel_btn_label="Cancel",
        parent=parent,
    )


def slider_ask_extend_range(
    proposed_val: str,
    old_range: str,
    new_range: str,
    parent: Optional[QWidget] = None,
) -> AskResult:
    """Ask whether a slider range should be extended to include a new value.

    Args:
        proposed_val: Proposed new value.
        old_range: Existing range.
        new_range: Extended range.
        parent: Optional parent widget.

    Returns:
        User's selected answer.
    """
    return ask_question(
        "Out of range",
        "The proposed <b>value</b> is outside the current range.",
        f"<b>Proposed value:</b> <code>{proposed_val}</code><br>"
        f"<b>Range:</b> <code>{old_range}</code> → <code>{new_range}</code><br><br>"
        "Press <b>OK</b> to extend the range to include this value, or <b>Cancel</b> to abort.",
        yes_btn_label="OK",
        cancel_btn_label="Cancel",
        parent=parent,
    )


def range_slider_ask_extend_range(
    proposed_vals: str,
    old_range: str,
    new_range: str,
    parent: Optional[QWidget] = None,
) -> AskResult:
    """Ask whether a range-slider range should be extended for new values.

    Args:
        proposed_vals: Proposed new range values.
        old_range: Existing range.
        new_range: Extended range.
        parent: Optional parent widget.

    Returns:
        User's selected answer.
    """
    return ask_question(
        "Out of range",
        "The proposed <b>values</b> are outside the current range limits.",
        f"<b>Proposed values:</b> <code>{proposed_vals}</code><br>"
        f"<b>Range:</b> <code>{old_range}</code> → <code>{new_range}</code><br><br>"
        "Press <b>OK</b> to extend the range to include these values, or <b>Cancel</b> to abort.",
        yes_btn_label="OK",
        cancel_btn_label="Cancel",
        parent=parent,
    )
