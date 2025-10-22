import sys
import heapq

from labyrinth import Labyrinth


def solve(lines: list[str]) -> int:
    start_labyrinth = parse_input(lines)
    pq = [(0, start_labyrinth)]
    costs = {start_labyrinth: 0}
    while pq:
        cost, state = heapq.heappop(pq)
        if state.is_final():
            return cost
        for move_cost, next_state in state.generate_moves():
            new_cost = cost + move_cost
            if next_state not in costs or new_cost < costs[next_state]:
                costs[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))
    return -1


def parse_input(lines : list[str]) -> Labyrinth:
    rooms = []
    for x in (3,5,7,9):
        room = []
        for y in range(2, len(lines) - 1):
            room.append(lines[y][x])
        rooms.append(tuple(room))
    return Labyrinth(tuple(rooms), tuple('.' * 11))


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
