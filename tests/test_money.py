#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: test_money.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Unit tests for money helpers.

Usage:
pytest -q

Notes:
- Ensures quantization and D() behave.

=================================================================================================================
"""
from decimal import Decimal

from fairsplit.money import D, quantize


def test_d_decimal_creation():
    assert D("1.10") == Decimal("1.10")
    assert D(1) == Decimal("1")


def test_quantize_half_up():
    assert quantize(Decimal("1.005")) == Decimal("1.01")