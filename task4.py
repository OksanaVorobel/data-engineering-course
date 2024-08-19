import abc
from enum import Enum
from typing import Optional, Type, Union

import numpy as np


class FileFormat(Enum):
    TXT = "txt"
    CSV = "csv"
    NPY = "npy"
    NPZ = "npz"


class BaseFileOperation(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def save(cls, array: np.array, file_name: str) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def load(cls, file_name: str) -> np.array:
        pass


class TextFileOperation(BaseFileOperation):
    file_format = FileFormat.TXT

    @classmethod
    def save(cls, array: np.array, file_name: str) -> None:
        np.savetxt(f"{file_name}.{cls.file_format.value}", array, fmt="%d")

    @classmethod
    def load(cls, file_name: str) -> np.array:
        return np.loadtxt(file_name)


class CSVFileOperation(BaseFileOperation):
    file_format = FileFormat.CSV

    @classmethod
    def save(cls, array: np.array, file_name: str) -> None:
        np.savetxt(f"{file_name}.{cls.file_format.value}", array, delimiter=",", fmt="%d")

    @classmethod
    def load(cls, file_name: str) -> np.array:
        return np.loadtxt(file_name, delimiter=',')


class NPYFileOperation(BaseFileOperation):
    file_format = FileFormat.NPY

    @classmethod
    def save(cls, array: np.array, file_name: str) -> None:
        np.save(f"{file_name}.{cls.file_format.value}", array)

    @classmethod
    def load(cls, file_name: str) -> np.array:
        return np.load(file_name)


class NPZFileOperation(BaseFileOperation):
    file_format = FileFormat.NPZ

    @classmethod
    def save(cls, array: np.array, file_name: str) -> None:
        np.savez(f"{file_name}.{cls.file_format.value}", array)

    @classmethod
    def load(cls, file_name: str) -> np.array:
        return np.load(file_name)


def save_array(array: np.array, file_name: str, file_operation: Type[BaseFileOperation]) -> None:
    file_operation.save(array, file_name)


def load_array(file_name: str, file_operation: Type[BaseFileOperation]) -> np.array:
    return file_operation.load(file_name)


def split_array(array: np.array, num_splits: int, axis: int = 0) -> np.array:
    return np.array_split(array, num_splits, axis=axis)


def sum_array_elements(array: np.array, axis: Optional[int] = None) -> int:
    return np.sum(array, axis=axis) if axis else np.sum(array)


def mean_array_elements(array: np.array, axis: Optional[int] = None) -> Union[int, float]:
    return np.mean(array, axis=axis) if axis else np.mean(array)


def median_array_elements(array: np.array, axis: Optional[int] = None) -> float:
    return np.median(array, axis=axis) if axis else np.median(array)


def standard_deviation_array_elements(array: np.array, axis: Optional[int] = None) -> float:
    return np.std(array, axis=axis) if axis else np.std(array)


def print_array(array: np.array, message: str = ""):
    print(message, array, sep="\n")


if __name__ == "__main__":
    matrix = np.random.randint(0, 100, size=(10, 10))
    print_array(matrix, "Original matrix:")

    print("\nSaving matrix to txt, csv, npy, npz files...")
    save_array(matrix, "matrix", TextFileOperation)
    save_array(matrix, "matrix", CSVFileOperation)
    save_array(matrix, "matrix", NPYFileOperation)
    save_array(matrix, "matrix", NPZFileOperation)

    print("\nReading matrix from txt, csv, npy, npz files...")
    matrix_txt = load_array("matrix.txt", TextFileOperation)
    matrix_csv = load_array("matrix.csv", CSVFileOperation)
    matrix_npy = load_array("matrix.npy", NPYFileOperation)
    matrix_npz = load_array("matrix.npz", NPZFileOperation)["arr_0"]
    print(matrix_npz)

    assert np.array_equal(matrix, matrix_txt), "Matrix loaded from TXT file does not match the original matrix"
    assert np.array_equal(matrix, matrix_csv), "Matrix loaded from CSV file does not match the original matrix"
    assert np.array_equal(matrix, matrix_npy), "Matrix loaded from NPY file does not match the original matrix"
    assert np.array_equal(matrix, matrix_npz), "Matrix loaded from NPZ file does not match the original matrix"

    total_sum = sum_array_elements(matrix)
    print("\nSum of all elements in the array:", total_sum)

    mean = mean_array_elements(matrix)
    print("\nMean of the array:", mean)

    median = median_array_elements(matrix)
    print("\nMedian of the array:", median)

    std = standard_deviation_array_elements(matrix)
    print("\nStandard deviation of the array:", median)
