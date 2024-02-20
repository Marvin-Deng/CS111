#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/queue.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

typedef uint32_t u32;
typedef int32_t i32;

struct process
{
  u32 pid;
  u32 arrival_time;
  u32 burst_time;
  u32 total_time_run;
  u32 index;

  TAILQ_ENTRY(process) pointers;
};

TAILQ_HEAD(process_list, process);

u32 next_int(const char **data, const char *data_end)
{
  u32 current = 0;
  bool started = false;
  while (*data != data_end)
  {
    char c = **data;

    if (c < 0x30 || c > 0x39)
    {
      if (started)
      {
        return current;
      }
    }
    else
    {
      if (!started)
      {
        current = (c - 0x30);
        started = true;
      }
      else
      {
        current *= 10;
        current += (c - 0x30);
      }
    }

    ++(*data);
  }

  printf("Reached end of file while looking for another integer\n");
  exit(EINVAL);
}

u32 next_int_from_c_str(const char *data)
{
  char c;
  u32 i = 0;
  u32 current = 0;
  bool started = false;
  while ((c = data[i++]))
  {
    if (c < 0x30 || c > 0x39)
    {
      exit(EINVAL);
    }
    if (!started)
    {
      current = (c - 0x30);
      started = true;
    }
    else
    {
      current *= 10;
      current += (c - 0x30);
    }
  }
  return current;
}

void init_processes(const char *path, struct process **process_data, u32 *process_size)
{
  int fd = open(path, O_RDONLY);
  if (fd == -1)
  {
    int err = errno;
    perror("open");
    exit(err);
  }

  struct stat st;
  if (fstat(fd, &st) == -1)
  {
    int err = errno;
    perror("stat");
    exit(err);
  }

  u32 size = st.st_size;
  const char *data_start = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (data_start == MAP_FAILED)
  {
    int err = errno;
    perror("mmap");
    exit(err);
  }

  const char *data_end = data_start + size;
  const char *data = data_start;

  *process_size = next_int(&data, data_end);

  *process_data = calloc(sizeof(struct process), *process_size);
  if (*process_data == NULL)
  {
    int err = errno;
    perror("calloc");
    exit(err);
  }

  for (u32 i = 0; i < *process_size; ++i)
  {
    (*process_data)[i].pid = next_int(&data, data_end);
    (*process_data)[i].arrival_time = next_int(&data, data_end);
    (*process_data)[i].burst_time = next_int(&data, data_end);
  }

  munmap((void *)data, size);
  close(fd);
}

int compare_arrival_time(const void* a, const void* b) {
  const struct process* processA = (const struct process*)a;
  const struct process* processB = (const struct process*)b;

  if (processA->arrival_time < processB->arrival_time) return -1;
  if (processA->arrival_time > processB->arrival_time) return 1;

  if (processA->index < processB->index) return -1;
  if (processA->index > processB->index) return 1;

  return 0;
}

void add_processes_to_ready_queue(struct process_list *not_processed, struct process_list *ready_queue, int time_elapsed) {
  if (!TAILQ_EMPTY(not_processed)) {
    struct process *next_to_process = TAILQ_FIRST(not_processed);
    while (next_to_process != NULL && next_to_process->arrival_time == time_elapsed) {
      struct process *new_process = (struct process*)malloc(sizeof(struct process));
      *new_process = *next_to_process;
      TAILQ_REMOVE(not_processed, next_to_process, pointers);
      TAILQ_INSERT_TAIL(ready_queue, new_process, pointers);
      next_to_process = TAILQ_FIRST(not_processed);
    }
  }
}

int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    return EINVAL;
  }
  struct process *data;
  u32 size;
  init_processes(argv[1], &data, &size);

  u32 quantum_length = next_int_from_c_str(argv[2]);

  struct process_list list;
  TAILQ_INIT(&list);

  u32 total_waiting_time = 0;
  u32 total_response_time = 0;

  // Record the index of each process
  for (int i = 0; i < size; i++) {
    data[i].index = i;
  }

  qsort(data, size, sizeof(struct process), compare_arrival_time);

  struct process_list not_processed;
  TAILQ_INIT (&not_processed);

  // Append processes to the not processed queue
  for (int i = 0; i < size; i++) {
    TAILQ_INSERT_TAIL(&not_processed, &data[i], pointers);
  }

  struct process* current_element;
  u32 time_elapsed = 0;
  u32 time_run = 0;

  // Add any processes which arrive at time 0
  add_processes_to_ready_queue(&not_processed, &list, time_elapsed);

  // Continue until processes have finished running
  while (!TAILQ_EMPTY(&not_processed) || !TAILQ_EMPTY(&list)) {

    // If possible, run a ready process
    if (!TAILQ_EMPTY(&list)) {
      current_element = TAILQ_FIRST(&list);
      
      // Calculate response time
      if (current_element->total_time_run == 0) {
        total_response_time += time_elapsed - current_element->arrival_time;
      }
      current_element->total_time_run += 1;
      time_run += 1;
    }
    
    time_elapsed++;

    // Add any processes which arrived
    add_processes_to_ready_queue(&not_processed, &list, time_elapsed);
      
    if (!TAILQ_EMPTY(&list)) {
      current_element = TAILQ_FIRST(&list);
      // Remove a finished process
      if (current_element->total_time_run == current_element->burst_time) {
        total_waiting_time += time_elapsed - current_element->arrival_time - current_element->burst_time;
        TAILQ_REMOVE(&list, current_element, pointers);
        current_element = TAILQ_FIRST(&list);
        time_run = 0;
      } 
      // Append a process which has finished its time slice to the back of the ready queue
      else if (time_run == quantum_length) {
          // Create a copy of the current element
          struct process* new_element = (struct process*)malloc(sizeof(struct process));
          *new_element = *current_element;

          // Move the interrupted process to the end of the queue
          TAILQ_REMOVE(&list, current_element, pointers);
          TAILQ_INSERT_TAIL(&list, new_element, pointers);
          time_run = 0;  
        }
      } 
  }

  printf("Average waiting time: %.2f\n", (float)total_waiting_time / (float)size);
  printf("Average response time: %.2f\n", (float)total_response_time / (float)size);

  free(data);
  return 0;
}
