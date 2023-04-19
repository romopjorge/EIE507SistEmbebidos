#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <iostream>
#include <fstream>
#include <wiringSerial.h>
#include <unistd.h>

using namespace std;

int main ()
{
  int fd ;
  int i = 0;

  if((fd=serialOpen("/dev/ttyACM0",9600))<0){
    fprintf(stderr,"Unable to open serial device: %s\n",strerror(errno));
    return 1;
  }

  while (i < 32000){
    char buffer[6];
    int j = 0;
    while (j < 6){
      int chars_read = read(fd, &buffer[j], 1);
      if (buffer[j] == 'A'){ 
        j = 6;
      }
      else{
      j++;
      }
    }
    buffer[5] = '\n';

    ofstream file("lecturas.txt", ios::app);
    if (file.is_open()) {
      file << buffer;
      file.close();
    }
    else{
      cout << "Error\n";
    }
    i++;
  }
 return 0;
}
