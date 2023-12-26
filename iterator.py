import os
import csv


class Iterator:
    def __init__(self, class_name, path_file_name):
        self.path_file_name = path_file_name
        self.counter = 0
        self.class_name = class_name
        data = []
        with open(path_file_name, 'r') as f:
            for line in f.readlines():
                if line.rstrip('\n').split(',')[2] == class_name:
                    image_path = line.rstrip('\n').split(',')[1]
                    data.append(image_path)
        self.data = data
        self.limit = len(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.limit:
            next_path = self.data[self.counter]
            self.counter += 1
            return next_path
        else:
            return None


if __name__ == "__main__":
    roses = Iterator('rose', 'paths.csv')
    tulips = Iterator('tulip', 'paths.csv')

    print(next(roses))
    print(next(roses))
    print(next(roses))
    print(next(tulips))
    print(next(tulips))
    print(next(tulips))
