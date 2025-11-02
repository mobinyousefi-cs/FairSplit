#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: models.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Core domain models: Person, Expense, and Transaction with validation.

Usage:
from fairsplit.models import Person, Expense, Transaction

Notes:
- Expense supports equal or weighted splits via `weights`.
- All amounts are Decimal (see money.py).

=================================================================================================================
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Iterable, List, Sequence

from .money import D, quantize


@dataclass(frozen=True)
class Person:
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Person name must be non-empty")


@dataclass
class Expense:
    desc: str
    amount: Decimal
    paid_by: str
    beneficiaries: Sequence[str]
    currency: str = "USD"
    weights: Dict[str, Decimal] | None = None  # beneficiary -> weight

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Expense amount must be positive")
        if not self.beneficiaries:
            raise ValueError("Expense must have at least one beneficiary")
        if self.weights is not None:
            if set(self.weights.keys()) != set(self.beneficiaries):
                raise ValueError("Weights must be provided for all beneficiaries if used")
            if any(w <= 0 for w in self.weights.values()):
                raise ValueError("Weights must be positive")

    def split(self) -> Dict[str, Decimal]:
        """Return each beneficiary's share as a dict (name -> Decimal)."""
        if self.weights:
            total_w = sum(self.weights.values())
            shares = {
                p: quantize(self.amount * (w / total_w)) for p, w in self.weights.items()
            }
            # Fix rounding drift by adjusting the largest share
            drift = quantize(self.amount - sum(shares.values()))
            if drift != 0:
                # add drift to the beneficiary with the max fractional part
                target = max(shares, key=lambda k: shares[k])
                shares[target] = quantize(shares[target] + drift)
            return shares

        # Equal split
        n = Decimal(len(self.beneficiaries))
        base = quantize(self.amount / n)
        shares = {b: base for b in self.beneficiaries}
        drift = quantize(self.amount - sum(shares.values()))
        if drift != 0:
            # assign remaining cents to first beneficiaries deterministically
            for b in self.beneficiaries:
                if drift == 0:
                    break
                shares[b] = quantize(shares[b] + Decimal("0.01"))
                drift = quantize(drift - Decimal("0.01"))
        return shares


@dataclass(frozen=True)
class Transaction:
    payer: str
    payee: str
    amount: Decimal

    def __post_init__(self) -> None:
        if self.payer == self.payee:
            raise ValueError("Transaction payer and payee must differ")
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")