import time
import threading
import requests

def call(url):
    start = time.time()
    requests.get(url)
    print(f"{url} finished in {time.time() - start:.2f}s")

def test(url):
    print(f"\n--- Testing {url} ---")
    start = time.time()
    threads = [threading.Thread(target=call, args=(url,)) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"TOTAL TIME: {time.time() - start:.2f}s")

test("http://127.0.0.1:8000/slow-sync")
test("http://127.0.0.1:8000/slow-async")