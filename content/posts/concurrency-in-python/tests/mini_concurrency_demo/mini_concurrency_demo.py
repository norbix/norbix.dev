# mini_concurrency_demo.py
import time, argparse, os, math, asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- helpers ---
def timer():
    t0 = time.perf_counter()
    return lambda label="elapsed": print(f"{label}: {time.perf_counter()-t0:.3f}s")

# --- simplest I/O-bound (sleep) ---

def sleep_blocking(_: int) -> int:
    time.sleep(1)  # pretend blocking I/O
    return 1

async def sleep_async(_: int) -> int:
    await asyncio.sleep(1)  # async I/O wait
    return 1

# --- simplest CPU-bound (tiny prime test) ---

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    r = int(math.isqrt(n))
    f = 3
    while f <= r:
        if n % f == 0: return False
        f += 2
    return True

# --- modes ---

def io_threading(n: int):
    print(f"[threading I/O] tasks={n}")
    done = timer()
    with ThreadPoolExecutor(max_workers=min(32, n)) as ex:
        list(ex.map(sleep_blocking, range(n)))
    done("threading (sleep 1s)")

async def io_async(n: int):
    print(f"[async I/O] tasks={n}")
    done = timer()
    await asyncio.gather(*(sleep_async(i) for i in range(n)))
    done("asyncio (sleep 1s)")

def cpu_serial(n: int):
    print(f"[CPU serial] nums={n}")
    nums = [10_000_019 + i for i in range(n)]  # small-ish primes check
    done = timer()
    _ = [is_prime(x) for x in nums]
    done("serial CPU")

def cpu_threads(n: int):
    print(f"[CPU threads] nums={n}  (GIL: expect ~no speedup)")
    nums = [10_000_019 + i for i in range(n)]
    done = timer()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        list(ex.map(is_prime, nums))
    done("threads CPU")

def cpu_processes(n: int):
    print(f"[CPU processes] nums={n}  (true parallelism)")
    nums = [10_000_019 + i for i in range(n)]
    done = timer()
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        list(ex.map(is_prime, nums, chunksize=5))
    done("processes CPU")

# --- CLI ---

def main():
    p = argparse.ArgumentParser(description="Simplest concurrency demo")
    p.add_argument("mode", choices=["io-threading", "io-async", "cpu-serial", "cpu-threads", "cpu-processes"])
    p.add_argument("--count", type=int, default=10, help="number of tasks/nums")
    args = p.parse_args()

    if args.mode == "io-threading":
        io_threading(args.count)
    elif args.mode == "io-async":
        asyncio.run(io_async(args.count))
    elif args.mode == "cpu-serial":
        cpu_serial(args.count)
    elif args.mode == "cpu-threads":
        cpu_threads(args.count)
    elif args.mode == "cpu-processes":
        cpu_processes(args.count)

if __name__ == "__main__":
    main()
