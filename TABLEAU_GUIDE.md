# Tableau Dashboard Guide - ABG Motors Market Entry Analysis

## Complete Step-by-Step Guide for Creating Tableau Dashboards

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Tableau Desktop installed (or Tableau Public)
- ✅ Your 3 CSV files from `data/tableau/`:
  - `japanese_market.csv`
  - `indian_market.csv`
  - `market_comparison_summary.csv`

---

## 🎯 Dashboard Overview

You'll create **4 comprehensive dashboards**:

1. **Market Overview Dashboard** - High-level comparison
2. **Customer Segmentation Dashboard** - Demographic analysis
3. **Indian Market Predictions Dashboard** - Prediction insights
4. **Business Recommendations Dashboard** - Strategic insights

---

# DASHBOARD 1: Market Overview

## Step 1: Import Data into Tableau

1. **Open Tableau Desktop**
2. Click **"Connect to Data"** → **"Text file"**
3. Navigate to `data/tableau/market_comparison_summary.csv`
4. Click **"Open"**
5. Verify data preview shows 6 rows (metrics)

### Data Preview Should Show:
```
Metric              | Japan    | India
--------------------|----------|----------
Total Customers     | 40000    | 70000
Purchase Count      | 23031    | 67410
Purchase Rate       | 57.58%   | 96.30%
Avg Age             | 45.0     | 45.0
Male %              | 55.71%   | 50.04%
Avg Income          | ¥359,399 | ₹1,148,679
```

## Step 2: Create Market Comparison Sheet

### 2.1 Total Customers Comparison
1. **Create new sheet** → Name it "Total Customers"
2. **Drag** `Metric` to **Filters** → Select "Total Customers"
3. **Drag** `Japan` to **Columns**
4. **Drag** `India` to **Columns** (next to Japan)
5. **Change chart type** to **Bar Chart**
6. **Add labels**: Right-click bars → **Mark Label** → **Show Mark Labels**
7. **Format**: 
   - Japan bar: Blue color
   - India bar: Orange color
8. **Add title**: "Total Customers: Japan vs India"

### 2.2 Purchase Count Comparison
1. **Duplicate sheet** (right-click "Total Customers" → Duplicate)
2. **Rename** to "Purchase Count"
3. **Change filter**: Metric = "Purchase Count"
4. **Update title**: "Predicted Purchases: Japan vs India"

### 2.3 Purchase Rate Comparison
1. **Create new sheet** → Name it "Purchase Rate"
2. **Drag** `Metric` to **Filters** → Select "Purchase Rate"
3. **Drag** `Japan` and `India` to **Rows**
4. **Change to Pie Charts** or **Horizontal Bars**
5. **Add percentage labels**
6. **Title**: "Purchase Rate Comparison"

### 2.4 KPI Cards
1. **Create new sheet** → "Japan KPIs"
2. **Drag** `Japan` to **Text** on Marks card
3. **Drag** `Metric` to **Rows**
4. **Format as Table**
5. **Repeat for India** → "India KPIs"

## Step 3: Create Dashboard 1

1. **Click** "New Dashboard" button (bottom)
2. **Rename** to "Market Overview"
3. **Set size**: 1200 x 800 pixels (or Automatic)
4. **Drag sheets** onto dashboard:
   - Top: "Total Customers" (left) + "Purchase Count" (right)
   - Middle: "Purchase Rate"
   - Bottom: "Japan KPIs" (left) + "India KPIs" (right)
5. **Add title**: "ABG Motors: Japan vs India Market Overview"
6. **Add text box**: "Target: 10,000 cars | Predicted: 67,410 | Achievement: 674%"

---

# DASHBOARD 2: Customer Segmentation

## Step 4: Import Japanese Market Data

1. **Data** → **New Data Source**
2. **Connect** to `japanese_market.csv`
3. **Verify columns**:
   - ID, CURR_AGE, GENDER, ANN_INCOME, AGE_CAR, AGE_CAR_SEGMENT, PURCHASE
   - COUNTRY, SEGMENT_LABEL, AGE_GROUP, INCOME_QUARTILE

## Step 5: Age Group Analysis

### 5.1 Purchase by Age Group (Japanese Market)
1. **Create new sheet** → "Japan Age Analysis"
2. **Drag** `AGE_GROUP` to **Columns**
3. **Drag** `PURCHASE` to **Rows** → Change to **SUM**
4. **Add** `PURCHASE` to **Color** (for stacked bars)
5. **Change to Stacked Bar Chart**
6. **Add labels** showing counts
7. **Sort** by age group order
8. **Title**: "Japanese Market: Purchases by Age Group"


### 5.2 Purchase Rate by Age Group
1. **Duplicate sheet** → "Japan Age Rate"
2. **Change** `SUM(PURCHASE)` to **AVG(PURCHASE)**
3. **Format as percentage** (right-click axis → Format → Percentage)
4. **Change to Line Chart**
5. **Title**: "Purchase Rate by Age Group"

## Step 6: Income Analysis

### 6.1 Purchase by Income Quartile
1. **Create new sheet** → "Japan Income Analysis"
2. **Drag** `INCOME_QUARTILE` to **Columns**
3. **Drag** `PURCHASE` to **Rows** (SUM)
4. **Add** `PURCHASE` to **Color**
5. **Create Stacked Bar Chart**
6. **Title**: "Purchases by Income Quartile"

### 6.2 Income Distribution
1. **Create new sheet** → "Income Distribution"
2. **Drag** `ANN_INCOME` to **Columns**
3. **Drag** `Number of Records` to **Rows**
4. **Change to Histogram**
5. **Add** `PURCHASE` to **Color**
6. **Title**: "Income Distribution by Purchase Status"

## Step 7: Maintenance Segment Analysis

### 7.1 Purchase by Segment
1. **Create new sheet** → "Segment Analysis"
2. **Drag** `SEGMENT_LABEL` to **Rows**
3. **Drag** `PURCHASE` to **Columns** (SUM)
4. **Add** `PURCHASE` to **Color**
5. **Create Horizontal Bar Chart**
6. **Sort by purchase count**
7. **Title**: "Purchases by Maintenance Segment"

### 7.2 Segment Purchase Rate
1. **Create new sheet** → "Segment Rate"
2. **Drag** `SEGMENT_LABEL` to **Rows**
3. **Drag** `PURCHASE` to **Columns** (AVG)
4. **Format as percentage**
5. **Add data labels**
6. **Color code**: Green (high) to Red (low)
7. **Title**: "Purchase Rate by Maintenance Segment"

## Step 8: Gender Analysis

1. **Create new sheet** → "Gender Analysis"
2. **Drag** `GENDER` to **Columns**
3. **Drag** `PURCHASE` to **Rows** (SUM)
4. **Create Pie Chart** or **Stacked Bar**
5. **Add percentages**
6. **Title**: "Purchases by Gender"

## Step 9: Create Dashboard 2

1. **New Dashboard** → "Customer Segmentation"
2. **Layout**:
   - Top row: "Japan Age Analysis" + "Japan Income Analysis"
   - Middle row: "Segment Analysis" + "Segment Rate"
   - Bottom row: "Gender Analysis" + "Income Distribution"
3. **Add title**: "Japanese Market: Customer Segmentation Analysis"
4. **Add filters**: Age Group, Income Quartile, Gender (apply to all sheets)

---

# DASHBOARD 3: Indian Market Predictions

## Step 10: Import Indian Market Data

1. **Data** → **New Data Source**
2. **Connect** to `indian_market.csv`
3. **Verify columns**:
   - ID, CURR_AGE, GENDER, ANN_INCOME, AGE_CAR, AGE_CAR_SEGMENT
   - PURCHASE_PREDICTION, PURCHASE_PROBABILITY
   - COUNTRY, SEGMENT_LABEL, AGE_GROUP, INCOME_QUARTILE, CONFIDENCE_CATEGORY

## Step 11: Prediction Overview

### 11.1 Total Predictions KPI
1. **Create new sheet** → "Prediction KPI"
2. **Drag** `PURCHASE_PREDICTION` to **Text** (SUM)
3. **Format as large number** with commas
4. **Add title**: "Predicted Purchases: 67,410"
5. **Format as KPI card** (large font, center aligned)

### 11.2 Target vs Predicted
1. **Create new sheet** → "Target Comparison"
2. **Create calculated field**: 
   - Name: "Target"
   - Formula: `10000`
3. **Drag** "Target" to **Columns**
4. **Drag** `SUM(PURCHASE_PREDICTION)` to **Columns**
5. **Create Bullet Chart** or **Bar Chart**
6. **Color**: Green for predicted, Red for target
7. **Add reference line** at 10,000
8. **Title**: "Predicted vs Target (10,000)"

## Step 12: Probability Distribution

### 12.1 Probability Histogram
1. **Create new sheet** → "Probability Distribution"
2. **Drag** `PURCHASE_PROBABILITY` to **Columns**
3. **Drag** `Number of Records` to **Rows**
4. **Create Histogram** (bin size: 0.05)
5. **Add** `CONFIDENCE_CATEGORY` to **Color**
6. **Title**: "Purchase Probability Distribution"

### 12.2 Confidence Breakdown
1. **Create new sheet** → "Confidence Breakdown"
2. **Drag** `CONFIDENCE_CATEGORY` to **Rows**
3. **Drag** `Number of Records` to **Columns**
4. **Create Horizontal Bar Chart**
5. **Add percentages**
6. **Color code**: Dark green (Very High) to Light green (Low)
7. **Title**: "Confidence Category Breakdown"

## Step 13: Indian Market Segmentation

### 13.1 Predictions by Age Group
1. **Create new sheet** → "India Age Predictions"
2. **Drag** `AGE_GROUP` to **Columns**
3. **Drag** `PURCHASE_PREDICTION` to **Rows** (SUM)
4. **Add** `PURCHASE_PROBABILITY` to **Color** (AVG)
5. **Create Bar Chart**
6. **Title**: "Predicted Purchases by Age Group"

### 13.2 Predictions by Income Quartile
1. **Create new sheet** → "India Income Predictions"
2. **Drag** `INCOME_QUARTILE` to **Columns**
3. **Drag** `PURCHASE_PREDICTION` to **Rows** (SUM)
4. **Add** `PURCHASE_PROBABILITY` to **Color** (AVG)
5. **Create Bar Chart**
6. **Title**: "Predicted Purchases by Income Quartile"

### 13.3 Predictions by Maintenance Segment
1. **Create new sheet** → "India Segment Predictions"
2. **Drag** `SEGMENT_LABEL` to **Rows**
3. **Drag** `PURCHASE_PREDICTION` to **Columns** (SUM)
4. **Add** `PURCHASE_PROBABILITY` to **Color** (AVG)
5. **Create Horizontal Bar Chart**
6. **Sort by predictions**
7. **Title**: "Predicted Purchases by Maintenance Segment"

## Step 14: Create Dashboard 3

1. **New Dashboard** → "Indian Market Predictions"
2. **Layout**:
   - Top: "Prediction KPI" (center) + "Target Comparison" (right)
   - Second row: "Probability Distribution" (full width)
   - Third row: "Confidence Breakdown" (left) + "India Age Predictions" (right)
   - Bottom row: "India Income Predictions" (left) + "India Segment Predictions" (right)
3. **Add title**: "Indian Market: Prediction Analysis"
4. **Add text**: "Model Accuracy: 68.53% | ROC-AUC: 75.87%"

---

# DASHBOARD 4: Business Recommendations

## Step 15: Target Segment Identification

### 15.1 High-Value Segments (Heat Map)
1. **Create new sheet** → "Target Segments"
2. **Drag** `INCOME_QUARTILE` to **Columns**
3. **Drag** `SEGMENT_LABEL` to **Rows**
4. **Drag** `PURCHASE_PREDICTION` to **Color** (SUM)
5. **Drag** `PURCHASE_PREDICTION` to **Label** (SUM)
6. **Create Heat Map**
7. **Color**: Green (high) to White (low)
8. **Title**: "Target Segments: Income × Maintenance"

### 15.2 Top Customer Profiles
1. **Create new sheet** → "Top Profiles"
2. **Create calculated field**:
   - Name: "Customer Profile"
   - Formula: `[AGE_GROUP] + " | " + [INCOME_QUARTILE] + " | " + [SEGMENT_LABEL]`
3. **Drag** "Customer Profile" to **Rows**
4. **Drag** `PURCHASE_PREDICTION` to **Columns** (SUM)
5. **Sort descending**
6. **Show top 10**
7. **Title**: "Top 10 Customer Profiles"

## Step 16: Marketing Strategy Visualization

### 16.1 Priority Segments
1. **Create new sheet** → "Priority Matrix"
2. **Drag** `AVG(PURCHASE_PROBABILITY)` to **Columns**
3. **Drag** `COUNT(ID)` to **Rows**
4. **Drag** `SEGMENT_LABEL` to **Detail**
5. **Create Scatter Plot**
6. **Add** `SEGMENT_LABEL` to **Label**
7. **Add quadrant lines**: 
   - Reference line at 0.7 (probability)
   - Reference line at median count
8. **Title**: "Priority Matrix: Probability × Volume"

### 16.2 Recommended Actions
1. **Create new sheet** → "Recommendations"
2. **Create text table** with recommendations:
   - Segment 3-4: "Partner with service centers"
   - High Income: "Premium positioning"
   - Age 25-45: "Digital marketing"
3. **Format as professional table**

## Step 17: ROI Projection

### 17.1 Sales Projection
1. **Create new sheet** → "Sales Projection"
2. **Create calculated fields**:
   - "Conservative (50%)": `SUM([PURCHASE_PREDICTION]) * 0.5`
   - "Expected (75%)": `SUM([PURCHASE_PREDICTION]) * 0.75`
   - "Optimistic (100%)": `SUM([PURCHASE_PREDICTION])`
3. **Create bar chart** showing all three scenarios
4. **Add reference line** at 10,000 target
5. **Title**: "Sales Projections: Conservative to Optimistic"

## Step 18: Create Dashboard 4

1. **New Dashboard** → "Business Recommendations"
2. **Layout**:
   - Top: "Target Segments" (heat map, full width)
   - Middle left: "Priority Matrix"
   - Middle right: "Top Profiles"
   - Bottom left: "Sales Projection"
   - Bottom right: "Recommendations" (text table)
3. **Add title**: "ABG Motors: Strategic Recommendations"
4. **Add text box**: "Recommendation: STRONG GO - Proceed with Market Entry"

---

# DASHBOARD 5: Executive Summary (Bonus)

## Step 19: Create Executive Dashboard

1. **New Dashboard** → "Executive Summary"
2. **Combine key metrics**:
   - Market size comparison (Japan vs India)
   - Predicted purchases KPI (67,410)
   - Target achievement (674%)
   - Model performance (ROC-AUC: 75.87%)
   - Top 3 insights
   - Final recommendation
3. **Use large fonts, minimal charts**
4. **Professional color scheme** (blues and greens)
5. **Add company logo** (if available)

---

## 🎨 Design Best Practices

### Color Scheme
- **Japan**: Blue (#1f77b4)
- **India**: Orange (#ff7f0e)
- **Positive/Purchase**: Green (#2ca02c)
- **Negative/No Purchase**: Red (#d62728)
- **Neutral**: Gray (#7f7f7f)

### Formatting Tips
1. **Consistent fonts**: Arial or Tableau Book
2. **Title size**: 14-16pt
3. **Label size**: 10-12pt
4. **Use gridlines sparingly**
5. **Add tooltips** with additional context
6. **Format numbers**: Commas for thousands, % for rates

### Interactive Elements
1. **Add filters** for:
   - Age Group
   - Income Quartile
   - Gender
   - Maintenance Segment
2. **Apply filters** to multiple sheets
3. **Add actions**: Click on segment to filter other views
4. **Add parameters**: Adjust target sales dynamically

---

## 📊 Final Checklist

Before presenting:

- [ ] All 4 dashboards created
- [ ] Titles are clear and descriptive
- [ ] Numbers are formatted (commas, percentages)
- [ ] Colors are consistent across dashboards
- [ ] Filters work correctly
- [ ] Tooltips provide additional context
- [ ] Dashboard sizes are appropriate
- [ ] No data errors or warnings
- [ ] Story flows logically
- [ ] Key insights are highlighted

---

## 🚀 Publishing Your Dashboard

### Option 1: Tableau Public (Free)
1. **File** → **Save to Tableau Public**
2. **Sign in** or create account
3. **Publish** (will be publicly visible)
4. **Share link** with stakeholders

### Option 2: Tableau Server (Enterprise)
1. **Server** → **Publish Workbook**
2. **Select project** and permissions
3. **Publish**
4. **Share URL** with team

### Option 3: Export as PDF/Image
1. **Dashboard** → **Export as PDF**
2. **Or** → **Export as Image**
3. **Include in presentation**

---

## 📝 Presentation Tips

When presenting your Tableau dashboards:

1. **Start with Executive Summary** (Dashboard 5)
2. **Show Market Overview** (Dashboard 1) - establish context
3. **Deep dive into Segmentation** (Dashboard 2) - explain patterns
4. **Present Predictions** (Dashboard 3) - show results
5. **Conclude with Recommendations** (Dashboard 4) - actionable insights

**Key talking points**:
- "67,410 predicted purchases exceed our 10,000 target by 674%"
- "Income and maintenance patterns are strongest predictors"
- "Segments 3-4 show highest purchase intent"
- "Recommendation: STRONG GO for market entry"

---

## 🎓 Your Tableau Files

After completing, you'll have:
- **5 Dashboards** (Overview, Segmentation, Predictions, Recommendations, Executive)
- **20+ Sheets** (individual visualizations)
- **3 Data Sources** (Japanese, Indian, Summary)
- **Professional presentation** ready for stakeholders

**Good luck with your Tableau dashboards!** 📊✨
