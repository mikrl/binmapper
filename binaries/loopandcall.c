#include <stdio.h>

float unit_inc(void);
int ten_inc(int increment);

int main(void){
  int idx = 0;
  float unit_counter = 0;
  int ten_counter = 0;
  
  for (idx = 0; idx < 100; idx++){
    unit_counter+=unit_inc();
    if (idx % 10 ==0){
      ten_counter+=ten_inc(idx);
    }
  }
  printf("[*]Printing values\n[*]unit=%f\n[*]ten=%i\n[*]Done\n", unit_counter, ten_counter);
  return 0;
}

float unit_inc(void){
  return 3.14;
    }

int ten_inc(int increment){
  return 100-increment;
    }
