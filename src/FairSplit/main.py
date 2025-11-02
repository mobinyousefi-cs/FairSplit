#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: FairSplit — Optimized Cost Sharing Calculator
File: main.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-11-02
Updated: 2025-11-02
License: MIT License (see LICENSE file for details)
=

Description:
Executable entrypoint for the FairSplit CLI.

Usage:
python -m fairsplit
# or after install:
fairsplit

Notes:
- Delegates to Typer application defined in cli.py

=================================================================================================================
"""
from __future__ import annotations

from .cli import app


def run() -> None:
    app()


if __name__ == "__main__":
    run()