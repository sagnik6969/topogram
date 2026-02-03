import httpx
import time
import threading

BASE_URL = "http://localhost:8000/main_backend_service/health"
HEADER = {"Authorization": "Bearer mocked_token"} 

def test_global_limit():
    print("Testing Global Limit (100/minute)...")
    success_count = 0
    blocked_count = 0
    
    start_time = time.time()
    
    for i in range(110):
        try:
            with httpx.Client() as client:
                response = client.get(BASE_URL)
                if response.status_code == 200:
                    success_count += 1
                elif response.status_code == 429:
                    blocked_count += 1
                    print(f"Blocked at request {i+1}")
                    break
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"Global Limit Test Result: Success: {success_count}, Blocked: {blocked_count}")

if __name__ == "__main__":
    # Note: Requires server running
    test_global_limit()
