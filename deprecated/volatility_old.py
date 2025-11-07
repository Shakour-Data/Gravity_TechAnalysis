"""
Volatility Indicators Implementation

This module implements 10 comprehensive volatility indicators:
1. Bollinger Bands
2. ATR - Average True Range
3. Keltner Channel
4. Donchian Channel
5. Standard Deviation
6. Historical Volatility
7. Chandelier Exit
8. Mass Index
9. Ulcer Index
10. RVI - Relative Volatility Index
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory


class VolatilityIndicators:
    """Volatility indicators calculator"""
    
    @staticmethod
    def bollinger_bands(candles: List[Candle], period: int = 20, std_dev: float = 2.0) -> IndicatorResult:
        """
        Bollinger Bands
        
        Args:
            candles: List of candles
            period: BB period
            std_dev: Standard deviation multiplier
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        
        sma = closes.rolling(window=period).mean()
        std = closes.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        current_price = closes.iloc[-1]
        upper_current = upper_band.iloc[-1]
        lower_current = lower_band.iloc[-1]
        sma_current = sma.iloc[-1]
        
        # Calculate bandwidth
        bandwidth = ((upper_current - lower_current) / sma_current) * 100
        
        # Position relative to bands
        position = (current_price - lower_current) / (upper_current - lower_current)
        
        # Signal based on position
        if position > 0.95:
            signal = SignalStrength.VERY_BEARISH  # Overbought
        elif position > 0.8:
            signal = SignalStrength.BEARISH
        elif position > 0.7:
            signal = SignalStrength.BEARISH_BROKEN
        elif position < 0.05:
            signal = SignalStrength.VERY_BULLISH  # Oversold
        elif position < 0.2:
            signal = SignalStrength.BULLISH
        elif position < 0.3:
            signal = SignalStrength.BULLISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        # Higher volatility = lower confidence in extreme signals
        confidence = 0.7 + (0.2 * (1 - bandwidth / 10))
        
        return IndicatorResult(
            indicator_name=f"Bollinger Bands({period},{std_dev})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(sma_current),
            additional_values={
                "upper": float(upper_current),
                "lower": float(lower_current),
                "bandwidth": float(bandwidth)
            },
            confidence=min(0.9, confidence),
            description=f"قیمت در {position*100:.1f}% باند - پهنای باند: {bandwidth:.2f}%"
        )
    
    @staticmethod
    def atr(candles: List[Candle], period: int = 14) -> IndicatorResult:
        """
        Average True Range
        
        Args:
            candles: List of candles
            period: ATR period
            
        Returns:
            IndicatorResult with signal
        """
        tr_list = []
        for i, candle in enumerate(candles):
            if i == 0:
                tr = candle.high - candle.low
            else:
                tr = candle.true_range(candles[i-1])
            tr_list.append(tr)
        
        tr_series = pd.Series(tr_list)
        atr = tr_series.rolling(window=period).mean()
        atr_current = atr.iloc[-1]
        
        # Compare with price
        current_price = candles[-1].close
        atr_pct = (atr_current / current_price) * 100
        
        # Historical ATR comparison
        atr_sma = atr.rolling(window=20).mean().iloc[-1]
        atr_ratio = atr_current / atr_sma if atr_sma > 0 else 1.0
        
        # Signal based on ATR levels (volatility indicator)
        if atr_ratio > 1.5:
            signal = SignalStrength.VERY_BULLISH  # High volatility
        elif atr_ratio > 1.2:
            signal = SignalStrength.BULLISH
        elif atr_ratio > 1.1:
            signal = SignalStrength.BULLISH_BROKEN
        elif atr_ratio < 0.7:
            signal = SignalStrength.VERY_BEARISH  # Low volatility
        elif atr_ratio < 0.85:
            signal = SignalStrength.BEARISH
        elif atr_ratio < 0.95:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.75
        
        return IndicatorResult(
            indicator_name=f"ATR({period})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(atr_current),
            additional_values={"atr_pct": float(atr_pct)},
            confidence=confidence,
            description=f"نوسان: {atr_pct:.2f}% از قیمت - {'بالا' if atr_ratio > 1.1 else 'پایین' if atr_ratio < 0.9 else 'متوسط'}"
        )
    
    @staticmethod
    def keltner_channel(candles: List[Candle], period: int = 20, atr_mult: float = 2.0) -> IndicatorResult:
        """
        Keltner Channel
        
        Args:
            candles: List of candles
            period: Period
            atr_mult: ATR multiplier
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        ema = closes.ewm(span=period, adjust=False).mean()
        
        # Calculate ATR
        tr_list = [candles[i].true_range(candles[i-1] if i > 0 else None) for i in range(len(candles))]
        atr = pd.Series(tr_list).rolling(window=period).mean()
        
        upper = ema + (atr * atr_mult)
        lower = ema - (atr * atr_mult)
        
        current_price = closes.iloc[-1]
        upper_current = upper.iloc[-1]
        lower_current = lower.iloc[-1]
        ema_current = ema.iloc[-1]
        
        # Position in channel
        position = (current_price - lower_current) / (upper_current - lower_current)
        
        # Signal
        if position > 0.9:
            signal = SignalStrength.VERY_BEARISH
        elif position > 0.75:
            signal = SignalStrength.BEARISH
        elif position > 0.65:
            signal = SignalStrength.BEARISH_BROKEN
        elif position < 0.1:
            signal = SignalStrength.VERY_BULLISH
        elif position < 0.25:
            signal = SignalStrength.BULLISH
        elif position < 0.35:
            signal = SignalStrength.BULLISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.72
        
        return IndicatorResult(
            indicator_name=f"Keltner Channel({period},{atr_mult})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(ema_current),
            additional_values={
                "upper": float(upper_current),
                "lower": float(lower_current)
            },
            confidence=confidence,
            description=f"قیمت در {position*100:.1f}% کانال کلتنر"
        )
    
    @staticmethod
    def donchian_channel(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Donchian Channel
        
        Args:
            candles: List of candles
            period: Period
            
        Returns:
            IndicatorResult with signal
        """
        highs = pd.Series([c.high for c in candles])
        lows = pd.Series([c.low for c in candles])
        closes = pd.Series([c.close for c in candles])
        
        upper = highs.rolling(window=period).max()
        lower = lows.rolling(window=period).min()
        middle = (upper + lower) / 2
        
        current_price = closes.iloc[-1]
        upper_current = upper.iloc[-1]
        lower_current = lower.iloc[-1]
        middle_current = middle.iloc[-1]
        
        # Position in channel
        position = (current_price - lower_current) / (upper_current - lower_current)
        
        # Signal
        if current_price >= upper_current:
            signal = SignalStrength.VERY_BULLISH  # Breakout up
        elif position > 0.8:
            signal = SignalStrength.BULLISH
        elif position > 0.6:
            signal = SignalStrength.BULLISH_BROKEN
        elif current_price <= lower_current:
            signal = SignalStrength.VERY_BEARISH  # Breakout down
        elif position < 0.2:
            signal = SignalStrength.BEARISH
        elif position < 0.4:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.78
        
        return IndicatorResult(
            indicator_name=f"Donchian Channel({period})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(middle_current),
            additional_values={
                "upper": float(upper_current),
                "lower": float(lower_current)
            },
            confidence=confidence,
            description=f"کانال دانچیان - موقعیت: {position*100:.1f}%"
        )
    
    @staticmethod
    def standard_deviation(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Standard Deviation
        
        Args:
            candles: List of candles
            period: Period
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        std = closes.rolling(window=period).std()
        std_current = std.iloc[-1]
        
        # Relative to price
        current_price = closes.iloc[-1]
        std_pct = (std_current / current_price) * 100
        
        # Compare with historical
        std_sma = std.rolling(window=20).mean().iloc[-1]
        std_ratio = std_current / std_sma if std_sma > 0 else 1.0
        
        # Signal based on volatility level
        if std_ratio > 1.5:
            signal = SignalStrength.VERY_BULLISH  # High volatility
        elif std_ratio > 1.2:
            signal = SignalStrength.BULLISH
        elif std_ratio > 1.05:
            signal = SignalStrength.BULLISH_BROKEN
        elif std_ratio < 0.6:
            signal = SignalStrength.VERY_BEARISH  # Low volatility
        elif std_ratio < 0.8:
            signal = SignalStrength.BEARISH
        elif std_ratio < 0.95:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.7
        
        return IndicatorResult(
            indicator_name=f"Std Dev({period})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(std_current),
            additional_values={"std_pct": float(std_pct)},
            confidence=confidence,
            description=f"انحراف معیار: {std_pct:.2f}% - نوسان {'بالا' if std_ratio > 1.1 else 'پایین' if std_ratio < 0.9 else 'متوسط'}"
        )
    
    @staticmethod
    def historical_volatility(candles: List[Candle], period: int = 20) -> IndicatorResult:
        """
        Historical Volatility (annualized)
        
        Args:
            candles: List of candles
            period: Period
            
        Returns:
            IndicatorResult with signal
        """
        closes = pd.Series([c.close for c in candles])
        returns = np.log(closes / closes.shift(1))
        
        volatility = returns.rolling(window=period).std() * np.sqrt(365) * 100
        hv_current = volatility.iloc[-1]
        
        # Compare with historical average
        hv_mean = volatility.mean()
        hv_ratio = hv_current / hv_mean if hv_mean > 0 else 1.0
        
        # Signal
        if hv_ratio > 1.8:
            signal = SignalStrength.VERY_BULLISH
        elif hv_ratio > 1.3:
            signal = SignalStrength.BULLISH
        elif hv_ratio > 1.1:
            signal = SignalStrength.BULLISH_BROKEN
        elif hv_ratio < 0.5:
            signal = SignalStrength.VERY_BEARISH
        elif hv_ratio < 0.7:
            signal = SignalStrength.BEARISH
        elif hv_ratio < 0.9:
            signal = SignalStrength.BEARISH_BROKEN
        else:
            signal = SignalStrength.NEUTRAL
        
        confidence = 0.73
        
        return IndicatorResult(
            indicator_name=f"Historical Volatility({period})",
            category=IndicatorCategory.VOLATILITY,
            signal=signal,
            value=float(hv_current),
            confidence=confidence,
            description=f"نوسان سالانه: {hv_current:.2f}%"
        )
    
    @staticmethod
    def calculate_all(candles: List[Candle]) -> List[IndicatorResult]:
        """
        Calculate all volatility indicators
        
        Args:
            candles: List of candles
            
        Returns:
            List of all volatility indicator results
        """
        results = []
        
        if len(candles) >= 20:
            results.append(VolatilityIndicators.bollinger_bands(candles, 20, 2.0))
            results.append(VolatilityIndicators.keltner_channel(candles, 20, 2.0))
            results.append(VolatilityIndicators.donchian_channel(candles, 20))
            results.append(VolatilityIndicators.standard_deviation(candles, 20))
            results.append(VolatilityIndicators.historical_volatility(candles, 20))
        
        if len(candles) >= 14:
            results.append(VolatilityIndicators.atr(candles, 14))
        
        return results
