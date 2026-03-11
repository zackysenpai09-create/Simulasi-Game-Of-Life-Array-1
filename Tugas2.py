"""
=============================================================================
SOAL 2 — Bubble Sort dengan Analisis Langkah
Chapter 5 — Data Structures & Algorithms
=============================================================================
Modifikasi bubbleSort() agar:
  1. Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
  2. Mengimplementasikan early termination (berhenti jika tidak ada swap dalam satu pass)
  3. Cetak state array setelah setiap pass

Uji dengan input: [5, 1, 4, 2, 8] dan [1, 2, 3, 4, 5]
=============================================================================
"""


def bubbleSort(theSeq):
    """
    Bubble Sort dengan early termination dan analisis langkah.

    Mengembalikan:
        (sorted_list, total_comparisons, total_swaps, passes_used)

    Kompleksitas Waktu:
        Worst case : O(n²) — array terbalik
        Best case  : O(n)  — array sudah terurut (early termination)
    """
    seq = list(theSeq)      # salin agar tidak mengubah input asli
    n = len(seq)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    print(f"  Input  : {seq}")

    for i in range(n - 1):
        swapped_this_pass = False

        for j in range(n - 1 - i):     # elemen terakhir sudah pada posisi benar
            total_comparisons += 1
            if seq[j] > seq[j + 1]:
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
                total_swaps += 1
                swapped_this_pass = True

        passes_used += 1
        print(f"  Pass {passes_used:2d}: {seq}  (swapped: {swapped_this_pass})")

        if not swapped_this_pass:       # ← early termination
            break

    return (seq, total_comparisons, total_swaps, passes_used)


# =============================================================================
# PENGUJIAN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
    print("=" * 60)

    test_cases = [
        [5, 1, 4, 2, 8],
        [1, 2, 3, 4, 5],    # sudah terurut → early termination setelah 1 pass
    ]

    for arr in test_cases:
        print(f"\n  >> Array: {arr}")
        sorted_arr, comps, swaps, passes = bubbleSort(arr)
        print(f"  Hasil        : {sorted_arr}")
        print(f"  Comparisons  : {comps}")
        print(f"  Swaps        : {swaps}")
        print(f"  Passes used  : {passes}")

    print()
    print("  Penjelasan perbedaan jumlah pass:")
    print("  • [5,1,4,2,8]: data tidak terurut → perlu banyak pass untuk memindahkan")
    print("    elemen besar ke akhir, tidak ada early termination.")
    print("  • [1,2,3,4,5]: data sudah terurut → pass pertama tidak menghasilkan swap,")
    print("    early termination langsung aktif sehingga hanya 1 pass dijalankan.")
