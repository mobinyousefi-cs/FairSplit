#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: cli.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Typer-based CLI commands: interactive wizard and file-based run.

Usage:
python -m fairsplit  # or `fairsplit`

Notes:
- Pretty output via `rich`.

=================================================================================================================
"""
from __future__ import annotations

from decimal import Decimal
from typing import Optional

import typer
from rich.console import Console
from rich import box

from .io_utils import load_json
from .ledger import compute_balances
from .models import Expense
from .money import D
from .optimizer import optimize_settlements
from .utils import make_table, normalize_people

app = typer.Typer(add_completion=False, help="FairSplit – Optimized cost sharing calculator")
console = Console()


@app.command()
def file(
    input: str = typer.Option("", "--input", "-i", help="Path to JSON input file"),
    optimize: bool = typer.Option(True, "--optimize/--no-optimize", help="Optimize settlements"),
) -> None:
    if not input:
        typer.echo("--input is required when using 'file' command.")
        raise typer.Exit(code=2)

    people, expenses = load_json(input)
    people = normalize_people(people)

    balances = compute_balances(people, expenses)

    table = make_table("Balances", ["Person", "Balance"])
    for p in people:
        table.add_row(p, str(balances[p]))
    console.print(table)

    if optimize:
        settlement = optimize_settlements(balances)
        t = make_table("Optimized Settlements", ["Payer", "Payee", "Amount"])
        for tx in settlement.transactions:
            t.add_row(tx.payer, tx.payee, str(tx.amount))
        console.print(t)


@app.command()
def wizard() -> None:
    console.rule("[bold]Interactive Wizard")
    n = typer.prompt("How many people?", type=int)
    people = [typer.prompt(f"Person #{i+1} name") for i in range(n)]

    m = typer.prompt("How many expenses?", type=int)
    expenses: list[Expense] = []

    for i in range(m):
        console.rule(f"Expense #{i+1}")
        desc = typer.prompt("Description")
        amount = D(typer.prompt("Amount (e.g., 120.00)"))
        paid_by = typer.prompt("Paid by (name)")
        ben_raw = typer.prompt("Beneficiaries (comma-separated names)")
        beneficiaries = [b.strip() for b in ben_raw.split(",") if b.strip()]
        use_weights = typer.confirm("Weighted split?", default=False)
        weights = None
        if use_weights:
            weights = {}
            for b in beneficiaries:
                w = D(typer.prompt(f"Weight for {b} (e.g., 1, 2, 0.5)"))
                weights[b] = w

        expenses.append(
            Expense(
                desc=desc,
                amount=amount,
                paid_by=paid_by,
                beneficiaries=beneficiaries,
                weights=weights,
            )
        )

    people = normalize_people(people)
    balances = compute_balances(people, expenses)

    table = make_table("Balances", ["Person", "Balance"])
    for p in people:
        table.add_row(p, str(balances[p]))
    console.print(table)

    settlement = optimize_settlements(balances)
    t = make_table("Optimized Settlements", ["Payer", "Payee", "Amount"])
    for tx in settlement.transactions:
        t.add_row(tx.payer, tx.payee, str(tx.amount))
    console.print(t)