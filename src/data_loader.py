"""
Data Loader Module for ABG Motors Market Entry Analysis
Loads Japanese and Indian datasets from ODS format and performs initial validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Load and validate datasets for ABG Motors analysis"""
    
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
        self.japanese_data = None
        self.indian_data = None
        
    def load_japanese_data(self, filename='japan dataset.ods'):
        """
        Load Japanese dataset (training data)
        
        Returns:
            pd.DataFrame: Japanese dataset with columns:
                - ID, CURR_AGE, GENDER, ANN_INCOME, AGE_CAR, PURCHASE
        """
        filepath = self.data_dir / filename
        print(f"Loading Japanese dataset from: {filepath}")
        
        try:
            # Load ODS file
            self.japanese_data = pd.read_excel(filepath, engine='odf')
            
            # Display basic info
            print(f"\n✓ Japanese dataset loaded successfully!")
            print(f"  Shape: {self.japanese_data.shape}")
            print(f"  Columns: {list(self.japanese_data.columns)}")
            
            # Data quality checks
            self._validate_japanese_data()
            
            return self.japanese_data
            
        except Exception as e:
            print(f"✗ Error loading Japanese dataset: {e}")
            raise
    
    def load_indian_data(self, filename='indian dataset.ods'):
        """
        Load Indian dataset (prediction data)
        
        Returns:
            pd.DataFrame: Indian dataset with columns:
                - ID, CURR_AGE, GENDER, ANN_INCOME, DT_MAINT
        """
        filepath = self.data_dir / filename
        print(f"Loading Indian dataset from: {filepath}")
        
        try:
            # Load ODS file
            self.indian_data = pd.read_excel(filepath, engine='odf')
            
            # Display basic info
            print(f"\n✓ Indian dataset loaded successfully!")
            print(f"  Shape: {self.indian_data.shape}")
            print(f"  Columns: {list(self.indian_data.columns)}")
            
            # Data quality checks
            self._validate_indian_data()
            
            return self.indian_data
            
        except Exception as e:
            print(f"✗ Error loading Indian dataset: {e}")
            raise
    
    def _validate_japanese_data(self):
        """Validate Japanese dataset structure and quality"""
        print("\n" + "="*60)
        print("JAPANESE DATASET VALIDATION")
        print("="*60)
        
        # Check for missing values
        missing = self.japanese_data.isnull().sum()
        print(f"\nMissing Values:")
        print(missing)
        
        # Check data types
        print(f"\nData Types:")
        print(self.japanese_data.dtypes)
        
        # Basic statistics
        print(f"\nBasic Statistics:")
        print(self.japanese_data.describe())
        
        # Target variable distribution
        if 'PURCHASE' in self.japanese_data.columns:
            purchase_dist = self.japanese_data['PURCHASE'].value_counts()
            purchase_rate = self.japanese_data['PURCHASE'].mean()
            print(f"\nTarget Variable (PURCHASE) Distribution:")
            print(purchase_dist)
            print(f"Purchase Rate: {purchase_rate:.2%}")
        
        # Gender distribution
        if 'GENDER' in self.japanese_data.columns:
            print(f"\nGender Distribution:")
            print(self.japanese_data['GENDER'].value_counts())
    
    def _validate_indian_data(self):
        """Validate Indian dataset structure and quality"""
        print("\n" + "="*60)
        print("INDIAN DATASET VALIDATION")
        print("="*60)
        
        # Check for missing values
        missing = self.indian_data.isnull().sum()
        print(f"\nMissing Values:")
        print(missing)
        
        # Check data types
        print(f"\nData Types:")
        print(self.indian_data.dtypes)
        
        # Basic statistics
        print(f"\nBasic Statistics:")
        print(self.indian_data.describe())
        
        # Gender distribution
        if 'GENDER' in self.indian_data.columns:
            print(f"\nGender Distribution:")
            print(self.indian_data['GENDER'].value_counts())
        
        # Check DT_MAINT format
        if 'DT_MAINT' in self.indian_data.columns:
            print(f"\nDT_MAINT Sample Values:")
            print(self.indian_data['DT_MAINT'].head(10))
    
    def save_to_csv(self, output_dir='data/processed'):
        """Save loaded datasets to CSV format for easier processing"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if self.japanese_data is not None:
            japanese_csv = output_path / 'japanese_raw.csv'
            self.japanese_data.to_csv(japanese_csv, index=False)
            print(f"\n✓ Japanese data saved to: {japanese_csv}")
        
        if self.indian_data is not None:
            indian_csv = output_path / 'indian_raw.csv'
            self.indian_data.to_csv(indian_csv, index=False)
            print(f"✓ Indian data saved to: {indian_csv}")
    
    def get_data_summary(self):
        """Get summary comparison of both datasets"""
        print("\n" + "="*60)
        print("DATASET COMPARISON SUMMARY")
        print("="*60)
        
        if self.japanese_data is not None and self.indian_data is not None:
            summary = pd.DataFrame({
                'Japanese Dataset': [
                    self.japanese_data.shape[0],
                    self.japanese_data.shape[1],
                    list(self.japanese_data.columns)
                ],
                'Indian Dataset': [
                    self.indian_data.shape[0],
                    self.indian_data.shape[1],
                    list(self.indian_data.columns)
                ]
            }, index=['Rows', 'Columns', 'Column Names'])
            
            print(summary)
            return summary


def main():
    """Main execution function"""
    print("="*60)
    print("ABG MOTORS - DATA LOADING MODULE")
    print("="*60)
    
    # Initialize loader
    loader = DataLoader(data_dir='data/raw')
    
    # Load datasets
    japanese_df = loader.load_japanese_data()
    indian_df = loader.load_indian_data()
    
    # Get summary
    loader.get_data_summary()
    
    # Save to CSV
    loader.save_to_csv()
    
    print("\n" + "="*60)
    print("DATA LOADING COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return japanese_df, indian_df


if __name__ == "__main__":
    japanese_data, indian_data = main()
