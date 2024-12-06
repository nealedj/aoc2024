import copy


class GameState:
    directions = (
        "up",
        "right",
        "down",
        "left",
    )
    guard_chars = {
        "up": "^",
        "right": ">",
        "down": "v",
        "left": "<",
    }

    def __init__(self, matrix: list[list], guard_coords: tuple[int, int]):
        self.matrix = matrix
        self.x_len = len(matrix)
        self.y_len = len(matrix[0])
        self.guard_coords = guard_coords
        self.current_coords = guard_coords
        self.visited_coords = {guard_coords}
        self.visited_coords_with_direction = {guard_coords: "up"}
        self.direction = "up"
        self.steps = 0

    def run_until_exit(self):
        while True:
            reason = self.step()
            if reason:
                return reason

    def is_revisiting(self, coords):
        visited_at_direction = self.visited_coords_with_direction.get(coords)
        return visited_at_direction and visited_at_direction == self.direction

    def step(self) -> str:
        if self.direction == "up":
            new_coords = (
                self.current_coords[0] - 1,
                self.current_coords[1],
            )
        elif self.direction == "down":
            new_coords = (
                self.current_coords[0] + 1,
                self.current_coords[1],
            )
        elif self.direction == "left":
            new_coords = (
                self.current_coords[0],
                self.current_coords[1] - 1,
            )
        elif self.direction == "right":
            new_coords = (
                self.current_coords[0],
                self.current_coords[1] + 1,
            )
        else:
            raise ValueError("Invalid direction: {}".format(self.direction))

        if self.will_leave_map(new_coords):
            return "exit"
        elif self.is_revisiting(new_coords):
            return "revisit"
        elif self.will_hit_obstacle(new_coords):
            self.turn_right()
            self.step()
        else:
            self.current_coords = new_coords
            self.visited_coords.add(new_coords)
            self.visited_coords_with_direction[new_coords] = self.direction
            self.steps += 1

        return ""

    def will_hit_obstacle(self, coords):
        x, y = coords
        return self.matrix[x][y] == "#"

    def will_leave_map(self, coords):
        x, y = coords

        return x < 0 or x >= self.x_len or y < 0 or y >= self.y_len

    def turn_right(self):
        idx = self.directions.index(self.direction)
        self.direction = self.directions[
            idx + 1 if idx < len(self.directions) - 1 else 0
        ]

    def render_matrix(self):
        for xi, row in enumerate(self.matrix):
            for yi, cell in enumerate(row):
                if (xi, yi) == self.current_coords:
                    guard_char = self.guard_chars[self.direction]
                    print(guard_char, end="")
                elif (xi, yi) in self.visited_coords:
                    print("X", end="")
                else:
                    print(cell, end="")
            print()


def part1():
    game = GameState(*read_matrix(read_raw()))

    game.run_until_exit()
    game.render_matrix()

    print("Count of visited coords:", len(game.visited_coords))


def part2():
    initial_matrix, guard_coords = read_matrix(read_raw())
    game = GameState(initial_matrix, guard_coords)

    obstable_placements = {}
    for xi, row in enumerate(game.matrix):
        for yi, cell in enumerate(row):
            if (
                xi,
                yi,
            ) == (6, 3):
                print("stop")
            if cell in (
                ".",
                "^",
            ):
                matrix = copy.deepcopy(initial_matrix)
                matrix[xi][yi] = "#"
                game = GameState(matrix, guard_coords)

                reason = game.run_until_exit()

                if reason == "revisit":
                    obstable_placements[(xi, yi)] = game.steps
                    print("Obstacle at", (xi, yi), "steps:", game.steps)

    print('Potential obstacles:', len(obstable_placements))
    print(
        "Obstacle with min steps:", min(obstable_placements.items(), key=lambda x: x[1])
    )


def read_matrix(raw_data: list) -> tuple[list, tuple[int, int]]:
    guard_coords = None
    matrix = []
    for xi, line in enumerate(raw_data):
        row = []
        for yi, c in enumerate(line):
            row.append(c)

            if c == "^":
                guard_coords = (
                    xi,
                    yi,
                )

        matrix.append(row)

    return matrix, guard_coords


def read_raw() -> list:
    with open("./inputs/day6") as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    # part1()
    part2()
