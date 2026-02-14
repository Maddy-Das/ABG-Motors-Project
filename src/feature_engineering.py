"""
Feature Engineering Module for ABG Motors Market Entry Analysis
Handles AGE_CAR segmentation and feature transformations
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


class FeatureEngineer:
    """Feature engineering for ABG Motors analysis"""
    
    def __init__(self):
        self.reference_date = datetime(2019, 7, 1)  # July 1, 2019
        
    def create_age_car_segments(self, df, age_car_column='AGE_CAR'):
        """
        Create 4 categorical segments from AGE_CAR (days since last maintenance)
        
        Segments:
            1: < 200 days
            2: 200-360 days
            3: 360-500 days
            4: > 500 days
        
        Args:
            df: DataFrame with AGE_CAR column
            age_car_column: Name of the column containing days since maintenance
            
        Returns:
            DataFrame with new AGE_CAR_SEGMENT column
        """
        df = df.copy()
        
        def segment_age_car(days):
            if days < 200:
                return 1
            elif days < 360:
                return 2
            elif days < 500:
                return 3
            else:
                return 4
        
        df['AGE_CAR_SEGMENT'] = df[age_car_column].apply(segment_age_car)
        
        print(f"\nAGE_CAR Segmentation Distribution:")
        print(df['AGE_CAR_SEGMENT'].value_counts().sort_index())
        
        return df
    
    def convert_indian_dates_to_age_car(self, df, date_column='DT_MAINT'):
        """
        Convert Indian dataset DT_MAINT to AGE_CAR (days since maintenance)
        Reference date: July 1, 2019
        
        Args:
            df: Indian DataFrame with DT_MAINT column
            date_column: Name of the date column
            
        Returns:
            DataFrame with AGE_CAR column
        """
        df = df.copy()
        
        # Convert string dates to datetime
        df[date_column] = pd.to_datetime(df[date_column], format='mixed')
        
        # Calculate days difference
        df['AGE_CAR'] = (self.reference_date - df[date_column]).dt.days
        
        print(f"\nIndian Dataset - AGE_CAR Statistics:")
        print(df['AGE_CAR'].describe())
        
        # Check for any negative values (maintenance after reference date)
        negative_count = (df['AGE_CAR'] < 0).sum()
        if negative_count > 0:
            print(f"\n⚠ Warning: {negative_count} records have maintenance dates after July 1, 2019")
            print("These will be handled appropriately.")
            # Set negative values to 0 (very recent maintenance)
            df.loc[df['AGE_CAR'] < 0, 'AGE_CAR'] = 0
        
        return df
    
    def encode_gender(self, df):
        """One-hot encode GENDER column"""
        df = df.copy()
        df['GENDER_M'] = (df['GENDER'] == 'M').astype(int)
        df['GENDER_F'] = (df['GENDER'] == 'F').astype(int)
        return df
    
    def prepare_japanese_features(self, df):
        """
        Complete feature engineering for Japanese dataset
        
        Args:
            df: Raw Japanese DataFrame
            
        Returns:
            DataFrame ready for modeling
        """
        print("="*60)
        print("JAPANESE DATASET - FEATURE ENGINEERING")
        print("="*60)
        
        df = df.copy()
        
        # Create AGE_CAR segments
        df = self.create_age_car_segments(df, 'AGE_CAR')
        
        # Encode gender
        df = self.encode_gender(df)
        
        # Create dummy variables for AGE_CAR_SEGMENT
        segment_dummies = pd.get_dummies(df['AGE_CAR_SEGMENT'], prefix='SEGMENT')
        df = pd.concat([df, segment_dummies], axis=1)
        
        print(f"\n✓ Japanese features prepared!")
        print(f"  Final shape: {df.shape}")
        print(f"  New columns: {[col for col in df.columns if col not in ['ID', 'CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR', 'PURCHASE']]}")
        
        return df
    
    def prepare_indian_features(self, df):
        """
        Complete feature engineering for Indian dataset
        
        Args:
            df: Raw Indian DataFrame
            
        Returns:
            DataFrame ready for prediction
        """
        print("\n" + "="*60)
        print("INDIAN DATASET - FEATURE ENGINEERING")
        print("="*60)
        
        df = df.copy()
        
        # Convert DT_MAINT to AGE_CAR
        df = self.convert_indian_dates_to_age_car(df, 'DT_MAINT')
        
        # Create AGE_CAR segments
        df = self.create_age_car_segments(df, 'AGE_CAR')
        
        # Encode gender
        df = self.encode_gender(df)
        
        # Create dummy variables for AGE_CAR_SEGMENT
        segment_dummies = pd.get_dummies(df['AGE_CAR_SEGMENT'], prefix='SEGMENT')
        df = pd.concat([df, segment_dummies], axis=1)
        
        print(f"\n✓ Indian features prepared!")
        print(f"  Final shape: {df.shape}")
        print(f"  New columns: {[col for col in df.columns if col not in ['ID', 'CURR_AGE', 'GENDER', 'ANN_INCOME', 'DT_MAINT']]}")
        
        return df
    
    def get_model_features(self):
        """Return list of features to use in modeling"""
        return [
            'CURR_AGE',
            'ANN_INCOME',
            'GENDER_M',
            'SEGMENT_1',
            'SEGMENT_2',
            'SEGMENT_3',
            'SEGMENT_4'
        ]


def main():
    """Main execution function"""
    print("="*60)
    print("ABG MOTORS - FEATURE ENGINEERING MODULE")
    print("="*60)
    
    # Load raw data
    japanese_df = pd.read_csv('data/processed/japanese_raw.csv')
    indian_df = pd.read_csv('data/processed/indian_raw.csv')
    
    # Initialize feature engineer
    fe = FeatureEngineer()
    
    # Prepare features
    japanese_processed = fe.prepare_japanese_features(japanese_df)
    indian_processed = fe.prepare_indian_features(indian_df)
    
    # Save processed data
    japanese_processed.to_csv('data/processed/japanese_processed.csv', index=False)
    indian_processed.to_csv('data/processed/indian_processed.csv', index=False)
    
    print("\n" + "="*60)
    print("FEATURE ENGINEERING COMPLETED!")
    print("="*60)
    print(f"✓ Japanese processed data saved to: data/processed/japanese_processed.csv")
    print(f"✓ Indian processed data saved to: data/processed/indian_processed.csv")
    
    # Display feature list
    print(f"\nModel Features: {fe.get_model_features()}")
    
    return japanese_processed, indian_processed


if __name__ == "__main__":
    japanese_data, indian_data = main()
