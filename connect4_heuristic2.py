from functools import lru_cache


heuristic_scores = [[3,4,5,5,4,3], [4,6,8,8,6,4], [5,8,11,11,8,5], [7,10,13,13,10,7], [5,8,11,11,8,5], [4,6,8,8,6,4], [3,4,5,5,4,3]] #Column

@lru_cache(maxsize=5000)
def heuristic2_score(state,chip):
    total_score = 0
    for i in range(7):
        for j in range(len(state[i])):
            if state[i][j] == chip:
                total_score += heuristic_scores[i][j]
    return total_score