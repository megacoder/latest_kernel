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

all::	latest-kernel.py

${TARGETS}::

clobber distclean:: clean

check::	latest-kernel.py
	./latest-kernel.py ${ARGS}

install:: latest-kernel.py
	${INSTALL} -D latest-kernel.py ${BINDIR}/latest-kernel

uninstall::
	${RM} ${BINDIR}/latest-kernel ${BINDIR}/latest_kernel

ifneq	(,${SUBDIRS})
${TARGETS}::
	${MAKE} TARGET=$@ ${SUBDIRS}
${SUBDIRS}::
	${MAKE} -C $@ ${TARGET}
endif
