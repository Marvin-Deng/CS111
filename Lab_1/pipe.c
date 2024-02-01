#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

int main(int argc, char *argv[])
{
	int pipefd[2];
    int prev_fd = -1; // Transfers the output of one command to the input of another

    for (int i = 1; i < argc; i++) {
		// Create a pipe if it isn't the last command
        if (i < argc - 1) { 
            if (pipe(pipefd) == -1) {
                perror("pipe");
                exit(EXIT_FAILURE);
            }
        }

        int ret = fork();
        if (ret == -1) {
            perror("fork");
            exit(EXIT_FAILURE);
        }

		// Child process
        if (ret == 0) { 
            if (prev_fd != -1) {
                dup2(prev_fd, 0); // Redirect standard input to previous read end
                close(prev_fd);
            }
            if (i < argc - 1) { // If not on the last command, redirect to pipe
                close(pipefd[0]); 
                dup2(pipefd[1], 1); // Redirect standard output to current write end
                close(pipefd[1]);
            }
			if (execlp(argv[i], argv[i], NULL) == -1) {
				perror("execlp failed");
				exit(EINVAL);
			}
        } 
		// Parent process
		else { 
            int status = 0;
            wait(&status); // Waits to get the status of the child 
            if (prev_fd != -1) {
                close(prev_fd); 
            }
            if (i < argc - 1) {
                close(pipefd[1]);
                prev_fd = pipefd[0]; // Save current read end for next iteration
            }
			// Return the error code if a child process failed
			if (WIFEXITED(status) && WEXITSTATUS(status) != 0) {
                return WEXITSTATUS(status); 
            }
        }
    }

    return 0;
}
