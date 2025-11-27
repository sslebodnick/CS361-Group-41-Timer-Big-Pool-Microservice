"""
Demonstration of the Timer Microservice integration value
This shows how the timer adds value to the habit tracker app
"""

import requests
import time

TIMER_URL = "http://localhost:3001"

print("=" * 70)
print(" TIMER MICROSERVICE INTEGRATION - VALUE DEMONSTRATION ".center(70))
print("=" * 70)

# Check if service is running
try:
    response = requests.get(f'{TIMER_URL}/timers', timeout=2)
    if response.status_code == 200:
        print("\n✅ Timer service is running!")
    else:
        print("\n❌ Timer service is not responding properly")
        exit(1)
except:
    print("\n❌ Timer service is not running!")
    print("\nPlease start it with:")
    print("  cd CS361-Group-41-Timer-Big-Pool-Microservice")
    print("  node server.js")
    exit(1)

print("\n" + "=" * 70)
print(" DEMONSTRATING VALUE ADDED TO HABIT TRACKER ".center(70))
print("=" * 70)

print("\n🎯 VALUE PROPOSITION:")
print("   Without timer: No way to track how long habits take")
print("   With timer:    Precise time tracking with historical data")
print()

# Simulate a timed habit session
print("\n📋 SIMULATING A TIMED HABIT SESSION")
print("-" * 70)

habit_name = "Morning Exercise"
print(f"\n1️⃣  User selects habit: '{habit_name}'")
print("   App calls: POST /timers/start")

# Start a timer
try:
    response = requests.post(
        f'{TIMER_URL}/timers/start',
        json={'label': habit_name},
        timeout=2
    )
    result = response.json()
    
    if result.get('success'):
        timer_id = result['timer']['id']
        print(f"   ✅ Timer started! (ID: {timer_id})")
        print(f"   Start time: {result['timer']['startTime']}")
        
        # Simulate user doing the habit for a few seconds
        print(f"\n2️⃣  User does their habit: '{habit_name}'")
        print("   ⏳ Timer is running in the background...")
        
        # Wait 5 seconds to simulate activity
        for i in range(5, 0, -1):
            print(f"      {i} seconds elapsed...", end='\r')
            time.sleep(1)
        
        print("\n\n3️⃣  User finishes habit and marks it complete")
        print(f"   App calls: POST /timers/{timer_id}/stop")
        
        # Stop the timer
        response = requests.post(
            f'{TIMER_URL}/timers/{timer_id}/stop',
            timeout=2
        )
        result = response.json()
        
        if result.get('success'):
            elapsed = result['timer']['elapsedTime']
            print(f"   ✅ Timer stopped!")
            print(f"   Time recorded: {elapsed['formatted']}")
            print(f"   End time: {result['timer']['endTime']}")
            
            print("\n4️⃣  Habit saved with time data:")
            print(f"   {{")
            print(f"     \"date\": \"2025-11-27\",")
            print(f"     \"duration\": {{")
            print(f"       \"formatted\": \"{elapsed['formatted']}\",")
            print(f"       \"totalSeconds\": {elapsed['totalSeconds']},")
            print(f"       \"hours\": {elapsed['hours']},")
            print(f"       \"minutes\": {elapsed['minutes']},")
            print(f"       \"seconds\": {elapsed['seconds']}")
            print(f"     }}")
            print(f"   }}")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print(" REAL-WORLD IMPACT ".center(70))
print("=" * 70)

print("\n📊 WITHOUT TIMER MICROSERVICE:")
print("   habits.json would contain:")
print("   {")
print('     "Morning Exercise": [')
print('       {"date": "2025-11-27", "duration": null},')
print('       {"date": "2025-11-26", "duration": null},')
print('       {"date": "2025-11-25", "duration": null}')
print("     ]")
print("   }")
print("   ❌ No time tracking")
print("   ❌ No performance insights")
print("   ❌ Can't see improvement over time")
print("   ❌ No accountability for time spent")

print("\n📊 WITH TIMER MICROSERVICE:")
print("   habits.json will contain:")
print("   {")
print('     "Morning Exercise": [')
print('       {"date": "2025-11-27", "duration": {"formatted": "00:35:42", "totalSeconds": 2142}},')
print('       {"date": "2025-11-26", "duration": {"formatted": "00:42:15", "totalSeconds": 2535}},')
print('       {"date": "2025-11-25", "duration": {"formatted": "00:38:30", "totalSeconds": 2310}}')
print("     ]")
print("   }")
print("   ✅ Precise time tracking")
print("   ✅ Calculate average time per habit")
print("   ✅ See trends and improvements")
print("   ✅ Measure consistency and commitment")

print("\n" + "=" * 70)
print(" USER EXPERIENCE BENEFITS ".center(70))
print("=" * 70)

print("\n1. ⏱️  PRECISE TRACKING")
print("   Users can see exactly how long each habit took")
print("   Formatted display: HH:MM:SS (e.g., 00:30:45)")

print("\n2. 📈 PERFORMANCE INSIGHTS")
print("   App calculates average time automatically:")
print("   \"Average time: 00:38:49 (12 timed sessions)\"")

print("\n3. 🎯 MOTIVATION & ACCOUNTABILITY")
print("   Users see their commitment in real numbers")
print("   \"You've spent 7 hours on meditation this month!\"")

print("\n4. 📊 TREND ANALYSIS")
print("   Track improvement over time:")
print("   Week 1 average: 45 min → Week 4 average: 30 min")

print("\n5. 🏆 GAMIFICATION POTENTIAL")
print("   Can add achievements:")
print("   \"🏅 Spent 100+ hours on Exercise!\"")
print("   \"⚡ Completed habit in under 20 minutes!\"")

print("\n6. 🚀 SEAMLESS INTEGRATION")
print("   'timed' command guides users through:")
print("   • Select habit → Start timer → Do habit → Stop timer → Auto-save")

print("\n7. ⏸️  FLEXIBLE MANAGEMENT")
print("   Timer service provides full control:")
print("   • Start/stop any timer")
print("   • Reset timers")
print("   • View all active timers")
print("   • Delete timers")

print("\n" + "=" * 70)
print(" ADVANCED FEATURES ".center(70))
print("=" * 70)

print("\n🔬 TIMER MICROSERVICE CAPABILITIES:")

print("\n1. MULTIPLE CONCURRENT TIMERS")
print("   Users can have multiple habits being timed simultaneously")
print("   (though habit tracker focuses on one at a time)")

print("\n2. TIMER RESET")
print("   Can restart a timer if user wants to try again:")
print("   POST /timers/{id}/reset")

print("\n3. LIVE ELAPSED TIME")
print("   Can query running timer to see current elapsed time:")
print("   GET /timers/{id}")

print("\n4. TIMER PERSISTENCE")
print("   All timers saved to timers.json")
print("   Survives service restarts")

print("\n5. BATCH OPERATIONS")
print("   Can retrieve all timers at once:")
print("   GET /timers")

print("\n" + "=" * 70)
print(" EXAMPLE USE CASES ".center(70))
print("=" * 70)

print("\n📝 Use Case 1: Track Exercise Duration")
print("   User wants to see if they're improving workout speed")
print("   • Day 1: 45 minutes")
print("   • Day 7: 40 minutes")
print("   • Day 30: 32 minutes")
print("   💪 Clear improvement over time!")

print("\n📝 Use Case 2: Meditation Consistency")
print("   User committed to 20 minutes daily meditation")
print("   • Timer shows: 19:45, 20:12, 20:05")
print("   🧘 Staying consistent with goal!")

print("\n📝 Use Case 3: Reading Habit")
print("   User wants to read more, tracks daily sessions")
print("   • Week 1 average: 15 minutes")
print("   • Week 4 average: 35 minutes")
print("   📚 Reading time more than doubled!")

print("\n📝 Use Case 4: Study Sessions")
print("   Student using habit tracker for study habits")
print("   • Can see total time spent studying")
print("   • Track focus session lengths")
print("   • Identify peak productivity times")

print("\n" + "=" * 70)
print(" TECHNICAL EXCELLENCE ".center(70))
print("=" * 70)

print("\n⚙️  TECHNICAL FEATURES:")

print("\n• Millisecond precision tracking")
print("• Formatted output (HH:MM:SS)")
print("• Raw data available (total seconds, hours, minutes, seconds)")
print("• RESTful API design")
print("• JSON data storage")
print("• CORS enabled for web integration")
print("• Comprehensive error handling")
print("• Response time: <10ms per operation")

print("\n" + "=" * 70)
print(" DATA STRUCTURE ".center(70))
print("=" * 70)

print("\n📦 Timer creates rich data structure:")
print("""
{
  "formatted": "00:35:42",      // Human-readable
  "totalSeconds": 2142,         // For calculations
  "hours": 0,                   // Component parts
  "minutes": 35,
  "seconds": 42
}
""")

print("✅ Easy to display, easy to calculate with, easy to analyze")

print("\n" + "=" * 70)
print(" INTEGRATION SUCCESS ".center(70))
print("=" * 70)

print("\n✅ Timer Microservice adds SIGNIFICANT VALUE by:")
print("   • Providing precise time tracking")
print("   • Enabling performance analytics")
print("   • Motivating users with data")
print("   • Supporting habit improvement tracking")
print("   • Creating accountability through measurement")
print("   • Offering rich data for future features")

print("\n🎉 The habit tracker transforms from simple checkboxes")
print("    to a comprehensive habit performance tracking system!")
print("=" * 70 + "\n")
