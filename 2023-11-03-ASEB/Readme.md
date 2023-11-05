# Introduction

This is a talk that I had given on Nov 3, 2023. It mainly dealt with creating a basic IRC botnet and detecting it with Wireshark (since the IRC connection was unencrypted, finding it was trivial), and I touched upon the various kernel APIs available to detect file changes that this malware creates.

# Files

- The PDF file is the file that was the presentation.
- `boatnet.py` is the malware that was showcased in the presentation. It is a simple botnet, that uses a local IRC server as the C2 infrastructure, and was made to be easy to understand and achieve my objectives with the simplest code possible.
- `filesnoop.bt` is a simple [bpftrace](https://github.com/iovisor/bpftrace) program that looks for files that were changed by this malware. This only works on bpftrace >=v0.17.0, which is not bundled in Ubuntu by default as of writing (the version bundled is v0.14.0). The latest bpftrace version can be copied with this docker command: `docker run -v $(pwd):/output quay.io/iovisor/bpftrace:master   /bin/bash -c "cp /usr/bin/bpftrace /output"`
- `noti.py` is a [pyfanotify](https://pyfanotify.readthedocs.io/en/latest/) program that uses the [fanotify](https://man7.org/linux/man-pages/man7/fanotify.7.html) API to detect file changes.

# Dependencies

- `bpftrace` >=v0.17.0 for `filesnoop.bt`, which uses a new function called `strcontains`.
- `pyfanotify` for `noti.py`, which can be found on PyPI.

# References

- https://github.com/iovisor/bpftrace/blob/master/docs/tutorial_one_liners.md
- https://attack.mitre.org/matrices/enterprise/
- https://pyfanotify.readthedocs.io/en/latest/
