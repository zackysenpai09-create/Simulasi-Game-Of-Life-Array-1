"""
=============================================================================
SOAL 1 — Modified Binary Search: countOccurrences
Chapter 5 — Data Structures & Algorithms
=============================================================================
Implementasikan fungsi countOccurrences(sortedList, target) yang menghitung
berapa kali sebuah nilai muncul dalam sorted list.
Kompleksitas: O(log n) menggunakan dua binary search:
  - findLeftBound  → indeks kemunculan PERTAMA
  - findRightBound → indeks kemunculan TERAKHIR
=============================================================================
"""


def findLeftBound(sortedList, target):
    """
    Binary search untuk menemukan indeks paling kiri (kemunculan pertama)
    dari target dalam sortedList.
    Mengembalikan -1 jika target tidak ditemukan.
    """
    low, high = 0, len(sortedList) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if sortedList[mid] == target:
            result = mid        # catat posisi, lalu cari lebih ke kiri
            high = mid - 1
        elif sortedList[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result


def findRightBound(sortedList, target):
    """
    Binary search untuk menemukan indeks paling kanan (kemunculan terakhir)
    dari target dalam sortedList.
    Mengembalikan -1 jika target tidak ditemukan.
    """
    low, high = 0, len(sortedList) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if sortedList[mid] == target:
            result = mid        # catat posisi, lalu cari lebih ke kanan
            low = mid + 1
        elif sortedList[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result


def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali target muncul dalam sortedList yang sudah terurut.
    Kompleksitas Waktu: O(log n)
    Kompleksitas Ruang: O(1)
    """
    left = findLeftBound(sortedList, target)
    if left == -1:
        return 0    # target tidak ada sama sekali
    right = findRightBound(sortedList, target)
    return right - left + 1


# =============================================================================
# PENGUJIAN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOAL 1 — Modified Binary Search: countOccurrences")
    print("=" * 60)

    test_cases = [
        ([1, 2, 4, 4, 4, 4, 7, 9, 12], 4, 4),
        ([1, 2, 4, 4, 4, 4, 7, 9, 12], 5, 0),
        ([1, 1, 1, 1, 1],              1, 5),
        ([1, 2, 3, 4, 5],              3, 1),
        ([],                            7, 0),
        ([5],                           5, 1),
        ([5],                           3, 0),
    ]

    for lst, target, expected in test_cases:
        result = countOccurrences(lst, target)
        status = "✓" if result == expected else "✗"
        print(f"  {status} countOccurrences({lst}, {target}) = {result}  (expected {expected})")
