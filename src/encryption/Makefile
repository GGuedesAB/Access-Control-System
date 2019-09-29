CC       = gcc
LD       = gcc
CFLAGS   = -Wall -Os -c
LDFLAGS  = -Wall -shared

default: encrypt.so decrypt.so

aes.o:  aes.c
	$(CC) $(CFLAGS) $^ -o $@

encrypt.o: encrypt.c aes.o
	   $(CC) $(CFLAGS) $^ -o $@

decrypt.o: decrypt.c aes.o
	   $(CC) $(CFLAGS) $^ -o $@

encrypt.so: encrypt.o aes.o
	     $(LD) $(LDFLAGS) $^ -o $@

decrypt.so: decrypt.o aes.o
	     $(LD) $(LDFLAGS) $^ -o $@

clean:
	rm -f *.OBJ *.LST *.so *.o *.gch *.out *.hex *.map *.elf
