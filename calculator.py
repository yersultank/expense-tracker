from abc import ABC, abstractmethod
import math
from pathlib import Path


class DiscountStrategy(ABC):
    """Strategy interface for calculating order discounts."""

    @abstractmethod
    def calculate_discount(self, subtotal: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal: float) -> float:
        return 0.0


class StudentDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal: float) -> float:
        return subtotal * 0.10


class BulkDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal: float) -> float:
        return subtotal * 0.15 if subtotal >= 100.0 else 0.0


class VipDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal: float) -> float:
        return subtotal * 0.20


DISCOUNT_STRATEGIES: dict[str, DiscountStrategy] = {
    "none": NoDiscount(),
    "student": StudentDiscount(),
    "bulk": BulkDiscount(),
    "vip": VipDiscount(),
}


def add_expense(expenses: list[dict], title: str, amount: float, category: str = "general") -> list[dict]:
    """Add a validated expense item to the list and return the updated list."""
    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty")
    numeric_amount = float(amount)
    if math.isnan(numeric_amount) or math.isinf(numeric_amount) or numeric_amount <= 0:
        raise ValueError("Expense amount must be a positive finite number")
    expenses.append({
        "title": title.strip(),
        "amount": numeric_amount,
        "category": category.strip().lower(),
    })
    return expenses


def calculate_subtotal(expenses: list[dict]) -> float:
    """Calculate raw sum of all expenses."""
    return round(sum(item["amount"] for item in expenses), 2)


def calculate_total(expenses: list[dict], discount_type: str = "none") -> float:
    """Calculate final total using the configured discount strategy."""
    strategy = DISCOUNT_STRATEGIES.get(discount_type)
    if strategy is None:
        raise ValueError(f"Unknown discount type: {discount_type}")

    subtotal = calculate_subtotal(expenses)
    discount = strategy.calculate_discount(subtotal)
    return round(subtotal - discount, 2)


def summarize_by_category(expenses: list[dict]) -> dict[str, float]:
    """Group and sum expenses by category."""
    summary: dict[str, float] = {}
    for item in expenses:
        cat = item["category"]
        summary[cat] = round(summary.get(cat, 0.0) + item["amount"], 2)
    return summary


def export_report(
    expenses: list[dict],
    filepath: str,
    discount_type: str = "none",
    base_dir: str | Path | None = None,
) -> str:
    """Export a plain-text expense summary to a validated file path."""
    raw_path = Path(filepath)
    if ".." in raw_path.parts:
        raise ValueError("Path traversal segments ('..') are not allowed")

    if base_dir is not None:
        allowed_root = Path(base_dir).resolve()
        resolved_target = (allowed_root / raw_path).resolve()
        if allowed_root not in resolved_target.parents:
            raise ValueError("Target filepath escapes the allowed output directory")
    else:
        resolved_target = raw_path.resolve()

    total = calculate_total(expenses, discount_type)
    lines = [f"Items: {len(expenses)}", f"Total ({discount_type}): {total:.2f}"]
    content = "\n".join(lines) + "\n"
    resolved_target.write_text(content, encoding="utf-8")
    return content