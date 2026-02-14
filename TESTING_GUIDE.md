# ABG Motors Project - Testing Guide

## Overview

This guide provides comprehensive testing instructions for the ABG Motors Market Entry Analysis project.

---

## Quick Test - Run Everything

### Option 1: Master Script (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Run complete pipeline
python run_analysis.py
```

This will execute all 5 steps in sequence and display a summary.

### Option 2: Individual Module Testing
```bash
source venv/bin/activate

# Step 1: Data Loading
python src/data_loader.py

# Step 2: Feature Engineering
python src/feature_engineering.py

# Step 3: Model Training
python src/model_builder.py

# Step 4: Indian Market Prediction
python src/indian_market_predictor.py

# Step 5: Tableau Export
python src/tableau_export.py
```

---

## Detailed Testing Checklist

### ✅ 1. Environment Setup Test

```bash
# Check Python version (should be 3.8+)
python3 --version

# Check virtual environment
source venv/bin/activate
which python  # Should show venv path

# Verify dependencies
pip list | grep -E "pandas|scikit-learn|odfpy"
```

**Expected Output**: All packages installed correctly

---

### ✅ 2. Data Loading Test

```bash
python src/data_loader.py
```

**What to Verify**:
- ✅ Japanese dataset: 40,000 records loaded
- ✅ Indian dataset: 70,000 records loaded
- ✅ No missing values in either dataset
- ✅ Purchase rate in Japanese data: ~57.58%
- ✅ Files created in `data/processed/`:
  - `japanese_raw.csv`
  - `indian_raw.csv`

**Quick Check**:
```bash
# Verify files exist
ls -lh data/processed/*.csv

# Check row counts
wc -l data/processed/japanese_raw.csv  # Should be 40,001 (including header)
wc -l data/processed/indian_raw.csv    # Should be 70,001
```

---

### ✅ 3. Feature Engineering Test

```bash
python src/feature_engineering.py
```

**What to Verify**:
- ✅ AGE_CAR segmentation created (4 segments)
- ✅ Japanese segments distribution:
  - Segment 1: ~6,459
  - Segment 2: ~16,452
  - Segment 3: ~11,694
  - Segment 4: ~5,395
- ✅ Indian AGE_CAR calculated from DT_MAINT
- ✅ Reference date: July 1, 2019
- ✅ Files created:
  - `data/processed/japanese_processed.csv`
  - `data/processed/indian_processed.csv`

**Quick Check**:
```bash
# Verify segment columns exist
head -1 data/processed/japanese_processed.csv | grep "SEGMENT"

# Check for AGE_CAR in Indian data
head -1 data/processed/indian_processed.csv | grep "AGE_CAR"
```

---

### ✅ 4. Model Training Test

```bash
python src/model_builder.py
```

**What to Verify**:
- ✅ Train/validation split: 28,000 / 12,000
- ✅ Hyperparameter tuning completed (5-fold CV)
- ✅ Best parameters found: C=0.01
- ✅ Model performance metrics:
  - ROC-AUC: ~0.76 (should be > 0.70)
  - Accuracy: ~68.5%
  - Precision: ~74%
  - Recall: ~69%
- ✅ Cross-validation stable (std < 0.01)
- ✅ Coefficient interpretation displayed
- ✅ Model files saved in `models/`:
  - `logistic_regression_model.pkl`
  - `feature_scaler.pkl`
  - `feature_names.txt`

**Quick Check**:
```bash
# Verify model files
ls -lh models/

# Check feature names
cat models/feature_names.txt
```

**Expected Features**:
```
CURR_AGE
ANN_INCOME
GENDER_M
SEGMENT_1
SEGMENT_2
SEGMENT_3
SEGMENT_4
```

---

### ✅ 5. Indian Market Prediction Test

```bash
python src/indian_market_predictor.py
```

**What to Verify**:
- ✅ Model loaded successfully
- ✅ Predictions generated for 70,000 customers
- ✅ Predicted purchases: ~67,410
- ✅ Purchase rate: ~96.3%
- ✅ Target assessment: ✅ TARGET MET
- ✅ Surplus: ~57,410 cars
- ✅ Recommendation: "STRONG GO"
- ✅ Segmentation analysis displayed
- ✅ Files created:
  - `data/processed/indian_predictions.csv`
  - `data/tableau/indian_market_predictions.csv`

**Quick Check**:
```bash
# Count predictions
wc -l data/processed/indian_predictions.csv  # Should be 70,001

# Check prediction columns
head -1 data/processed/indian_predictions.csv | grep "PURCHASE_PREDICTION"

# Verify predicted purchases
python3 -c "import pandas as pd; df = pd.read_csv('data/processed/indian_predictions.csv'); print(f'Predicted Purchases: {df[\"PURCHASE_PREDICTION\"].sum():,}')"
```

**Expected Output**: `Predicted Purchases: 67,410`

---

### ✅ 6. Tableau Export Test

```bash
python src/tableau_export.py
```

**What to Verify**:
- ✅ Japanese market file: 40,000 records
- ✅ Indian market file: 70,000 records
- ✅ Summary statistics created
- ✅ Files in `data/tableau/`:
  - `japanese_market.csv`
  - `indian_market.csv`
  - `market_comparison_summary.csv`

**Quick Check**:
```bash
# Verify Tableau files
ls -lh data/tableau/

# Check summary
cat data/tableau/market_comparison_summary.csv
```

**Expected Summary**:
```
Metric,Japan,India
Total Customers,40000,70000
Purchase Count,23031,67410
Purchase Rate,57.58%,96.30%
...
```

---

## Validation Tests

### Test 1: Data Integrity

```bash
# Check for duplicate IDs
python3 -c "
import pandas as pd
jp = pd.read_csv('data/processed/japanese_raw.csv')
ind = pd.read_csv('data/processed/indian_raw.csv')
print(f'Japanese duplicates: {jp[\"ID\"].duplicated().sum()}')
print(f'Indian duplicates: {ind[\"ID\"].duplicated().sum()}')
"
```

**Expected**: Both should be 0

### Test 2: Segment Distribution

```bash
# Verify segment creation
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/japanese_processed.csv')
print('Segment Distribution:')
print(df['AGE_CAR_SEGMENT'].value_counts().sort_index())
"
```

**Expected**: 4 segments (1, 2, 3, 4)

### Test 3: Model Performance

```bash
# Quick model test
python3 -c "
import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load('models/logistic_regression_model.pkl')
scaler = joblib.load('models/feature_scaler.pkl')

# Load test data
df = pd.read_csv('data/processed/japanese_processed.csv').head(10)
features = ['CURR_AGE', 'ANN_INCOME', 'GENDER_M', 'SEGMENT_1', 'SEGMENT_2', 'SEGMENT_3', 'SEGMENT_4']
X = df[features]
X_scaled = scaler.transform(X)

# Predict
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

print('Sample Predictions:')
for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    print(f'  Customer {i+1}: Prediction={pred}, Probability={prob:.2%}')
"
```

**Expected**: Predictions (0 or 1) with probabilities

### Test 4: Prediction Consistency

```bash
# Verify prediction totals
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/indian_predictions.csv')
total = len(df)
purchases = df['PURCHASE_PREDICTION'].sum()
rate = purchases / total

print(f'Total Customers: {total:,}')
print(f'Predicted Purchases: {purchases:,}')
print(f'Purchase Rate: {rate:.2%}')
print(f'Target (10,000): {\"✅ MET\" if purchases >= 10000 else \"❌ NOT MET\"}')
print(f'Surplus/Deficit: {purchases - 10000:,}')
"
```

**Expected**: 
- Total: 70,000
- Purchases: ~67,410
- Rate: ~96.3%
- Target: ✅ MET

---

## Output Verification

### Check All Generated Files

```bash
# List all output files
echo "=== Data Files ==="
ls -lh data/processed/

echo -e "\n=== Model Files ==="
ls -lh models/

echo -e "\n=== Tableau Files ==="
ls -lh data/tableau/

echo -e "\n=== Report Files ==="
ls -lh reports/
```

**Expected Files**:

**data/processed/**:
- japanese_raw.csv
- japanese_processed.csv
- indian_raw.csv
- indian_processed.csv
- indian_predictions.csv

**models/**:
- logistic_regression_model.pkl
- feature_scaler.pkl
- feature_names.txt

**data/tableau/**:
- japanese_market.csv
- indian_market.csv
- market_comparison_summary.csv
- indian_market_predictions.csv

**reports/**:
- final_report.md

---

## Performance Benchmarks

### Expected Execution Times

| Step | Expected Time | File |
|------|---------------|------|
| Data Loading | 5-10 seconds | data_loader.py |
| Feature Engineering | 3-5 seconds | feature_engineering.py |
| Model Training | 10-20 seconds | model_builder.py |
| Prediction | 5-10 seconds | indian_market_predictor.py |
| Tableau Export | 5-10 seconds | tableau_export.py |
| **Total** | **~30-60 seconds** | run_analysis.py |

---

## Troubleshooting

### Issue 1: Module Not Found

```bash
# Solution: Activate virtual environment
source venv/bin/activate
```

### Issue 2: ODS File Not Found

```bash
# Solution: Check data files exist
ls -la data/raw/

# Should see:
# - indian dataset.ods
# - japan dataset.ods
```

### Issue 3: Model Performance Low

**Check**:
- ROC-AUC should be > 0.70
- If lower, verify data quality and feature engineering

### Issue 4: Prediction File Empty

```bash
# Verify model was trained first
ls -lh models/logistic_regression_model.pkl

# If missing, run:
python src/model_builder.py
```

---

## Final Validation Checklist

Run this comprehensive check:

```bash
#!/bin/bash
echo "=== ABG MOTORS PROJECT VALIDATION ==="
echo ""

# 1. Check environment
echo "✓ Checking Python environment..."
python3 --version

# 2. Check data files
echo "✓ Checking data files..."
test -f "data/raw/japan dataset.ods" && echo "  ✅ Japanese dataset exists" || echo "  ❌ Japanese dataset missing"
test -f "data/raw/indian dataset.ods" && echo "  ✅ Indian dataset exists" || echo "  ❌ Indian dataset missing"

# 3. Check processed files
echo "✓ Checking processed files..."
test -f "data/processed/japanese_processed.csv" && echo "  ✅ Japanese processed" || echo "  ❌ Japanese not processed"
test -f "data/processed/indian_processed.csv" && echo "  ✅ Indian processed" || echo "  ❌ Indian not processed"
test -f "data/processed/indian_predictions.csv" && echo "  ✅ Predictions generated" || echo "  ❌ Predictions missing"

# 4. Check model files
echo "✓ Checking model files..."
test -f "models/logistic_regression_model.pkl" && echo "  ✅ Model trained" || echo "  ❌ Model missing"

# 5. Check Tableau files
echo "✓ Checking Tableau files..."
test -f "data/tableau/japanese_market.csv" && echo "  ✅ Japanese Tableau data" || echo "  ❌ Missing"
test -f "data/tableau/indian_market.csv" && echo "  ✅ Indian Tableau data" || echo "  ❌ Missing"

# 6. Check report
echo "✓ Checking report..."
test -f "reports/final_report.md" && echo "  ✅ Final report exists" || echo "  ❌ Report missing"

echo ""
echo "=== VALIDATION COMPLETE ==="
```

Save this as `validate_project.sh`, make it executable, and run:

```bash
chmod +x validate_project.sh
./validate_project.sh
```

---

## Testing for Presentation

### Demo Script

```bash
# Clean slate (optional - only if you want to re-run everything)
rm -rf data/processed/* data/tableau/* models/*

# Run complete analysis
source venv/bin/activate
python run_analysis.py

# Show key results
echo "=== KEY RESULTS ==="
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/indian_predictions.csv')
print(f'📊 Predicted Purchases: {df[\"PURCHASE_PREDICTION\"].sum():,}')
print(f'🎯 Target: 10,000')
print(f'✅ Achievement: {(df[\"PURCHASE_PREDICTION\"].sum()/10000*100):.0f}%')
print(f'💡 Recommendation: STRONG GO')
"
```

---

## Success Criteria

Your project passes testing if:

- ✅ All 5 modules run without errors
- ✅ Model ROC-AUC > 0.70
- ✅ Predicted purchases > 10,000
- ✅ All output files generated
- ✅ Tableau files contain correct data
- ✅ Final report is comprehensive

---

## Next Steps After Testing

1. **Review Final Report**: `reports/final_report.md`
2. **Import to Tableau**: Use files in `data/tableau/`
3. **Prepare Presentation**: Use walkthrough.md as guide
4. **Document Findings**: All insights in final report

---

**Project Status**: ✅ READY FOR SUBMISSION
