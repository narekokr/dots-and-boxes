from helper import get_opposite_direction


class ChainCounter:
    hashes = {}
    time_taken = 0
    times = 0

    def __init__(self, state):
        self.state = state

    def get_adjacent_lines(self, box):  # starting from top line and going clockwise
        if not box:
            return None, None, None, None

        vertical_1 = self.state.v_line_owners[box] if box in self.state.v_line_owners else None
        coords = (box[0] + 1, box[1])
        vertical_2 = self.state.v_line_owners[coords] if coords in self.state.v_line_owners else None

        horizontal_1 = self.state.h_line_owners[box] if box in self.state.h_line_owners else None
        coords = (box[0], box[1] + 1)
        horizontal_2 = self.state.h_line_owners[coords] if coords in self.state.h_line_owners else None

        return horizontal_1, vertical_2, horizontal_2, vertical_1

    def get_double_lined_boxes(self):
        boxes = []
        for box in self.state.game.boxes:
            if sum(bool(i) for i in self.get_adjacent_lines(box)) == 2:
                boxes.append(box)

        return boxes

    def get_adjacent_boxes(self, box):  # starting from top box and going clockwise
        boxes = [(box[0], box[1] - 1) if box[1] != 0 else None,
                 (box[0] + 1, box[1]) if box[0] != self.state.game.width - 1 else None,
                 (box[0], box[1] + 1) if box[1] != self.state.game.height - 1 else None,
                 (box[0] - 1, box[1]) if box[0] != 0 else None]

        return boxes

    def categorise(self, box, adjacent_lines):
        if adjacent_lines[1] and adjacent_lines[3]:
            return 1
        if adjacent_lines[0] and adjacent_lines[2]:
            return 2
        if adjacent_lines[0] and adjacent_lines[1]:
            return 3
        if adjacent_lines[1] and adjacent_lines[2]:
            return 4
        if adjacent_lines[2] and adjacent_lines[3]:
            return 5
        if adjacent_lines[0] and adjacent_lines[3]:
            return 6

    def count_chains(self):
        current_hash = self.state.hash_lines()

        if current_hash in ChainCounter.hashes:  # if the chain count has already been computed, then return it
            return ChainCounter.hashes[current_hash]

        double_lined_boxes = self.get_double_lined_boxes()
        chains = []
        visited = []
        for box in double_lined_boxes:
            current_chain = []
            started_chain = False
            if box in visited:
                continue
            adjacent_lines = self.get_adjacent_lines(box)
            category = self.categorise(box, adjacent_lines)
            for direction, allowed_categories in categories[category].items():
                current = box
                direction = get_opposite_direction(direction)
                while True:
                    adjacent_lines = self.get_adjacent_lines(current)
                    category = self.categorise(current, adjacent_lines)
                    current_directions = categories[category]
                    neighbors = self.get_adjacent_boxes(current)

                    opposite_direction = get_opposite_direction(direction)
                    direction_to_go = [i for i in current_directions.keys() if i != opposite_direction][0]
                    neighbor = neighbors[direction_to_go]
                    if neighbor in visited:
                        break

                    adjacent_lines = self.get_adjacent_lines(neighbor)
                    category = self.categorise(neighbor, adjacent_lines)
                    allowed_categories = current_directions[direction_to_go]

                    if not neighbor or neighbor not in double_lined_boxes or category not in allowed_categories:
                        break

                    current_chain.append(neighbor)
                    visited.append(neighbor)
                    direction = direction_to_go
                    if not started_chain:
                        current_chain.append(current)
                        visited.append(box)
                        started_chain = True
                    current = neighbor

            if len(current_chain) > 2:
                chains.append(current_chain)

        mirrors = self.state.mirror()
        for state_mirror in mirrors + (self.state,):  # adding the hashes for the current state and its mirrors
            state_hash = state_mirror.hash_lines()
            ChainCounter.hashes[state_hash] = len(chains)
        return len(chains)


categories = {  # each direction and allowed neighbor categories
    1: {
        0: [1, 3, 6],
        2: [1, 4, 5]
    },
    2: {
        1: [2, 3, 4],
        3: [2, 5, 6]
    },
    3: {
        2: [1, 4, 5],
        3: [2, 5, 6]
    },
    4: {
        0: [1, 3, 5],
        3: [2, 5, 6]
    },
    5: {
        0: [1, 3, 6],
        1: [2, 3, 4]
    },
    6: {
        1: [2, 3, 4],
        2: [1, 4, 5]
    }
}
