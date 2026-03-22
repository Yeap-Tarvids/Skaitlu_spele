## Ed variant minimax
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING: # for import correct work
    from base_code import GameState
## from minimax import ai_move, build_tree | add to base_code.py
MAX_DEPTH = 3

def heuristic(numSeq, firstMove):
    towardEven = firstMove
    seq = list(numSeq)
    count = 0
    for i in seq:
        if (i % 2 == 0) == towardEven:
            count += 1
    score = (count / len(seq)) * 2 - 1
    if (seq[0] % 2 == 0) == towardEven:
        fnumBonus = 0.5
    else:
        fnumBonus = -0.5
    delBonus = 0.0
    if len(seq) % 2 != 0:
        if (seq[-1] % 2 == 0) == towardEven:
            delBonus = -0.3
        else:
            delBonus = 0.3
    return score + fnumBonus + delBonus

def apply_move(state: "GameState", move: int) -> "GameState":
    from base_code import GameState
    new_state = GameState(list(state.virkne), state.punkti, state.banka)
    new_state.sumPair(move)
    return new_state

def get_moves(state: "GameState") -> list[int]:
    return list(range(1, math.ceil(len(state.virkne) / 2) + 1))

def evaluate_terminal(state: "GameState", ai_is_player1: bool) -> int:
    result = state.winCon()
    if ai_is_player1:
        return result * 100
    else:
        return result * -100

def minimax(state: "GameState", depth: int,
            maximizing: bool, ai_is_player1: bool) -> float:
    if state.Has_finished():
        return evaluate_terminal(state, ai_is_player1)
    if depth >= MAX_DEPTH:
        return heuristic(state.virkne, ai_is_player1)
    scores = [
        minimax(apply_move(state, move), depth + 1, not maximizing, ai_is_player1)
        for move in get_moves(state)
    ]
    return max(scores) if maximizing else min(scores)

def ai_move(state: "GameState", ai_is_player1: bool) -> int:
    moves = get_moves(state)
    scores = [
        minimax(apply_move(state, move), 0, False, ai_is_player1)
        for move in moves
    ]
    return moves[scores.index(max(scores))]

def build_tree(state: "GameState", maximizing: bool, ai_is_player1: bool, depth: int = 0) -> dict:
    node = {
        "depth": depth,
        "virkne": list(state.virkne),
        "punkti": state.punkti,
        "banka": state.banka,
        "turn": "AI" if maximizing else "opponent",
        "move": None,
        "score": None,
        "children": []
    }
    if state.Has_finished():
        node["score"] = evaluate_terminal(state, ai_is_player1)
        return node
    if depth >= MAX_DEPTH:
        node["score"] = heuristic(state.virkne, ai_is_player1)
        return node
    for move in get_moves(state):
        child = build_tree(apply_move(state, move), not maximizing, ai_is_player1, depth + 1)
        child["move"] = move
        node["children"].append(child)
    child_scores = [c["score"] for c in node["children"]]
    node["score"] = max(child_scores) if maximizing else min(child_scores)
    return node