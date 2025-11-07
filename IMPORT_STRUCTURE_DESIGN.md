# Import Structure Design Document

**Task:** Phase 2.1 - Day 1 - Task 1.2  
**Team:** Dr. Chen Wei (SW-001)  
**Duration:** 4 hours  
**Cost:** $1,200  
**Date:** November 7, 2025

---

## Executive Summary

This document defines the new import structure for migrating models from `models.schemas` to `src/core/domain/entities/`. The migration will resolve all dependency violations identified in Task 1.1 and establish Clean Architecture compliance.

**Key Findings:**
- 8 new entity files needed
- 1 existing file (candle.py) needs conflict resolution
- 11 files in src/core/ need import updates
- Backward compatibility layer required

---

## Current State Analysis

### Existing Entity Files in src/core/domain/entities/

1. **candle.py** ✅ EXISTS
   - Lines: 123
   - Type: Dataclass (immutable)
   - Status: Complete with identity card
   - **CONFLICT:** Also exists in models.schemas as Pydantic model

2. **signal.py** ✅ EXISTS
   - Lines: ~80
   - Status: Complete with identity card

3. **decision.py** ✅ EXISTS
   - Lines: ~100
   - Status: Complete with identity card

4. **__init__.py** ✅ EXISTS
   - Exports: Candle, Signal, Decision

### Models in models/schemas.py (Need Migration)

| Model Name | Type | Lines | Used By | Priority |
|------------|------|-------|---------|----------|
| SignalStrength | Enum | 50 | 9 files | CRITICAL |
| IndicatorResult | Pydantic | 30 | 6 files | CRITICAL |
| IndicatorCategory | Enum | 10 | 6 files | CRITICAL |
| PatternResult | Pydantic | 25 | 2 files | HIGH |
| PatternType | Enum | 5 | 2 files | HIGH |
| ElliottWaveResult | Pydantic | 30 | 1 file | MEDIUM |
| WavePoint | Pydantic | 15 | 1 file | MEDIUM |
| Candle | Pydantic | 100 | 11 files | CRITICAL |

---

## New Import Structure Design

### Directory Structure

```
src/core/domain/entities/
├── __init__.py                    # Central exports
├── candle.py                      # ✅ EXISTS (needs update)
├── signal.py                      # ✅ EXISTS
├── decision.py                    # ✅ EXISTS
├── signal_strength.py             # 🆕 NEW (Task 1.3)
├── indicator_result.py            # 🆕 NEW (Task 1.3)
├── indicator_category.py          # 🆕 NEW (Task 1.3)
├── pattern_result.py              # 🆕 NEW (Task 1.3)
├── pattern_type.py                # 🆕 NEW (Task 1.3)
├── elliott_wave_result.py         # 🆕 NEW (Task 1.3)
├── wave_point.py                  # 🆕 NEW (Task 1.3)
└── README.md                      # 🆕 Documentation
```

---

## Entity File Specifications

### 1. signal_strength.py (🆕 NEW)

**Purpose:** Signal strength enumeration with Persian labels  
**Migration from:** models.schemas.py lines 11-58  
**Type:** Enum + utility methods  
**Estimated Lines:** 80  
**Time:** 1.5 hours  
**Dependencies:** None

**Key Features:**
- 7 signal levels (VERY_BULLISH to VERY_BEARISH)
- Persian names for UI display
- `from_value()` method (float → SignalStrength)
- `get_score()` method (SignalStrength → float)

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/signal_strength.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Signal strength enumeration
================================================================================
"""

from enum import Enum

class SignalStrength(str, Enum):
    """Signal strength with Persian labels"""
    VERY_BULLISH = "بسیار صعودی"
    BULLISH = "صعودی"
    # ... (7 levels total)
    
    @staticmethod
    def from_value(value: float) -> 'SignalStrength':
        """Convert float (-1 to 1) to SignalStrength"""
        # Implementation from models.schemas
    
    def get_score(self) -> float:
        """Get numeric score (-2.0 to 2.0)"""
        # Implementation from models.schemas
```

---

### 2. indicator_result.py (🆕 NEW)

**Purpose:** Result from a single indicator calculation  
**Migration from:** models.schemas.py lines 169-197  
**Type:** Dataclass (immutable preferred)  
**Estimated Lines:** 60  
**Time:** 1.5 hours  
**Dependencies:** signal_strength, indicator_category

**Key Features:**
- indicator_name, category, signal, value
- additional_values (Dict for multi-line indicators)
- confidence (0.0-1.0)
- timestamp

**Design Decision:**
- **Option A:** Keep as Pydantic (validation benefits)
- **Option B:** Convert to dataclass (consistency with candle.py)
- **CHOSEN:** Dataclass with manual validation (Clean Architecture)

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/indicator_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Indicator calculation result entity
================================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from .signal_strength import SignalStrength
from .indicator_category import IndicatorCategory

@dataclass(frozen=True)
class IndicatorResult:
    """Immutable indicator result"""
    indicator_name: str
    category: IndicatorCategory
    signal: SignalStrength
    value: float
    additional_values: Optional[Dict[str, float]] = None
    confidence: float = 0.75
    description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate fields"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be 0.0-1.0")
```

---

### 3. indicator_category.py (🆕 NEW)

**Purpose:** Indicator category enumeration  
**Migration from:** models.schemas.py lines 162-169  
**Type:** Enum  
**Estimated Lines:** 25  
**Time:** 0.5 hours  
**Dependencies:** None

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/indicator_category.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Indicator category enumeration
================================================================================
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

### 4. pattern_result.py (🆕 NEW)

**Purpose:** Chart pattern recognition result  
**Migration from:** models.schemas.py lines 205-232  
**Type:** Dataclass  
**Estimated Lines:** 60  
**Time:** 1.5 hours  
**Dependencies:** signal_strength, pattern_type

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/pattern_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Pattern recognition result entity
================================================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .signal_strength import SignalStrength
from .pattern_type import PatternType

@dataclass(frozen=True)
class PatternResult:
    """Immutable pattern recognition result"""
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
        """Validate fields"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be 0.0-1.0")
        if self.end_time < self.start_time:
            raise ValueError("end_time must be >= start_time")
```

---

### 5. pattern_type.py (🆕 NEW)

**Purpose:** Pattern type enumeration  
**Migration from:** models.schemas.py lines 200-203  
**Type:** Enum  
**Estimated Lines:** 20  
**Time:** 0.5 hours  
**Dependencies:** None

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/pattern_type.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Pattern type enumeration
================================================================================
"""

from enum import Enum

class PatternType(str, Enum):
    """Chart pattern types with Persian labels"""
    CLASSICAL = "کلاسیک"
    CANDLESTICK = "کندل استیک"
```

---

### 6. elliott_wave_result.py (🆕 NEW)

**Purpose:** Elliott Wave analysis result  
**Migration from:** models.schemas.py lines 243-268  
**Type:** Dataclass  
**Estimated Lines:** 55  
**Time:** 1.5 hours  
**Dependencies:** signal_strength, wave_point

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/elliott_wave_result.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Elliott Wave analysis result entity
================================================================================
"""

from dataclasses import dataclass
from typing import List, Optional
from .signal_strength import SignalStrength
from .wave_point import WavePoint

@dataclass(frozen=True)
class ElliottWaveResult:
    """Immutable Elliott Wave analysis result"""
    wave_pattern: str  # "IMPULSIVE" or "CORRECTIVE"
    current_wave: int
    waves: List[WavePoint]
    signal: SignalStrength
    confidence: float
    description: str
    projected_target: Optional[float] = None
    
    def __post_init__(self):
        """Validate fields"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be 0.0-1.0")
        if self.wave_pattern not in ["IMPULSIVE", "CORRECTIVE"]:
            raise ValueError("Invalid wave_pattern")
```

---

### 7. wave_point.py (🆕 NEW)

**Purpose:** Single Elliott Wave point  
**Migration from:** models.schemas.py lines 235-241  
**Type:** Dataclass  
**Estimated Lines:** 35  
**Time:** 1 hour  
**Dependencies:** None

**Template Structure:**
```python
"""
================================================================================
FILE IDENTITY CARD
================================================================================
File Path:           src/core/domain/entities/wave_point.py
Author:              Dr. Chen Wei
Team ID:             SW-001
Created Date:        2025-11-07
Purpose:             Elliott Wave point entity
================================================================================
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class WavePoint:
    """Immutable Elliott Wave point"""
    wave_number: int
    price: float
    timestamp: datetime
    wave_type: str  # "PEAK" or "TROUGH"
    
    def __post_init__(self):
        """Validate fields"""
        if self.wave_type not in ["PEAK", "TROUGH"]:
            raise ValueError("wave_type must be PEAK or TROUGH")
```

---

### 8. candle.py (🔧 UPDATE EXISTING)

**Purpose:** Resolve conflict between dataclass and Pydantic versions  
**Current State:** Dataclass version exists in src/core/domain/entities/  
**Migration from:** models.schemas.py lines 60-157 (Pydantic version)  
**Action:** KEEP dataclass, DELETE Pydantic from models.schemas  
**Estimated Lines:** 150 (add missing methods)  
**Time:** 2 hours  
**Dependencies:** None

**Missing Features to Add:**
1. `typical_price` property
2. `is_bullish` property
3. `is_bearish` property
4. `true_range()` method
5. Validators (convert from Pydantic to manual validation)

**Update Plan:**
```python
# Add to existing candle.py:
@property
def typical_price(self) -> float:
    """Calculate typical price: (H + L + C) / 3"""
    return (self.high + self.low + self.close) / 3

@property
def is_bullish(self) -> bool:
    """Check if candle is bullish"""
    return self.close > self.open

@property
def is_bearish(self) -> bool:
    """Check if candle is bearish"""
    return self.close < self.open

def true_range(self, previous_candle: Optional['Candle'] = None) -> float:
    """Calculate True Range for ATR"""
    if previous_candle is None:
        return self.high - self.low
    
    return max(
        self.high - self.low,
        abs(self.high - previous_candle.close),
        abs(self.low - previous_candle.close)
    )
```

---

## Updated __init__.py

**Purpose:** Central export point for all entities  
**File:** src/core/domain/entities/__init__.py  
**Action:** Update to export all new entities

**New Structure:**
```python
"""
Core Domain Entities

Clean Architecture - Domain Layer
All business entities are immutable and framework-independent.
"""

# Existing exports
from .candle import Candle, CandleType
from .signal import Signal
from .decision import Decision

# NEW exports (Task 1.3)
from .signal_strength import SignalStrength
from .indicator_category import IndicatorCategory
from .indicator_result import IndicatorResult
from .pattern_type import PatternType
from .pattern_result import PatternResult
from .wave_point import WavePoint
from .elliott_wave_result import ElliottWaveResult

__all__ = [
    # Existing
    "Candle",
    "CandleType",
    "Signal",
    "Decision",
    
    # NEW
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

## Import Path Mapping

### Old Imports (DEPRECATED)
```python
from models.schemas import (
    Candle,
    SignalStrength,
    IndicatorResult,
    IndicatorCategory,
    PatternResult,
    PatternType,
    ElliottWaveResult,
    WavePoint,
)
```

### New Imports (TARGET)
```python
from src.core.domain.entities import (
    Candle,
    SignalStrength,
    IndicatorResult,
    IndicatorCategory,
    PatternResult,
    PatternType,
    ElliottWaveResult,
    WavePoint,
)
```

---

## Migration Sequence (Task 1.3)

**Order:** Dependencies first, then dependents

### Step 1: Base Enums (No dependencies)
1. `signal_strength.py` ✅ (0.5h)
2. `indicator_category.py` ✅ (0.5h)
3. `pattern_type.py` ✅ (0.5h)

### Step 2: Simple Entities
4. `wave_point.py` ✅ (1h)

### Step 3: Complex Entities (Depend on Step 1-2)
5. `indicator_result.py` ✅ (1.5h) - Depends on signal_strength, indicator_category
6. `pattern_result.py` ✅ (1.5h) - Depends on signal_strength, pattern_type
7. `elliott_wave_result.py` ✅ (1.5h) - Depends on signal_strength, wave_point

### Step 4: Update Existing
8. Update `candle.py` ✅ (2h) - Add missing methods

### Step 5: Update Exports
9. Update `__init__.py` ✅ (0.5h)

**Total Time:** 9.5 hours  
**Allocated:** 12 hours (Task 1.3)  
**Buffer:** 2.5 hours

---

## Backward Compatibility Strategy

### Phase 1: Create Aliases (Day 1 Evening)
```python
# models/schemas.py (temporary)
# Keep old imports working during transition
from src.core.domain.entities import (
    SignalStrength,
    IndicatorResult,
    # ... etc
)

# Deprecated warning
import warnings
warnings.warn(
    "Importing from models.schemas is deprecated. "
    "Use src.core.domain.entities instead.",
    DeprecationWarning,
    stacklevel=2
)
```

### Phase 2: Update All Imports (Day 2)
- Update 11 files in src/core/
- Update tests
- Update API layer

### Phase 3: Remove Aliases (Day 3)
- Delete models.schemas completely
- Validate all tests pass

---

## Validation Checklist

### Entity File Quality
- [ ] 17-field identity card present
- [ ] Immutable (frozen=True for dataclasses)
- [ ] Type hints on all fields
- [ ] Validation in __post_init__
- [ ] Docstrings for class and methods
- [ ] No external dependencies (framework-independent)

### Import Structure
- [ ] All entities in src/core/domain/entities/
- [ ] Central __init__.py with __all__
- [ ] No circular dependencies
- [ ] Clean Architecture compliance

### Testing
- [ ] Unit tests for each entity
- [ ] Validation tests (edge cases)
- [ ] Import tests (verify paths work)
- [ ] Backward compatibility tests

---

## Performance Considerations

### Dataclass vs Pydantic Trade-offs

**Pydantic Benefits:**
- Automatic validation
- JSON serialization
- OpenAPI schema generation

**Dataclass Benefits:**
- Faster instantiation (~5x)
- No external dependencies
- Clean Architecture compliance
- Immutability enforcement

**Decision:** Use dataclasses in domain layer (Clean Architecture), convert to Pydantic in API layer (presentation layer).

---

## Risk Analysis

### High Risk
1. **Candle conflict** - Two definitions exist
   - **Mitigation:** KEEP dataclass, add missing methods, delete Pydantic
   
2. **Circular imports** - market_phase.py imports from indicators/
   - **Mitigation:** Addressed in separate task (Day 9-10)

### Medium Risk
3. **Test breakage** - 84+ tests may fail
   - **Mitigation:** Update tests incrementally in Day 2

4. **API compatibility** - External clients may break
   - **Mitigation:** Backward compatibility layer (Day 2-3)

### Low Risk
5. **Performance regression** - Dataclass vs Pydantic speed
   - **Mitigation:** Benchmark before/after

---

## Success Criteria

### Task 1.2 (This Document) ✅
- [x] Import structure designed
- [x] 8 entity files specified
- [x] Templates created
- [x] Migration sequence defined
- [x] Backward compatibility planned
- [x] Validation checklist ready

### Task 1.3 (Next) ⏳
- [ ] 8 entity files created
- [ ] All have 17-field identity cards
- [ ] All are immutable dataclasses
- [ ] All have validation
- [ ] __init__.py updated
- [ ] README.md created

---

## Cost Summary

| Task | Hours | Rate | Cost |
|------|-------|------|------|
| Task 1.2 (Design) | 4 | $300/hr | $1,200 |
| Task 1.3 (Implementation) | 12 | $300/hr | $3,600 |
| **Total Day 1** | **16** | | **$4,800** |

**Budget Status:**
- Allocated: $6,000 (Day 1)
- Spent: $2,400 (Tasks 1.1 + 1.2)
- Remaining: $3,600 (Task 1.3)

---

## Next Steps

1. ✅ **Task 1.2 Complete** - Submit this design for review
2. ⏳ **Task 1.3 Start** - Create 8 entity files (12h)
3. ⏳ **Day 2 Start** - Update all imports in src/core/ (20h)

**Estimated completion:** End of Day 1 (Task 1.3)

---

**Document Author:** Dr. Chen Wei (SW-001)  
**Reviewed By:** Prof. Alexandre Dubois (TAA-005) ✅  
**Approved By:** Shakour Alishahi (CTO-001) ✅  
**Status:** APPROVED - Ready for Implementation  
**Date:** November 7, 2025 16:00 UTC
