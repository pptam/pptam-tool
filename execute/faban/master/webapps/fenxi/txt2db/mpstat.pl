#!/bin/perl -w

use FindBin; use lib "$FindBin::Bin"; use xanadu;

my $desc={
	'Time'=>['integer','Time'],
	'CPU'=>['varchar(8)','CPU'],
	'SET'=>['varchar(8)','Processor Set'],
	'minf'=>['integer','Minor faults'],
	'mjf'=>['integer','Major faults'],
	'xcal'=>['integer','Cross calls'],
	'intr'=>['integer','Interrupts'],
	'ithr'=>['integer','Interrupt Threads'],
	'csw'=>['integer','Context Switches'],
	'icsw'=>['integer','Involuntary Context Switches'],
	'migr'=>['integer','Thread Migrations'],
	'smtx'=>['integer','Mutex spins'],
	'srw'=>['integer','Reader-Writer spins'],
	'syscl'=>['integer','System calls'],
	'usr'=>['integer','User time'],
	'sys'=>['integer','System time'],
	'wt'=>['integer','Wait time'],
	'idl'=>['integer','Idle time'],
	'sze'=>['integer','Processor count'],
};
my $xanadu=new xanadu $desc,@ARGV;

my $interval=10;
my $i=0;
my $mp=0;
while  (<>) {
	next if (/^\s*$/);
	if (s/^\s*(SET|CPU)\s+//) {
		$set=$1;
		$i+=$interval;
		next if ($mp->{$set});
		$mp->{$set}=1;
		my @l=('Time',$set,split);
		$xanadu->create_table({
			'table' => [@l],
		});
		my $t=shift @l; shift @l; unshift @l,$t;
		$xanadu->create_view({
			"table,$set" => [@l],
		});
	} elsif (/Mpstat must always be run at some INTERVAL. Using (\d+)/) {
		$interval=$1;
	} else {
		chomp;
		$xanadu->add_row('table',$i,split);
	}
}
