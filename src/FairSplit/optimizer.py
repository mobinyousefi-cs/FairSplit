#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: optimizer.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Minimize settlement transfers given per-person balances using a greedy
min-cash-flow algorithm (pairs largest debtor with largest creditor).

Usage:
from fairsplit.optimizer import optimize_settlements

Notes:
- Produces a small set of transactions that settle all balances to zero.
- Greedy is fast and near-optimal for realistic group sizes.

=================================================================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

from .money import D, quantize
from .models import Transaction


@dataclass
class Settlement:
    transactions: List[Transaction]


def optimize_settlements(balances: Dict[str, Decimal]) -> Settlement:
    # Split into creditors (>0) and debtors (<0)
    creditors = [(p, amt) for p, amt in balances.items() if amt > 0]
    debtors = [(p, -amt) for p, amt in balances.items() if amt < 0]

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    txs: List[Transaction] = []

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]

        pay = quantize(min(d_amt, c_amt))
        if pay > 0:
            txs.append(Transaction(payer=d_name, payee=c_name, amount=pay))

        d_amt = quantize(d_amt - pay)
        c_amt = quantize(c_amt - pay)

        debtors[i] = (d_name, d_amt)
        creditors[j] = (c_name, c_amt)

        if d_amt == 0:
            i += 1
        if c_amt == 0:
            j += 1

    return Settlement(transactions=txs)