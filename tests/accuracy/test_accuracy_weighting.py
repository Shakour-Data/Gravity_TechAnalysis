"""
Test script to demonstrate accuracy weighting in overall signal calculation
"""
from datetime import datetime
from models.schemas import (
    TechnicalAnalysisResult,
    IndicatorResult,
    IndicatorCategory,
    SignalStrength
)


def create_test_indicator(name: str, category: IndicatorCategory, 
                         signal: SignalStrength, confidence: float) -> IndicatorResult:
    """Helper to create test indicator"""
    return IndicatorResult(
        indicator_name=name,
        category=category,
        signal=signal,
        value=0.0,
        confidence=confidence,
        timestamp=datetime.utcnow()
    )


def test_scenario(name: str, trend_conf: float, momentum_conf: float, 
                 cycle_conf: float, volume_conf: float):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"سناریو: {name}")
    print(f"{'='*60}")
    
    # Create analysis with same signals but different confidences
    analysis = TechnicalAnalysisResult(
        symbol="BTCUSDT",
        timeframe="1h",
        trend_indicators=[
            create_test_indicator("MA", IndicatorCategory.TREND, SignalStrength.BULLISH, trend_conf),
            create_test_indicator("MACD", IndicatorCategory.TREND, SignalStrength.BULLISH, trend_conf),
        ],
        momentum_indicators=[
            create_test_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, momentum_conf),
            create_test_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, momentum_conf),
        ],
        cycle_indicators=[
            create_test_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.BULLISH, cycle_conf),
            create_test_indicator("Phase", IndicatorCategory.CYCLE, SignalStrength.BULLISH, cycle_conf),
        ],
        volume_indicators=[
            create_test_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.BULLISH, volume_conf),
        ]
    )
    
    # Calculate signals
    analysis.calculate_overall_signal()
    
    # Display results
    print(f"\nدقت (Confidence) هر دسته:")
    print(f"  - روند: {trend_conf:.2f}")
    print(f"  - مومنتوم: {momentum_conf:.2f}")
    print(f"  - سیکل: {cycle_conf:.2f}")
    print(f"  - حجم: {volume_conf:.2f}")
    
    print(f"\nنتایج:")
    print(f"  - سیگنال کلی: {analysis.overall_signal.value}")
    print(f"  - اطمینان کلی: {analysis.overall_confidence:.3f}")
    
    # Show how weights were adjusted
    print(f"\nتأثیر دقت بر وزن‌ها:")
    print(f"  دسته‌هایی با دقت بالاتر، وزن بیشتری در تصمیم نهایی دارند")


if __name__ == "__main__":
    print("=" * 60)
    print("تست تأثیر دقت (Accuracy) در امتیازدهی کلی")
    print("=" * 60)
    
    # Scenario 1: All high confidence
    test_scenario(
        "همه دسته‌ها دقت بالا دارند",
        trend_conf=0.9,
        momentum_conf=0.9,
        cycle_conf=0.9,
        volume_conf=0.9
    )
    
    # Scenario 2: Trend has low confidence
    test_scenario(
        "روند دقت پایین، بقیه دقت بالا",
        trend_conf=0.3,
        momentum_conf=0.9,
        cycle_conf=0.9,
        volume_conf=0.9
    )
    
    # Scenario 3: Momentum has low confidence
    test_scenario(
        "مومنتوم دقت پایین، بقیه دقت بالا",
        trend_conf=0.9,
        momentum_conf=0.3,
        cycle_conf=0.9,
        volume_conf=0.9
    )
    
    # Scenario 4: Mixed confidences
    test_scenario(
        "دقت‌های متنوع",
        trend_conf=0.8,
        momentum_conf=0.6,
        cycle_conf=0.4,
        volume_conf=0.7
    )
    
    # Scenario 5: All low confidence
    test_scenario(
        "همه دسته‌ها دقت پایین",
        trend_conf=0.3,
        momentum_conf=0.3,
        cycle_conf=0.3,
        volume_conf=0.3
    )
    
    print(f"\n{'='*60}")
    print("توضیحات:")
    print("  1. دقت هر اندیکاتور در محاسبه امتیاز آن دسته استفاده می‌شود")
    print("  2. میانگین دقت هر دسته در وزن نهایی آن دسته اعمال می‌شود")
    print("  3. دسته‌هایی با دقت بالاتر، تأثیر بیشتری در سیگنال کلی دارند")
    print("  4. اطمینان کلی = 60% توافق اندیکاتورها + 40% دقت متوسط")
    print("=" * 60)
