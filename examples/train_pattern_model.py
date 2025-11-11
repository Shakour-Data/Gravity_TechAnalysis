"""
Train Pattern Recognition Model - Demo Script
Day 4: Pattern Recognition ML (Part 1)
Author: Dr. Rajesh Kumar Patel (Lead ML Engineer)
Date: November 11, 2025

This script demonstrates:
1. Generating synthetic training data
2. Training XGBoost classifier
3. Evaluating model performance
4. Saving trained model
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.pattern_classifier import (
    PatternClassifier,
    PatternConfidenceScorer,
    generate_synthetic_training_data
)
from ml.pattern_features import PatternFeatureExtractor


def main():
    """Main training script."""
    print("=" * 80)
    print("🎯 Harmonic Pattern Recognition - Model Training")
    print("=" * 80)
    
    # Step 1: Generate synthetic training data
    print("\n📊 Step 1: Generating Synthetic Training Data...")
    print("-" * 80)
    
    n_samples = 2000  # More data = better model
    X_train, y_train, y_success = generate_synthetic_training_data(n_samples)
    
    print(f"✅ Generated {n_samples} training samples")
    print(f"   Features: {X_train.shape[1]}")
    print(f"   Pattern distribution:")
    
    for pattern_type in ['gartley', 'butterfly', 'bat', 'crab']:
        count = sum(1 for y in y_train if y == pattern_type)
        percentage = (count / len(y_train)) * 100
        print(f"   - {pattern_type.capitalize()}: {count} ({percentage:.1f}%)")
    
    # Step 2: Initialize and train classifier
    print("\n🤖 Step 2: Training XGBoost Classifier...")
    print("-" * 80)
    
    classifier = PatternClassifier(
        n_estimators=150,  # More trees = better accuracy
        max_depth=8,       # Deeper trees for complex patterns
        learning_rate=0.05 # Slower learning for stability
    )
    
    metrics = classifier.train(
        X_train,
        y_train,
        y_success,
        test_size=0.2,
        verbose=True
    )
    
    # Step 3: Analyze feature importance
    print("\n📈 Step 3: Feature Importance Analysis...")
    print("-" * 80)
    
    extractor = PatternFeatureExtractor()
    feature_names = extractor.get_feature_names()
    importance_dict = classifier.get_feature_importance(feature_names)
    
    # Sort by importance
    sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
    
    print("Top 10 Most Important Features:")
    for i, (feature, importance) in enumerate(sorted_features[:10], 1):
        bar = "█" * int(importance * 50)
        print(f"{i:2d}. {feature:30s} {bar} {importance:.4f}")
    
    # Step 4: Test predictions
    print("\n🔮 Step 4: Testing Predictions on Sample Data...")
    print("-" * 80)
    
    # Test on 5 random samples
    test_indices = np.random.choice(len(X_train), 5, replace=False)
    
    for i, idx in enumerate(test_indices, 1):
        features = X_train[idx]
        actual_type = y_train[idx]
        actual_success = y_success[idx]
        
        # Make prediction
        prediction = classifier.predict_single(features)
        
        # Calculate confidence score
        scorer = PatternConfidenceScorer()
        confidence_result = scorer.calculate_confidence(
            fibonacci_accuracy=features[0],  # xab_ratio_accuracy
            ml_confidence=prediction['confidence'],
            volume_confirmation=features[15],  # volume_at_d
            momentum_confirmation=features[20],  # momentum_divergence
            geometric_quality=features[4]  # pattern_symmetry
        )
        
        print(f"\nSample {i}:")
        print(f"  Actual:    {actual_type.upper()} (success: {actual_success:.2f})")
        print(f"  Predicted: {prediction['pattern_type'].upper()} (confidence: {prediction['confidence']:.2f})")
        print(f"  Success Probability: {prediction['success_probability']:.2f}")
        print(f"  Overall Confidence: {confidence_result['confidence']:.1f}/100 ({confidence_result['category']})")
        print(f"  Signal: {confidence_result['signal']}")
        
        match = "✅" if prediction['pattern_type'] == actual_type else "❌"
        print(f"  Match: {match}")
    
    # Step 5: Save trained model
    print("\n💾 Step 5: Saving Trained Model...")
    print("-" * 80)
    
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, "pattern_classifier_v1.pkl")
    classifier.save(model_path)
    
    print(f"✅ Model saved to: {model_path}")
    
    # Step 6: Summary
    print("\n" + "=" * 80)
    print("🎉 Training Complete - Summary")
    print("=" * 80)
    print(f"Training Accuracy:     {metrics['train_accuracy']:.4f}")
    print(f"Test Accuracy:         {metrics['test_accuracy']:.4f}")
    print(f"Cross-Val Accuracy:    {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
    if 'r2_score' in metrics:
        print(f"Success Predictor R²:  {metrics['r2_score']:.4f}")
    print(f"Model Size:            {os.path.getsize(model_path) / 1024:.1f} KB")
    print("\n✅ Model is ready for production use!")
    print("=" * 80)


if __name__ == "__main__":
    main()
