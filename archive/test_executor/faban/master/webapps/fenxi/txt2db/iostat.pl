#!/usr/bin/perl -w

# Usage: iostat2xml.pl <input-iostat-file> <outputdir>

# This should be able to handle -xnz options

use FindBin; use lib "$FindBin::Bin"; use xanadu;

sub sanitizeTname
{
    my($fname) = @_;

    $fname =~ s/\./_/g;
    $fname =~ s/\-/_/g;
    $fname =~ s/\//_/g;
    $fname;
}

# This is the compression code
$totSamples = `fgrep extended $ARGV[0] | wc -l`;
$totPixels = 500;
$factor = int($totSamples / $totPixels);

use File::Basename;

my ($f, $dir) = @ARGV;
if ($f =~ /\.gz$/) {
	open(INFILE, "/usr/bin/gzcat $f|");
} elsif ($f =~ /\.bz2/) {

	open(INFILE, "/usr/bin/bzcat $f|");
} else {
	open(INFILE, $f);
}	

$tableNameOrig = basename($f);
$tableName = sanitizeTname(basename($f));

$dataFile = $dir . '/' . $tableName . ".data";
$createFile = $dir . '/' . $tableName . ".create";
$viewFile = $dir . '/' . $tableName . ".view";


open(DATFILE, ">$dataFile");

$samples = -1;
$firstTime = 1;
$interval = 10;

while (<INFILE>)
{
    if (/^Iostat/)
    {
	@fields = split;
	$interval = $fields[9];
    }
    elsif (/^\# iostat/)
    {
	@fields = split;
	$interval = $fields[3];
    }
    elsif (/extended/)
    {
        last;
    }
}

%colNames = ( 
	    "r/s" => "rps",
            "w/s" => "wps",
            "kr/s" => "kbrps",
            "kw/s" => "kbwps",
            "Mr/s" => "Mbrps",
            "Mw/s" => "Mbwps",
            "wait" => "wait",
            "actv" => "actv",
            "wsvc_t" => "waitt",
            "asvc_t" => "svct",
            "%w" => "waitp",
            "%b" =>  "busyp",
	    "s/w" => "softerr",
	    "h/w" => "harderr",
	    "trn" => "transerr",
	    "tot" => "toterr"
	    );

do {{
    if (/extended/)
    {
        $_ = <INFILE>;

	if ($firstTime)
	{
	    # Get the header
	    if (/r\/s/)
	    {
		@header = split;
		$firstTime = 0;
	    }
	}

	$samples++;
	$timeStamp+= $interval;
	next;
    } 

    # Skip the first sample
    next if $samples == 0;

    # For compression, only record every $factor sample
    next if $factor > 1 && ($samples -1) % $factor != 0;

    @fields = split;

    # Ignore invalid lines in input
    next if $#fields < 10;

    # Check to see if we know this disk already
    $diskName = sanitizeTname($fields[$#fields]);

    # Record the data

    print DATFILE "$timeStamp|$diskName";

    for ($i = 0; $i < $#fields; $i++)
    {
	# We are not going to record the wait stats
	next if ($i == 4 || $i == 6 || $i == 8);

	# $fields[$#fields] is device's name.
	print DATFILE "|$fields[$i]";
    }
    print DATFILE "\n";

}} while (<INFILE>);

close(DATFILE);
close(INFILE);


open(CREATEFILE, ">$createFile");

print CREATEFILE "create table $tableName (time integer, device varchar(50)";

foreach $label (@header)
{
    next if ($label eq "device" || $colNames{$label} =~ /wait/);

    print CREATEFILE ", $colNames{$label} real";
}
print CREATEFILE ")\n";
close(CREATEFILE);


#Each metric is a stat group
%metrics = ( 
	    "r/s" => "Reads per second",
            "w/s" => "Writes per second",
            "kr/s" => "Kilobytes read per second",
            "kw/s" => "Kilobytes written per second",
            "Mr/s" => "Megabytes read per second",
            "Mw/s" => "Megabytes written per second",
            "wait" => "Transactions waiting for service",
            "actv" => "Transactions actively being serviced",
            "wsvc_t" => "Average wait time (ms)",
            "asvc_t" => "Average service time (ms)",
            "%w" => "Wait Time Percentage",
            "%b" =>  "Disk Busy Percentage",
	    "s/w" => "Soft Errors",
	    "h/w" => "Hard Errors",
	    "trn" => "Transport Errors",
	    "tot" => "Total Errors"
	    );
open(VIEWFILE, ">$viewFile");

print VIEWFILE "$tableNameOrig|Overall System Activity (per second)|table|0|select avg(tot_rps) + avg(tot_wps) as total_ios,avg(tot_rps) as reads,avg(tot_wps) as writes, avg(tot_mbrps) + avg(tot_mbwps) as total_MB, avg(tot_mbrps) as MB_read,avg(tot_mbwps) as MB_written from (select sum(rps) as tot_rps, sum(wps) as tot_wps, sum(kbrps)/1000 as tot_mbrps,sum(kbwps)/1000 as tot_mbwps from $tableName group by time) as iostat_total|\n";

print VIEWFILE "$tableNameOrig|Top 5 Hot Disks (Avg)|table|0|select device, avg(svct) as avg_svc_time from $tableName group by device order by avg_svc_time desc limit 5|\n";
print VIEWFILE "$tableNameOrig|Top 5 Hot Disks (Peak)|table|0|select device, max(svct) as max_svc_time from $tableName group by device order by max_svc_time desc limit 5|\n";

foreach $label (@header)
{
    # Skipping all the wait stats
    next if ($label eq "device" || $colNames{$label} =~ /wait/);

     print VIEWFILE "$tableNameOrig|$metrics{$label}|line|2";
     print VIEWFILE "|select time, device, $colNames{$label} from $tableName|\n";
}

print VIEWFILE "$tableNameOrig|Active Disk Summary (per second)|table|0|select device, avg(rps) as reads, avg(wps) as writes, avg(kbrps) as KB_read, avg(kbwps) as KB_written, avg(actv) as actv_trans, avg(svct) as svc_time, avg(busyp) as busy_percent from $tableName group by device having avg(svct) >= 1 order by avg(svct) desc|\n";
print VIEWFILE "$tableNameOrig|Total Reads (per second)|summary|0|select avg(tot_rps), max(tot_rps), min(tot_rps) from (select sum(rps) as tot_rps from $tableName group by time) as a;select sum(rps) from $tableName group by time|\n";
print VIEWFILE "$tableNameOrig|Total Writes (per second)|summary|0|select avg(tot_wps), max(tot_wps), min(tot_wps) from (select sum(wps) as tot_wps from $tableName group by time) as a;select sum(wps) from $tableName group by time|\n";
print VIEWFILE "$tableNameOrig|Total KB Read (per second)|summary|0|select avg(tot_kbrps), max(tot_kbrps), min(tot_kbrps) from (select sum(kbrps) as tot_kbrps from $tableName group by time) as a;select sum(kbrps) from $tableName group by time|\n";
print VIEWFILE "$tableNameOrig|Total KB Write (per second)|summary|0|select avg(tot_kbwps), max(tot_kbwps), min(tot_kbwps) from (select sum(kbwps) as tot_kbwps from $tableName group by time) as a;select sum(kbwps) from $tableName group by time|\n";
print VIEWFILE "$tableNameOrig|Average Service Time|summary|0|select avg(svct), max(svct), min(svct) from $tableName;select avg(svct) from $tableName group by time|\n";
print VIEWFILE "$tableNameOrig|Average Disks used|summary|0|select avg(diskb), max(diskb), min(diskb) from (select count(device) as diskb from $tableName group by time) as a ;select count(device) from $tableName group by time|\n";

close(VIEWFILE);

__END__
