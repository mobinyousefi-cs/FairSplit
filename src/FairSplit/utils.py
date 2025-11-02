#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: utils.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Small helpers: stable person normalization and table rendering.

Usage:
from fairsplit.utils import normalize_people

Notes:
- Rendering uses `rich` for pleasant CLI output.

=================================================================================================================
"""
from __future__ import annotations

from typing import Iterable, List

from rich.table import Table


def normalize_people(people: Iterable[str]) -> List[str]:
    return sorted({p.strip(): None for p in people if p and p.strip()}.keys())


def make_table(title: str, columns: list[str]) -> Table:
    table = Table(title=title)
    for c in columns:
        table.add_column(c)
    return table