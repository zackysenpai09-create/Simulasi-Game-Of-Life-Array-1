"""
=============================================================================
SOAL 3 — Hybrid Sort
Chapter 5 — Data Structures & Algorithms
=============================================================================
Buat fungsi hybridSort(theSeq, threshold=10) yang menggunakan:
  - Insertion Sort jika panjang sub-array ≤ threshold
  - Selection Sort jika panjang sub-array > threshold

Bandingkan jumlah total operasi (comparisons + swaps) antara:
  - Hybrid Sort
  - Pure Insertion Sort
  - Pure Selection Sort
pada array random berukuran 50, 100, dan 500 elemen.
=============================================================================
"""

import random


def insertionSort(seq, count_ops=None):
    """
    Insertion Sort yang menghitung total operasi (comparisons + shifts).
    Kompleksitas: O(n²) worst case, O(n) best case.
    """
    ops = 0
    for i in range(1, len(seq)):
        value = seq[i]
        pos = i
        while pos > 0 and value < seq[pos - 1]:
            ops += 1                        # comparison + shift
            seq[pos] = seq[pos - 1]
            pos -= 1
        if pos != i:
            ops += 1                        # comparison terakhir yang gagal
        seq[pos] = value
    if count_ops is not None:
        count_ops[0] += ops
    return ops


def selectionSort(seq, count_ops=None):
    """
    Selection Sort yang menghitung total operasi (comparisons + swaps).
    Kompleksitas: O(n²) comparisons, O(n) swaps.
    """
    n = len(seq)
    ops = 0
    for i in range(n - 1):
        smallNdx = i
        for j in range(i + 1, n):
            ops += 1                        # comparison
            if seq[j] < seq[smallNdx]:
                smallNdx = j
        if smallNdx != i:
            seq[i], seq[smallNdx] = seq[smallNdx], seq[i]
            ops += 1                        # swap
    if count_ops is not None:
        count_ops[0] += ops
    return ops


def hybridSort(theSeq, threshold=10):
    """
    Hybrid Sort: pilih algoritma terbaik berdasarkan ukuran array.
      - len(array) ≤ threshold → Insertion Sort
      - len(array) > threshold → Selection Sort

    Mengembalikan:
        (sorted_list, total_ops)
    """
    seq = list(theSeq)
    total_ops = [0]

    if len(seq) <= threshold:
        insertionSort(seq, total_ops)
    else:
        selectionSort(seq, total_ops)

    return seq, total_ops[0]


def benchmark_sorts(size):
    """Bandingkan total operasi ketiga algoritma pada array random berukuran size."""
    arr = [random.randint(0, 1000) for _ in range(size)]

    arr_h = list(arr)
    _, hybrid_ops = hybridSort(arr_h)

    arr_i = list(arr)
    ins_ops = insertionSort(arr_i)

    arr_s = list(arr)
    sel_ops = selectionSort(arr_s)

    return hybrid_ops, ins_ops, sel_ops


# =============================================================================
# PENGUJIAN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOAL 3 — Hybrid Sort (threshold=10)")
    print("=" * 60)

    # Contoh kecil
    print("\n  >> Contoh hybridSort([3, 1, 4, 1, 5, 9, 2, 6], threshold=10):")
    result, ops = hybridSort([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"     Hasil : {result}")
    print(f"     Ops   : {ops}")

    # Benchmark
    sizes = [50, 100, 500]
    print(f"\n  {'Ukuran':>8} | {'Hybrid':>10} | {'Insertion':>10} | {'Selection':>10}")
    print(f"  {'-'*8}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")

    for size in sizes:
        random.seed(42)     # seed agar reproducible
        h, i, s = benchmark_sorts(size)
        print(f"  {size:>8} | {h:>10,} | {i:>10,} | {s:>10,}")

    print()
    print("  Analisis:")
    print("  • Array kecil (≤10): Insertion Sort dipilih → lebih efisien karena")
    print("    data kecil, overhead comparison Selection Sort tidak sepadan.")
    print("  • Array besar (>10): Selection Sort dipilih → hanya O(n) swap,")
    print("    lebih baik daripada Insertion Sort yang bisa O(n²) swap.")
    print("  • Hybrid Sort otomatis memilih strategi terbaik sesuai ukuran.")
