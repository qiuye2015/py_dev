from copy import deepcopy
import time

import numpy as np


def create_grid(puzzle_str: str) -> np.ndarray:
    """Create a 9x9 Sudoku grid from a string of digits"""

    # Deleting whitespaces and newlines (\n)
    lines = puzzle_str.replace(" ", "").replace("\n", "")
    digits = list(map(int, lines))
    # Turning it to a 9x9 numpy array
    grid = np.array(digits).reshape(9, 9)
    return grid


def get_subgrids(grid: np.ndarray) -> np.ndarray:
    """Divide the input grid into 9 3x3 sub-grids"""

    subgrids = []
    for box_i in range(3):
        for box_j in range(3):
            subgrid = []
            for i in range(3):
                for j in range(3):
                    subgrid.append(grid[3 * box_i + i][3 * box_j + j])
            subgrids.append(subgrid)
    return np.array(subgrids)


def get_candidates(grid: np.ndarray) -> list:
    """Get a list of candidates to fill empty cells of the input grid"""

    def subgrid_index(i, j):
        return (i // 3) * 3 + j // 3

    subgrids = get_subgrids(grid)
    grid_candidates = []
    for i in range(9):
        row_candidates = []
        for j in range(9):
            # Row, column and subgrid digits
            row = set(grid[i])
            col = set(grid[:, j])
            sub = set(subgrids[subgrid_index(i, j)])
            common = row | col | sub
            candidates = set(range(10)) - common
            # If the case is filled take its value as the only candidate
            if not grid[i][j]:
                row_candidates.append(list(candidates))
            else:
                row_candidates.append([grid[i][j]])
        grid_candidates.append(row_candidates)
    return grid_candidates


def is_valid_grid(grid: np.ndarray) -> bool:
    """Verify the input grid has a possible solution"""

    candidates = get_candidates(grid)
    for i in range(9):
        for j in range(9):
            if len(candidates[i][j]) == 0:
                return False
    return True


def is_solution(grid: np.ndarray) -> bool:
    """Verify if the input grid is a solution"""

    if (
        np.all(np.sum(grid, axis=1) == 45)
        and np.all(np.sum(grid, axis=0) == 45)
        and np.all(np.sum(get_subgrids(grid), axis=1) == 45)
    ):
        return True
    return False


def filter_candidates(grid: np.ndarray) -> list:
    """Filter input grid's list of candidates"""
    test_grid = grid.copy()
    candidates = get_candidates(grid)
    filtered_candidates = deepcopy(candidates)
    for i in range(9):
        for j in range(9):
            # Check for empty cells
            if grid[i][j] == 0:
                for candidate in candidates[i][j]:
                    # Use test candidate
                    test_grid[i][j] = candidate
                    # Remove candidate if it produces an invalid grid
                    if not is_valid_grid(fill_singles(test_grid)):
                        filtered_candidates[i][j].remove(candidate)
                    # Revert changes
                    test_grid[i][j] = 0
    return filtered_candidates


def merge(candidates_1: list, candidates_2: list) -> list:
    """Take shortest candidate list from inputs for each cell"""

    candidates_min = []
    for i in range(9):
        row = []
        for j in range(9):
            if len(candidates_1[i][j]) < len(candidates_2[i][j]):
                row.append(candidates_1[i][j][:])
            else:
                row.append(candidates_2[i][j][:])
        candidates_min.append(row)
    return candidates_min


def fill_singles(grid: np.ndarray, candidates=None) -> np.ndarray:
    """Fill input grid's cells with single candidates"""

    grid = grid.copy()
    if not candidates:
        candidates = get_candidates(grid)
    any_fill = True
    while any_fill:
        any_fill = False
        for i in range(9):
            for j in range(9):
                if len(candidates[i][j]) == 1 and grid[i][j] == 0:
                    grid[i][j] = candidates[i][j][0]
                    candidates = merge(get_candidates(grid), candidates)
                    any_fill = True
    return grid


def make_guess(grid: np.ndarray, candidates=None) -> np.ndarray:
    """Fill next empty cell with least candidates with first candidate"""

    grid = grid.copy()
    if not candidates:
        candidates = get_candidates(grid)
    # Getting the shortest number of candidates > 1:
    min_len = sorted(list(set(map(len, np.array(candidates).reshape(1, 81)[0]))))[1]
    for i in range(9):
        for j in range(9):
            if len(candidates[i][j]) == min_len:
                for guess in candidates[i][j]:
                    grid[i][j] = guess
                    solution = solve(grid)
                    if solution is not None:
                        return solution
                    # Discarding a wrong guess
                    grid[i][j] = 0


def solve(grid: np.ndarray) -> np.ndarray:
    """Recursively find a solution filtering candidates and guessing values"""

    candidates = filter_candidates(grid)
    grid = fill_singles(grid, candidates)
    if is_solution(grid):
        return grid
    if not is_valid_grid(grid):
        return None
    return make_guess(grid, candidates)


# Example usage
start = time.time()
puzzle = """100920000
            524010000
            000000070
            050008102
            000000000
            402700090
            060000000
            000030945
            000071006"""

grid = create_grid(puzzle)
r = solve(grid)
print(r)
print(time.time() - start)
