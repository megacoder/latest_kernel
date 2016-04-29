#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	platform

class	LatestKernel( object ):

	def	__init__( self ):
		return

	def	uname( self ):
		return platform.release()

	def	kernels( self ):
		return os.listdir( '/lib/modules' )

if __name__ == '__main__':
	lk = LatestKernel()
	uname = lk.uname()
	for kernel in sorted( lk.kernels() ):
		print '{0:<3} {1}'.format(
			'-->' if kernel == uname else '',
			kernel
		)
	exit( 0 )
