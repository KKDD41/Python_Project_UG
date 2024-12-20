def print_matrix(matrix, n):
    for i in range(n):
        print(matrix[i])


class BoardGenerator:
    side = None
    words_with_descriptions = None
    matrix = None

    def __init__(self, side, words_with_descriptions):
        self.side = side
        self.words_with_descriptions = words_with_descriptions
        self.matrix = ['#' * self.side for _ in range(self.side)]

    def generate_board(self):
        self.__solve_puzzle(self.matrix, 0)

    def __check_horizontal(self, x, y, matrix, current_word):
        n = len(current_word)
        for i in range(n):
            if matrix[x][y + i] == '#' or matrix[x][y + i] == current_word[i]:
                matrix[x] = matrix[x][:y + i] + current_word[i] + matrix[x][y + i + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                return matrix
        return matrix

    def __check_vertical(self, x, y, matrix, current_word):
        n = len(current_word)
        for i in range(n):
            if matrix[x + i][y] == '#' or matrix[x + i][y] == current_word[i]:
                matrix[x + i] = matrix[x + i][:y] + current_word[i] + matrix[x + i][y + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                return matrix
        return matrix

    def __solve_puzzle(self, matrix, index):
        ways = [0]

        if index < len(self.words_with_descriptions):
            current_word = self.words_with_descriptions[index]
            max_len = self.side - len(current_word)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp = self.__check_vertical(j, i, matrix.copy(), current_word)
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp = self.__check_horizontal(i, j, matrix.copy(), current_word)
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1)
        else:
            ways[0] += 1
            print(f"{ways[0]} way to solve the puzzle")
            print_matrix(matrix, self.side)
            print()



def main():
    n1 = 3
    words = ["MAM", "PAP"]

    board_generator = BoardGenerator(n1, words)
    board_generator.generate_board()


if __name__ == "__main__":
    main()
