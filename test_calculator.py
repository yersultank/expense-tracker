import pytest
from calculator import (
    add_expense,
    calculate_subtotal,
    calculate_total,
    summarize_by_category,
    export_report,
)


def test_add_and_subtotal():
    expenses = []
    add_expense(expenses, "Coffee", 4.50, "food")
    add_expense(expenses, "Notebook", 10.50, "study")
    assert calculate_subtotal(expenses) == 15.00


def test_discount_calculations():
    expenses = [{"title": "Laptop Stand", "amount": 120.00, "category": "tech"}]
    assert calculate_total(expenses, "none") == 120.00
    assert calculate_total(expenses, "student") == 108.00
    assert calculate_total(expenses, "bulk") == 102.00
    assert calculate_total(expenses, "vip") == 96.00


def test_summarize_by_category():
    expenses = [
        {"title": "Lunch", "amount": 12.0, "category": "food"},
        {"title": "Bus", "amount": 2.5, "category": "transport"},
        {"title": "Dinner", "amount": 18.0, "category": "food"},
    ]
    assert summarize_by_category(expenses) == {"food": 30.0, "transport": 2.5}


def test_export_report(tmp_path):
    expenses = [{"title": "Book", "amount": 25.0, "category": "study"}]
    out_file = tmp_path / "report.txt"
    result = export_report(expenses, str(out_file), "student")
    assert out_file.exists()
    assert "Total (student): 22.50" in result