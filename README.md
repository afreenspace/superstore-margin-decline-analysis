*# Superstore Margin Decline Analysis*



*Why did margin fall from 16.2% to 9.8% in Q4 2017 while revenue kept growing? This project diagnoses the drop with Python (pandas) and presents the findings in a Power BI dashboard.*



*## Key Findings*



*- Revenue grew about 20% year over year, but Q4 margin fell from 16.2% (2016) to 9.8% (2017). Q4 profit dropped by $10,691.*

*- Yearly margin only slipped from 13.4% to 12.7%, so the problem was hidden until the data was split by quarter.*

*- \*\*Binders\*\* account for 69% of the total negative profit drag. Orders with an 80% discount doubled (13 to 26), all in the Central region.*

*- \*\*Tables\*\* account for 16% of the drag. Q4 orders rose 55% (33 to 51), and the South region accounts for 94% of the Tables decline.*



*## Approach*



*1. \*\*Load and clean\*\* the Superstore data (dates, year/quarter fields, row margins)*

*2. \*\*Find when:\*\* yearly and quarterly margin trend*

*3. \*\*Find where:\*\* Q4 2016 vs Q4 2017 by category and sub-category*

*4. \*\*Find why:\*\* discount levels, region and segment breakdowns, outlier and mix-shift checks*

*5. \*\*Reconcile:\*\* profit bridge across all 17 sub-categories to the total change*

*6. \*\*Export\*\* the cleaned data and a findings summary for Power BI*



*## Dashboard*



*!\[Overview](screenshots/01-dashboard-overview.png)*

*!\[Root Cause](screenshots/02-dashboard-root-cause.png)*

*!\[Recommendations](screenshots/03-dashboard-recommendations.png)*



*## Recommendations*



*1. Cap discounts on Binders*

*2. Rethink Tables' pricing in the South*

*3. Track margin every quarter, not just yearly*



*Full write-up: \[executive-summary/recommendations.md](executive-summary/recommendations.md)*



*## Project Structure*



*- `data/` raw Superstore data, cleaned data and key findings summary*

*- `python/` margin\_analysis.py (analysis script)*

*- `powerbi/` Dashboard.pbix (open with Power BI Desktop)*

*- `executive-summary/` final recommendations*

*- `screenshots/` dashboard screenshots*



*## How to Run*



*Requires Python and pandas. From the project's main folder:*



&#x20;   *python python/margin\_analysis.py*



*## Tools*



*Python (pandas), Power BI, DAX*

