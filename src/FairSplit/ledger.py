#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: ledger.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Compute per-person balances from a list of expenses.
Positive balance => person is a **creditor** (others owe them).
Negative balance => person is a **debtor** (they owe others).

Usage:
from fairsplit.ledger import compute_balances

Notes:
- Ensures the sum of balances is ~0 at cent precision.

=================================================================================================================
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Dict, Iterable, Sequence

from .money import D, quantize
from .models import Expense


def compute_balances(people: Sequence[str], expenses: Iterable[Expense]) -> Dict[str, Decimal]:
    balances: Dict[str, Decimal] = defaultdict(lambda: D("0"))

    # Ensure all people appear in balances
    for p in people:
        balances[p] = D("0")

    # For each expense: payer gets credited, beneficiaries are charged
    for e in expenses:
        shares = e.split()
        balances[e.paid_by] = quantize(balances[e.paid_by] + e.amount)
        for b, share in shares.items():
            balances[b] = quantize(balances[b] - share)

    # Small invariant correction at cent level
    total = sum(balances.values())
    drift = quantize(total)
    if drift != 0:
        # assign drift to the lexicographically first person for determinism
        first = sorted(balances.keys())[0]
        balances[first] = quantize(balances[first] - drift)

    return dict(balances)