# You Spin Me Round Robin

An implementation for round robin scheduling for a given workload and quantum
length written in C

## Building

```shell
make
```

## Running

```shell
./rr processes .txt num_processes
```
where `num_processes` is an integer which represents the number of processes to run

```shell
./rr processes .txt 3
Average waiting time: 7.00
Average response time: 2.75
```

## Cleaning up

```shell
make clean
```

## Testing
python -m unittest
