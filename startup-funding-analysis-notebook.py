# %% [markdown]
# # Indian Startups Funding Analysis

# %% [markdown]
# In this notebook, we'll analyze data on Indian startups' funding from 2019 to 2021, as well as compare it with software professionals' salaries. Our goal is to uncover insights about funding trends, investor behavior, and the relationship between funding and salaries in different Indian cities.

# %% [markdown]
# ## 1. Data Loading and Preprocessing

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# List of files to process
files = [("startup_funding2019.csv", 2019), ("startup_funding2020.csv", 2020), ("startup_funding2021.csv", 2021)]

# Create an empty DataFrame to store the combined data
fnd = pd.DataFrame()

# Process each file
for filename, year in files:
    df_tmp = pd.read_csv(filename)
    df_tmp['Year'] = year
    fnd = pd.concat([fnd, df_tmp], ignore_index=True)

print(f"Shape of the combined DataFrame: {fnd.shape}")

# %% [markdown]
# ## 2. Data Cleaning and Formatting

# %%
# Function to clean the funding amount
def clean_funding_amount(column):
    column = column.replace('Undisclosed', np.nan)
    column = column.replace('[$]', '', regex=True)
    column = column.replace(',', '', regex=True)
    return pd.to_numeric(column, errors='coerce')

# Clean and format columns
fnd['Amount($)'] = clean_funding_amount(fnd['Amount($)'])
fnd['Founded'] = pd.to_numeric(fnd['Founded'], errors='coerce').astype('Int64')
fnd['Year'] = pd.to_numeric(fnd['Year'])

# Calculate total funding
total_funding = fnd['Amount($)'].sum()
print(f"Total funding from 2019 to 2021: ${total_funding:,.2f}")

# %% [markdown]
# ## 3. Investor Analysis

# %%
# Analyze top investors overall
top_investors = fnd.groupby('Investor', as_index=False).size().sort_values('size', ascending=False)
print("Top investor overall:")
print(top_investors.head(1))

# Analyze Inflection Point Ventures' ranking in 2020
fnd_2020 = fnd[fnd['Year'] == 2020]
ir_2020 = fnd_2020.groupby('Investor')['Company/Brand'].nunique().reset_index(name='count')
ir2020_sorted = ir_2020.sort_values(by='count', ascending=False)
rank_ipv_2020 = ir2020_sorted[ir2020_sorted['Investor'] == 'Inflection Point Ventures'].index[0] + 1
print(f"Inflection Point Ventures' ranking in 2020: {rank_ipv_2020}")

# %% [markdown]
# ## 4. City-wise Funding and Salary Comparison

# %%
# Load software professionals salary data
sps = pd.read_csv('Software Professionals Salary.csv')

# Create sps_loc DataFrame
sps_loc = sps.groupby('Location', as_index=False)[['Rating', 'Salary']].mean()

# Create fnd_loc DataFrame
fnd_21 = fnd[fnd.Year == 2021]
fnd_loc = fnd_21.groupby('HeadQuarter', as_index=False).agg({'Company/Brand': 'count', 'Amount($)': 'sum'})

# Merge DataFrames
sps_fnd_loc = pd.merge(sps_loc, fnd_loc, how='inner', left_on='Location', right_on='HeadQuarter')
sps_fnd_loc = sps_fnd_loc.drop(columns=['HeadQuarter'])
sps_fnd_loc['Amount($MM)'] = sps_fnd_loc['Amount($)'] / 1000000
sps_fnd_loc = sps_fnd_loc.drop(columns=['Amount($)'])
sps_fnd_loc = sps_fnd_loc.rename(columns={
    'Location': 'City',
    'Rating': 'Avg. Rating',
    'Salary': 'Avg. Salary',
    'Company/Brand': 'Nr. Companies Funded',
    'Amount($MM)': 'Sum Funding ($MM)'
})

print(sps_fnd_loc)

# Find city with highest average rating
highest_rating_city = sps_fnd_loc.loc[sps_fnd_loc['Avg. Rating'].idxmax()]
print(f"\nCity with highest average rating: {highest_rating_city['City']}")
print(f"Number of companies funded: {highest_rating_city['Nr. Companies Funded']}")

# %% [markdown]
# ## 5. Visualization of Results

# %%
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Avg. Salary', y='Sum Funding ($MM)', hue='City', size='Nr. Companies Funded', 
                sizes=(50, 500), data=sps_fnd_loc)

plt.title('Relationship between Average Salary and Total Funding by City')
plt.xlabel('Average Salary')
plt.ylabel('Total Funding (Millions $)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Conclusion

# %% [markdown]
# Based on our analysis, we can draw the following conclusions:
# 
# 1. The total funding received by Indian startups from 2019 to 2021 was substantial, indicating a thriving startup ecosystem.
# 2. Inflection Point Ventures was a significant player in the Indian startup funding scene, particularly in 2020.
# 3. There's a notable variation in both average salaries and total funding across different Indian cities.
# 4. Mumbai stands out as a city with both high average salaries and a large amount of total funding, suggesting it's a major hub for both tech talent and startup activity.
# 5. The relationship between average salaries and total funding isn't strictly linear across all cities, indicating that other factors may influence the startup ecosystem in each location.
# 
# This analysis provides valuable insights into the Indian startup ecosystem and could be useful for entrepreneurs, investors, and policymakers looking to understand the dynamics of startup funding and tech salaries across different Indian cities.
