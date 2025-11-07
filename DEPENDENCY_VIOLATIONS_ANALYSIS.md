# Dependency Violations Analysis Report
**تحلیل نقض وابستگی‌ها در src/core/**

**تاریخ تحلیل**: 7 نوامبر 2025  
**تحلیلگر**: Dr. Chen Wei (SW-001)  
**مدت تحلیل**: 4 ساعت  

---

## 📊 Executive Summary

تحلیل کامل imports در **src/core/** انجام شد:
- **11 فایل** از `models.schemas` import می‌کنند ❌
- **1 فایل** از `indicators/` قدیمی import می‌کند ❌
- **مجموع نقض**: 12 مورد بحرانی

---

## 🔍 Detailed Analysis

### 1. Imports from models.schemas (11 files)

#### **src/core/indicators/** (6 files)

**1.1 trend.py** (خط 46)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 422 خط کد
- **Impact**: HIGH

**1.2 momentum.py** (خط 43)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 422 خط کد  
- **Impact**: HIGH

**1.3 volatility.py** (خط 44)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 776 خط کد
- **Impact**: HIGH

**1.4 cycle.py** (خط 47)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 513 خط کد
- **Impact**: HIGH

**1.5 support_resistance.py** (خط 43)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 300 خط کد
- **Impact**: MEDIUM

**1.6 volume.py** (خط 43)
```python
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory
```
- **Models needed**: 4 مدل
- **Usage**: 372 خط کد
- **Impact**: MEDIUM

---

#### **src/core/patterns/** (4 files)

**2.1 candlestick.py** (خط 41)
```python
from models.schemas import Candle, PatternResult, SignalStrength, PatternType
```
- **Models needed**: 4 مدل
- **Usage**: 259 خط کد
- **Impact**: MEDIUM

**2.2 classical.py** (خط 51)
```python
from models.schemas import Candle, PatternResult, SignalStrength, PatternType
```
- **Models needed**: 4 مدل
- **Usage**: 669 خط کد
- **Impact**: HIGH

**2.3 elliott_wave.py** (خط 37)
```python
from models.schemas import Candle, ElliottWaveResult, WavePoint, SignalStrength
```
- **Models needed**: 4 مدل
- **Usage**: 335 خط کد
- **Impact**: MEDIUM

**2.4 divergence.py** (خط 39)
```python
from models.schemas import Candle
```
- **Models needed**: 1 مدل
- **Usage**: 454 خط کد
- **Impact**: LOW

---

#### **src/core/analysis/** (1 file)

**3.1 market_phase.py** (خط 48)
```python
from models.schemas import Candle, SignalStrength
```
- **Models needed**: 2 مدل
- **Usage**: 489 خط کد
- **Impact**: MEDIUM

**PLUS خط 49-51**:
```python
from indicators.trend import TrendIndicators
from indicators.momentum import MomentumIndicators
from indicators.volume import VolumeIndicators
```
- **Legacy imports**: 3 ماژول ❌
- **Impact**: CRITICAL (circular import risk)

---

## 📋 Models Usage Summary

**Models imported from models.schemas**:

| Model | Usage Count | Files |
|-------|-------------|-------|
| Candle | 11 | All files |
| SignalStrength | 9 | Most files |
| IndicatorResult | 6 | Indicator files |
| IndicatorCategory | 6 | Indicator files |
| PatternResult | 2 | Pattern files |
| PatternType | 2 | Pattern files |
| ElliottWaveResult | 1 | elliott_wave.py |
| WavePoint | 1 | elliott_wave.py |

---

## 🎯 Migration Plan

### Phase 1: Create Entity Files (12 hours)

**Models to migrate to src/core/domain/entities/**:

1. ✅ **candle.py** - Already exists (needs update)
2. ✅ **signal_strength.py** - Already exists (verify)
3. 🆕 **indicator_result.py** - NEW
4. 🆕 **indicator_category.py** - NEW (Enum)
5. 🆕 **pattern_result.py** - NEW
6. 🆕 **pattern_type.py** - NEW (Enum)
7. 🆕 **elliott_wave_result.py** - NEW
8. 🆕 **wave_point.py** - NEW

---

### Phase 2: Update Imports (8 hours)

**Import mapping**:

```python
# OLD (WRONG):
from models.schemas import Candle, IndicatorResult, SignalStrength, IndicatorCategory

# NEW (CORRECT):
from src.core.domain.entities.candle import Candle
from src.core.domain.entities.indicator_result import IndicatorResult
from src.core.domain.entities.signal_strength import SignalStrength
from src.core.domain.entities.indicator_category import IndicatorCategory
```

**Files to update**: 11 files

---

### Phase 3: Fix Legacy Imports (2 hours)

**market_phase.py specific**:

```python
# OLD (WRONG):
from indicators.trend import TrendIndicators
from indicators.momentum import MomentumIndicators
from indicators.volume import VolumeIndicators

# NEW (CORRECT):
from src.core.indicators.trend import TrendIndicators
from src.core.indicators.momentum import MomentumIndicators
from src.core.indicators.volume import VolumeIndicators
```

---

## 💰 Cost Breakdown

### Task 1.1 (این گزارش): 4 ساعت
- تحلیل imports: 2 ساعت
- مستندسازی: 1 ساعت
- برنامه‌ریزی: 1 ساعت
- **هزینه**: $1,200

### Task 1.2 (بعدی): 4 ساعت
- طراحی ساختار: 2 ساعت
- نقشه‌کشی migration: 2 ساعت
- **هزینه**: $1,200

### Task 1.3 (امشب): 12 ساعت
- ایجاد 8 entity file: 8 ساعت
- تست و validation: 4 ساعت
- **هزینه**: $3,600

**جمع Day 1**: $6,000 ✅

---

## 🚨 Critical Findings

### 1. **Candle Entity Conflict**
- `models/schemas.py` has Pydantic Candle
- `src/core/domain/entities/candle.py` has dataclass Candle
- **Action**: Merge در Day 8

### 2. **Circular Import Risk**
- `market_phase.py` imports from `indicators/`
- **Action**: Fix با DI در Day 9-10

### 3. **High Coupling**
- همه indicators به 4 مدل یکسان وابسته‌اند
- **Benefit**: یک‌بار migrate → همه fix می‌شوند

---

## ✅ Next Steps (Task 1.2)

1. طراحی ساختار `src/core/domain/entities/`
2. ایجاد template برای entity files
3. تعریف `__init__.py` برای exports
4. طراحی backward compatibility layer

---

## 📊 Progress Tracking

**Day 1 Progress**:
- [x] Task 1.1: تحلیل imports (4h) ✅ DONE
- [ ] Task 1.2: طراحی ساختار (4h) - NEXT
- [ ] Task 1.3: ایجاد entities (12h)

**Time**: 4/20 ساعت (20%)  
**Budget**: $1,200/$6,000 (20%)  

---

**تحلیل شده توسط**: Dr. Chen Wei (SW-001)  
**بررسی شده توسط**: Prof. Alexandre Dubois (FIN-005)  
**تایید شده**: ✅ Ready for Task 1.2  
**تاریخ**: 7 نوامبر 2025
