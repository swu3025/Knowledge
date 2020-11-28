import itertools
import random
from random import randint


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    # MY CODE
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            if self.count != 0:
                return self.cells
        else:
            return set()

    # MY CODE
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            if len(self.cells) != 0:
                return self.cells

    # MY CODE
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cell:
            self.cell.remove(cell)
            self.count -=1;

    # MY CODE
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # MY CODE
    def add_knowledge(self, cell, count):#cell = tuple corresponding count
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made 
            2) mark the cell as safe 
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3
        cells = set()
        for i in range(cell[0]-1,cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if cell == (i,j):
                    continue
                if 0 <= i < self.height and  0 <= j < self.width:
                    if(i,j) in self.mines:
                        count -=1
                    elif (i,j) not in self.safes:
                        cells.add((i,j))
        self.knowledge.append(Sentence(cells,count))

        #4 
        for part in self.knowledge:
            safe = part.known_safes()
            mine = part.known_mines()
            if safe != None:
                for s in safe:
                    if s not in self.safes:
                        self.safes.add(s)
            if mine != None:
                for m in mine:
                    if m not in self.mines:
                        self.mines.add(m)

        #5 More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, 
        #then we can construct the new sentence set2 - set1 = count2 - count1
        length = len(self.knowledge)
        for i in range(length):
            for j in range(i+1, length):
                set1 = self.knowledge[i]
                set2 = self.knowledge[j]
                if set1.cells.issubset(set2.cells):
                    cells = set2.cells - set1.cells
                    s = Sentence(set2.cells - set1.cells, set2.count - set1.count)
                    if s not in self.knowledge:
                        self.knowledge.append(s)

                elif set2.cells.issubset(set1.cells):
                    cells = set1.cells - set2.cells
                    s = Sentence(set1.cells - set2.cells, set1.count - set2.count)
                    if s not in self.knowledge:
                        self.knowledge.append(s)

    # MY CODE
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None

    # MY CODE
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    random.add((i,j))
        if len(random) != 0:
            return list(random)[randint(0,len(random)-1)]
        return None
