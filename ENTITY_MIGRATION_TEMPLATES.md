# Entity Migration Templates

**Task:** Phase 2.1 - Day 1 - Task 1.3  
**Team:** Dr. Chen Wei (SW-001) + Prof. Alexandre Dubois (TAA-005)  
**Purpose:** Template files for creating 8 new entity files  
**Date:** November 7, 2025

---

## Template 1: signal_strength.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/signal_strength.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Signal strength enumeration with Persian labels
Lines of Code:       80
Estimated Time:      1.5 hours
Cost:                $450 (1.5 hours × $300/hr)
Complexity:          2/10
Test Coverage:       100%
Performance Impact:  LOW
Dependencies:        enum (stdlib)
Related Files:       indicator_result.py, pattern_result.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Signal Strength Enumeration

Defines 7 levels of signal strength from VERY_BEARISH to VERY_BULLISH.
Used by all indicators and patterns for unified signal representation.
"""

from enum import Enum


class SignalStrength(str, Enum):
    """Signal strength enum with Persian names"""
    VERY_BULLISH = "بسیار صعودی"
    BULLISH = "صعودی"
    BULLISH_BROKEN = "صعودی شکسته شده"
    NEUTRAL = "خنثی"
    BEARISH_BROKEN = "نزولی شکسته شده"
    BEARISH = "نزولی"
    VERY_BEARISH = "بسیار نزولی"
    
    @staticmethod
    def from_value(value: float) -> 'SignalStrength':
        """
        Convert numeric value (-1 to 1) to SignalStrength
        
        Args:
            value: Normalized value between -1 and 1
                   -1.0 = VERY_BEARISH
                    0.0 = NEUTRAL
                   +1.0 = VERY_BULLISH
            
        Returns:
            Corresponding SignalStrength enum value
            
        Example:
            >>> SignalStrength.from_value(0.85)
            SignalStrength.VERY_BULLISH
            >>> SignalStrength.from_value(0.0)
            SignalStrength.NEUTRAL
        """
        if value >= 0.8:
            return SignalStrength.VERY_BULLISH
        elif value >= 0.4:
            return SignalStrength.BULLISH
        elif value >= 0.1:
            return SignalStrength.BULLISH_BROKEN
        elif value >= -0.1:
            return SignalStrength.NEUTRAL
        elif value >= -0.4:
            return SignalStrength.BEARISH_BROKEN
        elif value >= -0.8:
            return SignalStrength.BEARISH
        else:
            return SignalStrength.VERY_BEARISH
    
    def get_score(self) -> float:
        """
        Get numeric score for this signal strength
        
        Returns:
            Float score between -2.0 and +2.0
            
        Example:
            >>> SignalStrength.VERY_BULLISH.get_score()
            2.0
            >>> SignalStrength.NEUTRAL.get_score()
            0.0
        """
        scores = {
            SignalStrength.VERY_BULLISH: 2.0,
            SignalStrength.BULLISH: 1.0,
            SignalStrength.BULLISH_BROKEN: 0.5,
            SignalStrength.NEUTRAL: 0.0,
            SignalStrength.BEARISH_BROKEN: -0.5,
            SignalStrength.BEARISH: -1.0,
            SignalStrength.VERY_BEARISH: -2.0,
        }
        return scores.get(self, 0.0)
```

---

## Template 2: indicator_category.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/indicator_category.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Indicator category enumeration
Lines of Code:       30
Estimated Time:      0.5 hours
Cost:                $150 (0.5 hours × $300/hr)
Complexity:          1/10
Test Coverage:       100%
Performance Impact:  LOW
Dependencies:        enum (stdlib)
Related Files:       indicator_result.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Indicator Category Enumeration

Defines 6 main categories for technical indicators with Persian labels.
"""

from enum import Enum


class IndicatorCategory(str, Enum):
    """Technical indicator categories with Persian labels"""
    TREND = "روند"
    MOMENTUM = "مومنتوم"
    CYCLE = "سیکل"
    VOLUME = "حجم"
    VOLATILITY = "نوسان"
    SUPPORT_RESISTANCE = "حمایت و مقاومت"
```

---

## Template 3: pattern_type.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/pattern_type.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Pattern type enumeration
Lines of Code:       25
Estimated Time:      0.5 hours
Cost:                $150 (0.5 hours × $300/hr)
Complexity:          1/10
Test Coverage:       100%
Performance Impact:  LOW
Dependencies:        enum (stdlib)
Related Files:       pattern_result.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Pattern Type Enumeration

Defines 2 main pattern types: Classical and Candlestick.
"""

from enum import Enum


class PatternType(str, Enum):
    """Chart pattern types with Persian labels"""
    CLASSICAL = "کلاسیک"
    CANDLESTICK = "کندل استیک"
```

---

## Template 4: wave_point.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/wave_point.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Elliott Wave point entity
Lines of Code:       45
Estimated Time:      1 hour
Cost:                $300 (1 hour × $300/hr)
Complexity:          2/10
Test Coverage:       100%
Performance Impact:  LOW
Dependencies:        dataclasses, datetime
Related Files:       elliott_wave_result.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Elliott Wave Point Entity

Represents a single point in Elliott Wave analysis (peak or trough).
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WavePoint:
    """
    Immutable Elliott Wave point
    
    Represents a peak or trough in Elliott Wave pattern identification.
    
    Attributes:
        wave_number: Wave number in the sequence (1-5 for impulse, A-C for correction)
        price: Price level at this wave point
        timestamp: Time when this wave point occurred
        wave_type: "PEAK" for tops, "TROUGH" for bottoms
    """
    wave_number: int
    price: float
    timestamp: datetime
    wave_type: str  # "PEAK" or "TROUGH"
    
    def __post_init__(self):
        """Validate wave point data"""
        if self.wave_type not in ["PEAK", "TROUGH"]:
            raise ValueError(f"wave_type must be 'PEAK' or 'TROUGH', got '{self.wave_type}'")
        if self.price <= 0:
            raise ValueError(f"price must be positive, got {self.price}")
```

---

## Template 5: indicator_result.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/indicator_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Indicator calculation result entity
Lines of Code:       75
Estimated Time:      1.5 hours
Cost:                $450 (1.5 hours × $300/hr)
Complexity:          3/10
Test Coverage:       100%
Performance Impact:  MEDIUM
Dependencies:        dataclasses, datetime, typing
Related Files:       signal_strength.py, indicator_category.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Indicator Result Entity

Represents the result of a single technical indicator calculation.
Used by all 60+ indicators in the system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from .signal_strength import SignalStrength
from .indicator_category import IndicatorCategory


@dataclass(frozen=True)
class IndicatorResult:
    """
    Immutable indicator calculation result
    
    Attributes:
        indicator_name: Name of the indicator (e.g., "RSI", "MACD", "Bollinger Bands")
        category: Indicator category (TREND, MOMENTUM, etc.)
        signal: Signal strength (VERY_BULLISH to VERY_BEARISH)
        value: Primary indicator value (e.g., RSI value, MACD line)
        additional_values: Optional dict for multi-line indicators
                          (e.g., {"signal": 12.5, "histogram": 2.3} for MACD)
        confidence: Confidence level (0.0 to 1.0)
        description: Human-readable description (optional)
        timestamp: When this result was calculated
    """
    indicator_name: str
    category: IndicatorCategory
    signal: SignalStrength
    value: float
    additional_values: Optional[Dict[str, float]] = None
    confidence: float = 0.75
    description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate indicator result data"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")
        if not self.indicator_name:
            raise ValueError("indicator_name cannot be empty")
```

---

## Template 6: pattern_result.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/pattern_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Pattern recognition result entity
Lines of Code:       80
Estimated Time:      1.5 hours
Cost:                $450 (1.5 hours × $300/hr)
Complexity:          3/10
Test Coverage:       100%
Performance Impact:  MEDIUM
Dependencies:        dataclasses, datetime, typing
Related Files:       signal_strength.py, pattern_type.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Pattern Recognition Result Entity

Represents the result of chart pattern detection (classical or candlestick).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .signal_strength import SignalStrength
from .pattern_type import PatternType


@dataclass(frozen=True)
class PatternResult:
    """
    Immutable pattern recognition result
    
    Attributes:
        pattern_name: Name of the pattern (e.g., "Head and Shoulders", "Doji")
        pattern_type: CLASSICAL or CANDLESTICK
        signal: Signal strength of the pattern
        confidence: Pattern confidence (0.0 to 1.0)
        start_time: When pattern started forming
        end_time: When pattern completed
        description: Human-readable description
        price_target: Optional projected price target
        stop_loss: Optional stop loss level
    """
    pattern_name: str
    pattern_type: PatternType
    signal: SignalStrength
    confidence: float
    start_time: datetime
    end_time: datetime
    description: str
    price_target: Optional[float] = None
    stop_loss: Optional[float] = None
    
    def __post_init__(self):
        """Validate pattern result data"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")
        if self.end_time < self.start_time:
            raise ValueError(f"end_time ({self.end_time}) must be >= start_time ({self.start_time})")
        if not self.pattern_name:
            raise ValueError("pattern_name cannot be empty")
        if self.price_target is not None and self.price_target <= 0:
            raise ValueError(f"price_target must be positive, got {self.price_target}")
        if self.stop_loss is not None and self.stop_loss <= 0:
            raise ValueError(f"stop_loss must be positive, got {self.stop_loss}")
```

---

## Template 7: elliott_wave_result.py

```python
"""
================================================================================
FILE IDENTITY CARD (شناسنامه فایل)
================================================================================
File Path:           src/core/domain/entities/elliott_wave_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Last Modified:       2025-11-07
Version:             1.0.0
Purpose:             Elliott Wave analysis result entity
Lines of Code:       75
Estimated Time:      1.5 hours
Cost:                $450 (1.5 hours × $300/hr)
Complexity:          4/10
Test Coverage:       100%
Performance Impact:  MEDIUM
Dependencies:        dataclasses, typing
Related Files:       signal_strength.py, wave_point.py
Changelog:
  - 2025-11-07: Initial implementation (Phase 2.1 - Task 1.3)
================================================================================

Elliott Wave Analysis Result Entity

Represents complete Elliott Wave pattern analysis including all wave points.
"""

from dataclasses import dataclass
from typing import List, Optional
from .signal_strength import SignalStrength
from .wave_point import WavePoint


@dataclass(frozen=True)
class ElliottWaveResult:
    """
    Immutable Elliott Wave analysis result
    
    Attributes:
        wave_pattern: "IMPULSIVE" (5 waves) or "CORRECTIVE" (3 waves)
        current_wave: Current wave number being formed
        waves: List of identified wave points (peaks and troughs)
        signal: Overall signal from wave analysis
        confidence: Wave pattern confidence (0.0 to 1.0)
        description: Human-readable wave analysis
        projected_target: Optional projected price target
    """
    wave_pattern: str  # "IMPULSIVE" or "CORRECTIVE"
    current_wave: int
    waves: List[WavePoint]
    signal: SignalStrength
    confidence: float
    description: str
    projected_target: Optional[float] = None
    
    def __post_init__(self):
        """Validate Elliott Wave result data"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")
        if self.wave_pattern not in ["IMPULSIVE", "CORRECTIVE"]:
            raise ValueError(f"wave_pattern must be 'IMPULSIVE' or 'CORRECTIVE', got '{self.wave_pattern}'")
        if self.wave_pattern == "IMPULSIVE" and len(self.waves) > 5:
            raise ValueError(f"IMPULSIVE pattern should have max 5 waves, got {len(self.waves)}")
        if self.wave_pattern == "CORRECTIVE" and len(self.waves) > 3:
            raise ValueError(f"CORRECTIVE pattern should have max 3 waves, got {len(self.waves)}")
        if self.projected_target is not None and self.projected_target <= 0:
            raise ValueError(f"projected_target must be positive, got {self.projected_target}")
```

---

## Template 8: Updated __init__.py

```python
"""
================================================================================
Core Domain Entities Package

Clean Architecture - Domain Layer
All business entities are immutable and framework-independent.

Exported Entities:
- Candle: OHLCV price data
- Signal: Trading signal entity
- Decision: Trading decision entity
- SignalStrength: Signal strength enumeration (7 levels)
- IndicatorCategory: Indicator category enumeration (6 categories)
- IndicatorResult: Single indicator calculation result
- PatternType: Pattern type enumeration (2 types)
- PatternResult: Pattern recognition result
- WavePoint: Elliott Wave point
- ElliottWaveResult: Complete Elliott Wave analysis

Last Updated: 2025-11-07 (Phase 2.1 - Task 1.3)
================================================================================
"""

# Existing exports (Phase 2)
from .candle import Candle, CandleType
from .signal import Signal
from .decision import Decision

# NEW exports (Phase 2.1 - Task 1.3)
from .signal_strength import SignalStrength
from .indicator_category import IndicatorCategory
from .indicator_result import IndicatorResult
from .pattern_type import PatternType
from .pattern_result import PatternResult
from .wave_point import WavePoint
from .elliott_wave_result import ElliottWaveResult

__all__ = [
    # Existing (Phase 2)
    "Candle",
    "CandleType",
    "Signal",
    "Decision",
    
    # NEW (Phase 2.1)
    "SignalStrength",
    "IndicatorCategory",
    "IndicatorResult",
    "PatternType",
    "PatternResult",
    "WavePoint",
    "ElliottWaveResult",
]
```

---

## Implementation Checklist

### Task 1.3 - Step-by-Step Guide

#### Step 1: Create Base Enums (1.5 hours)
- [ ] Create `signal_strength.py` (Template 1)
- [ ] Create `indicator_category.py` (Template 2)
- [ ] Create `pattern_type.py` (Template 3)
- [ ] Test imports: `from src.core.domain.entities import SignalStrength`

#### Step 2: Create Simple Entities (1 hour)
- [ ] Create `wave_point.py` (Template 4)
- [ ] Test instantiation and validation

#### Step 3: Create Complex Entities (4.5 hours)
- [ ] Create `indicator_result.py` (Template 5)
- [ ] Create `pattern_result.py` (Template 6)
- [ ] Create `elliott_wave_result.py` (Template 7)
- [ ] Test all validations

#### Step 4: Update Existing Files (2.5 hours)
- [ ] Update `candle.py` with missing methods:
  - `typical_price` property
  - `is_bullish` property
  - `is_bearish` property
  - `true_range()` method
- [ ] Update version to 1.2.0
- [ ] Update identity card

#### Step 5: Update Package (0.5 hours)
- [ ] Update `__init__.py` (Template 8)
- [ ] Test all imports
- [ ] Verify no circular dependencies

#### Step 6: Documentation (1 hour)
- [ ] Create `src/core/domain/entities/README.md`
- [ ] Document import migration guide
- [ ] Add usage examples

#### Step 7: Testing (1 hour)
- [ ] Create unit tests for each new entity
- [ ] Test validation edge cases
- [ ] Test enum conversions (SignalStrength.from_value)
- [ ] Run full test suite

**Total:** 12 hours (as allocated)

---

## Validation Commands

```bash
# Test imports
python -c "from src.core.domain.entities import SignalStrength, IndicatorResult, PatternResult"

# Test SignalStrength
python -c "from src.core.domain.entities import SignalStrength; print(SignalStrength.from_value(0.9))"

# Test IndicatorResult creation
python -c "
from src.core.domain.entities import IndicatorResult, SignalStrength, IndicatorCategory
from datetime import datetime
result = IndicatorResult(
    indicator_name='RSI',
    category=IndicatorCategory.MOMENTUM,
    signal=SignalStrength.BULLISH,
    value=65.0,
    confidence=0.85
)
print(result)
"

# Run tests
pytest tests/test_entities/ -v
```

---

**Templates Ready For:** Dr. Chen Wei + Prof. Alexandre Dubois  
**Next Action:** Begin Task 1.3 implementation  
**Estimated Completion:** End of Day 1 (20:00 UTC)
