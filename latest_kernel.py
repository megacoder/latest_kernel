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
		uname = self.uname()
		for entry in os.listdir( '/lib/modules' ):
			yield(
				entry == uname,
				entry
			)
		return

if __name__ == '__main__':
	lk = LatestKernel()
	uname = lk.uname()
	for thumb,entry in lk.kernels():
		print '{0:<3} {1}'.format(
			'-->' if thumb else '',
			entry,
			entry
		)
	exit( 0 )
