import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

# Load data
df_chiba = pd.read_csv('../data/chiba_20071_20234_preprocessed.csv', encoding="utf-8", on_bad_lines='skip')
df_tokyo = pd.read_csv('../data/tokyo_20071_20234_preprocessed.csv', encoding="utf-8", on_bad_lines='skip')

# Function to plot and save graphs for each area
def plot_and_save(df, prefecture_name):
    for area in df['市区町村名'].unique():
        df_filtered = df[df['市区町村名'] == area]
        area_yearly_average_price = df_filtered.groupby('取引時期（年）')['取引価格（総額）'].mean()
        area_yearly_count = df_filtered.groupby('取引時期（年）')['取引価格（総額）'].count()

        plt.figure(figsize=(12, 8))
        ax1 = plt.gca()
        ax1.plot(area_yearly_average_price.index, area_yearly_average_price.values, color='red', label='Average Price')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('平均取引価格（万円）', color='red')
        ax1.tick_params(axis='y', labelcolor='red')

        ax2 = ax1.twinx()
        ax2.bar(area_yearly_count.index, area_yearly_count.values, color='lightblue', label='Transaction Count', width=0.4)
        ax2.set_ylabel('取引回数', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        plt.title(f'Combined Trend of Housing Prices and Transaction Counts in {area}')
        plt.grid(True)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        plt.savefig(f'./data/output/{prefecture_name}_{area}.png')  # Save the figure
        plt.close()  # Close the figure to free memory

# Plot and save for both prefectures
plot_and_save(df_chiba, 'Chiba')
plot_and_save(df_tokyo, 'Tokyo')