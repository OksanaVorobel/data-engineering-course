from enum import Enum
from typing import Optional

import pandas as pd


class CategorizePrice(Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"


class CategorizeLengthOfStay(Enum):
    SHORT: str = "short-term"
    MEDIUM: str = "medium-term"
    LONG: str = "long-term"


def categorize_price(price: int) -> str:
    if price < 100:
        return CategorizePrice.LOW.value
    elif 100 <= price < 300:
        return CategorizePrice.MEDIUM.value
    else:
        return CategorizePrice.HIGH.value


def categorize_length_of_stay(minimum_nights: int) -> str:
    if minimum_nights <= 3:
        return CategorizeLengthOfStay.SHORT.value
    elif 4 <= minimum_nights <= 14:
        return CategorizeLengthOfStay.MEDIUM.value
    else:
        return CategorizeLengthOfStay.LONG.value


def print_dataframe_info(df: pd.DataFrame, message: Optional[str] = None) -> None:
    if message:
        print(message)

    print("\nDataFrame Information:")
    print(f"Number of entries: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDataFrame Summary:")
    df.info()


if __name__ == "__main__":
    df = pd.read_csv("NYC-Airbnb-2023.csv")

    df.head()
    print_dataframe_info(df, "Airbnb NYC Dataset Info:")

    null_values_per_column = df.isnull().sum()
    columns_with_null = df.columns[null_values_per_column > 0]
    print("\nColumns with missing values:", columns_with_null.to_list())

    df.fillna({"name": "Unknown", "host_name": "Unknown", "last_review": pd.NaT}, inplace=True)

    df["price_category"] = df["price"].apply(categorize_price)
    df["length_of_stay_category"] = df["minimum_nights"].apply(categorize_length_of_stay)

    print_dataframe_info(df, "\nDataFrame after transformations:")

    missing_critical_columns = df[["name", "host_name"]].isnull().sum()
    assert missing_critical_columns.sum() == 0, "There are missing values in critical columns"

    df = df[df["price"] > 0]
    assert df["price"].min() > 0, "There are rows with price less than or equal to 0"

    print_dataframe_info(df, "Final DataFrame Info:")

    df.to_csv("cleaned_airbnb_data.csv", index=False, header=True)
