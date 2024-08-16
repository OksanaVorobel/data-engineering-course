import numpy as np


def add(array: np.array, number: int) -> np.array:
    return array + number


def multiply(array: np.array, number: int) -> np.array:
    return array * number


def print_array(array: np.array, message: str = ""):
    print(message, array, sep="\n")


if __name__ == "__main__":
    one_dimensional_array = np.arange(1, 11)
    two_dimensional_array = np.arange(1, 10).reshape(3, 3)

    third_element = one_dimensional_array[2]
    print("Third element of the one-dimensional array:", third_element)

    slices = two_dimensional_array[:2, :2]
    print("First two rows and columns of the two-dimensional array:", slices)

    sum_array = add(one_dimensional_array, 5)
    print_array(sum_array, "Array after adding 5 to each element")

    mult_array = multiply(two_dimensional_array, 2)
    print_array(mult_array, "Array after multiplying 2 to each element")
