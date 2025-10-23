import sys
import heapq

class Labyrinth:
    energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_indexes = [2, 4, 6, 8]
    hall_indexes = [0, 1, 3, 5, 7, 9, 10]

    def __init__(self, rooms: tuple[tuple[str, ...], ...], hall: tuple[str, ...]):
        self.rooms = rooms
        self.hall = hall
        self.depth = len(self.rooms[0])

    def __hash__(self):
        return hash((self.rooms, self.hall))

    def __eq__(self, other):
        if not isinstance(other, Labyrinth):
            return False
        return self.hall == other.hall and self.rooms == other.rooms

    def __lt__(self, other):
        if not isinstance(other, Labyrinth):
            return NotImplemented
        if self.hall != other.hall:
            return self.hall < other.hall
        return self.rooms < other.rooms

    def __str__(self):
        s = '#############\n#' + ''.join(self.hall) + '#\n'
        for i in range(self.depth):
            if i == 0:
                s += '###'
                for room in self.rooms:
                    s += room[i] + '#'
                s += '##\n'
            else:
                s += '  #'
                for room in self.rooms:
                    s += room[i] + '#'
                s += '  \n'
        s += '  #########  '
        return s

    def is_final(self) -> bool:
        for i, room in enumerate(self.rooms):
            if any(x != 'ABCD'[i] for x in room):
                return False
        return True

    def generate_moves(self) -> list[tuple[int, "Labyrinth"]]:
        result = []
        for room_idx, room in enumerate(self.rooms):
            top_index = -1
            top_char = ''
            for i, ch in enumerate(room):
                if ch != '.':
                    top_index = i
                    top_char = ch
                    break
            if top_index == -1:
                continue
            target_char = 'ABCD'[room_idx]
            if all(x == target_char for x in room[top_index:]):
                continue

            target_room = Labyrinth.room_indexes[room_idx]
            for x in range(target_room - 1, -1, -1):
                if self.hall[x] != '.':
                    break
                if x in Labyrinth.room_indexes:
                    continue
                new_hall = list(self.hall)
                new_hall[x] = top_char
                new_hall = tuple(new_hall)

                new_rooms = [list(r) for r in self.rooms]
                new_rooms[room_idx][top_index] = '.'
                new_rooms = tuple(tuple(r) for r in new_rooms)

                cost = ((top_index + 1) + (target_room - x)) * Labyrinth.energy[top_char]
                result.append((cost, Labyrinth(new_rooms, new_hall)))

            for x in range(target_room + 1, 11):
                if self.hall[x] != '.':
                    break
                if x in Labyrinth.room_indexes:
                    continue
                new_hall = list(self.hall)
                new_hall[x] = top_char
                new_hall = tuple(new_hall)

                new_rooms = [list(r) for r in self.rooms]
                new_rooms[room_idx][top_index] = '.'
                new_rooms = tuple(tuple(r) for r in new_rooms)

                cost = ((top_index + 1) + (x - target_room)) * Labyrinth.energy[top_char]
                result.append((cost, Labyrinth(new_rooms, new_hall)))

        for pos, ch in enumerate(self.hall):
            if ch == '.':
                continue

            target_room_idx = 'ABCD'.index(ch)
            target_room = Labyrinth.room_indexes[target_room_idx]
            if pos < target_room:
                path = range(pos + 1, target_room + 1)
            else:
                path = range(target_room, pos)
            if any(self.hall[p] != '.' for p in path):
                continue

            room = self.rooms[target_room_idx]
            if any(x != '.' and x != ch for x in room):
                continue

            place = -1
            for ind in range(self.depth - 1, -1, -1):
                if room[ind] == '.':
                    place = ind
                    break
            if place == -1:
                continue

            new_hall = list(self.hall)
            new_hall[pos] = '.'
            new_hall = tuple(new_hall)

            new_rooms = [list(r) for r in self.rooms]
            new_rooms[target_room_idx][place] = ch
            new_rooms = tuple(tuple(r) for r in new_rooms)

            distance = (place + 1) + abs(target_room - pos)
            cost = distance * Labyrinth.energy[ch]
            result.append((cost, Labyrinth(new_rooms, new_hall)))

        return result


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


