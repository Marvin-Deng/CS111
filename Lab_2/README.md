# You Spin Me Round Robin

A linked list implementation of round robin process scheduling using for a given workload and quantum
length written. Returns the average wait and response times.

## Building

```shell
make
```

## Running

```shell
./rr processes.txt quantum
```
where `quantum` is an integer which represents the quantum length

```shell
./rr processes.txt 3
Average waiting time: 7.00
Average response time: 2.75
```

## Cleaning up

```shell
make clean
```

## Testing
python -m unittest
