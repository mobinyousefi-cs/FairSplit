#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: test_ledger.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Unit tests for balance computation.

Usage:
pytest -q

Notes:
- Validates creditor/debtor signs.

=================================================================================================================
"""
from decimal import Decimal

from fairsplit.ledger import compute_balances
from fairsplit.models import Expense


def test_balances_sum_to_zero():
    people = ["A", "B", "C"]
    expenses = [
        Expense(desc="dinner", amount=Decimal("90.00"), paid_by="A", beneficiaries=["A", "B", "C"]),
        Expense(desc="taxi", amount=Decimal("30.00"), paid_by="B", beneficiaries=["B", "C"]),
    ]
    b = compute_balances(people, expenses)
    assert round(sum(b.values()), 2) == 0