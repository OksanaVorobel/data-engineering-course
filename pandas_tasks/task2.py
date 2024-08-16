from typing import Optional

import pandas as pd


def print_grouped_data(grouped_df: pd.DataFrame, message: Optional[str] = None) -> None:
    if message:
        print(message)
    print(grouped_df)


if __name__ == "__main__":
    df = pd.read_csv("cleaned_airbnb_data.csv")
    print_grouped_data(df, "Cleaned Airbnb NYC Dataset Info:")

    selected_iloc = df.iloc[:5, :3]
    print("\nSelected Rows and Columns using .iloc:\n", selected_iloc)

    selected_loc = df.loc[0:4, ["price_category", "price"]]
    print("\nSelected Rows and Columns using .loc:\n", selected_loc)

    filtered_df = df.loc[df["neighbourhood_group"].isin(["Manhattan", "Brooklyn"])]

    filtered_df = filtered_df[(filtered_df["price"] > 100) & (filtered_df["number_of_reviews"] > 10)]

    columns_of_interest = [
        "neighbourhood_group", "price", "minimum_nights",
        "number_of_reviews", "price_category", "availability_365"
    ]
    filtered_df = filtered_df[columns_of_interest]
    print_grouped_data(filtered_df.head(10), "\nFiltered Data:")

    grouped_stats = filtered_df.groupby(["neighbourhood_group", "price_category"]).agg({
        "price": "mean",
        "minimum_nights": "mean",
        "number_of_reviews": "mean",
        "availability_365": "mean",
    }).reset_index()
    grouped_stats = grouped_stats.rename(columns={
        "price": "average_price",
        "minimum_nights": "average_minimum_nights",
        "number_of_reviews": "average_number_of_reviews",
        "availability_365": "average_availability_365"
    })
    print_grouped_data(grouped_stats, "\nGrouped and Aggregated Data:")

    filtered_df.sort_values(["price", "number_of_reviews"], ascending=[False, True])

    neighbourhood_stats = df.groupby("neighbourhood_group").agg({
        "id": "count",
        "price": "mean"
    }).rename(columns={"id": "total_listings", "price": "average_price"})

    neighbourhood_stats["listings_rank"] = neighbourhood_stats["total_listings"].rank(ascending=False)
    neighbourhood_stats["price_rank"] = neighbourhood_stats["average_price"].rank(ascending=False)
    print_grouped_data(
        neighbourhood_stats,
        "\nRanking of Neighborhoods by Total Listings and Average Price:"
    )

    grouped_stats.to_csv("aggregated_airbnb_data.csv", index=False, header=True)
