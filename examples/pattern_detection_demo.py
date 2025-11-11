"""
Pattern Recognition Demo - Real-time Detection
Day 4: Pattern Recognition ML (Part 1)
Author: Dr. Rajesh Kumar Patel (Lead ML Engineer)
Date: November 11, 2025

Demonstrates:
1. Real-time pattern detection on sample data
2. Feature extraction
3. ML-based pattern classification
4. Confidence scoring
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.harmonic import detect_all_harmonic_patterns
from ml.pattern_features import PatternFeatureExtractor, extract_pattern_features_batch
from ml.pattern_classifier import PatternClassifier, PatternConfidenceScorer


def generate_sample_market_data(n_bars: int = 200) -> tuple:
    """Generate realistic sample market data."""
    np.random.seed(42)
    
    # Create trending price action with retracements
    base_prices = []
    price = 100.0
    
    for i in range(n_bars):
        # Add trend + noise
        trend = 0.1 if i % 50 < 25 else -0.1
        noise = np.random.normal(0, 0.5)
        price = max(50, min(150, price + trend + noise))
        base_prices.append(price)
    
    prices = np.array(base_prices, dtype=np.float32)
    
    # Create OHLC data
    highs = prices + np.abs(np.random.normal(0, 0.8, n_bars))
    lows = prices - np.abs(np.random.normal(0, 0.8, n_bars))
    closes = prices + np.random.normal(0, 0.3, n_bars)
    volume = np.random.uniform(1000, 10000, n_bars)
    
    return highs, lows, closes, volume


def main():
    """Main demo script."""
    print("=" * 80)
    print("🎯 Harmonic Pattern Recognition - Live Demo")
    print("=" * 80)
    
    # Step 1: Generate sample data
    print("\n📊 Step 1: Loading Market Data...")
    print("-" * 80)
    
    highs, lows, closes, volume = generate_sample_market_data(200)
    
    print(f"✅ Loaded {len(closes)} bars of market data")
    print(f"   Price range: ${lows.min():.2f} - ${highs.max():.2f}")
    print(f"   Current price: ${closes[-1]:.2f}")
    
    # Step 2: Detect harmonic patterns
    print("\n🔍 Step 2: Detecting Harmonic Patterns...")
    print("-" * 80)
    
    result = detect_all_harmonic_patterns(highs, lows, closes, tolerance=0.15)
    
    print(f"✅ Detected {result['total_patterns']} harmonic patterns")
    print(f"   - Gartley patterns: {len(result['gartley'])}")
    print(f"   - Butterfly patterns: {len(result['butterfly'])}")
    print(f"   - Bat patterns: {len(result['bat'])}")
    print(f"   - Crab patterns: {len(result['crab'])}")
    
    if result['total_patterns'] == 0:
        print("\n⚠️ No patterns detected in this dataset.")
        print("   Try with different market data or adjust tolerance parameter.")
        return
    
    # Step 3: Load trained classifier
    print("\n🤖 Step 3: Loading ML Classifier...")
    print("-" * 80)
    
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ml_models",
        "pattern_classifier_v1.pkl"
    )
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("   Run train_pattern_model.py first to train the model.")
        return
    
    classifier = PatternClassifier.load(model_path)
    print(f"✅ Model loaded successfully")
    print(f"   Test Accuracy: {classifier.test_accuracy:.4f}")
    
    # Step 4: Analyze detected patterns
    print("\n📈 Step 4: Analyzing Patterns with ML...")
    print("-" * 80)
    
    # For demonstration, we'll use synthetic pattern analysis
    # In real scenario, you'd extract features from actual detected patterns
    
    from patterns.harmonic import HarmonicPatternDetector
    detector = HarmonicPatternDetector(tolerance=0.15)
    patterns = detector.detect_patterns(highs, lows, closes)
    
    if len(patterns) > 0:
        extractor = PatternFeatureExtractor()
        scorer = PatternConfidenceScorer()
        
        print(f"\nAnalyzing {len(patterns)} detected pattern(s)...\n")
        
        for i, pattern in enumerate(patterns[:5], 1):  # Show first 5
            # Extract features
            features = extractor.extract_features(pattern, highs, lows, closes, volume)
            feature_array = extractor.features_to_array(features)
            
            # ML prediction
            prediction = classifier.predict_single(feature_array)
            
            # Calculate overall confidence
            confidence_result = scorer.calculate_confidence(
                fibonacci_accuracy=features.xab_ratio_accuracy,
                ml_confidence=prediction['confidence'],
                volume_confirmation=features.volume_confirmation,
                momentum_confirmation=features.momentum_divergence,
                geometric_quality=features.pattern_symmetry
            )
            
            # Display results
            print(f"{'=' * 80}")
            print(f"Pattern #{i}: {pattern.pattern_type.value.upper()} ({pattern.direction.value.upper()})")
            print(f"{'=' * 80}")
            
            print(f"\n📍 Pattern Points:")
            for label, point in pattern.points.items():
                print(f"   {label}: Bar {point.index}, Price ${point.price:.2f}")
            
            print(f"\n📊 Fibonacci Ratios:")
            for ratio_name, ratio_value in pattern.ratios.items():
                print(f"   {ratio_name}: {ratio_value:.4f}")
            
            print(f"\n🤖 ML Classification:")
            print(f"   Predicted Type: {prediction['pattern_type'].upper()}")
            print(f"   ML Confidence: {prediction['confidence'] * 100:.1f}%")
            print(f"   Success Probability: {prediction['success_probability'] * 100:.1f}%")
            print(f"   Quality Score: {prediction['quality_score'] * 100:.1f}%")
            
            print(f"\n💯 Overall Confidence Score:")
            print(f"   Score: {confidence_result['confidence']:.1f}/100")
            print(f"   Category: {confidence_result['category']}")
            print(f"   Signal: {confidence_result['signal']}")
            
            print(f"\n🎯 Trading Levels:")
            print(f"   Entry (D point): ${pattern.completion_point:.2f}")
            print(f"   Stop Loss: ${pattern.stop_loss:.2f}")
            print(f"   Target 1: ${pattern.target_1:.2f}")
            print(f"   Target 2: ${pattern.target_2:.2f}")
            
            # Risk/Reward
            risk = abs(pattern.completion_point - pattern.stop_loss)
            reward1 = abs(pattern.target_1 - pattern.completion_point)
            reward2 = abs(pattern.target_2 - pattern.completion_point)
            
            print(f"\n💰 Risk/Reward Analysis:")
            print(f"   Risk: ${risk:.2f}")
            print(f"   Reward (Target 1): ${reward1:.2f} (R/R: {reward1/risk:.2f}:1)")
            print(f"   Reward (Target 2): ${reward2:.2f} (R/R: {reward2/risk:.2f}:1)")
            
            print(f"\n{'=' * 80}\n")
    else:
        print("\n⚠️ No valid patterns found for ML analysis.")
        print("   Patterns detected but failed feature extraction requirements.")
    
    # Step 5: Summary
    print("\n" + "=" * 80)
    print("✅ Pattern Recognition Demo Complete!")
    print("=" * 80)
    print("\n📝 Summary:")
    print(f"   Total bars analyzed: {len(closes)}")
    print(f"   Patterns detected: {result['total_patterns']}")
    print(f"   ML classifier accuracy: {classifier.test_accuracy:.2%}")
    print("\n💡 Tip: Higher confidence scores (>70%) indicate more reliable patterns.")
    print("=" * 80)


if __name__ == "__main__":
    main()
