#!/bin/perl -w
use FindBin; use lib "$FindBin::Bin"; use xanadu;

my $desc={
	'Time'=>['integer','Time'],
	'Int'=>['varchar(10)','Interface'],
	'rKBps'=>['float','Receive KBytes/s'],
	'wKBps'=>['float','Transmit KBytes/s'],
	'rpps'=>['float','Receive packets per sec'],
	'wpps'=>['float','Transmit packets per sec'],
	'Util'=>['float','% Utilization'],
	'Sat'=>['float','Saturation'],
};
#	'Sat'=>['float','Saturation (defer+nocanput+norecvbuf+noxmtbuf)'],

my @column_names = qw( Time Int rKBps wKBps rpps wpps Util Sat );
my @column_names1 = qw( Time Util );

my $xanadu=new xanadu $desc,@ARGV;
$xanadu->create_table({
	'table' => [@column_names],
});
$xanadu->create_view({
	'table,Int' => [ grep(!/Int/, @column_names1) ]
});


my $header=0;
my $t = 0;
my @row;
my ($h,$m,$s);
my $rows = 0;
my $start;

while  (<>) {
	if (/^\s*Time/) {
		$header = [split] unless $header;
	} elsif (/(\d\d):(\d\d):(\d\d)\s/) {
		$t = ($1 * 60 + $2) * 60 + $3;
		if ($rows++ == 0) {
			# First sample from first interface
			$start = $t;
			next;
		}
		#
		# These will be equal for the first sample of 2nd & greater
		# interfaces
		#
		next if ($t eq $start);
		#
		# We now have data we want
		#
		chomp;
		@row = split;

		#time can overlap
		if ($t < $start) {
			$t = 24*60*60 + $t;
		}
		#
		# I think it wise to ditch the average figures, as they
		# can be calculated if necessary
		#
		$xanadu->add_row('table', $t - $start,
				 @row[1 .. 4], @row[7 .. $#row]);
	}
}
