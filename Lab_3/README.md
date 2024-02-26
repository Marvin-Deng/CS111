# Hash Hash Hash
A thread safe implementation of a hash table using two different locking techniques to `hash-table-v1.c` and `hash-table-v2.c` using mutex locks. This hash table utilizes separate chaining to manage collisions, with each bucket containing a singly linked list of key-value pairs. 

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
```

Version 1 is slower than the base version. 
- Thread Definition Overhead: 
- Contention: When a thread attempts to acquire a mutex that is already held by another thread, it will block until the mutex becomes available. The thread cannot proceed with its task, resulting in slower performance
- Context Switches:  Each time a thread is blocked on a mutex, the operating system may perform a context switch to allow another thread to run on the CPU, which increases overhead. 

## Second Implementation
In `hash_table_v2_add_entry()`, I locked the mutex for the specific hash table entry at the start of the add entry function and unlocked it at the end of the function. I used a fine grain locking strategy where each hash table entry has a mutex. A mutex is only locked on the has table entry that is being inserted into, allowing other operations to continue on other parts of the hash table. This allowed for parallelism without compromising correctness, resulting in faster performance compared to the base and first implementation. I also made sure to free the memory of each hash table entry's mutex in the `hash_table_v2_destroy()` function.

### Performance V2
```shell
./hash-table-tester -t 8 -s 50000

Generation: 73,514 usec
Hash table base: 1,252,320 usec
  - 0 missing
Hash table v2: 394,745 usec
  - 0 missing
```

TODO more results, speedup measurement, and analysis on v2
Version 2 is faster than the base and first implmentation. My implmentation satisfies the speed requirement of v2 ≤ base/(num cores - 1), since 394,745 usec < 1,252,320 usec/(4 - 1) = 417440 usec.

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