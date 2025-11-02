#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: money.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Decimal-backed money helpers to ensure exact currency arithmetic and rounding.

Usage:
from fairsplit.money import D, quantize

Notes:
- Always use Decimal with a fixed quantization of 2 fraction digits unless specified.
- Avoid binary float for money math.

=================================================================================================================
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, getcontext

# Global context tuned for currency math (sufficient precision for sums of many items)
getcontext().prec = 28

CENTS = Decimal("0.01")


def D(value: str | int | float | Decimal) -> Decimal:
    """Create a Decimal from various primitives, via string to avoid float artifacts."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def quantize(amount: Decimal, exp: Decimal = CENTS) -> Decimal:
    """Quantize to currency step using HALF_UP (typical for financial amounts)."""
    return amount.quantize(exp, rounding=ROUND_HALF_UP)