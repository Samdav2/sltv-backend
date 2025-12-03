import time
from app.services.automation_service import VTUAutomator

def verify_performance():
    print("Starting Performance Verification...")

    # Measure first initialization (should be slow-ish)
    start_time = time.time()
    automator1 = VTUAutomator()
    # Access driver to ensure it's initialized
    _ = automator1.driver
    end_time = time.time()
    print(f"First Initialization Time: {end_time - start_time:.4f} seconds")

    # Measure second initialization (should be instant)
    start_time = time.time()
    automator2 = VTUAutomator()
    _ = automator2.driver
    end_time = time.time()
    print(f"Second Initialization Time: {end_time - start_time:.4f} seconds")

    if automator1.driver is automator2.driver:
        print("SUCCESS: Driver instance is shared (Singleton working).")
    else:
        print("FAILURE: Driver instance is NOT shared.")

    # Clean up
    automator1.close()

if __name__ == "__main__":
    verify_performance()
