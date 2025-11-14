#!/usr/bin/env python3
"""
Complete System Test Suite

این اسکریپت تمام اجزای سیستم را تست می‌کند:
1. DynamicToolRecommender
2. DatabaseManager
3. ToolRecommendationService
4. API endpoints (mock)
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🧪 Gravity Tech Analysis - Complete System Test")
print("=" * 70)
print()


# ==================== Test 1: DynamicToolRecommender ====================
def test_tool_recommender():
    print("📋 Test 1: DynamicToolRecommender")
    print("-" * 70)
    
    try:
        from ml.ml_tool_recommender import DynamicToolRecommender, MarketContext
        
        # Create recommender
        recommender = DynamicToolRecommender(model_type="lightgbm")
        print("   ✅ DynamicToolRecommender initialized")
        
        # Create market context
        context = MarketContext(
            symbol="BTCUSDT",
            timeframe="1d",
            market_regime="trending_bullish",
            volatility_level=45.0,
            trend_strength=75.0,
            volume_profile="high",
            trading_style="swing"
        )
        print("   ✅ MarketContext created")
        
        # Get recommendations
        recommendations = recommender.recommend_tools(context, top_n=10)
        print(f"   ✅ Got {len(recommendations)} recommendations")
        
        # Display top 3
        print(f"\n   🎯 Top 3 Recommended Tools:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"      {i}. {rec.tool_name:20s} - {rec.priority:12s} (confidence: {rec.confidence:.1%})")
        
        # Test contextual recommendations
        print(f"\n   🔄 Testing contextual recommendations...")
        import pandas as pd
        import numpy as np
        
        # Create sample data
        dates = pd.date_range(end=datetime.utcnow(), periods=100, freq='D')
        candles = pd.DataFrame({
            'timestamp': dates,
            'open': 50000 + np.random.randn(100).cumsum() * 100,
            'high': 50200 + np.random.randn(100).cumsum() * 100,
            'low': 49800 + np.random.randn(100).cumsum() * 100,
            'close': 50000 + np.random.randn(100).cumsum() * 100,
            'volume': np.random.randint(1000000, 5000000, 100)
        })
        
        result = recommender.get_contextual_recommendations(
            symbol="BTCUSDT",
            candles=candles,
            analysis_goal="entry_signal"
        )
        
        print(f"   ✅ Contextual analysis complete")
        print(f"      Market regime: {result['market_context']['regime']}")
        print(f"      Must use: {len(result['recommendations']['must_use'])} tools")
        print(f"      Recommended: {len(result['recommendations']['recommended'])} tools")
        
        print("\n   ✅✅✅ DynamicToolRecommender: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n   ❌ FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# ==================== Test 2: DatabaseManager ====================
def test_database_manager():
    print("📋 Test 2: DatabaseManager")
    print("-" * 70)
    
    try:
        from database.database_manager import DatabaseManager
        
        # Initialize database
        db = DatabaseManager(auto_setup=True)
        print(f"   ✅ Database initialized: {db.db_type.value}")
        
        # Test write
        record_id = db.record_tool_performance(
            tool_name="MACD",
            tool_category="trend_indicators",
            symbol="BTCUSDT",
            timeframe="1d",
            market_regime="trending_bullish",
            prediction_type="bullish",
            confidence_score=0.85,
            volatility_level=45.5,
            trend_strength=72.3,
            volume_profile="high",
            metadata={"test": True}
        )
        print(f"   ✅ Record written: ID={record_id}")
        
        # Test read
        stats = db.get_tool_accuracy(
            tool_name="MACD",
            market_regime="trending_bullish",
            days=30
        )
        print(f"   ✅ Stats retrieved:")
        print(f"      Total predictions: {stats['total_predictions']}")
        print(f"      Accuracy: {stats.get('accuracy', 0):.1%}")
        
        # Test multiple writes
        for i in range(5):
            db.record_tool_performance(
                tool_name="RSI",
                tool_category="momentum_indicators",
                symbol="ETHUSDT",
                timeframe="1h",
                market_regime="ranging",
                prediction_type="neutral",
                confidence_score=0.70 + i * 0.05
            )
        print(f"   ✅ Multiple records written (5 records)")
        
        # Close
        db.close()
        print(f"   ✅ Database closed cleanly")
        
        print("\n   ✅✅✅ DatabaseManager: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n   ❌ FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# ==================== Test 3: ToolRecommendationService ====================
async def test_tool_recommendation_service():
    print("📋 Test 3: ToolRecommendationService")
    print("-" * 70)
    
    try:
        from src.gravity_tech.services.tool_recommendation_service import ToolRecommendationService
        
        # Initialize service
        service = ToolRecommendationService()
        print(f"   ✅ ToolRecommendationService initialized")
        
        # Test get recommendations
        result = await service.get_tool_recommendations(
            symbol="BTCUSDT",
            timeframe="1d",
            analysis_goal="entry_signal",
            trading_style="swing",
            limit_candles=200,
            top_n=10
        )
        
        print(f"   ✅ Recommendations retrieved:")
        print(f"      Symbol: {result['symbol']}")
        print(f"      Market regime: {result['market_context']['regime']}")
        print(f"      Must use: {len(result['recommendations']['must_use'])} tools")
        print(f"      Recommended: {len(result['recommendations']['recommended'])} tools")
        
        # Test custom analysis
        custom_result = await service.analyze_with_custom_tools(
            symbol="ETHUSDT",
            timeframe="1h",
            selected_tools=["MACD", "RSI", "ADX"],
            include_ml_scoring=True,
            include_patterns=True
        )
        
        print(f"   ✅ Custom analysis complete:")
        print(f"      Tools analyzed: {len(custom_result['selected_tools'])}")
        print(f"      Overall signal: {custom_result['summary']['overall_signal']}")
        print(f"      Consensus: {custom_result['summary']['consensus']}")
        
        print("\n   ✅✅✅ ToolRecommendationService: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n   ❌ FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# ==================== Test 4: Integration Test ====================
async def test_integration():
    print("📋 Test 4: Integration Test (Full Pipeline)")
    print("-" * 70)
    
    try:
        from ml.ml_tool_recommender import DynamicToolRecommender, MarketContext
        from database.database_manager import DatabaseManager
        from src.gravity_tech.services.tool_recommendation_service import ToolRecommendationService
        
        # Step 1: Get recommendations
        service = ToolRecommendationService()
        result = await service.get_tool_recommendations(
            symbol="BTCUSDT",
            timeframe="1d",
            analysis_goal="entry_signal",
            top_n=5
        )
        
        print(f"   ✅ Step 1: Got {len(result['recommendations']['must_use'])} recommendations")
        
        # Step 2: Record performance for each tool
        db = DatabaseManager()
        
        for tool_rec in result['recommendations']['must_use']:
            record_id = db.record_tool_performance(
                tool_name=tool_rec['name'],
                tool_category=tool_rec['category'],
                symbol=result['symbol'],
                timeframe="1d",
                market_regime=result['market_context']['regime'],
                prediction_type="bullish",
                confidence_score=tool_rec['confidence']
            )
            print(f"      ✓ Recorded {tool_rec['name']}: ID={record_id}")
        
        print(f"   ✅ Step 2: Recorded {len(result['recommendations']['must_use'])} tool performances")
        
        # Step 3: Retrieve statistics
        for tool_rec in result['recommendations']['must_use']:
            stats = db.get_tool_accuracy(tool_rec['name'], days=1)
            print(f"      ✓ {tool_rec['name']:15s}: {stats['total_predictions']} predictions")
        
        print(f"   ✅ Step 3: Retrieved statistics for all tools")
        
        db.close()
        
        print("\n   ✅✅✅ Integration Test: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n   ❌ FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# ==================== Main ====================
async def main():
    print("Starting comprehensive test suite...\n")
    
    results = {
        "DynamicToolRecommender": False,
        "DatabaseManager": False,
        "ToolRecommendationService": False,
        "Integration": False
    }
    
    # Run tests
    results["DynamicToolRecommender"] = test_tool_recommender()
    results["DatabaseManager"] = test_database_manager()
    results["ToolRecommendationService"] = await test_tool_recommendation_service()
    results["Integration"] = await test_integration()
    
    # Summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print()
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"   {test_name:30s}: {status}")
    
    print()
    print(f"   Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print()
    
    if passed == total:
        print("=" * 70)
        print("🎉 ALL TESTS PASSED! System is ready for production.")
        print("=" * 70)
        return 0
    else:
        print("=" * 70)
        print(f"⚠️  {total - passed} test(s) failed. Please review errors above.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
