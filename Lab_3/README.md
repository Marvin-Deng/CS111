# Hash Hash Hash
A thread safe implementation of a hash table applying two different locking techniques to `hash-table-v1.c` and `hash-table-v2.c` using mutex locks. The hash tables use separate chaining to manage collisions, with each bucket containing a singly linked list of key-value pairs. 

## Building
```shell
make
```

## Running
```shell
./hash-table-tester -t <number of threads> -s <hash table entries to add per thread>
```

Sample usage:
```shell
./hash-table-tester -t 8 -s 50000

Generation: 73,514 usec
Hash table base: 1,252,320 usec
  - 0 missing
Hash table v1: 1,514,597 usec
  - 0 missing
Hash table v2: 394,745 usec
  - 0 missing
```

## First Implementation
In the `hash_table_v1_add_entry()`, I locked the mutex at the start of the function and unlocked it at the end of the function. I employed a coarse-grained locking strategy using a single mutex for the entire hash table. This approach ensures thread safety by serializing access to the hash table, preventing concurrent modifications that could lead to race conditions or data corruption. I made sure to free memory of the hash table's `mutex hash_table_v1_destroy()`.

### Performance V1
```shell
./hash-table-tester -t 8 -s 50000

Generation: 73,514 usec
Hash table base: 1,252,320 usec
  - 0 missing
Hash table v1: 1,514,597 usec
  - 0 missing
Hash table v2: 394,745 usec
  - 0 missing
```

Version 1 is slower than the base version. 
- Thread Definition Overhead: When a thread attempts to acquire a mutex that is already held by another thread, it will block until the mutex becomes available. The thread cannot proceed with its task, resulting in slower performance. Even though we have multiple threads, they cannot concurrently execute due to a locked hash table, resulting in slower performance compared to the base implmentation
- Context Switches:  Each time a thread is blocked on a mutex, the operating system may perform a context switch to allow another thread to run on the CPU, which increases overhead. 

## Second Implementation
In hash_table_v2_add_entry(), I locked the mutex for the specific hash table entry at the start of the add entry function and unlocked it at the end of the function. I used a fine-grain locking strategy where each hash table entry has a mutex. A mutex is only locked on the hash table entry that is being inserted into, allowing other operations to continue on other parts of the hash table. This allowed for parallelism without compromising correctness, resulting in faster performance compared to the base and first implementation. I also made sure to free the memory of each hash table entry's mutex in the hash_table_v2_destroy() function.

### Performance V2
```shell
./hash-table-tester -t 8 -s 50000

Generation: 73,514 usec
Hash table base: 1,252,320 usec
  - 0 missing
Hash table v1: 1,514,597 usec
  - 0 missing
Hash table v2: 394,745 usec
  - 0 missing
```

Version 2 is faster than the base and first implementation. 
- Results: My implementation satisfies the speed requirement of v2 ≤ base/(num cores - 1), since 394,745 usec < 1,252,320 usec/(4 - 1) = 417,440 usec. Performance is consistent across multiple runs of both small and large number of operations.
- Increased Concurrency: This locking strategy is faster than the first implementation because multiple threads can still perform operations on the hash table if they insert into different hash table entries

## Cleaning up
```shell
make clean
```

## Testing
```shell
python -m unittest 

or

python3.11 -m unittest
```

## Testing memory leaks
```shell
valgrind ./hash-table-tester -t 8 -s 50000
```

## Number of cores

```shell
nproc
```