import pandas as pd
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt

import streamlit as st

st.set_page_config(layout="wide")

df_chiba = pd.read_csv('./data/chiba_20071_20234_preprocessed.csv', encoding="utf-8", on_bad_lines='skip')
df_tokyo = pd.read_csv('./data/tokyo_20071_20234_preprocessed.csv', encoding="utf-8", on_bad_lines='skip')

selected_prefecture = st.selectbox('Select a prefecture:', ['Tokyo', 'Chiba'])

# Conditional assignment based on the selected prefecture
if selected_prefecture == 'Tokyo':
    df = df_tokyo
else:
    df = df_chiba

selected_area = st.selectbox('Select an area:', df['市区町村名'].unique())

# Dropdown to select the layout (間取り)
if '間取り' in df.columns:
    # Add 'All' option to the list of layouts
    layouts = np.append(['All'], df['間取り'].unique())
    selected_layout = st.selectbox('Select a layout:', layouts)
else:
    st.error("The column '間取り' does not exist in the dataset.")
    st.stop()

# Age range selection in Streamlit
age_options = {
    "15年以内": df['築年数'] <= 15,
    "16年以上": df['築年数'] > 15
}
selected_age_range = st.selectbox("Select the building age range:", list(age_options.keys()))



# Filter the DataFrame based on the selected age range and layout
if selected_layout == 'All':
    df_filtered = df[(df['市区町村名'] == selected_area) & age_options[selected_age_range]]
else:
    df_filtered = df[(df['市区町村名'] == selected_area) & (df['間取り'] == selected_layout) & age_options[selected_age_range]]


# Group by area and year, then calculate the mean price
area_yearly_average_price = df_filtered.groupby(['市区町村名', '取引時期（年）'])['取引価格（総額）'].mean().unstack()
area_yearly_count = df_filtered.groupby(['市区町村名', '取引時期（年）'])['取引価格（総額）'].count().unstack()


# Plotting
# Plotting using Streamlit
st.title('Time Series Trend of Housing Prices ')


# Filter data based on selected area
selected_area_yearly_average_price = area_yearly_average_price.loc[selected_area]
selected_area_yearly_count = area_yearly_count.loc[selected_area]




# Assuming the data setup is done above this and 'selected_area_yearly_count' and 'selected_area_yearly_average_price' are available

plt.figure(figsize=(12, 8))

# Initially create the line plot for average transaction prices on the primary axis
ax1 = plt.gca()  # Get the current axis
ax1.plot(selected_area_yearly_average_price.index, selected_area_yearly_average_price.values, color='red', label='Average Price')
ax1.set_xlabel('Year')
ax1.set_ylabel('平均取引価格（万円）', color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Create a secondary y-axis for transaction counts
ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis
ax2.bar(selected_area_yearly_count.index, selected_area_yearly_count.values, color='lightblue', label='Transaction Count', width=0.4)
ax2.set_ylabel('取引回数', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Titles and grid
plt.title('Combined Trend of Housing Prices and Transaction Counts')
plt.grid(True)

# Add a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Show the plot in Streamlit
st.pyplot(plt)