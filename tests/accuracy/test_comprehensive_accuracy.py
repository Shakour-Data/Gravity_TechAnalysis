"""
Comprehensive test showing how accuracy affects decision making
"""
from datetime import datetime
from src.core.domain.entities import (
    IndicatorResult,
    IndicatorCategory,
    CoreSignalStrength as SignalStrength
)
from gravity_tech.models.schemas import TechnicalAnalysisResult


def create_indicator(name: str, category: IndicatorCategory, 
                    signal: SignalStrength, confidence: float) -> IndicatorResult:
    return IndicatorResult(
        indicator_name=name,
        category=category,
        signal=signal,
        value=0.0,
        confidence=confidence,
        timestamp=datetime.utcnow()
    )


def test_scenario(title: str, indicators: dict):
    """Test a specific scenario"""
    print(f"\n{'='*70}")
    print(f"📊 {title}")
    print(f"{'='*70}")
    
    analysis = TechnicalAnalysisResult(
        symbol="BTCUSDT",
        timeframe="1h",
        trend_indicators=indicators['trend'],
        momentum_indicators=indicators['momentum'],
        cycle_indicators=indicators['cycle'],
        volume_indicators=indicators['volume']
    )
    
    # Calculate signals
    analysis.calculate_overall_signal()
    
    # Calculate accuracies
    def get_avg_confidence(inds):
        if not inds:
            return 0.0
        return sum(i.confidence for i in inds) / len(inds)
    
    trend_acc = get_avg_confidence(indicators['trend'])
    momentum_acc = get_avg_confidence(indicators['momentum'])
    cycle_acc = get_avg_confidence(indicators['cycle'])
    volume_acc = get_avg_confidence(indicators['volume'])
    
    print(f"\nاندیکاتورها:")
    print(f"  روند:    {len(indicators['trend'])} اندیکاتور، دقت متوسط: {trend_acc:.2f}")
    print(f"  مومنتوم:  {len(indicators['momentum'])} اندیکاتور، دقت متوسط: {momentum_acc:.2f}")
    print(f"  سیکل:    {len(indicators['cycle'])} اندیکاتور، دقت متوسط: {cycle_acc:.2f}")
    print(f"  حجم:     {len(indicators['volume'])} اندیکاتور، دقت متوسط: {volume_acc:.2f}")
    
    print(f"\nسیگنال‌های دسته‌بندی:")
    print(f"  روند:    {analysis.overall_trend_signal.value}")
    print(f"  مومنتوم:  {analysis.overall_momentum_signal.value}")
    print(f"  سیکل:    {analysis.overall_cycle_signal.value}")
    
    print(f"\n🎯 نتیجه نهایی:")
    print(f"  سیگنال کلی: {analysis.overall_signal.value}")
    print(f"  اعتماد کلی: {analysis.overall_confidence:.1%}")
    
    return analysis


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 تست جامع: تأثیر دقت در تصمیم‌گیری")
    print("=" * 70)
    
    # Scenario 1: All high confidence, all bullish
    print("\n" + "▼" * 70)
    print("سناریو 1: همه صعودی، همه با دقت بالا")
    test_scenario(
        "شرایط ایده‌آل - سیگنال قوی و مطمئن",
        {
            'trend': [
                create_indicator("SMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.9),
                create_indicator("EMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.9),
            ],
            'momentum': [
                create_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.9),
                create_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.9),
            ],
            'cycle': [
                create_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.BULLISH, 0.9),
            ],
            'volume': [
                create_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.BULLISH, 0.9),
            ]
        }
    )
    
    # Scenario 2: All high confidence, mixed signals
    print("\n" + "▼" * 70)
    print("سناریو 2: سیگنال‌های متناقض، همه با دقت بالا")
    test_scenario(
        "عدم اطمینان - اندیکاتورهای دقیق با سیگنال‌های مختلف",
        {
            'trend': [
                create_indicator("SMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.9),
                create_indicator("EMA", IndicatorCategory.TREND, SignalStrength.BEARISH, 0.9),
            ],
            'momentum': [
                create_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.9),
                create_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BEARISH, 0.9),
            ],
            'cycle': [
                create_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.NEUTRAL, 0.9),
            ],
            'volume': [
                create_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.NEUTRAL, 0.9),
            ]
        }
    )
    
    # Scenario 3: Trend high confidence, others low
    print("\n" + "▼" * 70)
    print("سناریو 3: فقط روند قابل اعتماد")
    test_scenario(
        "تکیه بر روند - سایر اندیکاتورها نامطمئن",
        {
            'trend': [
                create_indicator("SMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.95),
                create_indicator("EMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.95),
                create_indicator("MACD", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.95),
            ],
            'momentum': [
                create_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.NEUTRAL, 0.3),
                create_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BEARISH, 0.2),
            ],
            'cycle': [
                create_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.NEUTRAL, 0.3),
            ],
            'volume': [
                create_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.NEUTRAL, 0.4),
            ]
        }
    )
    
    # Scenario 4: Momentum and Cycle high, Trend low
    print("\n" + "▼" * 70)
    print("سناریو 4: مومنتوم و سیکل قوی، روند ضعیف")
    test_scenario(
        "تغییر روند احتمالی - مومنتوم و سیکل سیگنال تغییر می‌دهند",
        {
            'trend': [
                create_indicator("SMA", IndicatorCategory.TREND, SignalStrength.BEARISH, 0.4),
                create_indicator("EMA", IndicatorCategory.TREND, SignalStrength.BEARISH, 0.3),
            ],
            'momentum': [
                create_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.95),
                create_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.9),
            ],
            'cycle': [
                create_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.BULLISH, 0.9),
                create_indicator("Phase", IndicatorCategory.CYCLE, SignalStrength.BULLISH, 0.95),
            ],
            'volume': [
                create_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.BULLISH, 0.8),
            ]
        }
    )
    
    # Scenario 5: All low confidence
    print("\n" + "▼" * 70)
    print("سناریو 5: همه دقت پایین")
    test_scenario(
        "بازار نامشخص - همه اندیکاتورها نامطمئن",
        {
            'trend': [
                create_indicator("SMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.3),
                create_indicator("EMA", IndicatorCategory.TREND, SignalStrength.BULLISH, 0.3),
            ],
            'momentum': [
                create_indicator("RSI", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.3),
                create_indicator("Stoch", IndicatorCategory.MOMENTUM, SignalStrength.BULLISH, 0.3),
            ],
            'cycle': [
                create_indicator("Sine", IndicatorCategory.CYCLE, SignalStrength.BULLISH, 0.3),
            ],
            'volume': [
                create_indicator("OBV", IndicatorCategory.VOLUME, SignalStrength.BULLISH, 0.3),
            ]
        }
    )
    
    print(f"\n{'='*70}")
    print("💡 خلاصه:")
    print("  1. دقت بالا + توافق → اعتماد بالا")
    print("  2. دقت بالا + عدم توافق → اعتماد متوسط")
    print("  3. دقت پایین → اعتماد پایین (حتی با توافق)")
    print("  4. دسته‌های با دقت بالاتر، وزن بیشتری در تصمیم دارند")
    print("="*70)
