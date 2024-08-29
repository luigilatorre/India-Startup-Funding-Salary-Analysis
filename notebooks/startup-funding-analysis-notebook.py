import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# List of files to process
files = [("startup_funding2019.csv", 2019), ("startup_funding2020.csv", 2020), ("startup_funding2021.csv", 2021)]

# Initialize an empty DataFrame to store combined data from multiple years
fnd = pd.DataFrame()

# Load and combine data from all years into a single DataFrame
for filename, year in files:
    df_tmp = pd.read_csv(filename)  # Read the CSV file for each year
    df_tmp['Year'] = year  # Add a column for the year
    fnd = pd.concat([fnd, df_tmp], ignore_index=True)  # Append data to the main DataFrame

print(f"Shape of the combined DataFrame: {fnd.shape}")  # Display the dimensions of the combined DataFrame

# Function to clean and convert the funding amount column
def clean_funding_amount(column):
    column = column.replace('Undisclosed', np.nan)  # Replace 'Undisclosed' with NaN
    column = column.replace('[$]', '', regex=True)  # Remove dollar signs
    column = column.replace(',', '', regex=True)  # Remove commas
    return pd.to_numeric(column, errors='coerce')  # Convert to numeric, setting errors to NaN

# Apply the cleaning function to the 'Amount($)' column and convert other columns to numeric
fnd['Amount($)'] = clean_funding_amount(fnd['Amount($)'])
fnd['Founded'] = pd.to_numeric(fnd['Founded'], errors='coerce').astype('Int64')
fnd['Year'] = pd.to_numeric(fnd['Year'])

# Calculate the total amount of funding received from 2019 to 2021
total_funding = fnd['Amount($)'].sum()
print(f"Total funding from 2019 to 2021: ${total_funding:,.2f}")

# Analyze the most frequent investors across all years
top_investors = fnd.groupby('Investor', as_index=False).size().sort_values('size', ascending=False)
print("Top investor overall:")
print(top_investors.head(1))  # Display the investor with the highest number of investments

# Analyze Inflection Point Ventures' ranking in 2020 based on the number of unique companies funded
fnd_2020 = fnd[fnd['Year'] == 2020]  # Filter data for the year 2020
ir_2020 = fnd_2020.groupby('Investor')['Company/Brand'].nunique().reset_index(name='count')  # Count unique companies per investor
ir2020_sorted = ir_2020.sort_values(by='count', ascending=False)  # Sort investors by count
rank_ipv_2020 = ir2020_sorted[ir2020_sorted['Investor'] == 'Inflection Point Ventures'].index[0] + 1
print(f"Inflection Point Ventures' ranking in 2020: {rank_ipv_2020}")

# Load salary data for software professionals
sps = pd.read_csv('Software Professionals Salary.csv')

# Create a DataFrame summarizing average rating and salary by location
sps_loc = sps.groupby('Location', as_index=False)[['Rating', 'Salary']].mean()

# Create a DataFrame summarizing the number of companies funded and total funding by headquarters location
fnd_21 = fnd[fnd.Year == 2021]  # Filter data for the year 2021
fnd_loc = fnd_21.groupby('HeadQuarter', as_index=False).agg({'Company/Brand': 'count', 'Amount($)': 'sum'})  # Aggregate data

# Merge the salary and funding DataFrames to compare city-wise data
sps_fnd_loc = pd.merge(sps_loc, fnd_loc, how='inner', left_on='Location', right_on='HeadQuarter')
sps_fnd_loc = sps_fnd_loc.drop(columns=['HeadQuarter'])
sps_fnd_loc['Amount($MM)'] = sps_fnd_loc['Amount($)'] / 1000000  # Convert funding to millions
sps_fnd_loc = sps_fnd_loc.drop(columns=['Amount($)'])
sps_fnd_loc = sps_fnd_loc.rename(columns={
    'Location': 'City',
    'Rating': 'Avg. Rating',
    'Salary': 'Avg. Salary',
    'Company/Brand': 'Nr. Companies Funded',
    'Amount($MM)': 'Sum Funding ($MM)'
})

print(sps_fnd_loc)  # Display the merged DataFrame with city-wise averages and funding

# Identify the city with the highest average rating
highest_rating_city = sps_fnd_loc.loc[sps_fnd_loc['Avg. Rating'].idxmax()]
print(f"\nCity with highest average rating: {highest_rating_city['City']}")
print(f"Number of companies funded: {highest_rating_city['Nr. Companies Funded']}")

# Create a scatter plot to visualize the relationship between average salary and total funding by city
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Avg. Salary', y='Sum Funding ($MM)', hue='City', size='Nr. Companies Funded', 
                sizes=(50, 500), data=sps_fnd_loc)

plt.title('Relationship between Average Salary and Total Funding by City')
plt.xlabel('Average Salary')
plt.ylabel('Total Funding (Millions $)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Conclusions drawn from the analysis
print("CONCLUSIONS:")
print("1. Total funding for Indian startups from 2019 to 2021 is substantial, reflecting a robust startup ecosystem.")
print("2. Inflection Point Ventures was a significant investor, especially in 2020.")
print("3. There is considerable variation in average salaries and funding across Indian cities.")
print("4. Mumbai stands out with high average salaries and significant funding, indicating it's a major hub for tech and startups.")
print("5. The relationship between average salaries and total funding varies by city, suggesting other factors influence the startup ecosystem.")
