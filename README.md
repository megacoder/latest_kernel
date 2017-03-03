LATEST_KERNEL
=============

What
----

Displays a list of installed kernels and highlights the kernel vesion presently booted.

How
---

	$ latest_kernel
	    4.9.3-200.fc25.x86_64           *** UNKNOWN ***
	    4.9.9-200.fc25.x86_64           kernel-core-4.9.9-200.fc25.x86_64.rpm
	    4.9.10-200.fc25.x86_64          kernel-core-4.9.10-200.fc25.x86_64.rpm
	--> 4.9.12-200.fc25.x86_64          kernel-core-4.9.12-200.fc25.x86_64.rpm

Notice the entry mared *UNKNOWN*; there is a directory present in:

	/lib/modules/4.9.3-200.fc25.x86_64

but there is no kernel RPM by that version installed.  Most likely this was caused by a custom kernel driver, which has long since been removed.

The entry marked with *-->* shows the currently-running kernel version.

Why
---

I tend to keep my servers running and cannot reboot them as soon as a new kernel version arrives.  This shell script allows me to see my backlog and just how out-of-date my present kernel is.
