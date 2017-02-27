TARGETS=all check clean clobber distclean install uninstall
TARGET=all

PREFIX=${DESTDIR}/opt
BINDIR=${PREFIX}/bin
SUBDIRS=

ifeq	(${MAKE},gmake)
	INSTALL=ginstall
else
	INSTALL=install
endif

.PHONY: ${TARGETS} ${SUBDIRS}

all::	latest_kernel.py

${TARGETS}::

clobber distclean:: clean

check::	latest_kernel.py
	./latest_kernel.py ${ARGS}

install:: latest_kernel.py
	${INSTALL} -D latest_kernel.py ${BINDIR}/latest_kernel

uninstall::
	${RM} ${BINDIR}/latest_kernel

ifneq	(,${SUBDIRS})
${TARGETS}::
	${MAKE} TARGET=$@ ${SUBDIRS}
${SUBDIRS}::
	${MAKE} -C $@ ${TARGET}
endif
