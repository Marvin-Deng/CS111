## Pipe Up
A C program which mimics the pipe operator (|) used in shells, which pipes the output of one program as the input of another program.

## Building
Run `make`

## Running
- Arguments must be programs without additional arguments or flags
- Example arguments include ls, cat, wc, and sort

Run `./pipe command_1 command_2 ... command_n`

Example:
Running `./pipe ls sort cat` should output the sorted contents of a directory in a sorted column

Makefile
pipe
pipe.c
pipe.o
__pycache__
README.md
test_lab1.py

## Testing
`python -m unittest`

## Cleaning up
`make clean`
