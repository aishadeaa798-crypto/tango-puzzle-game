import copy
class TangoBoard:
    def __init__(self, n, initial_values, grid_relations):
        self.n = n
        self.relations = grid_relations
        
        self.board = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(0)
            self.board.append(row)
        
        self.fixed_mask = []
        for i in range(n):
            mask_row = []
            for j in range(n):
                mask_row.append(False)
            self.fixed_mask.append(mask_row)
            
        for pos in initial_values:
            r = pos[0]
            c = pos[1]
            val = initial_values[pos]
            self.board[r][c] = val
            self.fixed_mask[r][c] = True

    def is_editable(self, r, c):
        if r < 0 or r >= self.n or c < 0 or c >= self.n:
            return False
        if self.fixed_mask[r][c] == True:
            return False
        return True

    def check_immediate_rules(self, r, c):
        val = self.board[r][c]
        if val == 0:
            return True

        for j in range(self.n - 2):
            if self.board[r][j] == val and self.board[r][j+1] == val and self.board[r][j+2] == val:
                return False

        for i in range(self.n - 2):
            if self.board[i][c] == val and self.board[i+1][c] == val and self.board[i+2][c] == val:
                return False

        return True
      

    def is_editable(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.n and not self.fixed_mask[r][c]

    def get_hash(self):
        return tuple(tuple(row) for row in self.board)

    def is_board_full(self):
        return all(self.board[r][c] != 0 for r in range(self.n) for c in range(self.n))

    def get_conflicting_cells(self):
        """Returns a set of cells that violate triple-repetition or relationship rules."""
        conflicts = set()
        # 1. Triple repetition check (Horizontal)
        for r in range(self.n):
            for c in range(self.n - 2):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r][c+1] == self.board[r][c+2]:
                    conflicts.update([(r, c), (r, c+1), (r, c+2)])
        
        # 2. Triple repetition check (Vertical)
        for c in range(self.n):
            for r in range(self.n - 2):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r+1][c] == self.board[r+2][c]:
                    conflicts.update([(r, c), (r+1, c), (r+2, c)])
        
        # 3. Relationship rules check (= and x)
        for (c1, c2), rel in self.relations.items():
            v1, v2 = self.board[c1[0]][c1[1]], self.board[c2[0]][c2[1]]
            if v1 != 0 and v2 != 0:
                if (rel == "=" and v1 != v2) or (rel == "x" and v1 == v2):
                    conflicts.add(c1)
                    conflicts.add(c2)
        return conflicts

    def is_count_valid(self):
        """Checks if any row or column exceeds the limit of n/2 Suns or Moons."""
        limit = self.n // 2
        for i in range(self.n):
            row = self.board[i]
            col = [self.board[r][i] for r in range(self.n)]
            if row.count(1) > limit or row.count(-1) > limit: return False
            if col.count(1) > limit or col.count(-1) > limit: return False
        return True



    def display_board(self):
        RED_BG = "\033[41m\033[37m"
        RESET = "\033[0m"
        bad_cells = self.get_conflicting_cells()
        
        print("\n      C0    C1    C2    C3")
        print("    ------------------------")
        for r in range(self.n):
            row_str = f"R{r} | "
            for c in range(self.n):
                val = self.board[r][c]
                icon = "☀️" if val == 1 else ("🌙" if val == -1 else "⬛")
                
                if (r, c) in bad_cells:
                    row_str += f"{RED_BG}{icon}{RESET}"
                else:
                    row_str += icon
                
                rel = self.relations.get(((r, c), (r, c+1))) or self.relations.get(((r, c+1), (r, c)))
                row_str += f" {rel}  " if rel else "    "
            print(row_str)
            
           
            if r < self.n - 1:
                rel_row = "    | "
                for c in range(self.n):
                    rel = self.relations.get(((r, c), (r+1, c))) or self.relations.get(((r+1, c), (r, c)))
                    rel_row += f" {rel}    " if rel else "      "
                print(rel_row)
        print("    ------------------------")


    def is_board_full(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == 0:
                    return False
        return True

    def check_all_relations(self):
        for pair in self.relations:
            cell1 = pair[0]
            cell2 = pair[1] 
            relation_type = self.relations[pair]
            
            v1 = self.board[cell1[0]][cell1[1]]
            v2 = self.board[cell2[0]][cell2[1]]
            
            if v1 == 0 or v2 == 0:
                continue
                
            if relation_type == "=":
                if v1 != v2:
                    return False
            
            
            if relation_type == "x":
                if v1 == v2:
                    return False
        
        return True
    
    def check_immediate_rules(self, r, c):
        
        val = self.board[r][c]
        if val == 0:
            return True

        for j in range(self.n - 2):
            if self.board[r][j] == val and self.board[r][j+1] == val and self.board[r][j+2] == val:
                return False

        for i in range(self.n - 2):
            if self.board[i][c] == val and self.board[i+1][c] == val and self.board[i+2][c] == val:
                return False

        for pair in self.relations:
            cell1, cell2 = pair[0], pair[1]
            if (r, c) == cell1 or (r, c) == cell2:
                v1 = self.board[cell1[0]][cell1[1]]
                v2 = self.board[cell2[0]][cell2[1]]
                if v1 == 0 or v2 == 0:
                    continue
                if self.relations[pair] == "=" and v1 != v2:
                    return False
                if self.relations[pair] == "x" and v1 == v2:
                    return False
        return True

    def make_move(self, r, c, val):
        if not self.is_editable(r, c):
            return False

        self.board[r][c] = val
        return True

   
    
    def check_rules(self):
     for i in range(self.n):
        if 0 in self.board[i]: return False
        if sum(self.board[i]) != 0: return False 
        if sum(self.board[r][i] for r in range(self.n)) != 0: return False 
     return True
    
    def check_win_condition(self):
        if not self.is_board_full():
            return False
            
        if len(self.get_conflicting_cells()) > 0:
            return False
            
        if not self.check_rules():
            return False
            
        return True
    
    def display_board(self):
        RED_BG = "\033[41m\033[37m"
        RESET = "\033[0m"           
        
        bad_cells = self.get_conflicting_cells()
        
        print("\n      C0    C1    C2    C3")
        print("    ------------------------")
        for r in range(self.n):
            row_str = "R" + str(r) + " | "
            for c in range(self.n):
                val = self.board[r][c]
                icon = "☀️" if val == 1 else ("🌙" if val == -1 else "⬛")
                
                if (r, c) in bad_cells:
                    row_str += f"{RED_BG}{icon}{RESET}"
                else:
                    row_str += icon
                
                if c < self.n - 1:
                    if ((r, c), (r, c+1)) in self.relations:
                        row_str += self.relations[((r, c), (r, c+1))]
                    elif ((r, c+1), (r, c)) in self.relations:
                        row_str += self.relations[((r, c+1), (r, c))]
                    else:
                        row_str += "  " 
                else:
                    row_str += "  "
                row_str += "  "
            
            print(row_str)
            
            
            rel_row = "    | "
            for c in range(self.n):
                if r < self.n - 1:
                    if ((r, c), (r+1, c)) in self.relations:
                        rel_row += " " + self.relations[((r, c), (r+1, c))] + "    "
                    elif ((r+1, c), (r, c)) in self.relations:
                        rel_row += " " + self.relations[((r+1, c), (r, c))] + "    "
                    else:
                        rel_row += "      "
            
            if r < self.n - 1: 
                print(rel_row)
                
        print("    ------------------------")   
        
def solve_dfs(state):
    """Deep-First Search algorithm to solve the puzzle."""
    if state.check_win_condition():
        return state

    target_cell = None
    for r in range(state.n):
        for c in range(state.n):
            if state.board[r][c] == 0:
                target_cell = (r, c)
                break
        if target_cell: break
    
    if not target_cell: return None

    r, c = target_cell
    for val in [1, -1]: 
        new_board = [row[:] for row in state.board]
        new_board[r][c] = val
        
        next_state = copy.copy(state)
        next_state.board = new_board
        print(f"Trying {val} at {target_cell}")
        
        if len(next_state.get_conflicting_cells()) == 0 and next_state.is_count_valid():
            result = solve_dfs(next_state)
            if result: return result
            
    return None

      
def main():
   
    starting_puzzles = {
        (0, 1): 1,    
        (3, 2): 1    
    }
    
    game_relations = {
        ((0, 0), (0, 1)): "=",  
        ((0, 0), (1, 0)): "x",
        ((2, 2), (2, 3)): "x",  
    }
    
    game = TangoBoard(4, starting_puzzles, game_relations)
    
    print("=== TANGO PUZZLE OPTIONS ===")
    print("1. Play Manually (Human Mode)")
    print("2. Solve Automatically (AI Expert System Mode)")
    
    choice = input("Select Mode (1 or 2): ").strip()
    if choice == "2":
        print("Solving...")
        solution = solve_dfs(game)
        if solution:
            solution.display_board()
            print("✅ Puzzle Solved!")
        else:
            print("❌ No solution exists for these values.")


    else:
        print("\nWelcome to Tango Puzzle!")
        print(" Enter 'row col val'. Use 1 for ☀️, -1 for 🌙, 0 for ⬛")
        
        while True:
            
            game.display_board()
            
            
            if game.check_win_condition():
                print("\n🎉🎉 CONGRATULATIONS! YOU SOLVED IT PERFECTLY! 🎉🎉")
                break

            
            if game.is_board_full():
                print("⚠️ The board is completely full, but you have some errors!")

            
            user_input = input("\nYour move or 'exit': ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye! Thanks for playing.")
                break
                
            try:
                parts = user_input.split()
                if len(parts) == 3:
                    r, c, v = int(parts[0]), int(parts[1]), int(parts[2])
                    
                    if v not in [1, -1, 0]:
                        print("❌ Invalid value! Use 1 for ☀️, -1 for 🌙, or 0 to clear.")
                        continue
                        
                    
                    if not game.make_move(r, c, v):
                        print("❌You cannot modify fixed starting cells or out of bounds")
                else:
                    print("❌ Please enter 3 numbers (row col val).")
            except ValueError:
                print("❌Please enter numbers only.")


if __name__ == "__main__" : 
    main()
