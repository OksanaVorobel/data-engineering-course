from typing import Optional

import numpy as np


def split_array(array: np.array, num_splits: int, axis: int = 0) -> np.array:
    return np.array_split(array, num_splits, axis=axis)


def combine_arrays(arrays: list[np.array], axis: int = 0) -> np.array:
    return np.concatenate(arrays, axis=axis)


def print_array(array: np.array, message: str = ""):
    print(message, array, sep="\n")


if __name__ == "__main__":
    matrix = np.random.randint(0, 100, size=(6, 6))
    print_array(matrix, "Original matrix:")

    transposed_matrix = np.transpose(matrix)
    print_array(transposed_matrix, "\nTransposed matrix:")

    reshaped_matrix = np.reshape(matrix, (3, 12))
    print_array(reshaped_matrix, "\nReshaped matrix (3x12):")

    sub_arrays_axis_1 = split_array(matrix, 3, axis=1)
    assert len(sub_arrays_axis_1) == 3, "Expected 3 sub-arrays after splitting"
    assert all(arr.shape == (6, 2) for arr in sub_arrays_axis_1), "Each sub-array should have shape (6, 2)"

    print("\nSub-arrays split along axis 1:")
    for i, sub_array in enumerate(sub_arrays_axis_1):
        print_array(sub_array, f"Sub-array {i + 1}:")

    array1 = np.random.randint(0, 5, size=(3, 3))
    array2 = np.random.randint(5, 10, size=(3, 3))
    array3 = np.random.randint(10, 15, size=(3, 3))
    print_array(array1, "\nArray 1:")
    print_array(array2, "Array 2:")
    print_array(array3, "Array 3:")

    combined_array_concat = combine_arrays([array1, array2, array3], axis=1)
    expected_shape = (3, 9)
    assert combined_array_concat.shape == expected_shape,\
        f"Expected combined array shape {expected_shape}, but got {combined_array_concat.shape}"
    print_array(combined_array_concat, "\nCombined array by concatenating along axis 1:")
