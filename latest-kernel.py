#!/usr/bin/env python
# vim: noet sw=4 ts=4

import	os
import	platform
import	re
import	sys
import	subprocess
import	argparse
import	natsort

Version = '2.0.5'

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
		for key,item in natsort.humansorted(
			self.items,
			key = lambda s : s
		):
			# print '{0}\t{1}'.format( key, item )
			yield item
		return

class	LatestKernel( object ):

	def	__init__( self ):
		self.libdir = '/lib/modules'
		self.uname_r = platform.release()
		return

	def	purge_orphan( self, version ):
		cmd = [
			'/bin/rm',
			'-r',
			'-f',
			os.path.join(
				self.libdir,
				version
			)
		]
		if self.opts.kidding:
			prompt = '$' if os.geteuid() else '#'
			print(
				'{0} '.format( prompt ) +
				( ' '.join( cmd ) )
			)
		else:
			try:
				_, _ = subprocess.check_output(
					cmd,
					stderr = subprocess.STDOUT,
					text   = True
				)
			except Exception as e:
				_ = None
		return

	def	rpm_name_for( self, version ):
		cmd = [
			'/bin/rpm',
			'-q',
			'-f',
			'--qf=%-40{NEVRA}  %{INSTALLTIME:day}',
			os.path.join(
				self.libdir,
				version
			)
		]
		# print >>sys.stderr, ' '.join( cmd )
		known = False
		try:
			output = subprocess.check_output(
				cmd,
				stderr = subprocess.STDOUT,
				text   = True,
			)
			known = True
		except Exception as e:
			output = None
		return known, output

	def	kernels( self ):
		vs = VersionSort()
		for version in os.listdir( self.libdir ):
			vs.add( version )
		for version in vs.sort():
			known, rpm = self.rpm_name_for( version )
			info = dict(
				current = (version == self.uname_r),
				orphan  = not known,
				rpm     = rpm if known else '*** {0} ***'.format( 'ORPHAN' ),
				version = version,
				where   = os.path.join(
					self.libdir,
					version
				)
			)
			yield info
		return

	def	main( self ):
		prog = os.path.splitext(
			os.path.basename(
					sys.argv[ 0 ]
			)
		)[ 0 ]
		if prog == '__init__':
			prog = 'latest-kernel'
		p = argparse.ArgumentParser(
			prog = prog,
			description = '''Show available kernels and their RPM name.
			Optionally delete orphan directory trees in "/lib/modules"
			for neatness.'''
		)
		p.add_argument(
			'-a',
			'--all',
			dest   = 'all',
			action = 'store_true',
			help   = 'also show RPM info',
		)
		p.add_argument(
			'-d',
			'--delete-orphans',
			dest   = 'clean_orphans',
			action = 'store_true',
			help   = 'delete orphan /lib/modules trees.',
		)
		p.add_argument(
			'-n',
			'--just-kidding',
			dest   = 'kidding',
			action = 'store_true',
			help   = 'show (not do) how to delete orphans',
		)
		p.add_argument(
			'--version',
			action  = 'version',
			version = Version,
			help    = 'program version',
		)
		self.opts = p.parse_args()
		if self.opts.clean_orphans and os.geteuid() != 0:
			print(
				'Must be root to purge orphans.'
			)
			return 1
		#
		width = max(
			map(
				lambda info : len( info['version'] ),
				self.kernels()
			)
		)
		thumb = '-->'
		fmt = '{{0:<{0:d}}} {{1:{1:d}}}  {{2}}'.format(
			len( thumb ),
			width,
		)
		#
		for info in self.kernels():
			print(
				fmt.format(
					thumb if info['current'] else '',
					info[ 'version' ],
					info[ 'rpm' ] if self.opts.all else '',
				)
			)
			if info[ 'orphan' ] and self.opts.clean_orphans:
				self.purge_orphan( info[ 'where' ] )
		return 0

if __name__ == '__main__':
	exit( LatestKernel().main() )
