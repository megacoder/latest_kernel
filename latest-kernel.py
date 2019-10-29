#!/usr/bin/env python2
#!/usr/bin/python2
# vim: noet sw=4 ts=4

import	os
import	platform
import	re
import	sys
import	subprocess

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

	def	rpm_name_for( self, version ):
		cmd = [
			'/bin/rpm',
			'-q',
			'-f',
			'--qf=%{NAME}-%{EVR}.%{ARCH}.rpm',
			'/lib/modules/{0}'.format( version )
		]
		# print >>sys.stderr, ' '.join( cmd )
		try:
			output = subprocess.check_output(
				cmd,
				stderr = subprocess.STDOUT
			)
			valid = True
		except Exception, e:
			output = 'UNKNOWN'
			valid = False
		return valid, output

	def	kernels( self ):
		vs = VersionSort()
		uname = self.uname()
		for entry in os.listdir( '/lib/modules' ):
			vs.add( entry )
		for entry in vs.sort():
			valid, rpm = self.rpm_name_for( entry )
			yield(
				entry == uname,
				entry,
				rpm if valid else '*** {0} ***'.format( rpm )
			)
		return

if __name__ == '__main__':
	lk = LatestKernel()
	uname = lk.uname()
	for thumb,entry,rpm in lk.kernels():
		print '{0:<3} {1:<31} {2}'.format(
			'-->' if thumb else '',
			entry,
			rpm
		)
	exit( 0 )
