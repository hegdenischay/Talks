obj-m += rootkit.o
EXTRA_CFLAGS += -Wno-incompatible-pointer-types -Wno-int-conversion 

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) EXTRA_CFLAGS=$(EXTRA_CFLAGS) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
