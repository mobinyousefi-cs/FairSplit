# FairSplit — Optimized Group Expense & Settlement Calculator

**Author:** [Mobin Yousefi](https://github.com/mobinyousefi-cs)  
**License:** MIT  

FairSplit helps you:
- Record expenses (amount, payer, beneficiaries, optional weights)
- Compute each person’s fair share
- **Minimize the number of settlement payments** (debtor→creditor matching)
- Import/export JSON, print tables, or get machine-readable output

---

## Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
```

## Quickstart
```bash
# Run interactive CLI wizard
fairsplit

# Or provide data file
fairsplit --input tests/data/sample_expenses.json --optimize
```

Sample JSON format (see `tests/data/sample_expenses.json`):
```json
{
  "people": ["Ali", "Sara", "Reza", "Mobin"],
  "expenses": [
    { "desc": "Dinner", "amount": "120.00", "currency": "USD", "paid_by": "Ali",   "for": ["Ali", "Sara", "Reza", "Mobin"] },
    { "desc": "Taxi",   "amount": "36.00",  "currency": "USD", "paid_by": "Sara",  "for": ["Sara", "Reza"] },
    { "desc": "Snacks", "amount": "24.00",  "currency": "USD", "paid_by": "Reza",  "for": ["Ali", "Sara", "Reza"] }
  ]
}
```

## Features
- Deterministic money math with `Decimal` (no float drift)
- Equal split **or** weighted shares per expense
- Greedy min-cash-flow optimizer (near-minimal #transfers)
- Pretty reports using `rich`

## Testing
```bash
pytest -q
```

## CLI Usage
```bash
fairsplit --help
```