#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: io_utils.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Load and dump FairSplit JSON documents.

Usage:
from fairsplit.io_utils import load_json, dump_json

Notes:
- JSON schema is deliberately simple; validations live in models.

=================================================================================================================
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from .money import D
from .models import Expense


def load_json(path: str | Path) -> tuple[List[str], List[Expense]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    people = list(data.get("people", []))
    expenses: List[Expense] = []
    for item in data.get("expenses", []):
        expenses.append(
            Expense(
                desc=item.get("desc", ""),
                amount=D(item["amount"]),
                paid_by=item["paid_by"],
                beneficiaries=list(item["for"]),
                currency=item.get("currency", "USD"),
                weights={k: D(v) for k, v in item.get("weights", {}).items()} if item.get("weights") else None,
            )
        )
    return people, expenses


def dump_json(path: str | Path, people: Sequence[str], expenses: Iterable[Expense]) -> None:
    obj = {
        "people": list(people),
        "expenses": [
            {
                "desc": e.desc,
                "amount": str(e.amount),
                "currency": e.currency,
                "paid_by": e.paid_by,
                "for": list(e.beneficiaries),
                "weights": {k: str(v) for k, v in (e.weights or {}).items()} or None,
            }
            for e in expenses
        ],
    }
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")