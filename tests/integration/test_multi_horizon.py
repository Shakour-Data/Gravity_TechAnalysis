"""
Test Multi-Horizon System

اسکریپت تست کامل سیستم چند افقی:
1. آموزش مدل با داده Bitcoin
2. تحلیل و نمایش سه امتیاز (3d, 7d, 30d)
3. تشخیص الگوها
4. ایجاد توصیه‌ها
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
from typing import List

# Add parent directory to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.schemas import Candle
from ml.train_multi_horizon import train_multi_horizon_system, load_trained_model, create_realistic_market_data
from ml.multi_horizon_feature_extraction import MultiHorizonFeatureExtractor
from ml.multi_horizon_analysis import MultiHorizonTrendAnalyzer
import json


def test_training():
    """
    تست 1: آموزش مدل با Bitcoin
    """
    print("\n" + "🧪"*35)
    print("TEST 1: TRAINING MULTI-HORIZON SYSTEM")
    print("🧪"*35)
    
    result = train_multi_horizon_system(
        symbol="BTCUSDT",
        interval="1d",
        lookback_days=365,
        horizons=[3, 7, 30],
        output_dir="ml_models/multi_horizon"
    )
    
    print("\n✅ TEST 1 PASSED - Training completed")
    return result


def test_analysis(result):
    """
    تست 2: تحلیل با مدل آموزش دیده
    """
    print("\n" + "🧪"*35)
    print("TEST 2: MULTI-HORIZON ANALYSIS")
    print("🧪"*35)
    
    # دریافت داده جدید (شبیه‌سازی)
    candles = create_realistic_market_data(
        base_price=50000,
        candles_count=150,
        trend="mixed"
    )
    
    print(f"\n📊 Latest data: {len(candles)} candles")
    print(f"   Last candle: {candles[-1].timestamp}")
    print(f"   Price: ${candles[-1].close:,.2f}")
    
    # استخراج ویژگی‌های فعلی
    extractor = MultiHorizonFeatureExtractor(
        lookback_period=100,
        horizons=[3, 7, 30]
    )
    
    # ویژگی‌های سطح 1
    features_l1 = extractor.extract_indicator_features(candles[-100:])
    
    # ایجاد analyzer با مدل آموزش دیده
    analyzer_l1 = MultiHorizonTrendAnalyzer(
        result['learner_indicators']
    )
    
    # تحلیل
    analysis_l1 = analyzer_l1.analyze(features_l1)
    
    # نمایش نتیجه
    analyzer_l1.print_analysis(analysis_l1)
    
    # ═══════════════════════════════════════════════════════════
    # تست سطح 2
    # ═══════════════════════════════════════════════════════════
    print("\n" + "-"*70)
    print("📊 LEVEL 2 ANALYSIS (Dimensions)")
    print("-"*70)
    
    features_l2 = extractor.extract_dimension_features(candles[-100:])
    
    analyzer_l2 = MultiHorizonTrendAnalyzer(
        result['learner_dimensions']
    )
    
    analysis_l2 = analyzer_l2.analyze(features_l2)
    analyzer_l2.print_analysis(analysis_l2)
    
    print("\n✅ TEST 2 PASSED - Analysis completed")
    
    return {
        'analysis_level1': analysis_l1,
        'analysis_level2': analysis_l2
    }


def test_pattern_detection(analyses):
    """
    تست 3: تشخیص الگوها
    """
    print("\n" + "🧪"*35)
    print("TEST 3: PATTERN DETECTION")
    print("🧪"*35)
    
    analysis_l1 = analyses['analysis_level1']
    analysis_l2 = analyses['analysis_level2']
    
    print("\n🔍 Level 1 Pattern:")
    print(f"   Type: {analysis_l1.pattern.value}")
    print(f"   Confidence: {analysis_l1.pattern_confidence:.0%}")
    
    print("\n🔍 Level 2 Pattern:")
    print(f"   Type: {analysis_l2.pattern.value}")
    print(f"   Confidence: {analysis_l2.pattern_confidence:.0%}")
    
    # مقایسه
    if analysis_l1.pattern == analysis_l2.pattern:
        print(f"\n✅ Both levels agree: {analysis_l1.pattern.value}")
    else:
        print(f"\n⚠️ Different patterns detected:")
        print(f"   L1: {analysis_l1.pattern.value}")
        print(f"   L2: {analysis_l2.pattern.value}")
    
    print("\n✅ TEST 3 PASSED - Pattern detection working")


def test_recommendations(analyses):
    """
    تست 4: توصیه‌ها
    """
    print("\n" + "🧪"*35)
    print("TEST 4: RECOMMENDATIONS")
    print("🧪"*35)
    
    analysis_l1 = analyses['analysis_level1']
    
    print("\n📋 Level 1 Recommendations:")
    print(f"\n  3-Day (Day Trading):")
    print(f"    {analysis_l1.recommendation_3d}")
    
    print(f"\n  7-Day (Swing Trading):")
    print(f"    {analysis_l1.recommendation_7d}")
    
    print(f"\n  30-Day (Position Trading):")
    print(f"    {analysis_l1.recommendation_30d}")
    
    print("\n✅ TEST 4 PASSED - Recommendations generated")


def test_save_and_load():
    """
    تست 5: ذخیره و بارگذاری
    """
    print("\n" + "🧪"*35)
    print("TEST 5: SAVE & LOAD")
    print("🧪"*35)
    
    # بارگذاری مدل ذخیره شده
    learner = load_trained_model(
        symbol="BTCUSDT",
        level="indicators",
        model_dir="ml_models/multi_horizon"
    )
    
    print("\n✅ Model loaded successfully")
    
    # بررسی وزن‌ها
    for horizon in ['3d', '7d', '30d']:
        weights = learner.get_horizon_weights(horizon)
        print(f"\n{horizon.upper()}:")
        print(f"  Confidence: {weights.confidence:.2f}")
        print(f"  R² Test: {weights.metrics['r2_test']:.4f}")
        print(f"  MAE Test: {weights.metrics['mae_test']:.4f}")
    
    print("\n✅ TEST 5 PASSED - Save/Load working")


def generate_report(result, analyses):
    """
    ایجاد گزارش نهایی
    """
    print("\n" + "="*70)
    print("📊 FINAL TEST REPORT")
    print("="*70)
    
    config = result['config']
    analysis_l1 = analyses['analysis_level1']
    
    report = {
        'test_date': analysis_l1.timestamp,
        'symbol': config['symbol'],
        'training_samples': config['n_samples'],
        'horizons': config['horizons'],
        
        'level1_results': {
            'pattern': analysis_l1.pattern.value,
            'pattern_confidence': analysis_l1.pattern_confidence,
            'scores': {
                '3d': analysis_l1.score_3d.score,
                '7d': analysis_l1.score_7d.score,
                '30d': analysis_l1.score_30d.score
            },
            'confidences': {
                '3d': analysis_l1.score_3d.confidence,
                '7d': analysis_l1.score_7d.confidence,
                '30d': analysis_l1.score_30d.confidence
            },
            'combined_score': analysis_l1.combined_score,
            'combined_confidence': analysis_l1.combined_confidence
        },
        
        'recommendations': {
            '3d': analysis_l1.recommendation_3d,
            '7d': analysis_l1.recommendation_7d,
            '30d': analysis_l1.recommendation_30d
        }
    }
    
    # ذخیره گزارش
    output_dir = Path(result['output_dir'])
    report_file = output_dir / "test_report.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Report saved: {report_file}")
    
    # نمایش خلاصه
    print("\n📈 SUMMARY:")
    print("-" * 70)
    print(f"Symbol: {config['symbol']}")
    print(f"Training Samples: {config['n_samples']}")
    print(f"Pattern: {analysis_l1.pattern.value} ({analysis_l1.pattern_confidence:.0%})")
    print(f"\nScores:")
    print(f"  3d:  {analysis_l1.score_3d.score:+.3f} (conf: {analysis_l1.score_3d.confidence:.0%})")
    print(f"  7d:  {analysis_l1.score_7d.score:+.3f} (conf: {analysis_l1.score_7d.confidence:.0%})")
    print(f"  30d: {analysis_l1.score_30d.score:+.3f} (conf: {analysis_l1.score_30d.confidence:.0%})")
    print(f"\nCombined: {analysis_l1.combined_score:+.3f} (conf: {analysis_l1.combined_confidence:.0%})")
    print("-" * 70)


def run_all_tests():
    """
    اجرای همه تست‌ها
    """
    print("\n" + "🚀"*35)
    print("MULTI-HORIZON SYSTEM - FULL TEST SUITE")
    print("🚀"*35)
    
    try:
        # Test 1: آموزش
        result = test_training()
        
        # Test 2: تحلیل
        analyses = test_analysis(result)
        
        # Test 3: تشخیص الگو
        test_pattern_detection(analyses)
        
        # Test 4: توصیه‌ها
        test_recommendations(analyses)
        
        # Test 5: ذخیره/بارگذاری
        test_save_and_load()
        
        # گزارش نهایی
        generate_report(result, analyses)
        
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED!")
        print("="*70)
        
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ TEST FAILED: {e}")
        print("="*70)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
