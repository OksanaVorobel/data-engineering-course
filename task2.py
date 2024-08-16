import datetime

import numpy as np


def get_total_unique_users(array: np.array) -> int:
    users = array[:, 1].astype(int)
    return np.unique(users).size


def get_most_purchased_product(array: np.array) -> int:
    products = array[:, 2].astype(int)
    return np.bincount(products).argmax()


def convert_float_price_to_int(array: np.array) -> int:
    prices = array[:, 4]
    return prices.astype(int)


def get_columns_type(array: np.array):
    for column in array.T:
        print(column.dtype)


def extract_product_id_quantity(array: np.array) -> np.array:
    product_id_quantity = array[:, [2, 3]]
    return product_id_quantity


def transaction_counts_per_user(array: np.array) -> np.array:
    user_ids = array[:, 1]
    unique_user_ids, counts = np.unique(user_ids, return_counts=True)
    user_transaction_counts = np.array(
        list(zip(unique_user_ids, counts)),
        dtype=[('user_id', 'i4'), ('transaction_count', 'i4')]
    )

    return user_transaction_counts


def mask_zero_quantity(array: np.array) -> np.array:
    quantity_column = array[:, 3].astype(int)
    masked_array = np.ma.array(
        transactions_array, mask=np.tile(quantity_column == 0, (transactions_array.shape[1], 1)).T
    )
    return masked_array


def increase_prices(array: np.array, percentage) -> np.array:
    new_array = np.array(array, dtype=object)
    price_column = new_array[:, 4].astype(float)
    new_array[:, 4] = np.round(price_column + price_column * (percentage / 100), 4)
    return new_array


def filter_transactions_by_quantity(array: np.array, quantity: int) -> np.array:
    quantity_column = array[:, 3].astype(int)
    filtered_row = np.where(quantity_column > quantity)
    return array[filtered_row]


def get_column_revenue(array: np.array) -> np.array:
    quantities = array[:, 3].astype(float)
    prices = array[:, 4].astype(float)
    return quantities * prices


def get_total_revenue(array: np.array) -> float:
    revenues = get_column_revenue(array)
    return np.sum(revenues)


def calculate_revenue(array: np.array, start_date: datetime, end_date: datetime) -> float:
    revenues = get_column_revenue(array)
    timestamps = array[:, 5]
    mask = (timestamps >= start_date) & (timestamps <= end_date)
    return np.sum(revenues[mask])


def compare_revenue(
        array: np.array, period1: tuple[datetime, datetime], period2: tuple[datetime, datetime]
):
    start1, end1 = period1
    start2, end2 = period2

    revenue1 = calculate_revenue(array, start1, end1)
    revenue2 = calculate_revenue(array, start2, end2)

    return revenue1, revenue2


def filter_transactions_by_date_range(array: np.array, start_date, end_date):
    timestamps = array[:, 5]
    mask = (timestamps >= start_date) & (timestamps <= end_date)
    return array[mask]


def extract_transactions_by_user(array: np.array, user_id: int) -> np.array:
    user_ids = array[:, 1].astype(int)
    return transactions_array[user_ids == user_id]


def top_products_by_revenue(array: np.array, number: int):
    product_ids = array[:, 2].astype(int)
    revenues = get_column_revenue(array)

    product_revenue = {}
    for product_id, revenue in zip(product_ids, revenues):
        if product_id in product_revenue:
            product_revenue[product_id] += revenue
        else:
            product_revenue[product_id] = revenue

    top_products = sorted(product_revenue, key=product_revenue.get, reverse=True)[:number]
    return transactions_array[np.isin(product_ids, top_products)]


if __name__ == "__main__":
    transactions = [
        [1001, 1, 302, 2, 15.99, datetime.datetime(2024, 8, 5, 10, 15)],
        [1002, 2, 302, 1, 15.99, datetime.datetime(2024, 8, 5, 10, 20)],
        [1003, 3, 303, 4, 9.99, datetime.datetime(2024, 8, 5, 10, 25)],
        [1004, 4, 304, 3, 49.99, datetime.datetime(2024, 8, 5, 10, 30)],
        [1005, 1, 305, 1, 19.99, datetime.datetime(2024, 8, 5, 10, 35)],
        [1006, 1, 305, 0, 19.99, datetime.datetime(2024, 8, 5, 10, 35)],
        [1007, 2, 306, 1, 0.2, datetime.datetime(2024, 8, 5, 10, 35)],
        [1007, 2, 307, 1, 0.1, datetime.datetime(2024, 8, 5, 10, 35)],
    ]
    transactions_array = np.array(transactions, dtype=object)

    # 1. Calculate total revenue
    total_revenue = get_total_revenue(transactions_array)
    print("Total revenue:", total_revenue)
    assert total_revenue == 258.19, f"Expected 258.19 but got {total_revenue}"

    # 2. Get total unique users
    unique_users = get_total_unique_users(transactions_array)
    print("The number of unique users:", unique_users)
    assert unique_users == 4, f"Expected 4 but got {unique_users}"

    # 3. Get the most purchased product
    most_purchased_product = get_most_purchased_product(transactions_array)
    print("The most purchased product:", most_purchased_product)
    assert most_purchased_product == 302, f"Expected 302 but got {most_purchased_product}"

    # 4. Convert float prices to int
    int_prices = convert_float_price_to_int(transactions_array)
    print("Prices as integers:", int_prices)
    assert np.array_equal(
        int_prices, [15, 15, 9, 49, 19, 19, 0, 0]
    ), f"Expected [15, 15, 9, 49, 19, 19, 0, 0] but got {int_prices}"

    # 5. Get column types
    print("Column types:")
    get_columns_type(transactions_array)

    # 6. Extract product ID and quantity
    product_id_quantity = extract_product_id_quantity(transactions_array)
    print("Product ID and Quantity:\n", product_id_quantity)
    assert np.array_equal(product_id_quantity, transactions_array[:, [2, 3]])

    # 7. Transaction counts per user
    transaction_counts = transaction_counts_per_user(transactions_array)
    print("Transaction counts per user:\n", transaction_counts)
    expected_transaction_counts = np.array(
        [(1, 3), (2, 3), (3, 1), (4, 1)],
        dtype=[('user_id', 'i4'), ('transaction_count', 'i4')]
    )
    assert np.array_equal(
        transaction_counts, expected_transaction_counts
    ), f"Expected {expected_transaction_counts} but got {transaction_counts}"

    # 8. Mask zero quantity
    masked_array = mask_zero_quantity(transactions_array)
    print("Masked array where quantity is zero:\n", masked_array)

    # 9. Increase prices by a percentage
    increased_prices_array = increase_prices(transactions_array, 5)
    print("Array with increased prices by 5%:\n", increased_prices_array)
    expected_prices = np.array(
        [16.7895, 16.7895, 10.4895, 52.4895, 20.9895, 20.9895, 0.21, 0.105],
        dtype=object
    )
    assert np.array_equal(
        increased_prices_array[:, 4], expected_prices
    ), f"Expected {expected_prices} but got {increased_prices_array[:, 4]}"

    # 10. Filter transactions by quantity greater than a given value
    filtered_transactions = filter_transactions_by_quantity(transactions_array, 1)
    print("Transactions with quantity greater than 1:\n", filtered_transactions)
    assert filtered_transactions.shape[0] == 3,\
        f"Expected 3 transactions but got {filtered_transactions.shape[0]}"

    # 11. Compare the revenue from two different time periods
    period1 = (
        datetime.datetime(2024, 8, 5, 10, 00),
        datetime.datetime(2024, 8, 5, 10, 26)
    )
    period2 = (
        datetime.datetime(2024, 8, 5, 10, 00),
        datetime.datetime(2024, 8, 5, 10, 16)
    )
    revenue_period1, revenue_period2 = compare_revenue(transactions_array, period1, period2)
    print("Revenue for Period 1:", revenue_period1)
    print("Revenue for Period 2:", revenue_period2)
    assert revenue_period1 == 87.93, f"Expected 87.93 but got {revenue_period1}"
    assert revenue_period2 == 31.98, f"Expected 31.98 but got {revenue_period2}"

    # 12. Extract transactions by user
    user_transactions = extract_transactions_by_user(transactions_array, 1)
    print("Transactions for user 1:\n", user_transactions)
    assert user_transactions.shape[0] == 3, f"Expected 3 transactions but got {user_transactions.shape[0]}"

    # 13. Filter transactions by date range
    filtered_by_date = filter_transactions_by_date_range(
        transactions_array,
        datetime.datetime(2024, 8, 5, 10, 20),
        datetime.datetime(2024, 8, 5, 10, 30)
    )
    print("Transactions filtered by date range:\n", filtered_by_date)
    assert filtered_by_date.shape[0] == 3, f"Expected 3 transactions but got {filtered_by_date.shape[0]}"

    # 14. Top 5 products by revenue
    top_5_products = top_products_by_revenue(transactions_array, number=5)
    print("Top 5 products by revenue:\n", top_5_products)
    assert top_5_products.shape[0] == 7, f"Expected 7 transactions but got {top_5_products.shape[0]}"
