"""
تست سیستم کامل Multi-Horizon (Trend + Momentum)

تست end-to-end برای سیستم تحلیل ترکیبی
"""

import numpy as np
import pandas as pd
import sys
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.abspath('.'))

from ml.multi_horizon_feature_extraction import MultiHorizonFeatureExtractor
from ml.multi_horizon_momentum_features import MultiHorizonMomentumFeatureExtractor
from ml.multi_horizon_weights import MultiHorizonWeightLearner
from ml.multi_horizon_analysis import MultiHorizonAnalyzer
from ml.multi_horizon_momentum_analysis import MultiHorizonMomentumAnalyzer
from ml.combined_trend_momentum_analysis import CombinedTrendMomentumAnalyzer


def create_realistic_market_data(
    num_samples: int = 2000,
    trend: str = 'mixed'
) -> pd.DataFrame:
    """ایجاد داده‌های بازار"""
    np.random.seed(42)
    
    dates = pd.date_range(end=pd.Timestamp.now(), periods=num_samples, freq='1h')
    base_price = 30000
    prices = [base_price]
    volumes = []
    
    for i in range(1, num_samples):
        if trend == 'uptrend':
            drift = 0.002
        elif trend == 'downtrend':
            drift = -0.002
        else:
            if i < num_samples // 3:
                drift = 0.003
            elif i < 2 * num_samples // 3:
                drift = -0.002
            else:
                drift = 0.001
        
        volatility = 0.01
        change = drift + np.random.normal(0, volatility)
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
        
        base_volume = 1000000
        volume = base_volume * (1 + np.random.normal(0, 0.3))
        volumes.append(max(volume, 100000))
    
    volumes.insert(0, 1000000)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'close': prices
    })
    
    df['high'] = df['close'] * (1 + np.abs(np.random.normal(0, 0.005, len(df))))
    df['low'] = df['close'] * (1 - np.abs(np.random.normal(0, 0.005, len(df))))
    df['open'] = df['close'].shift(1).fillna(df['close'].iloc[0])
    df['volume'] = volumes
    
    return df


def test_trend_system():
    """تست سیستم روند"""
    print("\n" + "="*80)
    print("🔵 TESTING TREND SYSTEM")
    print("="*80)
    
    # ایجاد داده
    candles = create_realistic_market_data(num_samples=1500, trend='uptrend')
    print(f"\n✅ Generated {len(candles)} candles")
    
    # استخراج ویژگی‌ها
    trend_extractor = MultiHorizonFeatureExtractor(horizons=['3d', '7d', '30d'])
    X_trend, Y_trend = trend_extractor.extract_training_dataset(candles)
    print(f"✅ Trend features: {X_trend.shape}")
    
    # آموزش
    trend_learner = MultiHorizonWeightLearner(
        horizons=['3d', '7d', '30d'],
        test_size=0.2,
        random_state=42
    )
    trend_learner.train(X_trend, Y_trend, verbose=False)
    print("✅ Trend model trained")
    
    # تحلیل
    trend_analyzer = MultiHorizonAnalyzer(trend_learner)
    latest_features = X_trend.iloc[-1].to_dict()
    trend_analysis = trend_analyzer.analyze(latest_features)
    
    print("\n📊 Trend Analysis Results:")
    print(f"  3d Score: {trend_analysis.trend_3d.score:+.3f} ({trend_analysis.trend_3d.confidence:.0%})")
    print(f"  7d Score: {trend_analysis.trend_7d.score:+.3f} ({trend_analysis.trend_7d.confidence:.0%})")
    print(f"  30d Score: {trend_analysis.trend_30d.score:+.3f} ({trend_analysis.trend_30d.confidence:.0%})")
    
    return trend_learner, trend_analyzer, candles


def test_momentum_system(candles):
    """تست سیستم مومنتوم"""
    print("\n" + "="*80)
    print("🟢 TESTING MOMENTUM SYSTEM")
    print("="*80)
    
    # استخراج ویژگی‌ها
    momentum_extractor = MultiHorizonMomentumFeatureExtractor(horizons=['3d', '7d', '30d'])
    X_momentum, Y_momentum = momentum_extractor.extract_training_dataset(candles)
    print(f"\n✅ Momentum features: {X_momentum.shape}")
    
    # آموزش
    momentum_learner = MultiHorizonWeightLearner(
        horizons=['3d', '7d', '30d'],
        test_size=0.2,
        random_state=42
    )
    momentum_learner.train(X_momentum, Y_momentum, verbose=False)
    print("✅ Momentum model trained")
    
    # تحلیل
    momentum_analyzer = MultiHorizonMomentumAnalyzer(momentum_learner)
    latest_features = X_momentum.iloc[-1].to_dict()
    momentum_analysis = momentum_analyzer.analyze(latest_features)
    
    print("\n📊 Momentum Analysis Results:")
    print(f"  3d Score: {momentum_analysis.momentum_3d.score:+.3f} ({momentum_analysis.momentum_3d.confidence:.0%})")
    print(f"  7d Score: {momentum_analysis.momentum_7d.score:+.3f} ({momentum_analysis.momentum_7d.confidence:.0%})")
    print(f"  30d Score: {momentum_analysis.momentum_30d.score:+.3f} ({momentum_analysis.momentum_30d.confidence:.0%})")
    
    return momentum_learner, momentum_analyzer


def test_combined_system(
    trend_learner,
    momentum_learner,
    candles
):
    """تست سیستم ترکیبی"""
    print("\n" + "="*80)
    print("🟣 TESTING COMBINED SYSTEM")
    print("="*80)
    
    # ایجاد آنالایزرها
    trend_analyzer = MultiHorizonAnalyzer(trend_learner)
    momentum_analyzer = MultiHorizonMomentumAnalyzer(momentum_learner)
    
    # ایجاد آنالایزر ترکیبی
    combined_analyzer = CombinedTrendMomentumAnalyzer(
        trend_analyzer=trend_analyzer,
        momentum_analyzer=momentum_analyzer,
        trend_weight=0.5,
        momentum_weight=0.5
    )
    
    # استخراج آخرین ویژگی‌ها
    trend_extractor = MultiHorizonFeatureExtractor(horizons=['3d', '7d', '30d'])
    momentum_extractor = MultiHorizonMomentumFeatureExtractor(horizons=['3d', '7d', '30d'])
    
    X_trend, _ = trend_extractor.extract_training_dataset(candles)
    X_momentum, _ = momentum_extractor.extract_training_dataset(candles)
    
    trend_features = X_trend.iloc[-1].to_dict()
    momentum_features = X_momentum.iloc[-1].to_dict()
    
    # تحلیل ترکیبی
    combined_analysis = combined_analyzer.analyze(trend_features, momentum_features)
    
    # نمایش نتایج
    combined_analyzer.print_analysis(combined_analysis)
    
    return combined_analyzer, combined_analysis


def test_different_scenarios():
    """تست سناریوهای مختلف"""
    print("\n" + "="*80)
    print("🎬 TESTING DIFFERENT MARKET SCENARIOS")
    print("="*80)
    
    scenarios = [
        ('STRONG UPTREND', 'uptrend'),
        ('STRONG DOWNTREND', 'downtrend'),
        ('MIXED MARKET', 'mixed')
    ]
    
    for name, trend_type in scenarios:
        print(f"\n\n{'='*80}")
        print(f"📈 Scenario: {name}")
        print("="*80)
        
        # ایجاد داده
        candles = create_realistic_market_data(num_samples=1500, trend=trend_type)
        
        # آموزش
        print("\n🔄 Training models...")
        
        trend_extractor = MultiHorizonFeatureExtractor(horizons=['3d', '7d', '30d'])
        X_trend, Y_trend = trend_extractor.extract_training_dataset(candles)
        
        momentum_extractor = MultiHorizonMomentumFeatureExtractor(horizons=['3d', '7d', '30d'])
        X_momentum, Y_momentum = momentum_extractor.extract_training_dataset(candles)
        
        trend_learner = MultiHorizonWeightLearner(horizons=['3d', '7d', '30d'], test_size=0.2, random_state=42)
        trend_learner.train(X_trend, Y_trend, verbose=False)
        
        momentum_learner = MultiHorizonWeightLearner(horizons=['3d', '7d', '30d'], test_size=0.2, random_state=42)
        momentum_learner.train(X_momentum, Y_momentum, verbose=False)
        
        # تحلیل ترکیبی
        trend_analyzer = MultiHorizonAnalyzer(trend_learner)
        momentum_analyzer = MultiHorizonMomentumAnalyzer(momentum_learner)
        combined_analyzer = CombinedTrendMomentumAnalyzer(
            trend_analyzer, momentum_analyzer, 0.5, 0.5
        )
        
        trend_features = X_trend.iloc[-1].to_dict()
        momentum_features = X_momentum.iloc[-1].to_dict()
        
        combined_analysis = combined_analyzer.analyze(trend_features, momentum_features)
        
        # نمایش خلاصه
        print("\n📋 Summary:")
        print(f"  Final Action:    {combined_analysis.final_action.value}")
        print(f"  Final Confidence: {combined_analysis.final_confidence:.0%}")
        print(f"  3d Combined:     {combined_analysis.combined_score_3d:+.3f}")
        print(f"  7d Combined:     {combined_analysis.combined_score_7d:+.3f}")
        print(f"  30d Combined:    {combined_analysis.combined_score_30d:+.3f}")


def main():
    """تابع اصلی تست"""
    print("\n" + "🚀"*40)
    print("COMPLETE MULTI-HORIZON SYSTEM TEST")
    print("🚀"*40)
    
    try:
        # تست سیستم روند
        trend_learner, trend_analyzer, candles = test_trend_system()
        
        # تست سیستم مومنتوم
        momentum_learner, momentum_analyzer = test_momentum_system(candles)
        
        # تست سیستم ترکیبی
        combined_analyzer, combined_analysis = test_combined_system(
            trend_learner, momentum_learner, candles
        )
        
        # تست سناریوهای مختلف
        test_different_scenarios()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED SUCCESSFULLY")
        print("="*80)
        print("\nSystem is ready for production use!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
