# ABG Motors Market Entry Analysis

## Project Overview

Market entry analysis for ABG Motors (Japanese car manufacturer) to assess viability of entering the Indian automotive market.

**Goal**: Determine if Indian market can support minimum sales of 10,000-12,000 cars/year

## Key Results

✅ **STRONG GO RECOMMENDATION**

- **Predicted Sales**: 67,410 cars/year (from 70,000 customer sample)
- **Target Achievement**: 674% of minimum target
- **Model Performance**: ROC-AUC 0.76
- **Recommendation**: Proceed with market entry via phased rollout

## Project Structure

```
CAPSTONE PROJECT/
├── data/
│   ├── raw/                    # Original ODS datasets
│   ├── processed/              # Processed CSV files with predictions
│   └── tableau/                # Tableau-ready exports
├── src/                        # Python modules
│   ├── data_loader.py          # Load and validate datasets
│   ├── feature_engineering.py  # AGE_CAR segmentation & transformations
│   ├── model_builder.py        # Train Logistic Regression model
│   ├── indian_market_predictor.py  # Apply model to Indian market
│   └── tableau_export.py       # Prepare Tableau visualizations
├── models/                     # Saved model artifacts
├── reports/                    # Final business report
├── notebooks/                  # Jupyter notebooks (optional)
└── requirements.txt            # Python dependencies
```

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Complete Analysis

```bash
# Step 1: Load data
python src/data_loader.py

# Step 2: Feature engineering
python src/feature_engineering.py

# Step 3: Train model
python src/model_builder.py

# Step 4: Predict Indian market
python src/indian_market_predictor.py

# Step 5: Export for Tableau
python src/tableau_export.py
```

### 3. View Results

- **Final Report**: `reports/final_report.md`
- **Predictions**: `data/processed/indian_predictions.csv`
- **Tableau Data**: `data/tableau/`

## Datasets

### Japanese Dataset (Training)
- **Records**: 40,000 customers
- **Features**: ID, CURR_AGE, GENDER, ANN_INCOME (¥), AGE_CAR (days), PURCHASE (0/1)
- **Purchase Rate**: 57.58%

### Indian Dataset (Prediction)
- **Records**: 70,000 customers  
- **Features**: ID, CURR_AGE, GENDER, ANN_INCOME (₹), DT_MAINT (date)
- **Analysis Date**: July 1, 2019

## Methodology

### Feature Engineering
- **AGE_CAR Segmentation** (4 categories):
  - Segment 1: < 200 days
  - Segment 2: 200-360 days
  - Segment 3: 360-500 days
  - Segment 4: > 500 days
- Gender encoding (Male/Female)
- Feature standardization

### Model
- **Algorithm**: Logistic Regression
- **Rationale**: Interpretability for business insights
- **Performance**: ROC-AUC 0.76, Accuracy 68.5%
- **Validation**: 5-fold cross-validation

### Key Findings

**Top Predictors**:
1. **Income** (+0.43): Higher income → 54% more likely to purchase
2. **Segment 4** (+0.42): Old maintenance → 53% more likely to purchase
3. **Segment 3** (+0.38): Moderate delay → 46% more likely to purchase
4. **Age** (-0.13): Younger customers more likely to purchase

## Deliverables

✅ Classification model (Logistic Regression, ROC-AUC 0.76)  
✅ Model justification and decision documentation  
✅ Business interpretation of coefficients  
✅ Performance metrics (Accuracy, Precision, Recall, F1, ROC-AUC)  
✅ Indian market assessment (67,410 predicted purchases)  
✅ Tableau-ready visualization files  
✅ Comprehensive final report  

## Tableau Visualizations

Import these files into Tableau:
- `data/tableau/japanese_market.csv` - Japanese customer data
- `data/tableau/indian_market.csv` - Indian predictions
- `data/tableau/market_comparison_summary.csv` - Summary statistics

**Suggested Dashboards**:
1. Market Overview (Japan vs India comparison)
2. Customer Segmentation (by age, income, maintenance)
3. Prediction Analysis (probability distribution, confidence levels)
4. Business Recommendations

## Business Recommendations

### 1. Market Entry: STRONG GO ✅
Predicted sales far exceed target with substantial buffer.

### 2. Target Segments
- **Priority 1**: High income + old maintenance (segments 3-4)
- **Priority 2**: Middle income + moderate maintenance
- **Priority 3**: Younger demographics (25-45 years)

### 3. Marketing Strategy
- Partner with service centers to target overdue maintenance customers
- Digital marketing for younger demographics
- Premium positioning for high-income segments
- Trade-in programs for aging vehicles

### 4. Risk Mitigation
- Start with pilot launch in 2-3 cities
- Plan for 50% of predicted sales as conservative baseline
- Monitor actual vs predicted performance
- Phased rollout based on pilot results

## Technical Details

### Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 68.53% |
| Precision | 74.32% |
| Recall | 69.27% |
| F1-Score | 71.71% |
| ROC-AUC | **75.87%** |

### Cross-Validation
- 5-fold CV ROC-AUC: 0.7528 ± 0.0048
- Consistent performance across folds

### Feature Coefficients

| Feature | Coefficient | Impact |
|---------|-------------|--------|
| ANN_INCOME | +0.433 | Strong Positive |
| SEGMENT_4 | +0.422 | Strong Positive |
| SEGMENT_3 | +0.381 | Positive |
| SEGMENT_1 | -0.374 | Negative |
| SEGMENT_2 | -0.364 | Negative |
| CURR_AGE | -0.131 | Slight Negative |
| GENDER_M | +0.096 | Slight Positive |

## Dependencies

- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- odfpy >= 1.4.1 (for ODS file reading)
- joblib >= 1.3.0

## Web_Site_Link
   - link: https://tableau-quest-guide.lovable.app/

## Contact
LinkedIn: www.linkedin.com/in/maddydas07
