# Fundamental Scoring & Ranking System (رتبه‌بندی بنیادی)

**Document Version:** 1.0  
**Created:** November 14, 2025  
**Author:** Dr. James Richardson & Shakour Alishahi  
**Domain:** Fundamental Analysis Integration

---

## 🎯 Overview

میکروسرویس باید **امتیازدهی و رتبه‌بندی بنیادی نمادها** را انجام دهد و با تحلیل تکنیکال ترکیب کند.

---

## 📊 Fundamental Scoring Dimensions

### **1. Financial Health (سلامت مالی) - 25%**

**شاخص‌های کلیدی:**
```python
financial_health_score = weighted_average([
    # نسبت‌های نقدینگی
    ("current_ratio", 15),          # نسبت جاری > 2
    ("quick_ratio", 10),             # نسبت آنی > 1
    
    # نسبت‌های اهرمی
    ("debt_to_equity", 15),         # بدهی به حقوق صاحبان < 1
    ("interest_coverage", 10),      # پوشش بهره > 5
    
    # سودآوری
    ("profit_margin", 20),          # حاشیه سود خالص > 10%
    ("roe", 15),                     # بازده حقوق صاحبان > 15%
    ("roa", 15),                     # بازده دارایی‌ها > 8%
])
```

**منابع داده:**
- صورت‌های مالی سه‌ماهه و سالانه
- گزارش‌های ناظر
- سامانه کدال (ایران)
- Yahoo Finance API (بین‌المللی)
- Alpha Vantage API

---

### **2. Growth Metrics (رشد) - 20%**

**شاخص‌های کلیدی:**
```python
growth_score = weighted_average([
    ("revenue_growth_yoy", 25),      # رشد درآمد سال به سال > 15%
    ("earnings_growth_yoy", 25),     # رشد سود سال به سال > 20%
    ("revenue_growth_qoq", 15),      # رشد درآمد فصل به فصل > 5%
    ("earnings_growth_qoq", 15),     # رشد سود فصل به فصل > 10%
    ("asset_growth", 10),            # رشد دارایی‌ها
    ("market_share_growth", 10),     # رشد سهم بازار
])
```

**Trend Analysis:**
- رشد 3 سال اخیر
- رشد 5 سال اخیر
- CAGR (Compound Annual Growth Rate)
- رشد پیش‌بینی شده (forward estimates)

---

### **3. Valuation (ارزش‌گذاری) - 20%**

**شاخص‌های کلیدی:**
```python
valuation_score = weighted_average([
    ("pe_ratio", 25),                # P/E نسبت به میانگین صنعت
    ("pb_ratio", 20),                # P/B < 3
    ("ps_ratio", 15),                # Price-to-Sales
    ("peg_ratio", 20),               # PEG < 1 (ارزش‌گذاری مناسب با رشد)
    ("ev_to_ebitda", 20),           # EV/EBITDA نسبت به صنعت
])
```

**Fair Value Calculation:**
```python
# DCF Model (Discounted Cash Flow)
fair_value_dcf = calculate_dcf(
    free_cash_flows_5y,
    discount_rate=0.12,
    terminal_growth_rate=0.03
)

# Comparable Companies (مقایسه با رقبا)
fair_value_comps = calculate_comparable_valuation(
    industry_pe_median,
    company_earnings
)

# Combined Fair Value
fair_value = (fair_value_dcf * 0.6) + (fair_value_comps * 0.4)

# Undervalued/Overvalued
valuation_gap = ((fair_value - current_price) / current_price) * 100
```

---

### **4. Industry Position (جایگاه صنعت) - 15%**

**شاخص‌های کلیدی:**
```python
industry_position_score = weighted_average([
    ("market_share", 30),            # سهم بازار در صنعت
    ("competitive_advantage", 25),   # مزیت رقابتی (moat)
    ("brand_strength", 15),          # قدرت برند
    ("innovation_score", 15),        # نوآوری و R&D
    ("management_quality", 15),      # کیفیت مدیریت
])
```

**Industry Analysis:**
- رتبه در صنعت (1st, 2nd, 3rd...)
- تعداد رقبا
- barrier to entry
- Porter's Five Forces
- SWOT Analysis

---

### **5. Momentum & Sentiment (حس بازار) - 10%**

**شاخص‌های کلیدی:**
```python
sentiment_score = weighted_average([
    ("analyst_recommendations", 30),  # توصیه‌های تحلیلگران
    ("insider_trading", 25),          # معاملات مدیران
    ("institutional_ownership", 20),  # مالکیت نهادی
    ("news_sentiment", 15),           # احساسات اخبار (NLP)
    ("social_media_buzz", 10),        # buzz در شبکه‌های اجتماعی
])
```

**Analyst Ratings:**
```python
analyst_score = (
    (strong_buy * 5) +
    (buy * 4) +
    (hold * 3) +
    (sell * 2) +
    (strong_sell * 1)
) / total_analysts
```

---

### **6. Dividends & Shareholder Returns (سود سهام) - 10%**

**شاخص‌های کلیدی:**
```python
dividend_score = weighted_average([
    ("dividend_yield", 35),          # بازده سود سهام > 3%
    ("dividend_growth", 25),         # رشد سود سهام
    ("payout_ratio", 20),            # نسبت پرداخت 30-60%
    ("dividend_consistency", 20),    # تداوم پرداخت سود
])
```

---

## 🎯 Overall Fundamental Score

```python
fundamental_score = (
    financial_health_score * 0.25 +
    growth_score * 0.20 +
    valuation_score * 0.20 +
    industry_position_score * 0.15 +
    sentiment_score * 0.10 +
    dividend_score * 0.10
)

# Scale: 0-100
# 80-100: Excellent (عالی)
# 60-79:  Good (خوب)
# 40-59:  Fair (متوسط)
# 20-39:  Poor (ضعیف)
# 0-19:   Very Poor (بسیار ضعیف)
```

---

## 🏆 Ranking System

### **Multi-Factor Ranking**

```python
def rank_symbols(symbols_list, market="iran"):
    scores = []
    
    for symbol in symbols_list:
        fundamental = calculate_fundamental_score(symbol)
        technical = calculate_technical_score(symbol)
        
        # Combined Score (60% fundamental, 40% technical)
        combined_score = (fundamental * 0.6) + (technical * 0.4)
        
        scores.append({
            "symbol": symbol,
            "fundamental_score": fundamental,
            "technical_score": technical,
            "combined_score": combined_score,
            "rank": None  # محاسبه بعداً
        })
    
    # Sort by combined score
    ranked = sorted(scores, key=lambda x: x["combined_score"], reverse=True)
    
    # Assign ranks
    for i, item in enumerate(ranked):
        item["rank"] = i + 1
        item["percentile"] = ((len(ranked) - i) / len(ranked)) * 100
    
    return ranked
```

### **Sector/Industry Ranking**

```python
def rank_within_sector(symbol, sector):
    """رتبه‌بندی در داخل صنعت"""
    sector_symbols = get_sector_symbols(sector)
    sector_ranking = rank_symbols(sector_symbols)
    
    symbol_rank = next(
        (i for i, s in enumerate(sector_ranking) if s["symbol"] == symbol),
        None
    )
    
    return {
        "rank_in_sector": symbol_rank + 1,
        "total_in_sector": len(sector_symbols),
        "percentile_in_sector": ((len(sector_symbols) - symbol_rank) / len(sector_symbols)) * 100
    }
```

---

## 📊 Data Sources

### **Iranian Market (بورس ایران):**
```python
data_sources = {
    "financial_statements": "CODAL (کدال)",
    "realtime_data": "TSETMC API",
    "company_info": "فیپیران، رهاورد",
    "industry_data": "سازمان بورس",
}
```

### **International Markets:**
```python
data_sources = {
    "financial_data": "Alpha Vantage API",
    "stock_prices": "Yahoo Finance API",
    "fundamental_data": "Financial Modeling Prep API",
    "news_sentiment": "News API + NLP",
    "analyst_ratings": "Finnhub API",
}
```

---

## 🔧 Implementation

### **File Structure:**
```
src/gravity_tech/
├── fundamental/                    # NEW MODULE
│   ├── __init__.py
│   ├── scoring.py                 # اصلی
│   ├── financial_health.py
│   ├── growth_metrics.py
│   ├── valuation.py
│   ├── industry_analysis.py
│   ├── sentiment_analysis.py
│   ├── dividend_analysis.py
│   ├── ranking.py
│   └── data_connectors/
│       ├── codal_connector.py     # ایران
│       ├── tsetmc_connector.py    # ایران
│       ├── alpha_vantage.py       # بین‌المللی
│       └── yahoo_finance.py       # بین‌المللی
```

### **API Endpoints:**

#### **1. Fundamental Score**
```python
POST /api/v1/fundamental/score
{
    "symbol": "فولاد",
    "market": "iran"
}

Response:
{
    "symbol": "فولاد",
    "fundamental_score": 75.5,
    "rating": "GOOD",
    "dimensions": {
        "financial_health": 82.0,
        "growth": 68.5,
        "valuation": 70.0,
        "industry_position": 85.0,
        "sentiment": 65.0,
        "dividends": 72.0
    },
    "strengths": ["strong_balance_sheet", "market_leader", "consistent_dividends"],
    "weaknesses": ["high_pe_ratio", "slow_growth"],
    "fair_value": 5500,
    "current_price": 4800,
    "upside_potential": 14.6
}
```

#### **2. Symbol Ranking**
```python
POST /api/v1/fundamental/rank
{
    "symbols": ["فولاد", "فملی", "شپنا", ...],
    "market": "iran",
    "sort_by": "combined_score"  # or "fundamental_score", "technical_score"
}

Response:
{
    "rankings": [
        {
            "rank": 1,
            "symbol": "فولاد",
            "fundamental_score": 85.5,
            "technical_score": 72.0,
            "combined_score": 80.1,
            "percentile": 95.2,
            "recommendation": "STRONG_BUY"
        },
        ...
    ],
    "total_symbols": 50,
    "timestamp": "2025-11-14T12:00:00Z"
}
```

#### **3. Sector Analysis**
```python
POST /api/v1/fundamental/sector-analysis
{
    "sector": "فلزات_اساسی",
    "market": "iran"
}

Response:
{
    "sector": "فلزات_اساسی",
    "sector_score": 68.5,
    "top_performers": ["فولاد", "فملی", ...],
    "worst_performers": [...],
    "sector_metrics": {
        "avg_pe_ratio": 8.5,
        "avg_growth": 15.2,
        "avg_dividend_yield": 12.5
    }
}
```

---

## 🎯 Integration with Technical Analysis

### **Combined Scoring:**
```python
def generate_comprehensive_analysis(symbol):
    # تحلیل تکنیکال (موجود)
    technical = analyze_technical(symbol)
    
    # تحلیل بنیادی (جدید)
    fundamental = analyze_fundamental(symbol)
    
    # تحلیل سناریو (جدید)
    scenarios = analyze_scenarios(symbol)
    
    return {
        "symbol": symbol,
        "technical_analysis": technical,
        "fundamental_analysis": fundamental,
        "scenario_analysis": scenarios,
        "final_recommendation": calculate_final_recommendation(
            technical, fundamental, scenarios
        ),
        "risk_level": calculate_risk_level(),
        "investment_horizon": suggest_horizon(),  # short/medium/long-term
    }
```

---

## ✅ Success Criteria

1. **Data Coverage:** 
   - 500+ نماد بورس ایران
   - 5000+ سهام بین‌المللی
2. **Update Frequency:**
   - صورت‌های مالی: روزانه (بعد از انتشار)
   - قیمت‌ها: realtime
   - احساسات: هر 15 دقیقه
3. **Accuracy:** 
   - Correlation با بازدهی واقعی > 0.7
   - Backtesting Sharpe Ratio > 2.0
4. **Performance:**
   - محاسبه هر نماد < 50ms
   - رتبه‌بندی 500 نماد < 5 ثانیه

---

**Team Assignment:**
- **Dr. Richardson:** طراحی مدل‌های مالی و ارزش‌گذاری
- **Dr. Patel:** ML برای پیش‌بینی و رتبه‌بندی
- **Maria Gonzalez:** تحلیل order flow و نهادی
- **Dmitry Volkov:** API integration و data connectors
- **Shakour:** تأیید نهایی و بررسی از منظر trading

---

**Status:** 🔴 در حال طراحی  
**Priority:** 🔥 CRITICAL  
**ETA:** 7-10 روز کاری
