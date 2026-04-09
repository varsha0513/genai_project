"""
Comprehensive test for intelligent visualization system
Tests with different datasets and prompts to show AI suggestions
"""
import requests
import io
import json

BASE_URL = "http://localhost:5001"

def test_sales_data():
    """Test with sales dataset"""
    print("\n" + "="*70)
    print("TEST 1: SALES DATA - Multiple visualization types")
    print("="*70)
    
    sales_csv = """Product,Month,Sales,Units,Region
Laptop,Jan,15000,10,North
Laptop,Feb,18000,12,North
Laptop,Mar,22000,15,North
Phone,Jan,8000,20,South
Phone,Feb,9500,25,South
Phone,Mar,11000,30,South
Tablet,Jan,5000,15,East
Tablet,Feb,6500,18,East
Tablet,Mar,8000,22,East"""
    
    # Upload
    print("\n[1] Uploading sales dataset...")
    files = {'file': ('sales.csv', io.BytesIO(sales_csv.encode()))}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"✅ Loaded {r.json()['rows']} records")
    
    # Test different visualization prompts
    test_queries = [
        "show the sales trend over time",
        "show correlation between units and sales",
        "compare sales by product",
        "show distribution of units",
        "sales by region pie chart"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] Query: '{query}'")
        r = requests.post(f"{BASE_URL}/query", json={"query": query})
        if r.status_code == 200:
            result = r.json()
            chart_type = result.get('chart_type', 'unknown')
            recommendation = result.get('recommendation', '')
            print(f"    📊 Chart Type: {chart_type.upper()}")
            print(f"    💡 Recommendation: {recommendation}")
        else:
            print(f"    ❌ Error: {r.json()}")


def test_student_data():
    """Test with student dataset"""
    print("\n" + "="*70)
    print("TEST 2: STUDENT DATA - Educational dataset")
    print("="*70)
    
    student_csv = """StudentID,Name,Math,Science,English,Grade
1,Alice,95,92,89,A
2,Bob,78,81,76,C
3,Charlie,88,85,90,B
4,Diana,92,94,91,A
5,Eve,65,62,68,D
6,Frank,82,80,85,B
7,Grace,98,96,94,A
8,Henry,71,74,70,C"""
    
    print("\n[1] Uploading student dataset...")
    files = {'file': ('students.csv', io.BytesIO(student_csv.encode()))}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"✅ Loaded {r.json()['rows']} records")
    
    # Test educational prompts
    test_queries = [
        "show the distribution of math scores",
        "compare math and science performance",
        "show grades distribution",
        "analyze performance across all subjects"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] Query: '{query}'")
        r = requests.post(f"{BASE_URL}/query", json={"query": query})
        if r.status_code == 200:
            result = r.json()
            chart_type = result.get('chart_type', 'unknown')
            recommendation = result.get('recommendation', '')
            print(f"    📊 Chart Type: {chart_type.upper()}")
            print(f"    💡 Recommendation: {recommendation}")
        else:
            print(f"    ❌ Error: {r.json()}")


def test_weather_data():
    """Test with weather dataset"""
    print("\n" + "="*70)
    print("TEST 3: WEATHER DATA - Time series dataset")
    print("="*70)
    
    weather_csv = """Date,Temperature,Humidity,Rainfall,WindSpeed,Condition
2024-01-01,5,78,2.5,15,Rainy
2024-01-02,7,72,0,12,Cloudy
2024-01-03,9,65,0,8,Sunny
2024-01-04,8,70,1.5,10,Rainy
2024-01-05,12,60,0,6,Sunny
2024-01-06,14,55,0,5,Sunny
2024-01-07,11,68,3,14,Rainy"""
    
    print("\n[1] Uploading weather dataset...")
    files = {'file': ('weather.csv', io.BytesIO(weather_csv.encode()))}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"✅ Loaded {r.json()['rows']} records")
    
    # Test weather-related prompts
    test_queries = [
        "show temperature trend over time",
        "analyze rainfall levels",
        "show relationship between temperature and humidity",
        "compare all weather metrics"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] Query: '{query}'")
        r = requests.post(f"{BASE_URL}/query", json={"query": query})
        if r.status_code == 200:
            result = r.json()
            chart_type = result.get('chart_type', 'unknown')
            recommendation = result.get('recommendation', '')
            print(f"    📊 Chart Type: {chart_type.upper()}")
            print(f"    💡 Recommendation: {recommendation}")
        else:
            print(f"    ❌ Error: {r.json()}")


def test_natural_language():
    """Test with natural language variations"""
    print("\n" + "="*70)
    print("TEST 4: NATURAL LANGUAGE - Various prompt styles")
    print("="*70)
    
    data_csv = """Category,Value,Count
A,100,5
B,150,8
C,200,12
D,120,7
E,180,10"""
    
    print("\n[1] Uploading test dataset...")
    files = {'file': ('test.csv', io.BytesIO(data_csv.encode()))}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"✅ Loaded {r.json()['rows']} records")
    
    # Test various natural language prompts
    test_queries = [
        "visualize the data",  # Generic
        "create a chart showing breakdown by category",  # Specific intent
        "i want to see how values are distributed",  # Informal
        "show me everything in a single visualization",  # Broad request
        "what's the best way to visualize this?"  # Question
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] Query: '{query}'")
        r = requests.post(f"{BASE_URL}/query", json={"query": query})
        if r.status_code == 200:
            result = r.json()
            chart_type = result.get('chart_type', 'unknown')
            recommendation = result.get('recommendation', '')
            print(f"    📊 Chart Type: {chart_type.upper()}")
            print(f"    💡 Recommendation: {recommendation}")
        else:
            print(f"    ❌ Error: {r.json()}")


if __name__ == "__main__":
    try:
        test_sales_data()
        test_student_data()
        test_weather_data()
        test_natural_language()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED")
        print("="*70)
        print("\n🎯 Key Features Demonstrated:")
        print("   • Intelligent chart type suggestion")
        print("   • Works with ANY dataset structure")
        print("   • Understands natural language prompts")
        print("   • Auto-selects best visualization")
        print("   • Provides reasoning for choices")
        
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
