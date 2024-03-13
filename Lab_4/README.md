# Hey! I'm Filing Here

An implementation of a 1 MiB ext2 file system with 2 directories, 1 regular file, and 1 symbolic link.

## Building

```shell
make
```
## Running

Run the executable to create cs111 -base.img
```shell
./ext2-create
```

Dumps the filesystem information to help debug
```shell
dumpe2fs cs111-base.img
```

Check that the filesystem is correct
```shell
fsck.ext2 cs111-base.img
```

Create a directory to mnt the filesystem to
```shell
mkdir mnt
```

Mount the filesystem 
```shell
sudo mount -o loop cs111-base.img mnt
```

Unmount the filesystem when you 're done
```shell
sudo umount mnt
```

Delete the directory used for mounting when you 're done
```shell
rmdir mnt
```

## Cleaning up

```shell
make clean
```

## Testing
```shell
python -m unittest
```
