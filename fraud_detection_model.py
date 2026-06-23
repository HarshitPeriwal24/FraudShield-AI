"""
FraudShield AI - Digital Arrest Scam Detection System
Core ML Pipeline for multi-class fraud detection
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    precision_recall_curve, f1_score, accuracy_score
)
import pickle
import json
import warnings

warnings.filterwarnings('ignore')


class FraudShieldDetector:
    """
    Multi-level fraud detection system for digital arrest scams
    - Binary classification: scam vs legitimate
    - Multi-class classification: scam type identification
    """

    def __init__(self):
        self.binary_model = None
        self.multiclass_model = None
        self.vectorizer = None
        self.scam_types = ['digital_arrest_general', 'tax_legal_threat',
                          'bank_account_freeze', 'courier_parcel_scam']

    def load_and_prepare_data(self, filepath):
        """Load and prepare the dataset"""
        df = pd.read_csv(filepath)

        # Data cleaning
        df['text'] = df['text'].str.strip()
        df = df.dropna(subset=['text', 'is_scam'])

        print(f"Dataset shape: {df.shape}")
        print(f"\nClass distribution:\n{df['is_scam'].value_counts()}")
        print(f"\nScam type distribution:\n{df[df['is_scam']==1]['scam_type'].value_counts()}")

        return df

    def extract_features(self, texts, max_features=5000, fit=False):
        """TF-IDF vectorization with channel encoding"""
        if fit:
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.9,
                lowercase=True,
                stop_words='english'
            )
            return self.vectorizer.fit_transform(texts)
        else:
            return self.vectorizer.transform(texts)

    def train_binary_classifier(self, X_train, y_train):
        """Train binary scam detector (XGBoost-like ensemble)"""
        print("\n" + "="*60)
        print("Training Binary Classifier (Scam vs Legitimate)")
        print("="*60)

        self.binary_model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.9,
                lowercase=True,
                stop_words='english'
            )),
            ('classifier', GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.05,
                max_depth=5,
                random_state=42
            ))
        ])

        self.binary_model.fit(X_train, y_train)
        print("[OK] Binary classifier trained successfully")

    def train_multiclass_classifier(self, df_scams):
        """Train multi-class classifier for scam type identification"""
        print("\n" + "="*60)
        print("Training Multi-Class Classifier (Scam Type Detection)")
        print("="*60)

        X_multi = df_scams['text'].values
        y_multi = df_scams['scam_type'].values

        self.multiclass_model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=3000,
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                lowercase=True,
                stop_words='english'
            )),
            ('classifier', GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=4,
                random_state=42
            ))
        ])

        self.multiclass_model.fit(X_multi, y_multi)
        print("[OK] Multi-class classifier trained successfully")

    def evaluate(self, X_test, y_test, X_test_multi=None, y_test_multi=None):
        """Comprehensive model evaluation"""
        print("\n" + "="*60)
        print("BINARY CLASSIFICATION EVALUATION")
        print("="*60)

        y_pred = self.binary_model.predict(X_test)
        y_pred_proba = self.binary_model.predict_proba(X_test)[:, 1]

        print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
        print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred,
                                   target_names=['Legitimate', 'Scam']))

        if X_test_multi is not None and y_test_multi is not None:
            print("\n" + "="*60)
            print("MULTI-CLASS CLASSIFICATION EVALUATION")
            print("="*60)

            y_pred_multi = self.multiclass_model.predict(X_test_multi)
            print(f"\nAccuracy: {accuracy_score(y_test_multi, y_pred_multi):.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test_multi, y_pred_multi))

    def predict(self, text):
        """Predict scam probability and type"""
        scam_prob = self.binary_model.predict_proba([text])[0][1]
        is_scam = self.binary_model.predict([text])[0]

        prediction = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'is_scam': bool(is_scam),
            'scam_probability': float(scam_prob),
            'risk_level': self._get_risk_level(scam_prob)
        }

        if is_scam and self.multiclass_model:
            scam_type = self.multiclass_model.predict([text])[0]
            scam_type_proba = self.multiclass_model.predict_proba([text])[0]
            prediction['scam_type'] = str(scam_type)
            prediction['scam_type_confidence'] = float(max(scam_type_proba))

        return prediction

    def _get_risk_level(self, probability):
        """Categorize risk based on scam probability"""
        if probability >= 0.8:
            return "CRITICAL"
        elif probability >= 0.6:
            return "HIGH"
        elif probability >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"

    def save_models(self, binary_path='models/binary_model.pkl',
                   multiclass_path='models/multiclass_model.pkl'):
        """Save trained models"""
        import os
        os.makedirs('models', exist_ok=True)

        with open(binary_path, 'wb') as f:
            pickle.dump(self.binary_model, f)
        print(f"[OK] Binary model saved to {binary_path}")

        if self.multiclass_model:
            with open(multiclass_path, 'wb') as f:
                pickle.dump(self.multiclass_model, f)
            print(f"[OK] Multi-class model saved to {multiclass_path}")

    def load_models(self, binary_path='models/binary_model.pkl',
                   multiclass_path='models/multiclass_model.pkl'):
        """Load pre-trained models"""
        with open(binary_path, 'rb') as f:
            self.binary_model = pickle.load(f)
        print(f"[OK] Binary model loaded from {binary_path}")

        try:
            with open(multiclass_path, 'rb') as f:
                self.multiclass_model = pickle.load(f)
            print(f"[OK] Multi-class model loaded from {multiclass_path}")
        except:
            print("[WARN] Multi-class model not found")


def main():
    """Main training pipeline"""

    # Initialize detector
    detector = FraudShieldDetector()

    # Load data
    df = detector.load_and_prepare_data('digital_arrest_scam_dataset.csv')

    # Split data
    X = df['text'].values
    y = df['is_scam'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train binary classifier
    detector.train_binary_classifier(X_train, y_train)

    # Prepare multi-class data
    df_scams = df[df['is_scam'] == 1].copy()
    X_scams = df_scams['text'].values
    y_scams = df_scams['scam_type'].values

    X_scams_train, X_scams_test, y_scams_train, y_scams_test = train_test_split(
        X_scams, y_scams, test_size=0.2, random_state=42, stratify=y_scams
    )

    # Train multi-class classifier
    detector.train_multiclass_classifier(df_scams)

    # Evaluate models
    detector.evaluate(X_test, y_test, X_scams_test, y_scams_test)

    # Save models
    detector.save_models()

    # Test predictions
    print("\n" + "="*60)
    print("SAMPLE PREDICTIONS")
    print("="*60)

    test_cases = [
        "Your HDFC account will be frozen by RBI in 2 hours due to suspicious transaction. Contact officer on video call to avoid digital arrest.",
        "Hi, just confirming our meeting tomorrow at 10 AM. Let me know if that works.",
        "You are under digital arrest warrant. Stay on this call or face physical arrest within 1 hour."
    ]

    for test in test_cases:
        result = detector.predict(test)
        print(f"\nText: {result['text']}")
        print(f"Is Scam: {result['is_scam']}")
        print(f"Scam Probability: {result['scam_probability']:.4f}")
        print(f"Risk Level: {result['risk_level']}")
        if 'scam_type' in result:
            print(f"Scam Type: {result['scam_type']} (confidence: {result['scam_type_confidence']:.4f})")


if __name__ == "__main__":
    main()
