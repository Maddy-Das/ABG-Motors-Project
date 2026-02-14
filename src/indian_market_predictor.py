"""
Indian Market Predictor Module for ABG Motors Market Entry Analysis
Applies trained model to Indian dataset and assesses market viability
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path


class IndianMarketPredictor:
    """Predict purchases in Indian market and assess viability"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.predictions = None
        
    def load_model(self):
        """Load trained model and scaler"""
        print("="*60)
        print("LOADING TRAINED MODEL")
        print("="*60)
        
        self.model = joblib.load(self.model_dir / 'logistic_regression_model.pkl')
        self.scaler = joblib.load(self.model_dir / 'feature_scaler.pkl')
        
        with open(self.model_dir / 'feature_names.txt', 'r') as f:
            self.feature_names = [line.strip() for line in f.readlines()]
        
        print(f"\n✓ Model loaded successfully!")
        print(f"  Features: {self.feature_names}")
        
    def predict_indian_market(self, indian_df):
        """
        Apply model to Indian dataset
        
        Args:
            indian_df: Processed Indian DataFrame
            
        Returns:
            DataFrame with predictions
        """
        print("\n" + "="*60)
        print("PREDICTING INDIAN MARKET PURCHASES")
        print("="*60)
        
        # Extract features
        X = indian_df[self.feature_names].copy()
        
        print(f"\nIndian dataset shape: {X.shape}")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        # Add predictions to dataframe
        result_df = indian_df.copy()
        result_df['PURCHASE_PREDICTION'] = predictions
        result_df['PURCHASE_PROBABILITY'] = probabilities
        
        self.predictions = result_df
        
        print(f"\n✓ Predictions completed!")
        print(f"  Total customers: {len(result_df):,}")
        print(f"  Predicted purchases: {predictions.sum():,}")
        print(f"  Predicted purchase rate: {predictions.mean():.2%}")
        
        return result_df
    
    def assess_market_viability(self, target_sales=10000):
        """
        Assess if Indian market can meet sales target
        
        Args:
            target_sales: Minimum required sales (default: 10,000)
            
        Returns:
            Assessment dictionary
        """
        print("\n" + "="*60)
        print("MARKET VIABILITY ASSESSMENT")
        print("="*60)
        
        predicted_purchases = self.predictions['PURCHASE_PREDICTION'].sum()
        total_customers = len(self.predictions)
        purchase_rate = self.predictions['PURCHASE_PREDICTION'].mean()
        
        # Calculate confidence intervals using probability distribution
        high_confidence = (self.predictions['PURCHASE_PROBABILITY'] >= 0.7).sum()
        medium_confidence = ((self.predictions['PURCHASE_PROBABILITY'] >= 0.5) & 
                            (self.predictions['PURCHASE_PROBABILITY'] < 0.7)).sum()
        low_confidence = ((self.predictions['PURCHASE_PROBABILITY'] >= 0.3) & 
                         (self.predictions['PURCHASE_PROBABILITY'] < 0.5)).sum()
        
        assessment = {
            'total_customers': total_customers,
            'predicted_purchases': predicted_purchases,
            'purchase_rate': purchase_rate,
            'target_sales': target_sales,
            'target_met': predicted_purchases >= target_sales,
            'surplus_deficit': predicted_purchases - target_sales,
            'high_confidence_buyers': high_confidence,
            'medium_confidence_buyers': medium_confidence,
            'low_confidence_buyers': low_confidence
        }
        
        print(f"\n📊 MARKET SIZE ANALYSIS:")
        print(f"  Total customers in dataset: {total_customers:,}")
        print(f"  Predicted purchases: {predicted_purchases:,}")
        print(f"  Purchase rate: {purchase_rate:.2%}")
        
        print(f"\n🎯 TARGET ASSESSMENT:")
        print(f"  Sales target: {target_sales:,} cars/year")
        print(f"  Predicted sales: {predicted_purchases:,} cars/year")
        
        if assessment['target_met']:
            print(f"  ✅ TARGET MET! Surplus: {assessment['surplus_deficit']:,} cars")
        else:
            print(f"  ❌ TARGET NOT MET. Deficit: {abs(assessment['surplus_deficit']):,} cars")
        
        print(f"\n📈 CUSTOMER CONFIDENCE BREAKDOWN:")
        print(f"  High confidence (≥70% probability): {high_confidence:,} customers")
        print(f"  Medium confidence (50-70%): {medium_confidence:,} customers")
        print(f"  Low confidence (30-50%): {low_confidence:,} customers")
        
        # Recommendation
        print(f"\n💡 RECOMMENDATION:")
        if predicted_purchases >= target_sales * 1.2:
            recommendation = "STRONG GO - Market shows strong potential with significant surplus"
        elif predicted_purchases >= target_sales:
            recommendation = "GO - Market meets target with moderate buffer"
        elif predicted_purchases >= target_sales * 0.8:
            recommendation = "CAUTIOUS GO - Close to target, requires marketing push"
        else:
            recommendation = "NO GO - Market unlikely to meet minimum target"
        
        print(f"  {recommendation}")
        assessment['recommendation'] = recommendation
        
        return assessment
    
    def segment_analysis(self):
        """Analyze predictions by customer segments"""
        print("\n" + "="*60)
        print("SEGMENTATION ANALYSIS")
        print("="*60)
        
        # By Age Group
        print("\n📊 BY AGE GROUP:")
        age_bins = [0, 30, 40, 50, 60, 100]
        age_labels = ['<30', '30-40', '40-50', '50-60', '60+']
        self.predictions['AGE_GROUP'] = pd.cut(
            self.predictions['CURR_AGE'], bins=age_bins, labels=age_labels
        )
        
        age_analysis = self.predictions.groupby('AGE_GROUP').agg({
            'PURCHASE_PREDICTION': ['count', 'sum', 'mean']
        }).round(4)
        print(age_analysis)
        
        # By Gender
        print("\n📊 BY GENDER:")
        gender_analysis = self.predictions.groupby('GENDER').agg({
            'PURCHASE_PREDICTION': ['count', 'sum', 'mean']
        }).round(4)
        print(gender_analysis)
        
        # By Maintenance Segment
        print("\n📊 BY MAINTENANCE SEGMENT:")
        segment_analysis = self.predictions.groupby('AGE_CAR_SEGMENT').agg({
            'PURCHASE_PREDICTION': ['count', 'sum', 'mean']
        }).round(4)
        print(segment_analysis)
        
        # By Income Quartile
        print("\n📊 BY INCOME QUARTILE:")
        self.predictions['INCOME_QUARTILE'] = pd.qcut(
            self.predictions['ANN_INCOME'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
        )
        income_analysis = self.predictions.groupby('INCOME_QUARTILE').agg({
            'PURCHASE_PREDICTION': ['count', 'sum', 'mean']
        }).round(4)
        print(income_analysis)
    
    def save_predictions(self, output_dir='data/processed'):
        """Save predictions to CSV"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save full predictions
        predictions_file = output_path / 'indian_predictions.csv'
        self.predictions.to_csv(predictions_file, index=False)
        
        # Save summary for Tableau
        tableau_file = Path('data/tableau') / 'indian_market_predictions.csv'
        tableau_file.parent.mkdir(parents=True, exist_ok=True)
        
        tableau_df = self.predictions[[
            'ID', 'CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR', 'AGE_CAR_SEGMENT',
            'PURCHASE_PREDICTION', 'PURCHASE_PROBABILITY'
        ]].copy()
        tableau_df.to_csv(tableau_file, index=False)
        
        print(f"\n✓ Predictions saved to: {predictions_file}")
        print(f"✓ Tableau data saved to: {tableau_file}")


def main():
    """Main execution function"""
    print("="*60)
    print("ABG MOTORS - INDIAN MARKET PREDICTION MODULE")
    print("="*60)
    
    # Load processed Indian data
    indian_df = pd.read_csv('data/processed/indian_processed.csv')
    
    # Initialize predictor
    predictor = IndianMarketPredictor(model_dir='models')
    
    # Load model
    predictor.load_model()
    
    # Make predictions
    predictions = predictor.predict_indian_market(indian_df)
    
    # Assess market viability
    assessment = predictor.assess_market_viability(target_sales=10000)
    
    # Segment analysis
    predictor.segment_analysis()
    
    # Save predictions
    predictor.save_predictions()
    
    print("\n" + "="*60)
    print("INDIAN MARKET PREDICTION COMPLETED!")
    print("="*60)
    
    return predictor, assessment


if __name__ == "__main__":
    predictor, assessment = main()
