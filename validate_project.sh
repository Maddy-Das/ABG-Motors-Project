#!/bin/bash

echo "============================================================"
echo "       ABG MOTORS PROJECT - VALIDATION SCRIPT"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Python environment
echo "📋 Checking Python environment..."
if command -v python3 &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Python3 installed: $(python3 --version)"
else
    echo -e "  ${RED}✗${NC} Python3 not found"
    exit 1
fi

# 2. Check virtual environment
echo ""
echo "📋 Checking virtual environment..."
if [ -d "venv" ]; then
    echo -e "  ${GREEN}✓${NC} Virtual environment exists"
else
    echo -e "  ${YELLOW}⚠${NC} Virtual environment not found"
fi

# 3. Check raw data files
echo ""
echo "📋 Checking raw data files..."
if [ -f "data/raw/japan dataset.ods" ]; then
    echo -e "  ${GREEN}✓${NC} Japanese dataset exists ($(du -h "data/raw/japan dataset.ods" | cut -f1))"
else
    echo -e "  ${RED}✗${NC} Japanese dataset missing"
fi

if [ -f "data/raw/indian dataset.ods" ]; then
    echo -e "  ${GREEN}✓${NC} Indian dataset exists ($(du -h "data/raw/indian dataset.ods" | cut -f1))"
else
    echo -e "  ${RED}✗${NC} Indian dataset missing"
fi

# 4. Check processed files
echo ""
echo "📋 Checking processed data files..."
for file in "japanese_raw.csv" "japanese_processed.csv" "indian_raw.csv" "indian_processed.csv" "indian_predictions.csv"; do
    if [ -f "data/processed/$file" ]; then
        rows=$(wc -l < "data/processed/$file")
        echo -e "  ${GREEN}✓${NC} $file ($((rows-1)) records)"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# 5. Check model files
echo ""
echo "📋 Checking model files..."
for file in "logistic_regression_model.pkl" "feature_scaler.pkl" "feature_names.txt"; do
    if [ -f "models/$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# 6. Check Tableau files
echo ""
echo "📋 Checking Tableau export files..."
for file in "japanese_market.csv" "indian_market.csv" "market_comparison_summary.csv"; do
    if [ -f "data/tableau/$file" ]; then
        rows=$(wc -l < "data/tableau/$file")
        echo -e "  ${GREEN}✓${NC} $file ($((rows-1)) records)"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# 7. Check reports
echo ""
echo "📋 Checking reports..."
if [ -f "reports/final_report.md" ]; then
    lines=$(wc -l < "reports/final_report.md")
    echo -e "  ${GREEN}✓${NC} Final report exists ($lines lines)"
else
    echo -e "  ${RED}✗${NC} Final report missing"
fi

# 8. Validate predictions (if Python available)
echo ""
echo "📋 Validating predictions..."
if [ -f "data/processed/indian_predictions.csv" ]; then
    python3 << EOF
import pandas as pd
try:
    df = pd.read_csv('data/processed/indian_predictions.csv')
    total = len(df)
    purchases = df['PURCHASE_PREDICTION'].sum()
    rate = purchases / total
    
    print(f"  Total customers: {total:,}")
    print(f"  Predicted purchases: {purchases:,}")
    print(f"  Purchase rate: {rate:.2%}")
    
    if purchases >= 10000:
        print(f"  \033[0;32m✓\033[0m Target (10,000) MET - Surplus: {purchases - 10000:,}")
    else:
        print(f"  \033[0;31m✗\033[0m Target (10,000) NOT MET - Deficit: {10000 - purchases:,}")
except Exception as e:
    print(f"  \033[0;31m✗\033[0m Error validating predictions: {e}")
EOF
else
    echo -e "  ${YELLOW}⚠${NC} Predictions file not found - run indian_market_predictor.py"
fi

# 9. Summary
echo ""
echo "============================================================"
echo "                  VALIDATION SUMMARY"
echo "============================================================"
echo ""

# Count files
processed_count=$(ls data/processed/*.csv 2>/dev/null | wc -l)
model_count=$(ls models/*.pkl 2>/dev/null | wc -l)
tableau_count=$(ls data/tableau/*.csv 2>/dev/null | wc -l)

echo "📊 Files Generated:"
echo "  • Processed data files: $processed_count/5"
echo "  • Model files: $model_count/2"
echo "  • Tableau files: $tableau_count/3"

if [ $processed_count -eq 5 ] && [ $model_count -eq 2 ] && [ $tableau_count -ge 3 ]; then
    echo ""
    echo -e "${GREEN}✅ PROJECT VALIDATION PASSED${NC}"
    echo ""
    echo "🎉 All deliverables are ready!"
    echo ""
    echo "Next steps:"
    echo "  1. Review: reports/final_report.md"
    echo "  2. Import Tableau files from: data/tableau/"
    echo "  3. Present findings to stakeholders"
else
    echo ""
    echo -e "${YELLOW}⚠ PROJECT INCOMPLETE${NC}"
    echo ""
    echo "Missing files detected. Run:"
    echo "  source venv/bin/activate"
    echo "  python run_analysis.py"
fi

echo ""
echo "============================================================"
