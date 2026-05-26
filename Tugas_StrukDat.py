"""
expr_heap_sorter.py
===================
Modul ExprHeapSorter: Expression Tree Builder/Evaluator + In-Place HeapSort
+ Complete Binary Tree Validator.

Algoritma yang diimplementasikan:
  1. Expression Tree – parsing ekspresi fully-parenthesized via antrian token & rekursi
  2. In-Place HeapSort – build max-heap + ekstraksi berulang (O(1) extra space)
  3. Complete Tree Validator – verifikasi properti complete binary tree via rumus indeks
"""

from typing import List, Optional
from collections import deque


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS UTAMA
# ═══════════════════════════════════════════════════════════════════════════════
class ExprHeapSorter:
    """
    Menggabungkan tiga modul dari Bab 13:
      • parse_and_evaluate()  – membangun expression tree & mengevaluasinya
      • heapsort_inplace()    – mengurutkan array ascending via in-place HeapSort
      • is_complete_tree()    – memvalidasi properti complete binary tree
    """

    def __init__(self, expr_str: str):
        """
        Parameters
        ----------
        expr_str : str
            Ekspresi aritmetika yang fully parenthesized, misal:
            "((8 * 5) + (9 / (7 - 4)))"
        """
        self.expr   = expr_str
        self.values: List[int] = []

    # =========================================================
    # 1. EXPRESSION TREE: Builder & Evaluator
    # =========================================================

    def parse_and_evaluate(self) -> List[int]:
        """
        Membangun pohon ekspresi dari self.expr, mengevaluasinya,
        lalu mengembalikan list berisi SATU nilai integer hasil evaluasi.

        Tahapan:
          1. Tokenisasi: ubah string menjadi deque token (angka & operator).
          2. _build_tree(): membangun pohon rekursif dari deque token.
          3. _eval_tree(): evaluasi postorder, kembalikan nilai integer.

        Return
        ------
        List[int] – berisi satu elemen: hasil evaluasi ekspresi.
        """
        # ── Tokenisasi ────────────────────────────────────────────────────────
        # Pisahkan ekspresi menjadi token: angka multi-digit dan operator/kurung
        raw_tokens = deque()
        i = 0
        expr = self.expr.replace(" ", "")   # Hapus spasi
        while i < len(expr):
            ch = expr[i]
            if ch.isdigit():
                # Baca angka multi-digit
                num = ""
                while i < len(expr) and expr[i].isdigit():
                    num += expr[i]
                    i += 1
                raw_tokens.append(int(num))
            elif ch in "()+-*/":
                raw_tokens.append(ch)
                i += 1
            else:
                raise ValueError(f"Token tidak valid: '{ch}'")

        # ── Bangun Pohon & Evaluasi ───────────────────────────────────────────
        root = self._build_tree(raw_tokens)
        result = self._eval_tree(root)
        self.values = [result]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Membangun pohon ekspresi secara rekursif dari antrian token.

        Pola ekspresi fully-parenthesized:
          ( <subexpr-kiri> <operator> <subexpr-kanan> )

        Algoritma (sesuai Listing 13.9):
          • Ambil token berikutnya.
          • Jika '(' → buat node internal:
              - left  = _build_tree() rekursif
              - op    = token berikutnya (operator)
              - right = _build_tree() rekursif
              - Konsumsi ')' penutup
          • Jika angka → buat node daun (leaf).
          • Jika ')' atau token tidak valid → raise ValueError.

        Node direpresentasikan sebagai dict:
          {'val': operator_atau_angka, 'left': node_kiri, 'right': node_kanan}
        """
        if not tokens:
            raise ValueError("Token habis saat membangun pohon.")

        token = tokens.popleft()

        # ── Kasus 1: Sub-ekspresi dalam kurung ────────────────────────────────
        if token == '(':
            # Bangun subpohon kiri
            left_node = self._build_tree(tokens)

            # Ambil operator
            if not tokens:
                raise ValueError("Operator tidak ditemukan setelah subexpr kiri.")
            op = tokens.popleft()
            if op not in "+-*/":
                raise ValueError(f"Operator tidak valid: '{op}'")

            # Bangun subpohon kanan
            right_node = self._build_tree(tokens)

            # Konsumsi tanda ')' penutup
            if not tokens:
                raise ValueError("Kurung tutup ')' tidak ditemukan.")
            closing = tokens.popleft()
            if closing != ')':
                raise ValueError(f"Diharapkan ')', ditemukan '{closing}'.")

            # Kembalikan node internal
            return {'val': op, 'left': left_node, 'right': right_node}

        # ── Kasus 2: Operand (angka) → node daun ─────────────────────────────
        elif isinstance(token, int):
            return {'val': token, 'left': None, 'right': None}

        # ── Kasus 3: Token tidak valid pada posisi ini ────────────────────────
        else:
            raise ValueError(f"Token tidak terduga: '{token}'")

    def _eval_tree(self, node: Optional[dict]) -> int:
        """
        Mengevaluasi pohon ekspresi secara POSTORDER rekursif:
          1. Evaluasi subpohon kiri → nilai_kiri
          2. Evaluasi subpohon kanan → nilai_kanan
          3. Terapkan operator pada nilai_kiri dan nilai_kanan

        Postorder secara alami menghasilkan notasi postfix –
        operator diproses setelah kedua operandnya siap.

        Raises
        ------
        ValueError jika terjadi pembagian dengan nol atau operator tidak dikenal.
        ZeroDivisionError ditangkap dan diubah menjadi ValueError yang informatif.
        """
        if node is None:
            raise ValueError("Node kosong (None) saat evaluasi.")

        # ── Node daun: kembalikan nilai integer ───────────────────────────────
        if node['left'] is None and node['right'] is None:
            val = node['val']
            if not isinstance(val, int):
                raise ValueError(f"Node daun bukan integer: '{val}'")
            return val

        # ── Node internal: evaluasi rekursif lalu terapkan operator ──────────
        left_val  = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op        = node['val']

        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError(
                    f"Pembagian dengan nol: {left_val} / {right_val}"
                )
            return left_val // right_val    # Integer division sesuai konteks embedded
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    # =========================================================
    # 2. IN-PLACE HEAPSORT
    # =========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array secara ASCENDING menggunakan HeapSort in-place.

        Fase 1 – Build Max-Heap:
          Mulai dari node non-leaf terakhir (indeks n//2 - 1) ke atas,
          panggil sift_down() untuk setiap node. Hasilnya: arr[0] = nilai terbesar.

        Fase 2 – Ekstraksi Berurutan:
          Tukar arr[0] (max) dengan arr[end], lalu kurangi heap_size dan
          sift-down kembali dari indeks 0.
          Diulang hingga heap_size = 1.

        Kompleksitas Waktu : O(n log n)
        Kompleksitas Ruang : O(1) – benar-benar in-place, hanya variabel indeks
        Stabilitas         : TIDAK STABLE (inherently unstable karena swap)
        """
        n = len(arr)
        if n <= 1:
            return arr

        # ── Fase 1: Bangun max-heap dari bawah ke atas ───────────────────────
        # Node non-leaf terakhir ada di indeks (n // 2 - 1)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # ── Fase 2: Ekstrak elemen terbesar satu per satu ────────────────────
        for end in range(n - 1, 0, -1):
            # Pindahkan root (max) ke posisi akhir yang belum terurut
            arr[0], arr[end] = arr[end], arr[0]
            # Pulihkan heap property untuk heap yang lebih kecil
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Memulihkan heap order property dengan mendorong node di indeks 'idx'
        ke bawah sampai properti max-heap terpenuhi.

        Rumus indeks (complete binary tree → array):
          left child  : 2 * idx + 1
          right child : 2 * idx + 2
          parent      : (i - 1) // 2

        Algoritma:
          1. Tentukan indeks 'largest' = idx.
          2. Jika anak kiri ada dan lebih besar dari arr[largest], update largest.
          3. Jika anak kanan ada dan lebih besar dari arr[largest], update largest.
          4. Jika largest != idx, swap dan ulangi dari posisi largest (loop).

        Jumlah perbandingan maksimum: 2 * floor(log2(n)) karena tinggi heap = log2(n).
        """
        while True:
            largest = idx
            left    = 2 * idx + 1
            right   = 2 * idx + 2

            # Bandingkan dengan anak kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Bandingkan dengan anak kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika arr[idx] sudah merupakan yang terbesar, heap property terpenuhi
            if largest == idx:
                break

            # Tukar idx dengan largest, lalu lanjutkan sift-down dari bawah
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest    # Lanjutkan iterasi dari posisi baru

    # =========================================================
    # 3. COMPLETE BINARY TREE VALIDATOR
    # =========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah array memenuhi properti COMPLETE BINARY TREE
        ketika dipetakan ke struktur heap berbasis array.

        Properti complete binary tree:
          • Semua level terisi penuh kecuali mungkin level terakhir.
          • Level terakhir diisi dari kiri ke kanan tanpa 'lubang'.

        Pembuktian via rumus indeks:
          Untuk setiap node di indeks i (0 ≤ i < n):
            - Anak kiri  ada di 2*i+1; harus < n jika anak kiri diharapkan ada.
            - Anak kanan ada di 2*i+2; harus < n jika anak kanan diharapkan ada.
          'Lubang' terjadi jika anak kanan ada tapi anak kiri tidak ada,
          atau jika setelah satu node tanpa anak kiri masih ada node lain.

        Dalam array yang merupakan complete binary tree dengan n elemen,
        semua indeks 0..n-1 harus terisi tanpa celah.
        Pengecekan: setelah menemukan node yang tidak punya anak kiri,
        semua node berikutnya harus juga berupa daun (leaf).
        """
        n = len(arr)
        if n == 0:
            return True     # Array kosong dianggap valid (pohon kosong)

        found_non_full = False    # Flag: sudah menemukan node yang tidak punya 2 anak

        for i in range(n):
            left  = 2 * i + 1
            right = 2 * i + 2

            # Jika anak kiri tidak ada
            if left >= n:
                # Semua node setelah ini harus juga tidak punya anak (leaf)
                found_non_full = True
            else:
                # Anak kiri ada — jika sebelumnya sudah found_non_full, ada 'lubang'
                if found_non_full:
                    return False

            # Jika anak kanan tidak ada
            if right >= n:
                found_non_full = True
            else:
                # Anak kanan ada — jika sebelumnya sudah found_non_full, ada 'lubang'
                if found_non_full:
                    return False

        return True


# ═══════════════════════════════════════════════════════════════════════════════
# CONTOH PENGGUNAAN & TESTING
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  ExprHeapSorter — Demo & Testing")
    print("=" * 60)

    # ── TEST 1: Expression Tree Builder & Evaluator ──────────────────────────
    print("\n[1] Expression Tree: ((8 * 5) + (9 / (7 - 4)))")
    sorter1 = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")
    result1 = sorter1.parse_and_evaluate()
    # Manual: (8*5)=40, (7-4)=3, 9//3=3, 40+3=43
    print(f"  Hasil evaluasi : {result1[0]}  (ekspektasi: 43)")

    print("\n[2] Expression Tree: ((3 + 4) * (10 - 2))")
    sorter2 = ExprHeapSorter("((3 + 4) * (10 - 2))")
    result2 = sorter2.parse_and_evaluate()
    # Manual: 7 * 8 = 56
    print(f"  Hasil evaluasi : {result2[0]}  (ekspektasi: 56)")

    print("\n[3] Expression Tree: Pembagian Nol — ((5 + 3) / (4 - 4))")
    try:
        sorter3 = ExprHeapSorter("((5 + 3) / (4 - 4))")
        sorter3.parse_and_evaluate()
    except ValueError as e:
        print(f"  Berhasil menangkap error: {e}")

    # ── TEST 2: In-Place HeapSort ─────────────────────────────────────────────
    print("\n[4] In-Place HeapSort")
    sorter4 = ExprHeapSorter("")
    arr_test = [43, 15, 7, 56, 3, 99, 21, 8]
    print(f"  Input : {arr_test}")
    sorter4.heapsort_inplace(arr_test)
    print(f"  Output: {arr_test}  (ascending)")

    # Kasus khusus: array 1 elemen
    arr_one = [42]
    sorter4.heapsort_inplace(arr_one)
    print(f"\n  Array 1 elemen: {arr_one}  (tidak berubah)")

    # Kasus khusus: semua elemen sama
    arr_dup = [5, 5, 5, 5, 5]
    sorter4.heapsort_inplace(arr_dup)
    print(f"  Array duplikat : {arr_dup}")

    # ── TEST 3: HeapSort + Expression Result ─────────────────────────────────
    print("\n[5] HeapSort + Hasil Evaluasi Ekspresi")
    # Gabungkan hasil evaluasi ekspresi dengan angka acak
    import random
    random.seed(7)
    extra_values = [random.randint(1, 100) for _ in range(7)]
    eval_result  = result1[0]    # = 43 dari ekspresi pertama
    combined     = extra_values + [eval_result]
    print(f"  Data gabungan (7 acak + hasil ekspresi): {combined}")
    sorter4.heapsort_inplace(combined)
    print(f"  Setelah HeapSort: {combined}")

    # ── TEST 4: Complete Binary Tree Validator ────────────────────────────────
    print("\n[6] Complete Binary Tree Validator")

    # Array terurut: [1,2,3,4,5] → complete tree yang valid
    arr_complete = [1, 2, 3, 4, 5]
    print(f"  {arr_complete} → complete? {sorter4.is_complete_tree(arr_complete)}")  # True

    # Array terurut: [1,2,3,4,5,6,7] → full binary tree (complete juga)
    arr_full = [1, 2, 3, 4, 5, 6, 7]
    print(f"  {arr_full} → complete? {sorter4.is_complete_tree(arr_full)}")  # True

    # Array kosong
    print(f"  [] → complete? {sorter4.is_complete_tree([])}")  # True

    # Array 1 elemen
    print(f"  [42] → complete? {sorter4.is_complete_tree([42])}")  # True

    # Catatan: array hasil heapsort (ascending) bukan max-heap,
    # tapi secara STRUKTUR indeks 0..n-1 selalu membentuk complete binary tree.
    arr_sorted = [1, 2, 3, 4, 5, 6]
    print(f"  {arr_sorted} → complete? {sorter4.is_complete_tree(arr_sorted)}")  # True

    # ── TEST 5: Verifikasi Kebenaran HeapSort ─────────────────────────────────
    print("\n[7] Verifikasi Kebenaran HeapSort vs Python Built-in")
    random.seed(99)
    big_arr  = [random.randint(0, 1000) for _ in range(200)]
    ref      = sorted(big_arr)          # Referensi (hanya untuk verifikasi test)
    sorter4.heapsort_inplace(big_arr)
    print(f"  200 elemen random — hasil benar: {big_arr == ref}")

    print("\n" + "=" * 60)
    print("  Semua test selesai.")
    print("=" * 60)
