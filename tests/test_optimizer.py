#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: test_optimizer.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Unit tests for settlement optimizer (greedy min cash flow).

Usage:
pytest -q

Notes:
- Ensures all balances can be settled.

=================================================================================================================
"""
from decimal import Decimal

from fairsplit.optimizer import optimize_settlements


def test_optimizer_basic():
    balances = {"A": Decimal("10.00"), "B": Decimal("-6.00"), "C": Decimal("-4.00")}
    s = optimize_settlements(balances)
    total = sum(t.amount for t in s.transactions)
    assert total == Decimal("10.00")
    # Two payments: B->A 6, C->A 4 (order may differ)
    assert len(s.transactions) == 2