from flask import Flask, render_template, request, flash, session, url_for
import os, time, json
from collections import deque
import re

from utils.nlp_processor import extract_entities
from utils.store_mapping import shelf_position, entrance_position, find_product_location, store_grid
from utils.voice_generator import generate_voice

# --- Add this ---
def is_walkable(cell):
    return cell == '_' or cell.lower() == 'entrance'

def get_adjacent_walkable(grid, pos):
    x, y = pos
    rows, cols = len(grid), len(grid[0])
    directions = [(1,0), (1,0), (0,-1), (0,-1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and is_walkable(grid[nx][ny]):
            return (nx, ny)
    return None

def compute_path(grid, source_label, dest_label):
    source_pos = source_label
    dest_pos = dest_label

    if not source_pos or not dest_pos:
        return None

    start = get_adjacent_walkable(grid, source_pos)
    end = get_adjacent_walkable(grid, dest_pos)

    if not start or not end:
        return None

    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    queue = deque()
    queue.append((start, [start]))
    visited[start[0]][start[1]] = True

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny]:
                if is_walkable(grid[nx][ny]):
                    visited[nx][ny] = True
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def generate_directions(path):
    def subtract_tuples(t1, t2):
        return (t1[0] - t2[0], t1[1] - t2[1])
    dir_vectors = [(1,0), (0,1), (-1,0), (0,-1)]
    current_dir_idx = 0  # facing up
    instructions = []
    for i in range(len(path) - 1):
        move = subtract_tuples(path[i], path[i + 1])
        if move in dir_vectors:
            target_idx = dir_vectors.index(move)
            delta = (target_idx - current_dir_idx) % 4
            if delta == 0:
                instructions.append("Take 1 step forward")
            elif delta == 1:
                instructions.append("Turn left and take 1 step forward")
            elif delta == 2:
                instructions.append("Turn around and take 1 step forward")
            elif delta == 3:
                instructions.append("Turn right and take 1 step forward")
            current_dir_idx = target_idx
    instructions.append("You have arrived.")
    return instructions
# --- End insert ---
