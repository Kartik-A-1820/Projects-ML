def calculate_total(subtotal: float, discount: float) -> float:
    """Return subtotal after an absolute discount."""
    return subtotal - discount

def tax_amount(total: float, rate: float = 0.18) -> float:
    return total * rate
