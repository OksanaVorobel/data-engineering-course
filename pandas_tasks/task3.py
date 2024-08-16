from typing import Union, Optional

import pandas as pd


def classify_availability(availability: int) -> str:
    if availability < 50:
        return "Rarely Available"
    elif 50 <= availability <= 200:
        return "Occasionally Available"
    else:
        return "Highly Available"


def print_analysis_results(
        analysis_results: Union[pd.DataFrame, pd.Series], message: Optional[str] = None
) -> None:
    if message:
        print(message)
    print(analysis_results)
    print("\n")


if __name__ == "__main__":
    df = pd.read_csv("cleaned_airbnb_data.csv")
    print_analysis_results(df, "Cleaned Airbnb NYC Dataset Info:")

    table = pd.pivot_table(
        df, index=["neighbourhood_group"], columns="room_type", values="price", aggfunc="mean"
    )
    print_analysis_results(table, "\nPricing Trends Across Neighborhoods and Room Types:")

    melted_df = df.melt(
        id_vars=["id", "name", "neighbourhood_group", "room_type"],
        value_vars=["price", "minimum_nights"],
        var_name="metric",
        value_name="value"
    )
    print_analysis_results(melted_df, "\nMelted DataFrame (Long Format):")

    df["availability_status"] = df["availability_365"].apply(classify_availability)
    print_analysis_results(df, "\nData with availability_status:")

    correlation_data = df[["price", "number_of_reviews"]].copy()
    correlation_data.loc[:, "availability_status_code"] = df["availability_status"].astype("category").cat.codes
    correlation_data.loc[:, "neighbourhood_group_code"] = df["neighbourhood_group"].astype("category").cat.codes
    corr_matrix = correlation_data.corr()
    print("\nCorrelation matrix :", corr_matrix)

    print_analysis_results(df.describe(), "\nDescriptive Statistics:")
    median_stats = df[["price", "minimum_nights", "number_of_reviews"]].agg(["median"])
    print_analysis_results(median_stats, "Median Values:")

    df["last_review"] = pd.to_datetime(df["last_review"])
    df.set_index("last_review", inplace=True)
    print_analysis_results(df.head(), "\nTime Data Converted and Indexed:")

    monthly_trends = df.resample("ME").agg({"price": "mean", "number_of_reviews": "sum"})
    print_analysis_results(monthly_trends.head(), "\nMonthly Trends:")

    monthly_averages = (
        df[["price", "minimum_nights", "number_of_reviews"]]
        .groupby(df.index.month)
        .agg(["mean"])
        .sort_values(["last_review"])
    )
    print_analysis_results(monthly_averages.head(), "\nMonthly Averages:")

    monthly_averages.to_csv("time_series_airbnb_data.csv", index=False)
