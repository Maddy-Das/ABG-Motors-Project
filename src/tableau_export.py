"""
Tableau Export Module for ABG Motors Market Entry Analysis
Prepares data for Tableau visualization
"""

import pandas as pd
import numpy as np
from pathlib import Path


def prepare_japanese_tableau_data():
    """Prepare Japanese dataset for Tableau"""
    print("="*60)
    print("PREPARING JAPANESE DATA FOR TABLEAU")
    print("="*60)
    
    df = pd.read_csv('data/processed/japanese_processed.csv')
    
    # Select relevant columns
    tableau_df = df[[
        'ID', 'CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR', 
        'AGE_CAR_SEGMENT', 'PURCHASE'
    ]].copy()
    
    # Add descriptive labels
    tableau_df['COUNTRY'] = 'Japan'
    tableau_df['SEGMENT_LABEL'] = tableau_df['AGE_CAR_SEGMENT'].map({
        1: 'Segment 1 (<200 days)',
        2: 'Segment 2 (200-360 days)',
        3: 'Segment 3 (360-500 days)',
        4: 'Segment 4 (>500 days)'
    })
    
    # Age groups
    tableau_df['AGE_GROUP'] = pd.cut(
        tableau_df['CURR_AGE'],
        bins=[0, 30, 40, 50, 60, 100],
        labels=['<30', '30-40', '40-50', '50-60', '60+']
    )
    
    # Income quartiles
    tableau_df['INCOME_QUARTILE'] = pd.qcut(
        tableau_df['ANN_INCOME'],
        q=4,
        labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
    )
    
    output_file = Path('data/tableau') / 'japanese_market.csv'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    tableau_df.to_csv(output_file, index=False)
    
    print(f"✓ Japanese Tableau data saved: {output_file}")
    print(f"  Records: {len(tableau_df):,}")
    
    return tableau_df


def prepare_indian_tableau_data():
    """Prepare Indian dataset with predictions for Tableau"""
    print("\n" + "="*60)
    print("PREPARING INDIAN DATA FOR TABLEAU")
    print("="*60)
    
    df = pd.read_csv('data/processed/indian_predictions.csv')
    
    # Select relevant columns
    tableau_df = df[[
        'ID', 'CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR',
        'AGE_CAR_SEGMENT', 'PURCHASE_PREDICTION', 'PURCHASE_PROBABILITY'
    ]].copy()
    
    # Add descriptive labels
    tableau_df['COUNTRY'] = 'India'
    tableau_df['SEGMENT_LABEL'] = tableau_df['AGE_CAR_SEGMENT'].map({
        1: 'Segment 1 (<200 days)',
        2: 'Segment 2 (200-360 days)',
        3: 'Segment 3 (360-500 days)',
        4: 'Segment 4 (>500 days)'
    })
    
    # Age groups
    tableau_df['AGE_GROUP'] = pd.cut(
        tableau_df['CURR_AGE'],
        bins=[0, 30, 40, 50, 60, 100],
        labels=['<30', '30-40', '40-50', '50-60', '60+']
    )
    
    # Income quartiles
    tableau_df['INCOME_QUARTILE'] = pd.qcut(
        tableau_df['ANN_INCOME'],
        q=4,
        labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
    )
    
    # Confidence categories
    tableau_df['CONFIDENCE_CATEGORY'] = pd.cut(
        tableau_df['PURCHASE_PROBABILITY'],
        bins=[0, 0.3, 0.5, 0.7, 1.0],
        labels=['Low (<30%)', 'Medium (30-50%)', 'High (50-70%)', 'Very High (>70%)']
    )
    
    output_file = Path('data/tableau') / 'indian_market.csv'
    tableau_df.to_csv(output_file, index=False)
    
    print(f"✓ Indian Tableau data saved: {output_file}")
    print(f"  Records: {len(tableau_df):,}")
    print(f"  Predicted Purchases: {tableau_df['PURCHASE_PREDICTION'].sum():,}")
    
    return tableau_df


def create_summary_statistics():
    """Create summary statistics for dashboard"""
    print("\n" + "="*60)
    print("CREATING SUMMARY STATISTICS")
    print("="*60)
    
    # Load data
    japanese_df = pd.read_csv('data/processed/japanese_processed.csv')
    indian_df = pd.read_csv('data/processed/indian_predictions.csv')
    
    summary = {
        'Metric': [
            'Total Customers',
            'Purchase Count',
            'Purchase Rate',
            'Avg Age',
            'Male %',
            'Avg Income'
        ],
        'Japan': [
            len(japanese_df),
            japanese_df['PURCHASE'].sum(),
            f"{japanese_df['PURCHASE'].mean():.2%}",
            f"{japanese_df['CURR_AGE'].mean():.1f}",
            f"{(japanese_df['GENDER'] == 'M').mean():.2%}",
            f"¥{japanese_df['ANN_INCOME'].mean():,.0f}"
        ],
        'India': [
            len(indian_df),
            indian_df['PURCHASE_PREDICTION'].sum(),
            f"{indian_df['PURCHASE_PREDICTION'].mean():.2%}",
            f"{indian_df['CURR_AGE'].mean():.1f}",
            f"{(indian_df['GENDER'] == 'M').mean():.2%}",
            f"₹{indian_df['ANN_INCOME'].mean():,.0f}"
        ]
    }
    
    summary_df = pd.DataFrame(summary)
    
    output_file = Path('data/tableau') / 'market_comparison_summary.csv'
    summary_df.to_csv(output_file, index=False)
    
    print(f"✓ Summary statistics saved: {output_file}")
    print("\n" + summary_df.to_string(index=False))
    
    return summary_df


def main():
    """Main execution function"""
    print("="*60)
    print("ABG MOTORS - TABLEAU EXPORT MODULE")
    print("="*60)
    
    # Prepare datasets
    japanese_tableau = prepare_japanese_tableau_data()
    indian_tableau = prepare_indian_tableau_data()
    summary = create_summary_statistics()
    
    print("\n" + "="*60)
    print("TABLEAU EXPORT COMPLETED!")
    print("="*60)
    print("\n📊 Files ready for Tableau:")
    print("  • data/tableau/japanese_market.csv")
    print("  • data/tableau/indian_market.csv")
    print("  • data/tableau/market_comparison_summary.csv")
    
    return japanese_tableau, indian_tableau, summary


if __name__ == "__main__":
    japanese_data, indian_data, summary = main()
