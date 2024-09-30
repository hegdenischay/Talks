# Introduction

This has the PDF and the source code of a talk that was given in the bi0s Meetup, September 2024. The idea was to create a rootkit that was easy to understand and detect it with eBPF.

The source code for the rootkit was heavily inspired by, and much of it was taken from the blog posts and code of XCellerator's linux_kernel_hacking repository. I have merely merged it into a single file for the sake of readability, and made it a bit more straightforward. 

The source code for the detection is a slightly modified version of `stacksnoop.py`, otherwise available [here](https://github.com/iovisor/bcc/blob/master/examples/tracing/stacksnoop.py). 

# How to run

Compile the rootkit using `make`. Install it with `sudo insmod rootkit.ko`. Have fun.

Before running the rootkit, stacksnoop must be running with `sudo python3 stacksnoop.py -v __x64_sys_kill`. This is because we are examining the stack before and after the rootkit is loaded. 
