"""
Test script for student max/min/list query functionality
"""
import requests
import pandas as pd
import io
import json

BASE_URL = "http://localhost:5001"

# Create test CSV data with student scores
csv_data = """Name,Score,Grade
Alice,95,A
Bob,78,C
Charlie,88,B
Diana,92,A
Eve,65,D
Frank,82,B
Grace,98,A
Henry,71,C"""

print("=" * 70)
print("STUDENT MAX/MIN/LIST QUERY TEST")
print("=" * 70)

try:
    # [1] Upload dataset
    print("\n[1] Uploading student dataset...")
    files = {'file': ('students.csv', io.BytesIO(csv_data.encode()))}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    assert response.status_code == 200, f"Upload failed: {response.status_code}"
    print(f"✅ Upload successful - {response.json()['rows']} students loaded")
    
    # [2] Test max/min/list student query
    print("\n[2] Testing compound student query...")
    print('   Query: "show the maximum scored student and minimum scored student and give the total number of student list"')
    
    query_data = {
        "query": "show the maximum scored student and minimum scored student and give the total number of student list"
    }
    response = requests.post(f"{BASE_URL}/query", json=query_data)
    
    print(f"   Status: {response.status_code}")
    result = response.json()
    
    if response.status_code == 200:
        print("\n✅ Query successful!")
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        
        # Verify structure
        if "data" in result:
            data = result["data"]
            if "max_student" in data:
                print("\n✅ Max student found:")
                print(f"   {data['max_student']}")
            if "min_student" in data:
                print("\n✅ Min student found:")
                print(f"   {data['min_student']}")
            if "total_students" in data:
                print(f"\n✅ Total students: {data['total_students']}")
    else:
        print(f"❌ Query failed: {result}")
    
    # [3] Test individual max query
    print("\n[3] Testing maximum score only...")
    query_data = {"query": "show maximum scored student"}
    response = requests.post(f"{BASE_URL}/query", json=query_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Max student: {result.get('data', {}).get('max_student', {})}")
    else:
        print(f"❌ Failed: {response.json()}")
    
    # [4] Test individual min query
    print("\n[4] Testing minimum score only...")
    query_data = {"query": "show minimum scored student"}
    response = requests.post(f"{BASE_URL}/query", json=query_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Min student: {result.get('data', {}).get('min_student', {})}")
    else:
        print(f"❌ Failed: {response.json()}")
    
    # [5] Test list all students
    print("\n[5] Testing student list query...")
    query_data = {"query": "list all students"}
    response = requests.post(f"{BASE_URL}/query", json=query_data)
    if response.status_code == 200:
        result = response.json()
        total = result.get('data', {}).get('total_students', 0)
        print(f"✅ Total students: {total}")
        students = result.get('data', {}).get('student_list', [])
        for idx, student in enumerate(students[:3], 1):  # Show first 3
            print(f"   {idx}. {student}")
        if len(students) > 3:
            print(f"   ... and {len(students) - 3} more")
    else:
        print(f"❌ Failed: {response.json()}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
