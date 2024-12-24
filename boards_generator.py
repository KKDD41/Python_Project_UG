import pandas as pd
import multiprocessing
import signal
import json
from contextlib import contextmanager


def load_words(file_name: str):
    words_dataset = pd.read_csv(file_name, sep=';')
    return words_dataset


def get_subset(words_dataset: pd.DataFrame, number_of_words: int):
    subset_of_words = words_dataset.sample(number_of_words)
    return {row['Word']: row['Description'] for _, row in subset_of_words.iterrows()}


class BoardGenerator:
    # General board parameters:
    side = None
    words_with_descriptions = None
    words_list = None
    matrix = None

    # Board quality parameters:
    current_number_of_intersections = None
    samples_covered = None

    # Words location metadata:
    words_coordinates = None

    def __init__(self, side, words_with_descriptions):
        self.side = side

        self.words_with_descriptions = words_with_descriptions
        self.words_list = list(words_with_descriptions.keys())
        self.matrix = [['#'] * self.side for _ in range(self.side)]

        # Adjust stoppers inside matrix:
        for i in range(0, self.side, 2):
            for j in range(0, self.side, 2):
                self.matrix[i][j] = '*'
        self.matrix = list(map(lambda x: ''.join(x), self.matrix))

        self.current_number_of_intersections = -1
        self.samples_covered = 0

        self.words_coordinates = dict({word: None for word in self.words_list})

    def generate_board(self):
        self.__solve_puzzle(self.matrix, 0, self.words_coordinates)

    def save_board_to_file(self, filepath):
        board = '\n'.join([row.replace('*', '#') for row in self.matrix])

        board_data = {
            'board_size': self.side,
            'board': board,
            'number_of_intersections': self.current_number_of_intersections,
            'words_with_descriptions': self.words_with_descriptions,
            'words_coordinates': self.words_coordinates
        }

        with open(filepath, 'w') as file:
            json.dump(board_data, file)

    def get_number_of_intersections(self, matrix):
        number_of_letters_total = sum([len(word) for word in self.words_list])

        number_of_stoppers = sum([row.count("*") for row in matrix])
        empty_places = sum([row.count('#') for row in matrix])
        number_of_letters_on_board = self.side * self.side - number_of_stoppers - empty_places

        return number_of_letters_total - number_of_letters_on_board

    @staticmethod
    def __check_horizontal(x, y, matrix, current_word, word_coordinates):
        n = len(current_word)
        word_coordinates[current_word] = (x, y, 'horizontal')

        for i in range(n):
            if matrix[x][y + i] == '#' or matrix[x][y + i] == current_word[i]:
                matrix[x] = matrix[x][:y + i] + current_word[i] + matrix[x][y + i + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                word_coordinates[current_word] = None
                return matrix, word_coordinates
        return matrix, word_coordinates

    @staticmethod
    def __check_vertical(x, y, matrix, current_word, word_coordinates):
        n = len(current_word)
        word_coordinates[current_word] = (x, y, 'vertical')

        for i in range(n):
            if matrix[x + i][y] == '#' or matrix[x + i][y] == current_word[i]:
                matrix[x + i] = matrix[x + i][:y] + current_word[i] + matrix[x + i][y + 1:]
            else:
                matrix[0] = '@' + matrix[0][1:]
                word_coordinates[current_word] = None
                return matrix, word_coordinates
        return matrix, word_coordinates

    def __solve_puzzle(self, matrix, index, words_coordinates):
        if self.samples_covered >= 1000 or self.current_number_of_intersections >= 6:
            return

        if index < len(self.words_list):
            current_word = self.words_list[index]
            max_len = self.side - len(current_word)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp, temp_word_coordinates = self.__check_vertical(
                        j,
                        i,
                        matrix.copy(),
                        current_word,
                        words_coordinates.copy()
                    )
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1, temp_word_coordinates)

            for i in range(self.side):
                for j in range(max_len + 1):
                    temp, temp_word_coordinates = self.__check_horizontal(
                        i,
                        j,
                        matrix.copy(),
                        current_word,
                        words_coordinates.copy()
                    )
                    if temp[0][0] != '@':
                        self.__solve_puzzle(temp, index + 1, temp_word_coordinates)
        else:
            self.samples_covered += 1

            if self.get_number_of_intersections(matrix) > self.current_number_of_intersections:
                self.matrix = matrix
                self.current_number_of_intersections = self.get_number_of_intersections(matrix)
                self.words_coordinates = words_coordinates


def generate_boards(theme, sample_size, board_size, sample_index):
    words_dataset = load_words(f"./words_dataset/{theme}/{theme}_dataset.csv")
    boards_folder = f"./boards/{theme}/"

    words_subset = get_subset(words_dataset, sample_size)
    board_generator = BoardGenerator(board_size, words_subset)

    board_generator.generate_board()
    print(board_generator.matrix)

    if board_generator.current_number_of_intersections >= 5:
        board_generator.save_board_to_file(
            boards_folder + f"sample_{sample_index}.json"
        )

        print(f"Board was saved as sample_{sample_index}.json")


if __name__ == "__main__":
    run_number = 1

    theme = "animals"
    sample_size = 10
    board_size = 8
    num_processes = 10  # Number of processes to run concurrently

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Start multiple processes
    for sample_index in range(num_processes):
        pool.apply_async(generate_boards, args=(theme, sample_size, board_size, str(sample_index + run_number)))

    # Close the pool and wait for the processes to finish
    pool.close()
    pool.join()
