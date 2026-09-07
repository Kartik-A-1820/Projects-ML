from .pricing import calculate_total, tax_amount

def checkout(subtotal: float, discount: float) -> dict:
    total = calculate_total(subtotal, discount)
    return {"total": total, "tax": tax_amount(total)}
