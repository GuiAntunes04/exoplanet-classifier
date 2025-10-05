#!/usr/bin/env python3
"""
API usage example for the Exoplanet Classifier
This file demonstrates how to use the model programmatically
"""

import pandas as pd
import numpy as np
import joblib
from typing import Dict, List, Tuple

class ExoplanetClassifier:
    """Class for exoplanet classification."""
    
    def __init__(self, model_path: str = "data/model_and_features.pkl"):
        """
        Initialize the classifier.
        
        Args:
            model_path: Path to the model file
        """
        self.model_path = model_path
        self.model = None
        self.features = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data[0]
            self.features = model_data[1]
            print(f"✅ Model loaded with {len(self.features)} features")
        except FileNotFoundError:
            print(f"❌ Model not found in {self.model_path}")
            raise
    
    def prepare_data(self, data: Dict) -> pd.DataFrame:
        """
        Prepare data for classification.
        
        Args:
            data: Dictionary with exoplanet data
            
        Returns:
            Processed DataFrame
        """
        # Create DataFrame
        df = pd.DataFrame([data])
        
        # Mission treatment
        if 'mission' not in df.columns or df['mission'].isna().all():
            df['mission'] = 'UNCLASSIFIED'
        
        # Binary flags treatment
        binary_cols = [col for col in self.features if 'fpflag' in col]
        for col in binary_cols:
            if col not in df.columns:
                df[col] = pd.NA
        df[binary_cols] = df[binary_cols].fillna(0)
        
        # One-hot encoding
        df = pd.get_dummies(df, columns=['mission'], drop_first=False)
        
        # Ensure column consistency
        ohe_cols = [col for col in self.features if 'mission_' in col]
        for col in ohe_cols:
            if col not in df.columns:
                df[col] = 0
        
        # Final imputation
        df = df.fillna(-999)
        
        return df[self.features]
    
    def classify(self, data: Dict) -> Tuple[str, float]:
        """
        Classify an exoplanet.
        
        Args:
            data: Exoplanet data
            
        Returns:
            Tuple with (class, probability)
        """
        # Prepare data
        X = self.prepare_data(data)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]
        
        # Map result
        class_name = "EXOPLANET" if prediction == 1 else "FALSE_POSITIVE"
        
        return class_name, probability
    
    def classify_batch(self, data_list: List[Dict]) -> List[Dict]:
        """
        Classify multiple exoplanets.
        
        Args:
            data_list: List of exoplanet data
            
        Returns:
            List of results
        """
        results = []
        
        for i, data in enumerate(data_list):
            try:
                class_name, probability = self.classify(data)
                results.append({
                    'index': i,
                    'classification': class_name,
                    'probability': probability,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'classification': None,
                    'probability': None,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results

def main():
    """API usage example."""
    print("🚀 Exoplanet Classifier API Usage Example")
    print("=" * 60)
    
    # Initialize classifier
    classifier = ExoplanetClassifier()
    
    # Example data
    example_data = {
        'koi_period': 10.5,
        'koi_time0bk': 2000.0,
        'koi_impact': 0.3,
        'koi_duration': 2.5,
        'koi_depth': 1000.0,
        'koi_prad': 1.5,
        'koi_teq': 300.0,
        'koi_insol': 50.0,
        'koi_model_snr': 15.0,
        'koi_steff': 5700.0,
        'koi_slogg': 4.5,
        'koi_srad': 1.0,
        'ra': 290.0,
        'dec': 45.0,
        'koi_kepmag': 12.0,
        'koi_fpflag_nt': 0,
        'koi_fpflag_ss': 0,
        'koi_fpflag_co': 0,
        'koi_fpflag_ec': 0,
        'mission': 'Kepler',
        'pl_orbsmax': 0.1,
        'pl_bmasse': 5.0,
        'pl_orbeccen': 0.0,
        'st_mass': 1.0
    }
    
    # Individual classification
    print("\n🔬 Individual Classification:")
    class_name, probability = classifier.classify(example_data)
    print(f"Result: {class_name}")
    print(f"Probability: {probability:.4f}")
    
    # Batch classification
    print("\n📊 Batch Classification:")
    batch_data = [example_data, example_data.copy()]
    results = classifier.classify_batch(batch_data)
    
    for result in results:
        if result['status'] == 'success':
            print(f"Item {result['index']}: {result['classification']} ({result['probability']:.4f})")
        else:
            print(f"Item {result['index']}: Error - {result['error']}")
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()
