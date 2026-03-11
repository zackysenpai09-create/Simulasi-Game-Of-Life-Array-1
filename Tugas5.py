"""
=============================================================================
SOAL 5 — Inversions Counter
Chapter 5 — Data Structures & Algorithms
=============================================================================
Sebuah inversion dalam array adalah pasangan indeks (i, j) di mana:
  i < j  tapi  arr[i] > arr[j]

Jumlah inversion mengukur seberapa "tidak terurut" sebuah array.

Implementasikan dua fungsi:
  a) countInversionsNaive(arr)  — brute force O(n²)
  b) countInversionsSmart(arr)  — modifikasi merge sort O(n log n)

Uji kedua fungsi dan bandingkan waktu eksekusinya pada array random
berukuran 1000, 5000, dan 10000 elemen.
=============================================================================
"""

import random
import time


# =============================================================================
# a) Brute Force — O(n²)
# =============================================================================

def countInversionsNaive(arr):
    """
    Hitung jumlah inversion menggunakan brute force.
    Cek semua pasangan (i, j) di mana i < j.

    Kompleksitas Waktu: O(n²)
    Kompleksitas Ruang: O(1)
    """
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# =============================================================================
# b) Merge Sort — O(n log n)
# =============================================================================

def mergeSortCount(arr):
    """
    Merge sort yang menghitung inversion selama proses merge.

    Kunci insight: saat elemen kanan dipilih sebelum elemen kiri,
    SEMUA elemen kiri yang belum diproses adalah inversion dengan elemen kanan itu.

    Kompleksitas: O(n log n)
    """
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left,  left_inv  = mergeSortCount(arr[:mid])
    right, right_inv = mergeSortCount(arr[mid:])

    merged = []
    inversions = left_inv + right_inv
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # left[i] > right[j]:
            # semua left[i..] lebih besar dari right[j] → semua adalah inversion
            merged.append(right[j])
            inversions += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions


def countInversionsSmart(arr):
    """
    Hitung jumlah inversion menggunakan modifikasi merge sort.

    Kompleksitas Waktu: O(n log n)
    Kompleksitas Ruang: O(n)
    """
    _, count = mergeSortCount(arr)
    return count


# =============================================================================
# PENGUJIAN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOAL 5 — Inversions Counter")
    print("=" * 60)

    # --- Uji kebenaran ---
    print("\n  >> Uji kebenaran (naive == smart):")
    test_cases = [
        ([2, 4, 1, 3, 5],  3),
        ([5, 4, 3, 2, 1], 10),   # fully reversed → maksimum inversion
        ([1, 2, 3, 4, 5],  0),   # sudah terurut → tidak ada inversion
        ([1],               0),
        ([2, 1],            1),
        ([1, 5, 2, 4, 3],  4),
    ]

    for arr, expected in test_cases:
        naive = countInversionsNaive(arr)
        smart = countInversionsSmart(arr)
        status = "✓" if naive == smart == expected else "✗"
        print(f"  {status} {arr} → naive={naive}, smart={smart} (expected {expected})")

    # --- Benchmark waktu ---
    print("\n  >> Benchmark waktu eksekusi:")
    print(f"  {'Ukuran':>8} | {'Naive (s)':>12} | {'Smart (s)':>12} | {'Speedup':>10}")
    print(f"  {'-'*8}-+-{'-'*12}-+-{'-'*12}-+-{'-'*10}")

    for size in [1000, 5000, 10000]:
        random.seed(99)
        arr = [random.randint(0, 10000) for _ in range(size)]

        t0 = time.perf_counter()
        naive_result = countInversionsNaive(arr)
        t_naive = time.perf_counter() - t0

        t0 = time.perf_counter()
        smart_result = countInversionsSmart(arr)
        t_smart = time.perf_counter() - t0

        assert naive_result == smart_result, "ERROR: hasil berbeda!"
        speedup = t_naive / t_smart if t_smart > 0 else float('inf')
        print(f"  {size:>8} | {t_naive:>12.4f} | {t_smart:>12.4f} | {speedup:>9.1f}x")

    print()
    print("  Penjelasan mengapa merge sort lebih cepat:")
    print("  • Naive : dua nested loop → O(n²) comparisons.")
    print("    Untuk n=10.000, itu ~50 juta perbandingan.")
    print("  • Smart : merge sort membagi array secara rekursif dan menghitung")
    print("    inversion dalam satu langkah bersama proses merge.")
    print("    Total hanya O(n log n) ≈ 130.000 operasi untuk n=10.000.")
    print("  • Hasilnya: versi smart bisa 100× hingga 1000× lebih cepat")
    print("    pada array besar, sementara kedua fungsi menghasilkan jawaban sama.")
