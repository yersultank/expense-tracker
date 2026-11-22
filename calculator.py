from pathlib import Path


def add_expense(expenses: list[dict], title: str, amount: float, category: str = "general") -> list[dict]:
    """Add an expense item to the list and return the updated list."""
    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty")
    expenses.append({
        "title": title.strip(),
        "amount": float(amount),
        "category": category.strip().lower()
    })
    return expenses


def calculate_subtotal(expenses: list[dict]) -> float:
    """Calculate raw sum of all expenses."""
    return round(sum(item["amount"] for item in expenses), 2)


def calculate_total(expenses: list[dict], discount_type: str = "none") -> float:
    """Calculate final total after applying discount rules."""
    subtotal = calculate_subtotal(expenses)

    if discount_type == "none":
        discount = 0.0
    elif discount_type == "student":
        discount = subtotal * 0.10
    elif discount_type == "bulk":
        discount = subtotal * 0.15 if subtotal >= 100.0 else 0.0
    elif discount_type == "vip":
        discount = subtotal * 0.20
    else:
        raise ValueError(f"Unknown discount type: {discount_type}")

    return round(subtotal - discount, 2)


def summarize_by_category(expenses: list[dict]) -> dict[str, float]:
    """Group and sum expenses by category."""
    summary: dict[str, float] = {}
    for item in expenses:
        cat = item["category"]
        summary[cat] = round(summary.get(cat, 0.0) + item["amount"], 2)
    return summary


def export_report(expenses: list[dict], filepath: str, discount_type: str = "none") -> str:
    """Export a plain-text expense summary to a file."""
    total = calculate_total(expenses, discount_type)
    lines = [f"Items: {len(expenses)}", f"Total ({discount_type}): {total:.2f}"]
    content = "\n".join(lines) + "\n"
    Path(filepath).write_text(content, encoding="utf-8")
    return content