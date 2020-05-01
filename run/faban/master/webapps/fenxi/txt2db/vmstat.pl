#!/bin/perl -w
# vmstat.pl -	Xanadu parser for "vmstat" or "vmstat -p"
#
# $Header: /cvs/fenxi/src/txt2db/vmstat.pl,v 1.1 2007/12/06 19:47:44 realneel Exp $

# Solaris 8 (and probably much earlier):
# procs     memory            page            disk          faults      cpu
# r b w   swap  free  re  mf pi po fr de sr s0 s1 s3 s3   in   sy   cs us sy id
# 0 0 0 87219288 64102840 1 1 3  0  0  0  0  0  0  0  0  170  122  152  1  0 99
#
# Solaris 9/10/Nevada:
# kthr      memory            page            disk          faults      cpu
# r b w   swap  free  re  mf pi po fr de sr s2 s4 s6 s7   in   sy   cs us sy id
# 0 0 1 10569320 6594720 30 1 208 6 5  0  6  0  0  0  0 1140   78   98  1  0 99
#
# Solaris 7 & later (vmstat -p):
#     memory           page          executable      anonymous      filesystem
#   swap  free  re  mf  fr  de  sr  epi  epo  epf  api  apo  apf  fpi  fpo  fpf
# 59236304 7673960 141 2001 27 0 5   11    2    2    3    7    7   39   17   18
# 48693752 2021936 208 3438 11 0 0    3    0    0    0    0    0    0   11   11

use FindBin; use lib "$FindBin::Bin"; use xanadu;

my $xanadu;

sub init_vmstat {
	my $desc = {
		'Time' => ['integer', 'Time'],
		'kthr_r' => ['integer', 'Kthreads runnable'],
		'kthr_b' => ['integer', 'Kthreads blocked'],
		'kthr_w' => ['integer', 'Kthreads swapped'],
		'vm_swap_KB' => ['integer', 'Available swap space (KBytes)'],
		'vm_free_KB' => ['integer', 'Size of the free list (KBytes)'],
		'page_re_ps' => ['integer', 'Page reclaims per second'],
		'page_mf_ps' => ['integer', 'Minor faults per second'],
		'page_KB_pi_ps' => ['integer', 'KBytes paged-in per second'],
		'page_KB_po_ps' => ['integer', 'KBytes paged-out per second'],
		'page_KB_fr_ps' => ['integer', 'KBytes freed per second'],
		'page_de_KB' => ['integer', 'Short-term deficit (KBytes)'],
		'page_scan_rate' => ['integer', 'Pages scanned per second'],
		'interrupts' => ['integer', 'Interrupts per second'],
		'syscalls' => ['integer', 'System calls per second'],
		'cswitches' => ['integer', 'Context switches per second'],
		'usr' => ['integer', 'User time %'],
		'sys' => ['integer', 'System time %'],
		'idle' => ['integer', 'Idle time %'],
	};
	my @column_names = qw(
		Time kthr_r kthr_b kthr_w vm_swap_KB vm_free_KB
		page_re_ps page_mf_ps page_KB_pi_ps page_KB_po_ps
		page_KB_fr_ps page_de_KB page_scan_rate
		interrupts syscalls cswitches
		usr sys idle
	);

	$xanadu = new xanadu $desc, @ARGV;
	my $tables = $xanadu->create_table({
		'table' => [ @column_names ],
	});
	$xanadu->create_view_col(
		'table', 'CPU', 'line', 'Time',
		qw( usr sys idle ),
	);
	$xanadu->create_view_col(
		'table', 'Faults', 'line', 'Time',
		qw( interrupts syscalls cswitches ),
	);
	$xanadu->create_view_col(
		'table', 'Kernel Threads', 'line', 'Time',
		qw( kthr_r kthr_b kthr_w ),
	);
	$xanadu->create_view_col(
		'table', 'Paging', 'line', 'Time',
		qw( page_re_ps page_mf_ps page_KB_pi_ps page_KB_po_ps
		      page_KB_fr_ps page_de_KB page_scan_rate ),
	);
	$xanadu->create_view_col(
		'table', 'Free Memory & Swap', 'line', 'Time',
		qw( vm_swap_KB vm_free_KB ),
	);
	# Summaries (with trend graphs)
	$xanadu->add_view(
		'table', 'CPU Utilization (USR)', 'Summary', 0,
	        'select avg("usr"), max("usr"), min("usr") '
		. 'from ' . $tables->[0] . '; select "usr" '
		. 'from ' . $tables->[0]
	);
	$xanadu->add_view(
		'table', 'CPU Utilization (SYS)', 'Summary', 0,
	        'select avg("sys"), max("sys"), min("sys") '
		. 'from ' . $tables->[0] . '; select "sys" '
		. 'from ' . $tables->[0]
	);
	$xanadu->add_view(
		'table', 'CPU Utilization (Total)', 'Summary', 0,
	        'select avg("usr"+"sys"), max("usr"+"sys"), min("usr"+"sys") '
		. 'from ' . $tables->[0] . '; select "usr" + "sys" '
		. 'from ' . $tables->[0]
	);

}

sub init_vmstat_p {
	my $desc = {
		'Time' => ['integer', 'Time'],
		'page_epi_ps' => ['integer', 'Executable page-ins per second'],
		'page_epo_ps' => ['integer', 'Executable page-outs per second'],
		'page_epf_ps' => ['integer', 'Executable page-frees per second'],
		'page_api_ps' => ['integer', 'Anonymous page-ins per second'],
		'page_apo_ps' => ['integer', 'Anonymous page-outs per second'],
		'page_apf_ps' => ['integer', 'Anonymous page-frees per second'],
		'page_fpi_ps' => ['integer', 'Filesystem page-ins per second'],
		'page_fpo_ps' => ['integer', 'Filesystem page-outs per second'],
		'page_fpf_ps' => ['integer', 'Filesystem page-frees per second'],
	};
	my @column_names = qw(
		Time
		page_epi_ps page_epo_ps page_epf_ps
		page_api_ps page_apo_ps page_apf_ps
		page_fpi_ps page_fpo_ps page_fpf_ps
	);

	$xanadu = new xanadu $desc, @ARGV;
	$xanadu->create_table({
		'table' => [ @column_names ],
	});
}

#========================================================================
#	MAIN
#========================================================================

my $time = 0;
my $interval = 10;
my @row;
my $rows = 0;
my $state = 'init';		# State machine
my $filename = $ARGV[0];	# Need to pass all of @ARGV to xanadu->new

open(STATS, "< $filename")
  or die("$0: can not open $filename for reading: $!\n");

while  (<STATS>) {
	goto $state;

    init:
	if (/vmstat\s(.*)(\d+)\s+(\d+)$/) {
		# GUDS or GUDS-style output
		$interval = $2;
		next;
	}
	if (/ must always be run at some INTERVAL. Using (\d+)/) {
		$interval = $1;
		next;
	}
	if (/\sdisk\s+faults\s+cpu$/) {
		# vmstat
		init_vmstat();
		$state = 'vmstat';
		next;
	}
	if (/^\s+memory\s+page\s+executable\s+anonymous\s+filesystem\s*$/) {
		# vmstat -p
		init_vmstat_p();
		$state = 'vmstat_p';
		next;
	}
	next;

    vmstat:
	next if (! /\s*\d+\s.*\s\d+$/);
	#
	# We only care about the 2nd and later samples, as the
	# first is average since boot
	#
	if ($rows++) {
		chomp;
		@row = split;
		# Skip the four disk columns - 12 through 15
		$xanadu->add_row('table', $time,
				 @row[0..11], @row[16..$#row]);
	}
	$time += $interval;
	next;

    vmstat_p:
	next if (! /\s*\d+\s.*\s\d+$/);
	# We have data
	if ($rows++) {
		chomp;
		@row = split;
		# What we want should be just the last 9 columns
		$xanadu->add_row('table', $time, @row[-9..-1]);
	}
	$time += $interval;
	next;
}
close(STATS);
