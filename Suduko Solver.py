"""
CSP Sudoku Solver (Simple + Step-Based)
Uses: Backtracking + Forward Checking + AC-3
"""

class SudokuCSP:

    def __init__(self, board_str):
        self.board = self._parse(board_str)
        self.vars = self._make_vars()
        self.dom = self._init_domains()
        self.bt_count = 0


    # ================= FILE LOAD =================
    def load_file(self, fname):
        with open(fname, 'r') as f:
            data = f.read()
        self.board = self._parse(data)
        self.dom = self._init_domains()


    # ================= BASIC FUNCTIONS =================
    def _parse(self, s):
        board = []
        lines = s.strip().split('\n')

        for line in lines:
            row = []
            for ch in line.strip():
                row.append(int(ch))
            board.append(row)

        return board


    def _make_vars(self):
        v = []
        for i in range(9):
            for j in range(9):
                v.append((i, j))
        return v


    def _init_domains(self):
        d = {}

        for i in range(9):
            for j in range(9):

                if self.board[i][j] == 0:
                    d[(i, j)] = set(range(1, 10))
                else:
                    d[(i, j)] = {self.board[i][j]}

        return d


    # ================= NEIGHBORS =================
    def _row(self, r):
        return [(r, j) for j in range(9)]

    def _col(self, c):
        return [(i, c) for i in range(9)]

    def _box(self, r, c):
        cells = []
        sr = (r // 3) * 3
        sc = (c // 3) * 3

        for i in range(sr, sr + 3):
            for j in range(sc, sc + 3):
                cells.append((i, j))

        return cells


    def _neigh(self, v):
        r, c = v

        n = set()
        n.update(self._row(r))
        n.update(self._col(c))
        n.update(self._box(r, c))
        n.discard(v)

        return n


    #  CONSTRAINT CHECK 
    def is_ok(self, v, val):

        for n in self._neigh(v):

            # STEP: check assigned neighbor
            if len(self.dom[n]) == 1 and val in self.dom[n]:
                return False

        return True


    # FORWARD CHECK 
    def fwd_check(self, v, val):

        removed = []

        for n in self._neigh(v):

            if val in self.dom[n]:
                self.dom[n].remove(val)
                removed.append((n, val))

        return removed


    #  AC-3 
    def _revise(self, v1, v2):

        revised = False

        d1 = self.dom[v1]
        d2 = self.dom[v2]

        remove_list = []

        for val in d1:

            ok = False

            for val2 in d2:
                if val2 != val:
                    ok = True
                    break

            if not ok and len(d2) == 1:
                remove_list.append(val)

        for val in remove_list:
            d1.discard(val)
            revised = True

        return revised


    def ac3(self):
        q = []
        for v1 in self.vars:
            for v2 in self._neigh(v1):
                q.append((v1, v2))
        while q:

            v1, v2 = q.pop(0)

            if self._revise(v1, v2):
                if len(self.dom[v1]) == 0:
                    return False
                for n in self._neigh(v1):
                    if n != v2:
                        q.append((n, v1))

        return True


    #  MRV 
    def pick_var(self):

        unassigned = []

        for v in self.vars:
            if len(self.dom[v]) > 1:
                unassigned.append(v)

        if not unassigned:
            return None

        # STEP: select min domain
        best = unassigned[0]

        for v in unassigned:
            if len(self.dom[v]) < len(self.dom[best]):
                best = v

        return best


    # ================= SAVE / RESTORE =================
    def _save(self):
        s = {}
        for v in self.vars:
            s[v] = self.dom[v].copy()
        return s


    def _restore(self, s):
        for v in self.vars:
            self.dom[v] = s[v].copy()


    # ================= BACKTRACK =================
    def backtrack(self):

        self.bt_count += 1
        v = self.pick_var()
        if v is None:
            return True

        # STEP 4: try values
        for val in list(self.dom[v]):

            if self.is_ok(v, val):
                saved = self._save()
                self.dom[v] = {val}

                self.fwd_check(v, val)
                if self.ac3() and self.backtrack():
                    return True
                self._restore(saved)

        return False


    # ================= SOLVE =================
    def solve(self):

        # STEP 1: initial AC3
        if not self.ac3():
            return False

        # STEP 2: backtrack
        return self.backtrack()


    # ================= PRINT =================
    def print_board(self):

        for i in range(9):

            if i % 3 == 0 and i != 0:
                print("------+-------+------")

            row = ""

            for j in range(9):

                if j % 3 == 0 and j != 0:
                    row += "| "

                val = list(self.dom[(i, j)])[0]
                row += str(val) + " "

            print(row)


# ================= MAIN =================
if __name__ == "__main__":

    files = {
        "easy": "easy.txt",
        "medium": "medium.txt",
        "hard": "hard.txt",
        "veryhard": "veryhard.txt"
    }

    for name, fname in files.items():

        print("\n" + "="*40)
        print(f"Solving {name.upper()}")
        print("="*40)

        # STEP 1: create solver
        s = SudokuCSP("000000000\n"*9)

        # STEP 2: load file
        s.load_file(fname)

        # STEP 3: solve
        if s.solve():

            print("\nSolved:")
            s.print_board()

            print("\nBacktracks:", s.bt_count)

        else:
            print("No solution")