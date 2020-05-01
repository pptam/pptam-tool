#!/bin/perl -w

=head1 NAME

prstat.pl - GUDS prstat parser

=head1 SYNOPSIS

prstat.pl input_file output_directory

=head1 DESCRIPTION

GUDS prstat output parser

=head1 EXAMPLES

prstat 10 5 > /tmp/prstat ; prstat.pl /tmp/prstat /tmp

=head1 AUTHOR

charles.suresh@sun.com

=cut

use strict;
use Pod::Text;
use Getopt::Std;
#use HTTP::Date;

use FindBin; use lib "$FindBin::Bin"; use xanadu;

sub usage {
	pod2text($0);
	die "usage: $0";
}

usage() unless (getopts(''));

sub canontime {
	my ($rn)=@_;
	my ($rh,$rm,$rs)=split(/:/,$rn);
	$rn=($rh*60+$rm)*60+$rs;
}

my $suffix={K=>10**3,M=>10**6,G=>10**9};
sub canonsize {
	my ($s)=@_;
	my $mu=chop $s;
	my $mult;
	if ($mult=$suffix->{$mu}) {
		$s*=$mult;
	} else {
		$s.=$mu;
	}
}
my ($v,$i,$tbl,$k,$nproc,$nlwp,$r,$r5,$r15);

$i=-1;

my ($pidhead,$cmdhead);

my $desc={
	'TIME'=>['integer','Time'], 
	'NPROCS'=>['integer','# of Processes'], 
	'NLWP'=>['integer','# of LWPs'], 
	'RQ'=>['real','Run Queue Length (1 minute)'],
	'RQ5MIN'=>['real','Run Queue Length (5 minutes)'],
	'RQ15MIN'=>['real','Run Queue Length (15 minutes)'],
	'UCP'=>['varchar(50)','Process id'],
	'SIZE'=>['real','Memory Size'],
	'RSS'=>['real','Resident Set Size'],
	'ONCPU'=>['integer','Running on CPU'],
	'PRI'=>['integer','Priority'],
	'NICE'=>['integer','Nice Value'],
	'TS'=>['integer','Aggregate CPU time'],
	'CPUTIME'=>['real','Percent CPU used'],
	'USER'=>['varchar(50)','User'],
	'MEM'=>['real','Memory Utilization'],
};

my $xanadu=new xanadu $desc,@ARGV;

$xanadu->create_table({
	'RUNQ' => [qw(TIME NPROCS NLWP RQ RQ5MIN RQ15MIN)],
});

$xanadu->create_view({
	'RUNQ' => {
		'Number of Processes and LWPs' => [qw(TIME NPROCS NLWP)],
		'Run Queue Lengths' => [qw(TIME RQ RQ5MIN RQ15MIN)],
	},
	#'PID,UCP'=>[qw(TIME SIZE RSS ONCPU PRI NICE TS CPUTIME NLWP)],
	#'USER,USER,NPROCS'=>[qw(TIME SIZE RSS MEM)],
});

#$xanadu->create_view_col('RUNQ','Number of Processes and LWPs','line',
#	'TIME','NPROCS','NLWP');
#$xanadu->create_view_row('USER','Number of Processes per user','line',
#	'TIME','USER','NPROCS');
#$xanadu->add_view($id,'USER','Number of Processes per user','table',
#	0,'..sql..');

my $interval=0;
my $mode='';
while  (<>) {
	if (/^\s*PID/) {
		unless ($pidhead) {
			$pidhead=[split];
			$xanadu->create_table({
				'PID' => [qw(UCP TIME SIZE RSS ONCPU PRI NICE TS CPUTIME NLWP)],
			});
		};
		$mode='PID';
		$i++;
	} elsif (/^\s*NPROC/) {
		unless ($cmdhead) {
			$cmdhead=[split];
			$xanadu->create_table({
				'USER' => [qw(USER TIME NPROCS SIZE RSS MEM TS CPUTIME)],
			});
			$xanadu->create_view({
				'USER,USER'=>[qw(TIME NPROCS SIZE RSS MEM TS CPUTIME)],
			});
		};
		$mode='USER';
	} elsif (/^\s*Total/) {
		s/,//g;
		($k,$nproc,$k,$nlwp,$k,$k,$k,$r,$r5,$r15)=split;
		$xanadu->add_row('RUNQ',$i,$nproc,$nlwp,$r,$r5,$r15);
	} elsif (/^$/) {
		next;
	} elsif (s/\s+\-\s+started//) {
		#$starttick=str2time($_);
		next;
	} elsif (s/\s+\-\s+ended//) {
		#$endtick=str2time($_);
		#$interval=int(($endtick-$starttick)/$i) if ($interval==0);
		next;
	} else {
		if ($mode eq 'PID') {
			my ($p,$u,$sz,$rss,$st,$pri,$nice,$ts,$cpu,$pl)=split;
			$sz=canonsize($sz);
			$rss=canonsize($rss);
			$st=~s/cpu//;
			$st=-2 if ($st eq 'sleep');
			$st=-1 if ($st eq 'run');
			#$st=0 if ($st eq 'sleep');
			$nice=0 if ($nice eq '-');
			$ts=canontime($ts);
			die "unexpected format" unless (chop($cpu) eq '%');
			my ($pn,$np)=split(/\//,$pl);
			$xanadu->add_row('PID',
				"$u.$pn.$p",$i,$sz,$rss,$st,$pri,$nice,$ts,$cpu,$np);
		} elsif ($mode eq 'USER') {
			my ($c,$p,$sz,$rss,$mem,$ts,$cpu)=split;
			$sz=canonsize($sz);
			$rss=canonsize($rss);
			die "unexpected memory format $mem" unless (chop($mem) eq '%');
			$ts=canontime($ts);
			die "unexpected cpu format" unless (chop($cpu) eq '%');
			$xanadu->add_row('USER',$p,$i,$c,$sz,$rss,$mem,$ts,$cpu);
		}
	}
}
exit 0;
