import requests
import time

BASE_URL = 'http://localhost:3001'


def test_start_timer():
    """Test starting a new timer"""
    print("\n" + "="*60)
    print("TEST 1: Start a Timer")
    print("="*60)
    
    data = {'label': 'Test Timer - Exercise Session'}
    response = requests.post(f'{BASE_URL}/timers/start', json=data)
    result = response.json()
    
    if result.get('success'):
        timer_id = result['timer']['id']
        print(f"✅ SUCCESS - Timer started!")
        print(f"   Timer ID: {timer_id}")
        print(f"   Label: {result['timer']['label']}")
        print(f"   Status: {result['timer']['status']}")
        print(f"   Start Time: {result['timer']['startTime']}")
        return timer_id
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
        return None


def test_get_timer_status(timer_id):
    """Test getting the status of a running timer"""
    print("\n" + "="*60)
    print("TEST 2: Get Timer Status (while running)")
    print("="*60)
    
    print("Waiting 3 seconds to accumulate time...")
    time.sleep(3)
    
    response = requests.get(f'{BASE_URL}/timers/{timer_id}')
    result = response.json()
    
    if result.get('success'):
        timer = result['timer']
        print(f"✅ SUCCESS - Retrieved timer status!")
        print(f"   Timer ID: {timer['id']}")
        print(f"   Label: {timer['label']}")
        print(f"   Status: {timer['status']}")
        print(f"   Elapsed Time: {timer['elapsedTime']['formatted']}")
        print(f"   Total Seconds: {timer['elapsedTime']['totalSeconds']}")
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")


def test_stop_timer(timer_id):
    """Test stopping a timer and getting elapsed time"""
    print("\n" + "="*60)
    print("TEST 3: Stop Timer and Get Elapsed Time")
    print("="*60)
    
    print("Waiting 2 more seconds...")
    time.sleep(2)
    
    response = requests.post(f'{BASE_URL}/timers/{timer_id}/stop')
    result = response.json()
    
    if result.get('success'):
        timer = result['timer']
        print(f"✅ SUCCESS - Timer stopped!")
        print(f"   Timer ID: {timer['id']}")
        print(f"   Label: {timer['label']}")
        print(f"   Status: {timer['status']}")
        print(f"   Elapsed Time: {timer['elapsedTime']['formatted']}")
        print(f"   Total Seconds: {timer['elapsedTime']['totalSeconds']}")
        print(f"   Started: {timer['startTime']}")
        print(f"   Stopped: {timer['endTime']}")
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")


def test_invalid_timer():
    """Test stopping an invalid timer ID"""
    print("\n" + "="*60)
    print("TEST 4: Stop Invalid Timer (Error Handling)")
    print("="*60)
    
    invalid_id = 999999
    response = requests.post(f'{BASE_URL}/timers/{invalid_id}/stop')
    result = response.json()
    
    if not result.get('success') and result.get('error'):
        print(f"✅ SUCCESS - Correctly returned error for invalid timer!")
        print(f"   Error: {result['error']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"❌ FAILED - Should have returned an error")


def test_multiple_timers():
    """Test creating and managing multiple timers"""
    print("\n" + "="*60)
    print("TEST 5: Multiple Timers")
    print("="*60)
    
    # Start multiple timers
    timer_ids = []
    for i in range(3):
        data = {'label': f'Multi-Timer Test {i+1}'}
        response = requests.post(f'{BASE_URL}/timers/start', json=data)
        result = response.json()
        if result.get('success'):
            timer_ids.append(result['timer']['id'])
            print(f"   Started timer {i+1}: ID {result['timer']['id']}")
    
    print(f"\n✅ Created {len(timer_ids)} timers")
    
    # Wait a bit
    print("   Waiting 2 seconds...")
    time.sleep(2)
    
    # Get all timers
    response = requests.get(f'{BASE_URL}/timers')
    result = response.json()
    
    if result.get('success'):
        print(f"\n✅ Retrieved all timers:")
        print(f"   Total count: {result['count']}")
        for timer in result['timers'][-3:]:  # Show last 3
            print(f"   - {timer['label']}: {timer['elapsedTime']['formatted']} ({timer['status']})")
    
    # Stop all test timers
    print("\n   Stopping all test timers...")
    for timer_id in timer_ids:
        requests.post(f'{BASE_URL}/timers/{timer_id}/stop')
    
    print("✅ Test completed")


def test_reset_timer():
    """Test resetting a timer"""
    print("\n" + "="*60)
    print("TEST 6: Reset Timer")
    print("="*60)
    
    # Start a timer
    data = {'label': 'Reset Test Timer'}
    response = requests.post(f'{BASE_URL}/timers/start', json=data)
    result = response.json()
    timer_id = result['timer']['id']
    
    print(f"   Started timer: ID {timer_id}")
    
    # Wait and stop
    time.sleep(2)
    response = requests.post(f'{BASE_URL}/timers/{timer_id}/stop')
    result = response.json()
    elapsed_before = result['timer']['elapsedTime']['totalSeconds']
    print(f"   Stopped at {elapsed_before} seconds")
    
    # Reset
    response = requests.post(f'{BASE_URL}/timers/{timer_id}/reset')
    result = response.json()
    
    if result.get('success'):
        print(f"✅ Timer reset successfully!")
        print(f"   Status: {result['timer']['status']}")
        
        # Check it's running again
        time.sleep(1)
        response = requests.get(f'{BASE_URL}/timers/{timer_id}')
        result = response.json()
        elapsed_after = result['timer']['elapsedTime']['totalSeconds']
        print(f"   New elapsed time: {elapsed_after} seconds (should be ~1)")
        
        # Clean up
        requests.delete(f'{BASE_URL}/timers/{timer_id}')
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")


def test_delete_timer():
    """Test deleting a timer"""
    print("\n" + "="*60)
    print("TEST 7: Delete Timer")
    print("="*60)
    
    # Start a timer
    data = {'label': 'Timer to Delete'}
    response = requests.post(f'{BASE_URL}/timers/start', json=data)
    result = response.json()
    timer_id = result['timer']['id']
    
    print(f"   Created timer: ID {timer_id}")
    
    # Delete it
    response = requests.delete(f'{BASE_URL}/timers/{timer_id}')
    result = response.json()
    
    if result.get('success'):
        print(f"✅ Timer deleted successfully!")
        
        # Verify it's gone
        response = requests.get(f'{BASE_URL}/timers/{timer_id}')
        result = response.json()
        if not result.get('success'):
            print(f"✅ Verified: Timer no longer exists")
        else:
            print(f"❌ Warning: Timer still exists after deletion")
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")


def test_get_all_timers():
    """Display all current timers"""
    print("\n" + "="*60)
    print("FINAL: View All Timers")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/timers')
    result = response.json()
    
    if result.get('success'):
        print(f"\n📊 Total Timers: {result['count']}\n")
        if result['count'] > 0:
            for timer in result['timers']:
                status_icon = "🟢" if timer['status'] == 'running' else "🔴"
                print(f"{status_icon} {timer['label']}")
                print(f"   ID: {timer['id']}")
                print(f"   Status: {timer['status']}")
                print(f"   Elapsed: {timer['elapsedTime']['formatted']} ({timer['elapsedTime']['totalSeconds']}s)")
                print(f"   Started: {timer['startTime']}")
                if timer['endTime']:
                    print(f"   Stopped: {timer['endTime']}")
                print()
        else:
            print("   No timers found.")
    else:
        print(f"❌ FAILED - {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  TIMER MICROSERVICE - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"  Server: {BASE_URL}")
    print("="*60)
    
    try:
        # Run all tests
        timer_id = test_start_timer()
        
        if timer_id:
            test_get_timer_status(timer_id)
            test_stop_timer(timer_id)
        
        test_invalid_timer()
        test_multiple_timers()
        test_reset_timer()
        test_delete_timer()
        test_get_all_timers()
        
        print("\n" + "="*60)
        print("  ALL TESTS COMPLETED!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server.")
        print("   Is the server running on http://localhost:3001?")
        print("   Start it with: node server.js\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
