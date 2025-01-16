import json


class Board:
    # General board parameters:
    side = None
    words_with_descriptions = None
    matrix = None
    matrix_current_fill = None
    matrix_words_coordinates = None

    # Board quality parameters:
    current_number_of_intersections = None
    samples_covered = None

    # Words location metadata:
    words_coordinates = None

    def __init__(self, board_filepath):
        with open(board_filepath, 'r') as f:
            board_data = json.load(f)

        self.side = board_data['board_size']
        self.words_with_descriptions = board_data['words_with_descriptions']
        self.words_coordinates = board_data['words_coordinates']

        for i, word in enumerate(self.words_coordinates.keys()):
            self.words_coordinates[word].append(i + 1)

        self.matrix = [list(row) for row in board_data['board'].split('\n')]
        self.matrix_current_fill = [['#'] * self.side for _ in range(self.side)]

    def is_complete(self):
        for i in range(self.side):
            for j in range(self.side):
                if self.matrix[i][j] != self.matrix_current_fill[i][j]:
                    return False
        return True

    def get_words_description_text(self):
        board_assignment_text = ""

        for word_with_coordinates in self.words_coordinates.items():
            word = word_with_coordinates[0]
            coordinates = word_with_coordinates[1]

            index = coordinates[3]

            board_assignment_text += f"""
            {index} ({coordinates[2]}). {self.words_with_descriptions[word]} 
            """

        return board_assignment_text

    def get_task_number(self, x, y):
        for coordinates in self.words_coordinates.values():
            if coordinates[0] == x and coordinates[1] == y:
                return coordinates[3]

        return None
