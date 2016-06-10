#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	platform
import	re
import	sys

class	VersionSort( object ):

	def	__init__( self ):
		self.items = []
		self.re = re.compile(
			r'((\d\d*)|(\D\D*))'
		)
		return

	def	add( self, s ):
		orig = s
		key = []
		while True:
			# print 'Offered "{0}"'.format( s )
			# if( len( s ) == 0 ):
				# break
			mo = self.re.search( s )
			if not mo:
				break
			token = mo.group()
			key.append( int( token ) if token.isdigit() else token )
			s = s[mo.end():]
			# print 'group(0)={0}'.format(
				# mo.group()
			# )
		self.items.append( [ key, orig ] )
		return

	def	sort( self ):
		for key,item in sorted( self.items ):
			# print '{0}\t{1}'.format( key, item )
			yield item
		return

class	LatestKernel( object ):

	def	__init__( self ):
		return

	def	uname( self ):
		return platform.release()

	def	kernels( self ):
		vs = VersionSort()
		uname = self.uname()
		for entry in os.listdir( '/lib/modules' ):
			vs.add( entry )
		for entry in vs.sort():
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
