# Notes you can mention in interviews

- Model boundary: the “model” is just a function today; swap with a real model (e.g., load a .pt/.pkl) in startup.

- Batch endpoint: improves throughput, reduces overhead.

- Validation: FastAPI’s Pydantic schemas give type validation & OpenAPI docs for free (/docs).

- Scaling: run with multiple workers (e.g., uvicorn --workers 4) behind a reverse proxy; add request timeouts & logging.

- Concurrency: I/O-bound models (remote vector DB, files) benefit from async (FastAPI); CPU-bound models may need process workers.

## Python / Programming

- Difference between list, tuple, and set in Python

1. Difference between list, tuple, and set in Python

    - List: Ordered, mutable, allows duplicates.
    
    ```python
     l = [1, 2, 2, 3]
     ```

    - Tuple: Ordered, immutable, allows duplicates.

    ```python
    t = (1, 2, 2, 3)
    ```

    - Set: Unordered, mutable, unique elements only.

    ```python
     s = {1, 2, 3}
     ```

- How Python handles memory management and garbage collection

    - Python uses reference counting + garbage collector (for cyclic references).

    - Garbage collector is in gc module.

    - Objects are freed when reference count = 0.

- Multithreading vs multiprocessing in Python

    - Multithreading: Good for I/O-bound tasks, limited by GIL (only one thread executes Python bytecode at a time).

    - Multiprocessing: Good for CPU-bound tasks, spawns multiple processes with independent GILs.

- Writing efficient Pandas operations for large datasets

    - Use vectorized operations instead of loops.
    
    - Use .applymap(), .apply() sparingly.
    
    - Use categorical data types for repeated strings.
    
        Example:
        
        ````python
        import panda as pd
        
        df['col3'] = df['col1'] + df['col2']  # vectorized, faster, no loop
        ````
        
        what is this syntac df['col3']
        - df['col3'] is a way to create or access a column named 'col3' in a Pandas DataFrame (df). It uses the column label as a key to get or set the data in that column.
        
        is this column a list?
        - Yes, df['col3'] returns a Pandas Series, which is similar to a list but with additional functionality and metadata (like index).

## SQL & Databases

- Write a query to find the nth highest salary in an Employee table

```sql
SELECT DISTINCT salary
FROM employees e1
WHERE N-1 = (
  SELECT COUNT(DISTINCT salary)
  FROM employees e2
  WHERE e2.salary > e1.salary
);
```

- Difference between OLTP and OLAP systems

    - OLTP: Transactional, frequent small updates (e.g., bank transactions).

    - OLAP: Analytical, read-heavy, aggregate queries (e.g., business intelligence).

- How indexes work in relational databases and when to use them

    - Index = data structure (usually B-Tree) to speed up lookups.
    
    - Use on frequently queried columns, WHERE, JOIN, ORDER BY.
    
    - Avoid indexing low-cardinality columns (e.g., gender).

- Partitioning vs sharding in large datasets

    - Partitioning: Splitting a single DB/table into smaller pieces within same system (horizontal/vertical).
    
    - Sharding: Splitting data across multiple databases/servers (distributed).

## Big Data & ETL

- Difference between batch and streaming data pipelines

    - Batch: Processes large chunks at scheduled intervals (e.g., daily ETL job).
    
    - Streaming: Processes events in real time (e.g., fraud detection).

- Kafka vs Kinesis: when to use each

    - Kafka: Open-source, on-prem or cloud, high throughput, ecosystem rich.
    
    - Kinesis: AWS managed, integrates with AWS ecosystem, simpler to set up.

    what is kinesis
    - Kinesis is a fully managed data streaming service provided by Amazon Web Services (AWS). 
      It allows you to collect, process, and analyze real-time streaming data at scale. 
      Kinesis is commonly used for applications such as real-time analytics, log and event data collection, and data ingestion for big data processing.
    
    What is Kafka
    - Apache Kafka is an open-source distributed event streaming platform used for building real-time data pipelines and streaming applications. 
      It is designed to handle high-throughput, fault-tolerant, and scalable data streams. 
      Kafka is widely used for applications such as log aggregation, real-time analytics, and event-driven architectures.

- How Spark optimizes jobs under the hood (RDD, DataFrame, Catalyst Optimizer)

    - DD: Low-level, immutable distributed collections.
    
    - DataFrame: High-level abstraction, optimized via Catalyst Optimizer.
    
    - Catalyst Optimizer: Applies query optimization (predicate pushdown, column pruning, etc.).

- Best practices for building resilient ETL pipelines

    - Idempotent operations.
    
    - Logging & monitoring (Prometheus, ELK).
    
    - Retry policies & dead-letter queues.
    
    - Schema evolution handling.
    
    - Test with sample + production-like data.

## Cloud & Data Warehousing

- Snowflake vs Redshift vs BigQuery: key differences

    - Snowflake: Multi-cloud, separates storage & compute, easy scaling.
    
    - Redshift: AWS-native, cluster-based, good for existing AWS users.
    
    - BigQuery: Serverless, pay-per-query, Google-native, great for ad-hoc analytics.

- How to design a data lake vs a data warehouse

    - Data Lake: Raw, unstructured + structured, cheap storage (S3, HDFS).
    
    - Data Warehouse: Processed, structured, optimized for queries (Snowflake, Redshift).

    But how to design a data lake vs a data warehouse
    - Designing a Data Lake:
      1. Choose a scalable storage solution (e.g., AWS S3, Azure Data Lake Storage).
      2. Define a clear folder structure (e.g., raw/, processed/, curated/).
      3. Implement data ingestion pipelines (batch and streaming).
      4. Use metadata management tools (e.g., AWS Glue, Apache Atlas).
      5. Set up access controls and security policies.

- Role of IAM and data security in cloud environments

    - IAM = Identity and Access Management.
    
    - Used for fine-grained access control (users, roles, policies).
    
    - Ensure encryption at rest & in transit.

- How orchestration works with Apache Airflow

    - Airflow = workflow orchestration tool (DAGs = Directed Acyclic Graphs).
    
    - Handles scheduling, retries, dependencies, monitoring.
    
    - Example: ETL pipeline → extract → transform → load.

## Coding Round

- Reverse words in a string without using built-in functions

    ```python
  def reverse_words(s):
    words, word, result = [], "", ""
    for c in s:
        if c == " ":
            words.append(word)
            word = ""
        else:
            word += c
    words.append(word)  # last word
    for i in range(len(words)-1, -1, -1):
        result += words[i] + " "
    return result.strip()

    print(reverse_words("Data Engineer Interview"))
    # Output: Interview Engineer Data
    ```

- Implement a Kafka producer-consumer in Python

    ```python
    from kafka import KafkaProducer, KafkaConsumer
    
    # Producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send('my_topic', b'Hello Kafka')
    producer.flush()
    
    # Consumer
    consumer = KafkaConsumer('my_topic', bootstrap_servers='localhost:9092')
    for msg in consumer:
    print(msg.value.decode())
    ```

- Write an Airflow DAG for a daily ETL job

    ```python
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime, timedelta
    
    def etl_task():
    print("Running ETL...")
    
    default_args = {"owner": "airflow", "start_date": datetime(2023, 1, 1)}
    dag = DAG("daily_etl", default_args=default_args, schedule_interval="@daily")
    
    etl = PythonOperator(task_id="etl", python_callable=etl_task, dag=dag)
    ```

- Find duplicates in a dataset efficiently

    ```python
    import pandas as pd
    df = pd.DataFrame({'id':[1,2,2,3,3,3,4]})
    duplicates = df[df.duplicated('id', keep=False)]
    print(duplicates)
    ```

## Arrays & Strings

## Reverse a string (list-based, in place)

```python
def reverse_string(s: str) -> str:
    chars = list(s)          # convert string → list of chars
    left, right = 0, len(chars) - 1
    
    while left < right:      # two-pointer swap
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    
    return ''.join(chars)    # back to string
```

Example: 

```python
print(reverse_string("hello"))  # "olleh"
print(reverse_string("norbix")) # "xibron"
```

## Find first non-repeating character

```python
def first_non_repeating_char(s: str):
    freq = {}

    # Count frequency of each character
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    # Find first character with frequency = 1
    for ch in s:
        if freq[ch] == 1:
            return ch
    return None
```

Example: 
    
```matlab
Input: "swiss"
Output: "w"     # because 's' repeats, 'w' is first non-repeating
```

```python
print(first_non_repeating_char("swiss"))     # w
print(first_non_repeating_char("aabbcc"))    # None
print(first_non_repeating_char("alphabet"))  # l
```

## Merge two sorted arrays

```python
def merge_sorted(arr1, arr2):
    i, j = 0, 0
    merged = []

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1

    # add leftovers
    merged += arr1[i:]
    merged += arr2[j:]
    return merged
```

Example:

```matlab
Input:  
    arr1 = [1, 3, 5] 
    arr2 = [2, 4, 6]

Output: 
    [1, 2, 3, 4, 5, 6]

Compare 1 and 2, take 1 -> merged = [1]
Compare 3 and 2, take 2 -> merged = [1, 2]
Compare 3 and 4, take 3 -> merged = [1, 2, 3]
Compare 5 and 4, take 4 -> merged = [1, 2, 3, 4]
Compare 5 and 6, take 5 -> merged = [1, 2, 3, 4, 5]
Leftover: add 6 -> merged = [1, 2, 3, 4, 5, 6]
```

```python
print(merge_sorted([1, 3, 5], [2, 4, 6]))
# [1, 2, 3, 4, 5, 6]

print(merge_sorted([1, 2, 7], [3, 4, 5, 6]))
# [1, 2, 3, 4, 5, 6, 7]
```

## Rotate an array by k steps

```python
def rotate_array(arr, k):
    n = len(arr)
    k = k % n  # handle k > n, normalize k to within array length
    
    return arr[-k:] + arr[:-k] # [last k elements] + [first n-k elements]
```

Example:
```matlab
Input:
    arr = [1, 2, 3, 4, 5]
    k = 2
Output:
    [4, 5, 1, 2, 3]
Rotate right by 2:
Take last 2 elements: [4, 5]
Take first 3 elements: [1, 2, 3]
Concatenate: [4, 5] + [1, 2, 3]
```











