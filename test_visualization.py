"""
Test the new compound query and PNG visualization features
"""
import requests
import json
import pandas as pd
import io

API_BASE = "http://localhost:5001"

# Test data - CSV with missing values and duplicates
test_data = """Name,Age,Salary,Department
Alice,25,50000,Sales
Bob,,45000,IT
Charlie,30,60000,Sales
Alice,25,50000,Sales
David,28,,Marketing
Eve,35,75000,IT
David,28,,Marketing
Frank,,55000,Sales"""

print("=" * 70)
print("COMPOUND QUERY & PNG VISUALIZATION TEST")
print("=" * 70)

# Step 1: Upload test data
print("\n[1] Uploading dataset...")
files = {'file': ('test_data.csv', io.StringIO(test_data))}
upload_response = requests.post(f"{API_BASE}/upload", files=files)
print(f"✅ Upload Status: {upload_response.status_code}")
print(f"   Rows: {upload_response.json()['rows']}")

# Step 2: Test compound query with cleaning + statistics
print("\n[2] Testing COMPOUND QUERY...")
query_text = "remove duplicate and missing value and show total value"
print(f"   Query: '{query_text}'")

response = requests.post(
    f"{API_BASE}/query",
    json={"query": query_text, "session_id": None}
)

print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Response:")
print(json.dumps(data, indent=2)[:500])

# Step 3: Test visualization query
print("\n[3] Testing VISUALIZATION QUERY...")
viz_query = "show histogram salary"
response = requests.post(
    f"{API_BASE}/query",
    json={"query": viz_query, "session_id": None}
)

print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Chart Type: {data.get('chart_type')}")
print(f"   Chart Path: {data.get('chart_path')}")
if data.get('chart_path'):
    print(f"   ✅ PNG Visualization created: {data['chart_path'].split(chr(92))[-1]}")

# Step 4: Test downloading the chart
if data.get('chart_path'):
    chart_filename = data['chart_path'].split('\\')[-1]
    chart_url = f"{API_BASE}/chart/{chart_filename}"
    chart_response = requests.get(chart_url)
    print(f"\n[4] Chart Download Test")
    print(f"   URL: {chart_url}")
    print(f"   Status: {chart_response.status_code}")
    print(f"   Content-Type: {chart_response.headers.get('content-type')}")
    print(f"   Size: {len(chart_response.content)} bytes")
    if chart_response.status_code == 200:
        print(f"   ✅ Chart image successfully served!")

print("\n" + "=" * 70)
print("TEST COMPLETE!")
print("=" * 70)
