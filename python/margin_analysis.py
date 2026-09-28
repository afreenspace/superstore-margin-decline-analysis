import pandas as pd

# ===== PHASE 1: LOAD & CLEAN =====
df = pd.read_csv('data/Sample - Superstore.csv', encoding='latin1')

print(df.shape)
print(df.columns)

df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

print(df.isnull().sum())
print(df.dtypes)

df['Year'] = df['Order Date'].dt.year
df['Quarter'] = df['Order Date'].dt.quarter
df['Row Margin%'] = (df['Profit'] / df['Sales'] * 100).round(2)

# Check duplicates
dupes = df[df.duplicated(subset=['Order ID', 'Product ID'], keep=False)]
print(dupes[['Order ID', 'Product ID', 'Product Name', 'Order Date', 'Sales', 'Quantity', 'Discount', 'Profit']].sort_values('Order ID'))
print(df['Row Margin%'].describe())

# ===== PHASE 2: YEARLY & QUARTERLY MARGIN TREND =====
yearly = df.groupby('Year').agg(Revenue=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
yearly['Margin%'] = (yearly['Profit'] / yearly['Revenue'] * 100).round(2)
print(yearly)

sub = df[df['Year'].isin([2016, 2017])]
quarterly = sub.groupby(['Year', 'Quarter']).agg(Revenue=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
quarterly['Margin%'] = (quarterly['Profit'] / quarterly['Revenue'] * 100).round(2)
print(quarterly)

# ===== PHASE 3: FIND WHERE — Q4 2016 vs Q4 2017 =====
q4 = df[(df['Year'].isin([2016, 2017])) & (df['Quarter'] == 4)]

by_category = q4.groupby(['Year', 'Category']).agg(Revenue=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
by_category['Margin%'] = (by_category['Profit'] / by_category['Revenue'] * 100).round(2)
print(by_category)

q4_problem = q4[q4['Category'].isin(['Furniture', 'Office Supplies'])]
by_subcat = q4_problem.groupby(['Year', 'Category', 'Sub-Category']).agg(Revenue=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
by_subcat['Margin%'] = (by_subcat['Profit'] / by_subcat['Revenue'] * 100).round(2)
print(by_subcat.sort_values(['Category', 'Sub-Category', 'Year']))

# ===== PHASE 4: FIND WHY — discount, region, segment =====
binders = q4_problem[q4_problem['Sub-Category'] == 'Binders']
discount_check = binders.groupby('Year').agg(
    Avg_Discount=('Discount', 'mean'),
    AvgSalesPerOrder=('Sales', 'mean'),
    TotalRevenue=('Sales', 'sum'),
    TotalProfit=('Profit', 'sum')
).reset_index()
discount_check['Avg_Discount'] = (discount_check['Avg_Discount'] * 100).round(1)
print(discount_check)

binders_2016 = binders[binders['Year'] == 2016]
binders_2017 = binders[binders['Year'] == 2017]
print(binders_2016['Discount'].value_counts().sort_index())
print(binders_2017['Discount'].value_counts().sort_index())
print(binders_2016['Discount'].describe())
print(binders_2017['Discount'].describe())

tables = q4_problem[q4_problem['Sub-Category'] == 'Tables']
tables_discount = tables.groupby('Year').agg(
    Avg_Discount=('Discount', 'mean'),
    AvgSalesPerOrder=('Sales', 'mean'),
    OrderCount=('Sales', 'count'),
    TotalRevenue=('Sales', 'sum'),
    TotalProfit=('Profit', 'sum')
).reset_index()
tables_discount['Avg_Discount'] = (tables_discount['Avg_Discount'] * 100).round(1)
print(tables_discount)

problem_subs = q4_problem[q4_problem['Sub-Category'].isin(['Binders', 'Tables'])]
by_region = problem_subs.groupby(['Sub-Category', 'Year', 'Region']).agg(
    Revenue=('Sales', 'sum'), Profit=('Profit', 'sum'), OrderCount=('Sales', 'count')
).reset_index()
by_region['Margin%'] = (by_region['Profit'] / by_region['Revenue'] * 100).round(2)
print(by_region.sort_values(['Sub-Category', 'Region', 'Year']))

by_segment = problem_subs.groupby(['Sub-Category', 'Year', 'Segment']).agg(
    Revenue=('Sales', 'sum'), Profit=('Profit', 'sum'), OrderCount=('Sales', 'count')
).reset_index()
by_segment['Margin%'] = (by_segment['Profit'] / by_segment['Revenue'] * 100).round(2)
print(by_segment.sort_values(['Sub-Category', 'Segment', 'Year']))

# Outlier check
outliers = df.sort_values('Row Margin%').head(15)
print(outliers[['Order Date', 'Year', 'Quarter', 'Category', 'Sub-Category', 'Sales', 'Discount', 'Profit', 'Row Margin%']])
outliers_in_scope = outliers[(outliers['Year'].isin([2016, 2017])) & (outliers['Quarter'] == 4) & (outliers['Sub-Category'].isin(['Binders', 'Tables']))]
print(outliers_in_scope)

# Mix shift check
q4_all = q4  # same thing, all categories
q4_totals = q4_all.groupby('Year')['Sales'].sum()
mix = q4_all[q4_all['Sub-Category'].isin(['Binders', 'Tables'])].groupby(['Year', 'Sub-Category'])['Sales'].sum().reset_index()
mix['Total Q4 Revenue'] = mix['Year'].map(q4_totals)
mix['Share of Q4 Revenue %'] = (mix['Sales'] / mix['Total Q4 Revenue'] * 100).round(2)
print(mix)

# ===== PHASE 5: MARGIN BRIDGE =====
bridge = q4_all.groupby(['Year', 'Sub-Category'])['Profit'].sum().unstack('Year')
bridge['Change'] = (bridge[2017] - bridge[2016]).round(0)
bridge = bridge.sort_values('Change')
print(bridge.round(0))

total_change = bridge['Change'].sum()
print(f"Total Q4 profit change: {total_change:.0f}")

top_drag = bridge['Change'].sort_values().head(3)
for sc, val in top_drag.items():
    pct = val / bridge[bridge['Change'] < 0]['Change'].sum() * 100
    print(f"  {sc}: {val:.0f}  ({pct:.0f}% of total negative drag)")

# ===== PHASE 6: EXPORT FOR POWER BI =====
df.to_csv('data/superstore_cleaned.csv', index=False)
print("Cleaned dataset exported.")

findings = pd.DataFrame({
    'Finding': [
        'Q4 2016 Total Profit', 'Q4 2017 Total Profit', 'Q4 Profit Change',
        'Binders Q4 Profit Change', 'Binders % of Total Negative Drag',
        'Binders Avg Discount 2016', 'Binders Avg Discount 2017',
        'Binders Central Region % of Its Own Decline',
        'Tables Q4 Profit Change', 'Tables % of Total Negative Drag',
        'Tables Order Count 2016', 'Tables Order Count 2017',
        'Tables South Region % of Its Own Decline',
        'Duplicate Row Found', 'Appliances 80% Discount Issue (all years)'
    ],
    'Value': [
        '38,140', '27,449', '-10,691',
        '-12,688', '69%',
        '32.5%', '36.9%',
        '79%',
        '-2,979', '16%',
        '33', '51',
        '94%',
        '1 exact duplicate, Order US-2014-150119',
        'Consistent -270% to -275% margin, all 4 years'
    ]
})

findings.to_csv('data/key_findings_summary.csv', index=False)
print("Findings summary exported.")