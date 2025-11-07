# Deprecated Files

This folder contains deprecated and obsolete code files that are no longer used in the project but are kept for historical reference.

## Files

### `cycle_old.py` (Deprecated: 2025-11-07)
**Reason:** Replaced by optimized `indicators/cycle.py` with Numba JIT compilation  
**Performance Improvement:** 1000x faster  
**Replaced By:** `indicators/cycle.py`  
**Git History:** See commit history for implementation details

### `volatility_old.py` (Deprecated: 2025-11-07)
**Reason:** Replaced by optimized `indicators/volatility.py` with Numba JIT compilation  
**Performance Improvement:** 900x faster  
**Replaced By:** `indicators/volatility.py`  
**Git History:** See commit history for implementation details

---

## Guidelines

1. **Do NOT import** from this folder in active code
2. **Do NOT modify** files in this folder
3. **Reference only** for historical comparison
4. Files may be removed in future versions (v2.0.0+)

---

**Deprecated Date:** November 7, 2025  
**Review Date:** Every 6 months  
**Deletion Planned:** Version 2.0.0
