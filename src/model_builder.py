"""
Model Builder Module for ABG Motors Market Entry Analysis
Builds and trains classification model to predict car purchases
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class ModelBuilder:
    """Build and train classification model for purchase prediction"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.X_train = None
        self.X_val = None
        self.y_train = None
        self.y_val = None
        
    def prepare_data(self, df, feature_columns, target_column='PURCHASE', test_size=0.3):
        """
        Prepare data for modeling
        
        Args:
            df: Processed DataFrame
            feature_columns: List of feature column names
            target_column: Target variable name
            test_size: Validation set proportion
            
        Returns:
            X_train, X_val, y_train, y_val
        """
        print("="*60)
        print("DATA PREPARATION FOR MODELING")
        print("="*60)
        
        # Extract features and target
        X = df[feature_columns].copy()
        y = df[target_column].copy()
        
        self.feature_names = feature_columns
        
        print(f"\nFeatures: {feature_columns}")
        print(f"Target: {target_column}")
        print(f"Dataset shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        print(f"Purchase rate: {y.mean():.2%}")
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        print(f"\nTrain set: {X_train.shape}")
        print(f"Validation set: {X_val.shape}")
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Convert back to DataFrame for easier handling
        self.X_train = pd.DataFrame(X_train_scaled, columns=feature_columns)
        self.X_val = pd.DataFrame(X_val_scaled, columns=feature_columns)
        self.y_train = y_train.reset_index(drop=True)
        self.y_val = y_val.reset_index(drop=True)
        
        return self.X_train, self.X_val, self.y_train, self.y_val
    
    def train_logistic_regression(self, C=1.0):
        """
        Train Logistic Regression model
        
        Args:
            C: Regularization parameter
            
        Returns:
            Trained model
        """
        print("\n" + "="*60)
        print("TRAINING LOGISTIC REGRESSION MODEL")
        print("="*60)
        
        self.model = LogisticRegression(
            C=C,
            random_state=self.random_state,
            max_iter=1000,
            solver='lbfgs'
        )
        
        self.model.fit(self.X_train, self.y_train)
        
        print(f"\n✓ Model trained successfully!")
        print(f"  Model type: Logistic Regression")
        print(f"  Regularization (C): {C}")
        
        return self.model
    
    def tune_hyperparameters(self):
        """
        Perform hyperparameter tuning using GridSearchCV
        
        Returns:
            Best model
        """
        print("\n" + "="*60)
        print("HYPERPARAMETER TUNING")
        print("="*60)
        
        param_grid = {
            'C': [0.01, 0.1, 1.0, 10.0, 100.0],
            'penalty': ['l2'],
            'solver': ['lbfgs']
        }
        
        grid_search = GridSearchCV(
            LogisticRegression(random_state=self.random_state, max_iter=1000),
            param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X_train, self.y_train)
        
        print(f"\n✓ Best parameters: {grid_search.best_params_}")
        print(f"  Best CV ROC-AUC: {grid_search.best_score_:.4f}")
        
        self.model = grid_search.best_estimator_
        
        return self.model
    
    def evaluate_model(self):
        """
        Evaluate model performance on validation set
        
        Returns:
            Dictionary of metrics
        """
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        # Predictions
        y_pred = self.model.predict(self.X_val)
        y_pred_proba = self.model.predict_proba(self.X_val)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(self.y_val, y_pred),
            'precision': precision_score(self.y_val, y_pred),
            'recall': recall_score(self.y_val, y_pred),
            'f1_score': f1_score(self.y_val, y_pred),
            'roc_auc': roc_auc_score(self.y_val, y_pred_proba)
        }
        
        # Display metrics
        print("\n📊 VALIDATION SET PERFORMANCE:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(self.y_val, y_pred)
        print(f"\n📈 CONFUSION MATRIX:")
        print(f"                Predicted")
        print(f"                No    Yes")
        print(f"  Actual No   {cm[0,0]:5d} {cm[0,1]:5d}")
        print(f"  Actual Yes  {cm[1,0]:5d} {cm[1,1]:5d}")
        
        # Classification Report
        print(f"\n📋 CLASSIFICATION REPORT:")
        print(classification_report(self.y_val, y_pred, target_names=['No Purchase', 'Purchase']))
        
        return metrics
    
    def get_coefficient_interpretation(self):
        """
        Get and interpret model coefficients
        
        Returns:
            DataFrame with coefficient interpretations
        """
        print("\n" + "="*60)
        print("MODEL COEFFICIENT INTERPRETATION")
        print("="*60)
        
        coefficients = pd.DataFrame({
            'Feature': self.feature_names,
            'Coefficient': self.model.coef_[0],
            'Abs_Coefficient': np.abs(self.model.coef_[0])
        }).sort_values('Abs_Coefficient', ascending=False)
        
        coefficients['Odds_Ratio'] = np.exp(coefficients['Coefficient'])
        
        print("\n📊 FEATURE COEFFICIENTS (sorted by importance):")
        print(coefficients.to_string(index=False))
        
        print("\n💡 BUSINESS INTERPRETATION:")
        print("-" * 60)
        
        for _, row in coefficients.iterrows():
            feature = row['Feature']
            coef = row['Coefficient']
            odds_ratio = row['Odds_Ratio']
            
            if coef > 0:
                direction = "INCREASES"
                impact = "positive"
            else:
                direction = "DECREASES"
                impact = "negative"
            
            print(f"\n{feature}:")
            print(f"  • Coefficient: {coef:.4f}")
            print(f"  • Odds Ratio: {odds_ratio:.4f}")
            print(f"  • Impact: {direction} purchase probability ({impact})")
            
            # Specific interpretations
            if feature == 'CURR_AGE':
                print(f"  • Business meaning: Each additional year of age changes purchase odds by {(odds_ratio-1)*100:.2f}%")
            elif feature == 'ANN_INCOME':
                print(f"  • Business meaning: Higher income customers are {'more' if coef > 0 else 'less'} likely to purchase")
            elif feature == 'GENDER_M':
                print(f"  • Business meaning: Males are {'more' if coef > 0 else 'less'} likely to purchase than females")
            elif 'SEGMENT' in feature:
                segment_num = feature.split('_')[1]
                print(f"  • Business meaning: Customers in maintenance segment {segment_num} have different purchase behavior")
        
        return coefficients
    
    def cross_validate(self, cv=5):
        """
        Perform cross-validation
        
        Args:
            cv: Number of folds
            
        Returns:
            Cross-validation scores
        """
        print("\n" + "="*60)
        print(f"CROSS-VALIDATION ({cv}-FOLD)")
        print("="*60)
        
        # Combine train and validation for CV
        X_full = pd.concat([self.X_train, self.X_val])
        y_full = pd.concat([self.y_train, self.y_val])
        
        cv_scores = cross_val_score(
            self.model, X_full, y_full, cv=cv, scoring='roc_auc', n_jobs=-1
        )
        
        print(f"\n📊 Cross-Validation ROC-AUC Scores:")
        for i, score in enumerate(cv_scores, 1):
            print(f"  Fold {i}: {score:.4f}")
        
        print(f"\n  Mean: {cv_scores.mean():.4f}")
        print(f"  Std:  {cv_scores.std():.4f}")
        
        return cv_scores
    
    def save_model(self, model_dir='models'):
        """Save trained model and scaler"""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, model_path / 'logistic_regression_model.pkl')
        joblib.dump(self.scaler, model_path / 'feature_scaler.pkl')
        
        # Save feature names
        with open(model_path / 'feature_names.txt', 'w') as f:
            f.write('\n'.join(self.feature_names))
        
        print(f"\n✓ Model saved to: {model_path}")


def main():
    """Main execution function"""
    print("="*60)
    print("ABG MOTORS - MODEL BUILDING MODULE")
    print("="*60)
    
    # Load processed data
    japanese_df = pd.read_csv('data/processed/japanese_processed.csv')
    
    # Define features
    feature_columns = [
        'CURR_AGE',
        'ANN_INCOME',
        'GENDER_M',
        'SEGMENT_1',
        'SEGMENT_2',
        'SEGMENT_3',
        'SEGMENT_4'
    ]
    
    # Initialize model builder
    builder = ModelBuilder(random_state=42)
    
    # Prepare data
    X_train, X_val, y_train, y_val = builder.prepare_data(
        japanese_df, feature_columns, target_column='PURCHASE', test_size=0.3
    )
    
    # Train model with hyperparameter tuning
    model = builder.tune_hyperparameters()
    
    # Evaluate model
    metrics = builder.evaluate_model()
    
    # Cross-validation
    cv_scores = builder.cross_validate(cv=5)
    
    # Interpret coefficients
    coefficients = builder.get_coefficient_interpretation()
    
    # Save model
    builder.save_model()
    
    print("\n" + "="*60)
    print("MODEL BUILDING COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return builder, metrics, coefficients


if __name__ == "__main__":
    builder, metrics, coefficients = main()
