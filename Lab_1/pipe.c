#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
	pid_t child_pid;

	child_pid = fork();

	if (child_pid == -1) {
		perror("fork");
	}

	// If fork returns 0, we are in the child
	if(child_pid == 0) {
		printf("In Child Process: Parent PID = %d, Child process PID = %d", getppid(), getpid());
	} 
	// Otherwise, we are in the parent
	else {
		printf("In Parent Process: Parent PID = %d, Child process PID = %d", getpid(), child_pid);
	}

	return 0;
}
