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

Generation: 38,572 usec
Hash table base: 673,331 usec
  - 0 missing
Hash table v1: 1,042,002 usec
  - 0 missing
Hash table v2: 537,222 usec
  - 0 missing
```

## First Implementation
In the `hash_table_v1_add_entry()`, I locked the mutex at the start of the function and unlocked it at the end of the function. I employed a coarse-grained locking strategy using a single mutex for the entire hash table. This approach ensures thread safety by serializing access to the hash table, preventing concurrent modifications that could lead to race conditions or data corruption. 

### Performance
```shell
TODO how to run and results
```
Version 1 is a little slower than the base version. 
- Contention: When a thread attempts to acquire a mutex that is already held by another thread, it will block until the mutex becomes available. The thread cannot proceed with its task, resulting in slower performance
- Context Switches:  Each time a thread is blocked on a mutex, the operating system may perform a context switch to allow another thread to run on the CPU, which increases overhead. 

## Second Implementation
In the `hash_table_v2_add_entry` function, I TODO

### Performance
```shell
TODO how to run and results
```

TODO more results, speedup measurement, and analysis on v2

## Cleaning up
```shell
make clean
```

## Testing
```shell
python -m unittest 
```