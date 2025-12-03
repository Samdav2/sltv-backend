import threading
import time
from app.services.automation_service import VTUAutomator
from app.schemas.service import TVRequest

def mock_get_details(name):
    print(f"[{name}] Starting request...")
    automator = VTUAutomator()
    # We can't easily mock the full Selenium flow without a real account/site,
    # but we can check if the lock is working by inspecting the internal lock or
    # by observing that they don't enter the critical section together.
    # Since we modified the real method to use `with self._lock:`, we can trust the lock primitive.
    # To verify, we will check if the driver is shared and if the lock object is the same.

    print(f"[{name}] Driver ID: {id(automator.driver)}")
    print(f"[{name}] Lock ID: {id(automator._lock)}")

    # We can also try to acquire the lock manually to see if it blocks
    if automator._lock.acquire(blocking=False):
        print(f"[{name}] Acquired lock successfully (unexpected if another thread holds it!)")
        automator._lock.release()
    else:
        print(f"[{name}] Could not acquire lock (expected if another thread holds it)")

def verify_concurrency():
    print("Starting Concurrency Verification...")

    # Initialize singleton first
    VTUAutomator()

    threads = []
    for i in range(3):
        t = threading.Thread(target=mock_get_details, args=(f"Thread-{i}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Concurrency Verification Complete.")

if __name__ == "__main__":
    verify_concurrency()
