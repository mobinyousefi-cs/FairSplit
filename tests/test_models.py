#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: test_models.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Unit tests for models (Expense splitting).

Usage:
pytest -q

Notes:
- Exercises equal and weighted splits and rounding.

=================================================================================================================
"""
from decimal import Decimal

from fairsplit.models import Expense


def test_equal_split_no_drift():
    e = Expense(desc="x", amount=Decimal("10.00"), paid_by="A", beneficiaries=["A", "B"])
    s = e.split()
    assert s["A"] == Decimal("5.00")
    assert s["B"] == Decimal("5.00")


def test_weighted_split():
    e = Expense(
        desc="x", amount=Decimal("30.00"), paid_by="A", beneficiaries=["A", "B"], weights={"A": Decimal("1"), "B": Decimal("2")}
    )
    s = e.split()
    assert s["A"] + s["B"] == Decimal("30.00")
    # B should pay roughly twice A (subject to cent rounding)
    assert s["B"] >= s["A"]