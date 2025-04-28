def calculate_result(m):
    if m <= 0:
        raise ValueError("Parameter m harus bilangan positif.")
    
    n = 3
    results = []
    for _ in range(m):
        result = ((4 * n) + 7) % m
        results.append(result)
        n = result  # Update nilai n untuk iterasi berikutnya
    return results  # Kembalikan semua hasil