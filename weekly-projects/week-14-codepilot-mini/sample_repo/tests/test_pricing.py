from orders.pricing import calculate_total

def test_normal_discount():
    assert calculate_total(100.0, 25.0) == 75.0
