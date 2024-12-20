def print_matrix(matrix, n):
    for i in range(n):
        print(matrix[i])


class BoardGenerator:
    # General board parameters:
    side = None
    words_with_descriptions = None
    words_list = None
    matrix = None

    # Board quality parameters:
    current_number_of_intersections = None

    # Words location metadata:
    words_coordinates = None

    def __init__(self, side, words_with_descriptions):
        self.side = side

        self.words_with_descriptions = words_with_descriptions
        self.words_list = list(words_with_descriptions.keys())
        self.matrix = ['#' * self.side for _ in range(self.side)]

        self.current_number_of_intersections = -1

    def generate_board(self):
        self.__solve_puzzle(self.matrix, 0)

    def get_number_of_intersections(self, matrix):
        empty_places = sum([row.count('#') for row in matrix])
        empty_places_wo_intersections = self.side * self.side - sum([len(word) for word in self.words_list])
        return empty_places - empty_places_wo_intersections


    @staticmethod
    def __check_horizontal(x, y, matrix, current_word, word_coordinates):
        n = len(current_word)
        for i in range(n):
            if matrix[x][y + i] == '#' or matrix[x][y + i] == current_word[i]:
                matrix[x] = matrix[x][:y + i] + current_word[i] + matrix[x][y + i + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                return matrix
        return matrix

    @staticmethod
    def __check_vertical(x, y, matrix, current_word, word_coordinates):
        n = len(current_word)
        for i in range(n):
            if matrix[x + i][y] == '#' or matrix[x + i][y] == current_word[i]:
                matrix[x + i] = matrix[x + i][:y] + current_word[i] + matrix[x + i][y + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                return matrix
        return matrix

    def __solve_puzzle(self, matrix, index):
        words_coordinates = dict({word: None for word in self.words_list})

        if index < len(self.words_list):
            current_word = self.words_list[index]
            max_len = self.side - len(current_word)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp = self.__check_vertical(j, i, matrix.copy(), current_word, words_coordinates.copy())
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp = self.__check_horizontal(i, j, matrix.copy(), current_word, words_coordinates.copy())
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1)
        else:
            if self.get_number_of_intersections(matrix) > self.current_number_of_intersections:
                self.matrix = matrix
                self.current_number_of_intersections = self.get_number_of_intersections(matrix)


if __name__ == "__main__":
    n1 = 3
    words = {"MAM": "sfva", "PAP": "vav"}

    board_generator = BoardGenerator(n1, words)
    board_generator.generate_board()

    print_matrix(board_generator.matrix, board_generator.side)
    print(board_generator.current_number_of_intersections)
