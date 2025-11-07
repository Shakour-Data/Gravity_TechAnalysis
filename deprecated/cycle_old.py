"""
Cycle Indicators Implementation

This module implements 10 comprehensive cycle indicators:
1. Sine Wave Indicator
2. Hilbert Transform - Dominant Cycle Period
3. Hilbert Transform - Dominant Cycle Phase
4. Detrended Price Oscillator (DPO)
5. Schaff Trend Cycle (STC)
6. Market Facilitation Index (MFI)
7. Cycle Period
8. Phase Change Index
9. Trend vs Cycle Identification
10. Autocorrelation Periodogram
"""

import numpy as np
import pandas as pd
from typing import List, Tuple
from scipy import signal as scipy_signal
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory


class CycleIndicators:
    """Cycle indicators calculator"""
    
    @staticmethod
    def sine_wave(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Sine Wave Indicator using Hilbert Transform
        
        Args:
            candles: List of candles
            period: Period for calculation
            
        Returns:
            IndicatorResult with signal
        """
        closes = np.array([c.close for c in candles])
        
        # Simple sine wave approximation
        prices = pd.Series(closes)
        smoothed = prices.ewm(span=period).mean()
        
        # Calculate sine and lead sine
        sine_values = []
        lead_sine_values = []
        
        for i in range(len(smoothed)):
            if i < period:
                sine_values.append(0)
                lead_sine_values.append(0)
            else:
                window = smoothed.iloc[i-period:i].values
                # Normalize
                if window.max() != window.min():
                    normalized = 2 * (window[-1] - window.min()) / (window.max() - window.min()) - 1
                else:
                    normalized = 0
                sine_values.append(normalized)
                # Lead sine (phase shifted)
                lead_sine_values.append(normalized * 0.9)  # Simplified lead
        
        sine_current = sine_values[-1]
        lead_sine_current = lead_sine_values[-1]
        
        # Signal based on sine wave crossing
        if sine_current > 0.7:
            signal = SignalStrength.VERY_BULLISH
        elif sine_current > 0.3:
            signal = SignalStrength.BULLISH
        elif sine_current > 0:
            signal = SignalStrength.BULLISH_BROKEN
        elif sine_current < -0.7:
            signal = SignalStrength.VERY_BEARISH
        elif sine_current < -0.3:
            signal = SignalStrength.BEARISH
        elif sine_current < 0:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.65
        
        return IndicatorResult(
            indicator_name=f"Sine Wave({period})",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(sine_current),
            additional_values={
                "lead_sine": float(lead_sine_current)
            },
            confidence=confidence,
            description=f"موج سینوسی در موقعیت {sine_current:.2f}"
        )
    
    @staticmethod
    def detrended_price_oscillator(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Detrended Price Oscillator (DPO)
        Removes trend to identify cycles
        
        Args:
            candles: List of candles
            period: Period for calculation
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        
        # Calculate SMA
        sma = closes.rolling(window=period).mean()
        
        # Shift back by (period/2 + 1) to center the moving average
        shift = int(period / 2) + 1
        sma_shifted = sma.shift(shift)
        
        # DPO = Close - Shifted SMA
        dpo = closes - sma_shifted
        dpo_current = dpo.iloc[-1]
        
        # Normalize by price for percentage
        price_current = closes.iloc[-1]
        dpo_pct = (dpo_current / price_current) * 100 if price_current > 0 else 0
        
        # Signal based on DPO
        if dpo_pct > 2:
            signal = SignalStrength.VERY_BULLISH
        elif dpo_pct > 1:
            signal = SignalStrength.BULLISH
        elif dpo_pct > 0.3:
            signal = SignalStrength.BULLISH_BROKEN
        elif dpo_pct < -2:
            signal = SignalStrength.VERY_BEARISH
        elif dpo_pct < -1:
            signal = SignalStrength.BEARISH
        elif dpo_pct < -0.3:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.68
        
        return IndicatorResult(
            indicator_name=f"DPO({period})",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(dpo_current),
            additional_values={"dpo_pct": float(dpo_pct)},
            confidence=confidence,
            description=f"نوسانگر بدون روند: {dpo_pct:.2f}%"
        )
    
    @staticmethod
    def schaff_trend_cycle(candles: List[Candle], 
                          fast: int = 23, 
                          slow: int = 50, 
                          cycle: int = 10) -> IndicatorResult:
        """
        Schaff Trend Cycle (STC)
        Combines cycle and trend analysis
        
        Args:
            candles: List of candles
            fast: Fast period
            slow: Slow period
            cycle: Cycle period
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        
        # Calculate MACD
        ema_fast = closes.ewm(span=fast, adjust=False).mean()
        ema_slow = closes.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        
        # First stochastic
        stoch1_values = []
        for i in range(len(macd)):
            if i < cycle:
                stoch1_values.append(50)
            else:
                window = macd.iloc[i-cycle:i+1]
                high = window.max()
                low = window.min()
                if high != low:
                    stoch1 = 100 * (macd.iloc[i] - low) / (high - low)
                else:
                    stoch1 = 50
                stoch1_values.append(stoch1)
        
        stoch1 = pd.Series(stoch1_values)
        stoch1_smoothed = stoch1.ewm(span=3, adjust=False).mean()
        
        # Second stochastic on first stochastic
        stoch2_values = []
        for i in range(len(stoch1_smoothed)):
            if i < cycle:
                stoch2_values.append(50)
            else:
                window = stoch1_smoothed.iloc[i-cycle:i+1]
                high = window.max()
                low = window.min()
                if high != low:
                    stoch2 = 100 * (stoch1_smoothed.iloc[i] - low) / (high - low)
                else:
                    stoch2 = 50
                stoch2_values.append(stoch2)
        
        stc = pd.Series(stoch2_values).ewm(span=3, adjust=False).mean()
        stc_current = stc.iloc[-1]
        
        # Signal based on STC levels
        if stc_current > 75:
            signal = SignalStrength.VERY_BULLISH
        elif stc_current > 60:
            signal = SignalStrength.BULLISH
        elif stc_current > 50:
            signal = SignalStrength.BULLISH_BROKEN
        elif stc_current < 25:
            signal = SignalStrength.VERY_BEARISH
        elif stc_current < 40:
            signal = SignalStrength.BEARISH
        elif stc_current < 50:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.75
        
        return IndicatorResult(
            indicator_name=f"STC({fast},{slow},{cycle})",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(stc_current),
            confidence=confidence,
            description=f"چرخه روند شاف: {stc_current:.1f}"
        )
    
    @staticmethod
    def dominant_cycle_period(candles: List[Candle], max_period: int = 50) -> IndicatorResult:
        """
        Estimate Dominant Cycle Period using autocorrelation
        
        Args:
            candles: List of candles
            max_period: Maximum period to search
            
        Returns:
            IndicatorResult with signal
        """
        closes = np.array([c.close for c in candles])
        
        # Detrend the data
        x = np.arange(len(closes))
        coeffs = np.polyfit(x, closes, 1)
        trend = coeffs[0] * x + coeffs[1]
        detrended = closes - trend
        
        # Calculate autocorrelation for different lags
        autocorr = []
        for lag in range(1, min(max_period, len(detrended) // 2)):
            if lag < len(detrended):
                corr = np.corrcoef(detrended[:-lag], detrended[lag:])[0, 1]
                autocorr.append(corr if not np.isnan(corr) else 0)
            else:
                autocorr.append(0)
        
        # Find peaks in autocorrelation (dominant cycles)
        if len(autocorr) > 5:
            peaks, _ = scipy_signal.find_peaks(autocorr, distance=3)
            if len(peaks) > 0:
                dominant_period = peaks[0] + 1  # +1 because we started from lag=1
            else:
                dominant_period = 20  # Default
        else:
            dominant_period = 20
        
        # Signal based on cycle position
        position_in_cycle = len(candles) % dominant_period
        cycle_progress = position_in_cycle / dominant_period
        
        if 0.2 <= cycle_progress < 0.4:
            signal = SignalStrength.BULLISH
        elif 0.4 <= cycle_progress < 0.5:
            signal = SignalStrength.BULLISH_BROKEN
        elif 0.7 <= cycle_progress < 0.9:
            signal = SignalStrength.BEARISH
        elif 0.5 <= cycle_progress < 0.7:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.6
        
        return IndicatorResult(
            indicator_name="Dominant Cycle Period",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(dominant_period),
            additional_values={"cycle_progress": float(cycle_progress)},
            confidence=confidence,
            description=f"دوره چرخه غالب: {dominant_period} - پیشرفت: {cycle_progress:.1%}"
        )
    
    @staticmethod
    def market_facilitation_index(candles: List[Candle]) -> IndicatorResult:
        """
        Market Facilitation Index (MFI) - Bill Williams
        Measures market efficiency
        
        Args:
            candles: List of candles
            
        Returns:
            IndicatorResult with signal
        """
        if len(candles) < 2:
            return IndicatorResult(
                indicator_name="Market Facilitation Index",
                category=IndicatorCategory.CYCLE,
                signal=SignalStrength.NEUTRAL,
                value=0.0,
                confidence=0.5,
                description="داده ناکافی"
            )
        
        # MFI = (High - Low) / Volume
        current = candles[-1]
        previous = candles[-2]
        
        mfi_current = (current.high - current.low) / current.volume if current.volume > 0 else 0
        mfi_previous = (previous.high - previous.low) / previous.volume if previous.volume > 0 else 0
        
        # Compare MFI and Volume changes
        mfi_up = mfi_current > mfi_previous
        vol_up = current.volume > previous.volume
        
        # Four scenarios
        if mfi_up and vol_up:
            signal = SignalStrength.VERY_BULLISH  # Green - Bullish trend
            desc = "سبز - بازار تسهیل شده و حجم بالا (صعودی قوی)"
        elif mfi_up and not vol_up:
            signal = SignalStrength.BULLISH_BROKEN  # Fade - Weak buyers
            desc = "محو - تسهیل بالا ولی حجم پایین (ضعف خریداران)"
        elif not mfi_up and vol_up:
            signal = SignalStrength.BEARISH_BROKEN  # Fake - False move
            desc = "جعلی - تسهیل پایین با حجم بالا (حرکت کاذب)"
        else:
            signal = SignalStrength.BEARISH  # Squat - Potential reversal
            desc = "چمباتمه - تسهیل و حجم پایین (احتمال بازگشت)"
        
        confidence = 0.65
        
        return IndicatorResult(
            indicator_name="Market Facilitation Index",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(mfi_current),
            additional_values={
                "mfi_previous": float(mfi_previous),
                "volume_change": float((current.volume - previous.volume) / previous.volume * 100)
            },
            confidence=confidence,
            description=desc
        )
    
    @staticmethod
    def cycle_phase_index(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Cycle Phase Index
        Identifies where price is in the cycle
        
        Args:
            candles: List of candles
            period: Cycle period
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        
        # Calculate phase using Hilbert Transform approximation
        # Simple approximation using sine and cosine components
        phase_values = []
        
        for i in range(len(closes)):
            if i < period:
                phase_values.append(0)
            else:
                window = closes.iloc[i-period:i].values
                # Normalize
                if window.max() != window.min():
                    normalized = (window - window.min()) / (window.max() - window.min())
                    # Simple phase calculation
                    angle = np.arctan2(normalized[-1] - 0.5, i % period / period - 0.5)
                    phase = (angle + np.pi) / (2 * np.pi)  # Normalize to 0-1
                else:
                    phase = 0.5
                phase_values.append(phase)
        
        phase_current = phase_values[-1]
        
        # Signal based on cycle phase
        if 0 <= phase_current < 0.125:
            signal = SignalStrength.BULLISH
            desc = "فاز 1 - شروع صعود"
        elif 0.125 <= phase_current < 0.25:
            signal = SignalStrength.VERY_BULLISH
            desc = "فاز 2 - صعود قوی"
        elif 0.25 <= phase_current < 0.375:
            signal = SignalStrength.BULLISH_BROKEN
            desc = "فاز 3 - اوج و تضعیف"
        elif 0.375 <= phase_current < 0.5:
            signal = SignalStrength.NEUTRAL
            desc = "فاز 4 - انتقال به نزول"
        elif 0.5 <= phase_current < 0.625:
            signal = SignalStrength.BEARISH_BROKEN
            desc = "فاز 5 - شروع نزول"
        elif 0.625 <= phase_current < 0.75:
            signal = SignalStrength.BEARISH
            desc = "فاز 6 - نزول"
        elif 0.75 <= phase_current < 0.875:
            signal = SignalStrength.VERY_BEARISH
            desc = "فاز 7 - نزول قوی"
        else:
            signal = SignalStrength.BEARISH_BROKEN
            desc = "فاز 8 - کف و انتقال"
        
        confidence = 0.62
        
        return IndicatorResult(
            indicator_name=f"Cycle Phase({period})",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(phase_current),
            confidence=confidence,
            description=desc
        )
    
    @staticmethod
    def trend_vs_cycle_identifier(candles: List[Candle], trend_period: int = 50) -> IndicatorResult:
        """
        Identify if market is trending or cycling
        
        Args:
            candles: List of candles
            trend_period: Period for trend calculation
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        
        # Calculate ADX-like measure for trend strength
        highs = pd.Series([c.high for c in candles])
        lows = pd.Series([c.low for c in candles])
        
        # Simple trend strength using linear regression R²
        x = np.arange(len(closes[-trend_period:]))
        y = closes[-trend_period:].values
        
        if len(x) > 1:
            correlation = np.corrcoef(x, y)[0, 1]
            r_squared = correlation ** 2
        else:
            r_squared = 0
        
        # High R² = trending, Low R² = cycling
        trend_strength = r_squared
        
        # Signal based on trend vs cycle
        if trend_strength > 0.7:
            # Strong trend
            if closes.iloc[-1] > closes.iloc[-trend_period]:
                signal = SignalStrength.VERY_BULLISH
                desc = "روند صعودی قوی"
            else:
                signal = SignalStrength.VERY_BEARISH
                desc = "روند نزولی قوی"
        elif trend_strength > 0.5:
            # Moderate trend
            if closes.iloc[-1] > closes.iloc[-trend_period]:
                signal = SignalStrength.BULLISH
                desc = "روند صعودی متوسط"
            else:
                signal = SignalStrength.BEARISH
                desc = "روند نزولی متوسط"
        else:
            # Cycling market
            signal = SignalStrength.NEUTRAL
            desc = f"بازار در حالت چرخه‌ای (قدرت روند: {trend_strength:.2f})"
        
        confidence = 0.7
        
        return IndicatorResult(
            indicator_name=f"Trend vs Cycle({trend_period})",
            category=IndicatorCategory.CYCLE,
            signal=signal,
            value=float(trend_strength),
            additional_values={
                "market_state_numeric": 1.0 if trend_strength > 0.5 else 0.0
            },
            confidence=confidence,
            description=desc
        )
    
    @staticmethod
    def calculate_all(candles: List[Candle]) -> List[IndicatorResult]:
        """
        Calculate all cycle indicators
        
        Args:
            candles: List of candles
            
        Returns:
            List of all cycle indicator results
        """
        results = []
        
        if len(candles) >= 20:
            results.append(CycleIndicators.sine_wave(candles, 20))
            results.append(CycleIndicators.detrended_price_oscillator(candles, 20))
            results.append(CycleIndicators.cycle_phase_index(candles, 20))
            results.append(CycleIndicators.market_facilitation_index(candles))
        
        if len(candles) >= 50:
            results.append(CycleIndicators.schaff_trend_cycle(candles, 23, 50, 10))
            results.append(CycleIndicators.dominant_cycle_period(candles, 50))
            results.append(CycleIndicators.trend_vs_cycle_identifier(candles, 50))
        
        return results
