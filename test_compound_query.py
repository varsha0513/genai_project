"""
Test script to verify compound query processing
Tests: "remove missing value and give the passenger total"
"""
import requests
import json
import pandas as pd
import io

API_BASE = "http://localhost:5001"

# Test data - Create a small CSV with some missing values
test_data = """Name,Age,Passengers,Fare
Alice,25,1,100.5
Bob,,2,50.0
Charlie,30,1,75.25
David,28,3,
Eve,35,2,120.0
Frank,,1,65.50"""

print("=" * 60)
print("COMPOUND QUERY TEST: Remove Missing & Show Total Passengers")
print("=" * 60)

# Step 1: Upload test data
print("\n[1] Uploading test CSV with missing values...")
files = {'file': ('test.csv', io.StringIO(test_data))}
upload_response = requests.post(f"{API_BASE}/upload", files=files)
print(f"Upload Status: {upload_response.status_code}")
print(f"Response: {json.dumps(upload_response.json(), indent=2)}")

# Step 2: Test the compound query
print("\n[2] Testing Compound Query...")
query_text = "remove missing value and give the passenger total"
print(f"Query: '{query_text}'")

query_payload = {
    "query": query_text,
    "session_id": None
}

response = requests.post(
    f"{API_BASE}/query",
    json=query_payload
)

print(f"\nResponse Status: {response.status_code}")
if response.status_code != 200:
    print(f"Response Text: {response.text}")
else:
    print(f"Response Body:\n{json.dumps(response.json(), indent=2)}")

# Step 3: Verify data after cleaning
print("\n[3] Checking dataset info after cleaning...")
info_response = requests.get(f"{API_BASE}/info")
print(f"Dataset Info:\n{json.dumps(info_response.json(), indent=2)}")

# Step 4: Test direct count query
print("\n[4] Testing direct count query...")
count_response = requests.post(
    f"{API_BASE}/query",
    json={"query": "how many passengers total", "session_id": None}
)
print(f"Count Query Status: {count_response.status_code}")
if count_response.status_code != 200:
    print(f"Count Query Response Text: {count_response.text}")
else:
    print(f"Count Query Response:\n{json.dumps(count_response.json(), indent=2)}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
