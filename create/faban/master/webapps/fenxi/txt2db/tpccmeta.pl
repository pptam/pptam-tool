#!/bin/perl

=head1 NAME

tpccmeta.pl - GUDS TPCC report parser

=head1 SYNOPSIS

tpccmeta.pl input_file output_directory

=head1 DESCRIPTION

GUDS TPCC report output parser

=head1 AUTHOR

murlee@sun.com

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

# Function to trim leading and trailing spaces.
sub trim($)
{
    my $string = shift;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    return $string;
}

usage() unless (getopts(''));

my ($k,$hst,$prm,$val,$sysconf,$cpucnt,$tpcparam,$tpcval);

my $desc={
	'ETC_PARAM'=>['varchar(32)','Parameter'],
	'ETC_VALUE'=>['varchar(256)','Value'],
	'TPC_PARAM'=>['varchar(32)','TPCC Parameter'],
	'TPC_VALUE'=>['varchar(256)','TPCC Value'],
	'SYS_PARAM'=>['varchar(32)','Machine Parameter'],
	'SYS_VALUE'=>['varchar(256)','Machine Value'],
};

my $xanadu=new xanadu $desc,@ARGV;

$xanadu->create_table({
	'SYSTEM' => [qw(SYS_PARAM SYS_VALUE)],
});

$xanadu->create_table({
	'TPCC' => [qw(TPC_PARAM TPC_VALUE)],
});

$xanadu->create_table({
	'ETC_SYSTEM' => [qw(ETC_PARAM ETC_VALUE)],
});

$xanadu->create_view_table({
	'SYSTEM' => {
		'Machine Config' => [qw(SYS_PARAM SYS_VALUE)],
	},
});

$xanadu->create_view_table({
    'TPCC' => {
        'TPCSO Config' => [qw(TPC_PARAM TPC_VALUE)],
    },
});

$xanadu->create_view_table({
	'ETC_SYSTEM' => {
		'OS Config' => [qw(ETC_PARAM ETC_VALUE)],
    },
});


#$xanadu->create_view({
#    'ETC_SYSTEM' => {
#        'OS Config' => [qw(ETC_PARAM ETC_VALUE)],
#    },
#});

while (<>) {
 	#print $_;
	if (/^\s*MASTER_MACHINE/) {
		($k,$hst)=split(/:/);
		$xanadu->add_row('SYSTEM',"Hostname",trim($hst));
	}
	elsif (/^\s*Contents of \/etc\/system/) {
		until (/^\s*set|^-+/) {
			$_=<>;
		}
		until (/^\s*-+$/) {
			while (/^\s*set/) {
				s/set//;
#				print "ETC_SYSTEM:", $_;
				($prm,$val)=split(/=/);
				$xanadu->add_row('ETC_SYSTEM',trim($prm),trim($val));
				$_=<>;
			}
			if (/^\s*$/) {
				$_=<>;
			}
		}
	}
	elsif (/^\s*System Configuration/) {
		($k,$sysconf)=split(/:/);
		$xanadu->add_row('SYSTEM',"Platform",trim($sysconf));
	}
	elsif (/^\s*cpu_count/) {
		($k,,$k,$cpucnt)=split;
		$xanadu->add_row('SYSTEM',"Num CPUs",trim($cpucnt));
	}
	elsif (/TPCSO PARAMETERS ARE/) {
		until (/^\s*$/) {
			$_=<>;
		}
		$_=<>;
		until (/^\s$/) {
			($tpcparam,$tpcval)=split(/:/);
			$tpcparam=~s/is$//;
			$xanadu->add_row('TPCC',trim($tpcparam),trim($tpcval));
			$_=<>;
		}	
	}
}
exit 0;
