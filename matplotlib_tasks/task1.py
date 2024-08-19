import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=['number_of_reviews', 'last_review', 'neighbourhood_group'])

    data['last_review'] = pd.to_datetime(data['last_review'])
    data['neighbourhood_group'] = data['neighbourhood_group'].astype('category')
    data['room_type'] = data['room_type'].astype('category')

    return data


def neighbourhood_group_distribution(df: pd.DataFrame):
    grouped_count = df['neighbourhood_group'].value_counts()
    plt.bar(
        grouped_count.index, grouped_count.values, color=plt.cm.Set3(np.arange(grouped_count.size))
    )
    plt.title('Neighborhood Distribution of Listings')
    plt.xlabel('Neighborhood')
    plt.ylabel('Number of Listings')
    for i, value in enumerate(grouped_count.values):
        plt.text(grouped_count.index[i], value, str(value), ha='center', va='bottom')

    plt.show()

    plt.savefig('./media/neighbourhood_group_distribution.png')


def price_distribution_neighbourhood_group(df: pd.DataFrame):
    neighbourhood_groups = data_frame['neighbourhood_group'].cat.categories
    price_data = [df[df['neighbourhood_group'] == group]['price'] for group in neighbourhood_groups]

    box = plt.boxplot(price_data, patch_artist=True, showfliers=True)
    plt.title('Price Distribution Across Neighbourhood Groups in NYC')
    plt.xlabel('Neighbourhood Group')
    plt.ylabel('Price')
    plt.xticks(ticks=range(1, len(neighbourhood_groups) + 1), labels=neighbourhood_groups)
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightpink', 'lightyellow']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

    plt.savefig('./media/price_distribution_neighbourhood_group.png')


def availability_room_type_neighbourhood_group(df: pd.DataFrame):
    pivot_table = pd.pivot_table(
        df,
        values="availability_365",
        index="neighbourhood_group",
        columns="room_type",
        aggfunc=['mean', 'std']
    )
    means = pivot_table['mean']
    stds = pivot_table['std']
    neighbourhood_groups = means.index
    room_types = means.columns

    fig, ax = plt.subplots(figsize=(14, 8))

    bar_width = 0.2
    bar_positions = np.arange(len(neighbourhood_groups))

    for i, room_type in enumerate(room_types):
        ax.bar(bar_positions + i * bar_width, means[room_type], bar_width,
               yerr=stds[room_type], label=room_type, capsize=5)

    ax.set_title('Average Availability by Room Type Across Neighbourhood Groups in NYC')
    ax.set_xlabel('Neighbourhood Group')
    ax.set_ylabel('Average Availability (days)')
    ax.set_xticks(bar_positions + bar_width * (len(room_types) - 1) / 2)
    ax.set_xticklabels(neighbourhood_groups)
    ax.legend(title='Room Type')
    plt.show()

    plt.savefig('./media/availability_room_type_neighbourhood_group.png')


def correlation_between_price_and_number_of_reviews(df: pd.DataFrame):
    plt.figure(figsize=(14, 8))

    markers = ['o', 's', 'D', '^']
    colors = ['blue', 'green', 'red', 'purple']

    for i, room_type in enumerate(df['room_type'].cat.categories):
        room_data = df[df['room_type'] == room_type]
        plt.scatter(room_data['price'], room_data['number_of_reviews'],
                    alpha=0.6, edgecolors='w', label=room_type,
                    marker=markers[i], color=colors[i])

    x = df['price']
    y = df['number_of_reviews']
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='black', linestyle='--', label='Regression Line')
    plt.title('Correlation Between Price and Number of Reviews')
    plt.xlabel('Price')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Room Type')
    plt.show()

    plt.savefig('./media/price_vs_reviews_by_room_type.png')


def time_series_analysis_of_reviews(df: pd.DataFrame):
    grouped = df.groupby(
        ['last_review', 'neighbourhood_group']
    )['number_of_reviews'].sum().reset_index()
    pivot_table = grouped.pivot(
        index='last_review', columns='neighbourhood_group', values='number_of_reviews'
    )
    smoothed = pivot_table.rolling(window=30).mean()

    plt.figure(figsize=(14, 8))
    for neighbourhood_group in smoothed.columns:
        plt.plot(smoothed.index, smoothed[neighbourhood_group], label=neighbourhood_group)

    plt.title('Time Series Analysis of Reviews')
    plt.xlabel('Last Review')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Neighbourhood Group')
    plt.show()

    plt.savefig('./media/reviews_trend_by_neighbourhood_group.png')


def price_and_availability_heatmap(df: pd.DataFrame):
    heatmap_data = df.pivot_table(index='neighbourhood_group',
                                  values=['price', 'availability_365'],
                                  aggfunc='mean')
    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    plt.xticks(np.arange(len(heatmap_data.columns)), heatmap_data.columns, rotation=45)
    plt.yticks(np.arange(len(heatmap_data.index)), heatmap_data.index)
    plt.title('Price and Availability Heatmap Across Neighbourhoods')
    plt.xlabel('Price & Availability')
    plt.ylabel('Neighbourhood Groups')
    plt.colorbar(label='Mean Value')
    plt.show()

    plt.savefig('./media/price_availability_heatmap.png')


def room_type_and_review_analysis(df: pd.DataFrame):
    agg_data = df.groupby(
        ['neighbourhood_group', 'room_type']
    )['number_of_reviews'].sum().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.get_cmap('tab20').colors

    bottoms = np.zeros(len(agg_data.index))
    for i, room_type in enumerate(agg_data.columns):
        ax.bar(
            agg_data.index, agg_data[room_type], bottom=bottoms, color=colors[i], label=room_type
        )
        bottoms += agg_data[room_type]

    ax.set_title('Number of Reviews by Room Type Across Neighbourhood Groups')
    ax.set_xlabel('Neighbourhood Group')
    ax.set_ylabel('Total Number of Reviews')
    ax.legend(title='Room Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.savefig('./media/room_type_reviews_neighbourhood_group_stacked.png')


if __name__ == "__main__":
    data_frame = pd.read_csv("../pandas_tasks/cleaned_airbnb_data.csv")
    data_frame = prepare_data(data_frame)

    # 1. Neighborhood Distribution of Listings
    neighbourhood_group_distribution(data_frame)

    # 2. Price Distribution Across Neighborhoods
    price_distribution_neighbourhood_group(data_frame)

    # 3. Room Type vs. Availability
    availability_room_type_neighbourhood_group(data_frame)

    # 4. Correlation Between Price and Number of Reviews
    correlation_between_price_and_number_of_reviews(data_frame)

    # 5. Time Series Analysis of Reviews
    time_series_analysis_of_reviews(data_frame)

    # 6. Price and Availability Heatmap
    price_and_availability_heatmap(data_frame)

    # 7. Room Type and Review Count Analysis
    room_type_and_review_analysis(data_frame)
