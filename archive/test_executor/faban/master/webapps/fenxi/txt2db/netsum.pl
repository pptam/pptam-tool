#!/bin/perl -w
use FindBin; use lib "$FindBin::Bin"; use xanadu;

my $desc={
	'Time'=>['integer','Time'],
	'Name'=>['varchar(10)','NIC'],
	'KBi/s'=>['float','Receive KBps'],
	'KBo/s'=>['float','Transmit KBps'],
	'ipkts/s'=>['float','Receive packets/sec'],
	'opkts/s'=>['float','Transmit packets/sec'],
	'ierr'=>['float','Receive Errors'],
	'oerr'=>['float','Transmit Errors'],
	'Bi/pkt'=>['float','Receive bytes/pkt'],
	'Bo/pkt'=>['float','Transmit bytes/pkt'],
};
my $xanadu=new xanadu $desc,@ARGV;
$xanadu->create_table({
	'table' => [qw(Name KBi/s KBo/s ipkts/s opkts/s ierr oerr Bi/pkt Bo/pkt Time)],
});
$xanadu->create_view({
	'table,Name' => [qw(Time KBi/s KBo/s ipkts/s opkts/s ierr oerr Bi/pkt Bo/pkt)],
});

my $header=0;
my $t;
my @row;
my ($h,$m,$s);
while  (<>) {
	next if (/^\s*$/);
	if (/^\s*Name/) {
		$header=[split] unless $header;
	} else {
		chomp;
		@row=split;
		$_=pop @row;
		($h,$m,$s)=split(/:/);
		if ($s && $m && $h) {
			$t=($h*60+$m)*60+$s;
			$xanadu->add_row('table',@row,$t);
		}
	}
}
