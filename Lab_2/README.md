# You Spin Me Round Robin

A linked list implementation of round robin process scheduler given a text file with processes quantum length. Returns the average wait and response times.

## Building

```shell
make
```

## Running

processes.txt should have the number of processes in the first line followed by a list of processes in the form `pid arrival_time burst_time`

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
