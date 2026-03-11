"""
=============================================================================
SOAL 4 — Merge Tiga Sorted Lists
Chapter 5 — Data Structures & Algorithms
=============================================================================
Implementasikan mergeThreeSortedLists(listA, listB, listC) yang menggabungkan
tiga sorted list menjadi satu sorted list baru dalam waktu O(n).

Aturan:
  - TIDAK BOLEH memanggil fungsi merge dua list secara bertahap (dua pass)
  - Gunakan SATU PASS dengan tiga pointer

Contoh:
  mergeThreeSortedLists([1, 5, 9], [2, 6, 10], [3, 4, 7])
  → [1, 2, 3, 4, 5, 6, 7, 9, 10]
=============================================================================
"""


def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list.

    Algoritma: gunakan tiga pointer (ia, ib, ic).
    Setiap iterasi, pilih elemen terkecil dari ketiga pointer aktif,
    tambahkan ke hasil, dan majukan pointer yang bersangkutan.

    Kompleksitas Waktu: O(n) — n = len(A) + len(B) + len(C)
    Kompleksitas Ruang: O(n)
    """
    result = []
    ia, ib, ic = 0, 0, 0
    na, nb, nc = len(listA), len(listB), len(listC)

    while ia < na or ib < nb or ic < nc:
        # Gunakan float('inf') untuk list yang sudah habis
        va = listA[ia] if ia < na else float('inf')
        vb = listB[ib] if ib < nb else float('inf')
        vc = listC[ic] if ic < nc else float('inf')

        if va <= vb and va <= vc:
            result.append(va)
            ia += 1
        elif vb <= va and vb <= vc:
            result.append(vb)
            ib += 1
        else:
            result.append(vc)
            ic += 1

    return result


# =============================================================================
# PENGUJIAN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOAL 4 — Merge Tiga Sorted Lists")
    print("=" * 60)
    print()

    test_cases = [
        ([1, 5, 9],          [2, 6, 10],      [3, 4, 7],   [1, 2, 3, 4, 5, 6, 7, 9, 10]),
        ([1, 2, 3],          [4, 5, 6],        [7, 8, 9],   [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([],                 [1, 3, 5],         [2, 4, 6],   [1, 2, 3, 4, 5, 6]),
        ([1],                [1],               [1],          [1, 1, 1]),
        ([2, 8, 15, 23, 37], [4, 6, 15, 20],   [],           [2, 4, 6, 8, 15, 15, 20, 23, 37]),
    ]

    for a, b, c, expected in test_cases:
        result = mergeThreeSortedLists(a, b, c)
        status = "✓" if result == expected else "✗"
        print(f"  {status} A={a}")
        print(f"       B={b}")
        print(f"       C={c}")
        print(f"       → {result}")
        print()

    print("  Penjelasan:")
    print("  • Satu pass dengan 3 pointer — tidak ada dua kali merge bertahap.")
    print("  • Setiap langkah memilih elemen terkecil dari tiga kandidat.")
    print("  • Saat satu list habis, pointer-nya diganti float('inf') agar")
    print("    tidak pernah dipilih, sehingga logika tetap seragam.")
    print("  • Kompleksitas: O(n) waktu, O(n) ruang untuk list hasil.")
