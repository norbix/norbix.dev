# What you’ll see

- io-threading vs io-async: ~1s for many tasks (they overlap waits).

- cpu-serial ≈ cpu-threads: similar (GIL).

- cpu-processes: noticeably faster on multi-core (true parallelism).

```shell

# I/O (sleep) — both finish in ~1s for many tasks, showing overlap
python mini_concurrency_demo.py io-threading --count 20
#python mini_concurrency_demo.py io-async --count 20

# CPU — compare serial vs threads vs processes
#python mini_concurrency_demo.py cpu-serial --count 20
#python mini_concurrency_demo.py cpu-threads --count 20      # GIL: little/no speedup
#python mini_concurrency_demo.py cpu-processes --count 20    # real parallel speedup
```
