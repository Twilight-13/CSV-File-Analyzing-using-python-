import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import matplotlib as mpl



mpl.use('TkAgg')

file_path = "sales_data_500.csv"
file_path2 = "countries.geo.json"

world_map = gpd.read_file(file_path2)
sales_data = pd.read_csv(file_path)

# To view all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)



###########################################################################################

# WORLD SALE HEATMAP


merged = world_map.merge(sales_data, left_on="name", right_on="Country", how="left")

# Calculate total sales per country (Important!)
country_sales = sales_data.groupby("Country")["Amount"].sum().reset_index()

# Merge total sales back into the merged GeoDataFrame
merged = merged.merge(country_sales, left_on="name", right_on="Country", how="left")

# Create the choropleth map
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

ax1.set_aspect('equal')

merged.plot(column="Amount_y", cmap="viridis", linewidth=0.8, ax=ax1, edgecolor="0.8", missing_kwds={
    "color": "lightgrey",
    "edgecolor": "0.8",
    "hatch": "///",
    "label": "Missing values",
})

ax1.set_title("World Sales by Country")

# Seaborn colorbar with explicit `ax` argument
norm = mpl.colors.Normalize(vmin=merged['Amount_y'].min(), vmax=merged['Amount_y'].max())
sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax1, label='Total Sales Amount')  # Pass the axes object

# plt.show()


#################################################################################################################

sales_data['Shipping_Time'] = (pd.to_datetime(sales_data['Ship_Date']) - pd.to_datetime(sales_data['Order_Date']))
sales_data['Shipping_Time_Days'] = sales_data['Shipping_Time'].dt.days

# Get min and max days
min_days = sales_data['Shipping_Time_Days'].min()
max_days = sales_data['Shipping_Time_Days'].max()

# Bar graph on ax2
ax2.bar(sales_data['Shipping_Time_Days'].unique(), sales_data['Shipping_Time_Days'].value_counts(), color='skyblue', edgecolor='black')  # Using value_counts for bar heights
ax2.set_xlabel("Shipping Time (Days)")
ax2.set_ylabel("Number of Orders")
ax2.set_title("Distribution of Shipping Times")
ax2.set_xticks(np.arange(min_days, max_days + 1))  # Set x-axis ticks for all possible days

# Adjust layout (optional)
plt.tight_layout()

# plt.show()


#################################################################################################################


product_category = sales_data['Product_Category'].unique()

category_counts = sales_data['Product_Category'].value_counts()

ax3.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
        shadow=True, startangle=140, explode=(0.2, 0.01, 0.01, 0.1))
ax3.set_title('Product Category Distribution')
# plt.show()


##################################################################################################################

# Calculate total sales per category
category_sales = sales_data.groupby('Product_Category')['Amount'].sum()

categories = category_sales.index
sales = category_sales.values

ax4.barh(categories, sales, color='skyblue')  # Use barh for horizontal bars

# Set labels and title (adjustments for horizontal bars)
ax4.set_xlabel('Total Sales')
ax4.set_ylabel('Product Category')
ax4.set_title('Total Sales per Product Category')

plt.tight_layout(pad=3)
plt.show()






