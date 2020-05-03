package xanadu;

use Carp;
use strict;

=head1 NAME

xanadu - Xanadu utility routines

=head1 DESCRIPTION

Common functions for parsing a tool output file.

=head1 SYNOPSIS

 use xanadu;
 my $xanadu=new xanadu {
	field => [SQLType,OptionalFieldDescription],
	...
 },@ARGV;

	This is the usual instantiation call sequence from any of the tool
	parsers. The SQLType must be a valid SQL/Oracle type such as
	'integer' or 'real' or 'varchar(50)' and will be passed as is to
	the next layer.  The OptionalFieldDescription as the name implies
	is an optional string entry that describes the field. If you use
	the create_view() interface listed below, it must be filled in and
	is not an optional field.  See the mpstat parser for an example of
	use.

 $xanadu->create_table({
	TableName1=>[qw(Table1Field1 Table1Field2 ... Table1FieldN1)],
	TableName2=>[qw(Table2Field1 Table2Field2 ... Table2FieldN2)],
	...
	TableNameN=>[qw(TableNField1 TableNField2 ... TableNFieldNM)],
 });

	This will create entries for TableName[1..N], with the named
	fields.  In the table described above, Table1 will have N1 fields,
	Table2 has N2 fields ... and TableN has NM fields.  See the mpstat
	parser for an example of use.

	This function returns a reference to an array of created
	TableNames[1..N]

 $xanadu->add_row(TableName, fields ...);

	Add a row of values to the specified table.  The number and order
	of fields must correspond to the order in which they were
	specified during the create.  See the mpstat parser for an example
	of use.

 $xanadu->create_view_col(TableName,GraphLabel,GraphType,XaxisField,
	ColumnsToGraph);

	This call is usually used to create a graph with time on the
	X-axis and all the selected columns from the table on the Y axis.
	TableName must be one of the TableName[1..N] from a create_table
	GraphLabel is a string which will be used to label the graph.
	GraphType can be a case insensitive versions of one of the following:
	{"Line", "MultiAxisLine", "Log", "Area", "Stacked Area", "Pie",
	"Scatter", "Bar", "Bar2", "Bar3D","Stacked Bar", "Stacked Bar 3D",
	"Histogram","LogBar"}.
	XaxisField must be a column from the table and will correspond to
	the X-axis of the graph.
	ColumnsToGraph is the list of columns from the table that need to
	be displayed in a single graph and must be a subset of the fields
	in TableName.

 $xanadu->create_view_row(TableName,GraphLabel,GraphType,XaxisField
	SeriesColumn,ColumnToGraph);

	This call is usually used to graph a selected field against
	another field over time. Eg: Utilization per disk over time.
	TableName must be one of the TableName[1..N] from a create_table
	GraphLabel is a string which will be used to label the graph
	GraphType can be a case insensitive versions of one of the following:
	{"Line", "MultiAxisLine", "Log", "Area", "Stacked Area", "Pie",
	"Scatter", "Bar", "Bar2", "Bar3D","Stacked Bar", "Stacked Bar 3D",
	"Histogram","LogBar"}.
	XaxisField is the column in the table corresponding to the X axis.
	SeriesColumn is the column in the table corresponding to the Series.
	ColumnToGraph is the field to graph against the series over time.

 $xanadu->add_view(TableName,GraphLabel,GraphType,Cookie,SQLstmt);

	This call is to allow direct SQL access to the lower layers.
	TableName must be one of the TableName[1..N] from a create_table
	GraphLabel is a string which will be used to label the graph
	GraphType can be a case insensitive versions of one of the following:
	{"Line", "MultiAxisLine", "Log", "Area", "Stacked Area", "Pie",
	"Scatter", "Bar", "Bar2", "Bar3D","Stacked Bar", "Stacked Bar 3D",
	"Histogram","LogBar"}.
	Cookie is passed as is to the lower layer.
	SQLstmt is passed as is to the lower layer.

 $xanadu->add_nv_pair(Description, Name, Value);

	Add a name value pair with a description to a table which can be
	queried later.

 $xanadu->create_view();

	See mpstat and prstat for usage and examples.  It is undocumented
	on purpose since you are encouraged to use the documented
	interfaces listed above.

=head1 FILES

This part of the documentation is implementation specific to the Derby-DB
based lower layer. Two files are used by the lower layers and end with
extensions .create and .view. The format of the .create file is a sequence
of SQL create statements. The format of the .view file is a sequence of
graph/table views each line containing fields delimited by | 
Here's a sample line from the .view file generated for mpstat:
mpstat|Minor faults per CPU|line|2|select "Time","CPU","minf" from mpstat_table
The general format is:
TableName|FieldName|GraphType|Dimensions|SQLstmt.
TableName is the data set from which the graph will be extracted.
GraphLabel is the label that should be applied to the graph.
GraphType can be a case insensitive versions of one of the following:
	{"Line", "MultiAxisLine", "Log", "Area", "Stacked Area", "Pie",
	"Scatter", "Bar", "Bar2", "Bar3D","Stacked Bar", "Stacked Bar 3D",
	"Histogram","LogBar"}.
Dimensions is used to differentiate between a XY graph (eg vmstat) and
	a XYY graph (eg: mpstat or iostat) -this is Neel's terminology -go ask him.
The SQLstmt must generate either XY or XYY data with the appropriate labels 
	which will be graphed by the lower layers. Dimensions higher than 2 cannot
	be graphed but can be displayed as HTML tables.

=head1 BUGS

The damn documentation is almost as large as the code. Learn some perl people!

=head1 AUTHOR

charles.suresh@sun.com

=cut

sub new {
	my ($this,$desc,$oid,$od)=@_;
	my $class = ref($this) || $this;
	my $self = {OID=>$oid,OD=>$od,DESC=>$desc};
	my $id=$oid; $id=~s|.*/||;
	my $xid=$id;
	$id=~s/\W/_/g;
	$self->{XID}=$xid; # original filename with path removed
	my ($fhc,$fhv);
	mkdir($od,0755) unless (-d $od);
	my $k="$od/$id.create"; open($fhc,">$k") or croak "can't open $k";
	$self->{CFH}=$fhc;
	$k="$od/$id.view"; open($fhv,">$k") or croak "can't open $k";
	$self->{VFH}=$fhv;
	$self->{ID}=$id;
	bless $self, $class;
	@ARGV=($oid);
	return $self;
}

sub create_table {
	my ($self,$tbl)=@_;
	my ($fh,$k,$v);

	my $fields=$self->{DESC};
	my $id=$self->{ID};
	my $od=$self->{OD};
	$fh=$self->{CFH};
	my $tblnames=[];
	my ($db);
	while (($k,$v)=each %$tbl) {
		$db="$id\_$k.data";
		my $tn;
		open($tn,">$od/$db") or croak "can't open table $k($od/$db)for writing";
		$self->{FH}->{$k}=[$tn, @$v+0];
		print $fh "create table $id\_$k (",
			join(',',map{join(" ","\"$_\"",$fields->{$_}->[0])} @$v),")\n";
		push @$tblnames, "$id\_$k";
	}
	return $tblnames;
}

sub add_nv_pair {
	my ($self,$d,$n,$v)=@_;
	my $fh=$self->{CFH};
	print $fh qq{insert into Metatable values('$d','$n','$v')\n};
}

sub create_view_common {
	my ($i,$self,$tn,$p,$t,@cols)=@_;
	my $id=$self->{ID};
	my $fh=$self->{VFH};
	$tn="$id\_$tn";
	print $fh "$self->{XID}|$p|$t|$i|select \"",join('","',@cols),"\" from $tn\n";
}

sub create_view_col {
	create_view_common(1,@_);
}

sub create_view_row {
	create_view_common(2,@_);
}

sub create_view {
	my ($self,$spec)=@_;
	my ($tn,$fh,$k,$v,$p,$q,$dims,$dim,$n,$x,$t,$l);
	my $fields=$self->{DESC};
	my $id=$self->{ID};
	$fh=$self->{VFH};
	while (($k,$v)=each %$spec) {
		$dims=[split(/,/,$k)];
		croak "Too many dimensions to $k\n" unless (($dim=@$dims)<4);
		$tn=shift(@$dims);
		$tn="$id\_$tn";
		if ($dim==1) {
			while (($p,$q)=each %$v) {
				$n=@$q;
				$x=shift(@$q);
				print $fh qq{$self->{XID}|$p|line|1|select "$x","},join('","',@$q),
					"\" from $tn\n";
			}
		} elsif ($dim>=2) {
			$t=join(" per ", map {$fields->{$_}->[1]} @$dims);
			$x=shift @$v;
			$l=join('","', @$dims);
			map {print $fh "$self->{XID}|",$fields->{$_}->[1],
				qq{ per $t|line|2|select "$x","$l","$_" from $tn\n}} @$v;
		}
	}
}

sub create_view_table {
    my ($self,$spec)=@_;
    my ($tn,$fh,$k,$v,$p,$q,$dims,$dim,$n,$x,$t,$l);
    my $fields=$self->{DESC};
    my $id=$self->{ID};
    $fh=$self->{VFH};
    while (($k,$v)=each %$spec) {
        $dims=[split(/,/,$k)];
        croak "Too many dimensions to $k\n" unless (($dim=@$dims)<4);
        $tn=shift(@$dims);
        $tn="$id\_$tn";
        while (($p,$q)=each %$v) {
            $n=@$q;
            $x=shift(@$q);
            print $fh qq{$self->{XID}|$p|table|0|select "$x","},join('","',@$q),
                "\" from $tn\n";
        }
    }
}

# Catchall to add a user specified view

sub add_view {
	my ($self,$tn,$p,$t,$y,$sql)=@_;
	my $id=$self->{ID};
	my $fh=$self->{VFH};
	$tn="$id\_$tn";
	print $fh "$self->{XID}|$p|$t|$y|$sql";
	if ($sql !~ /\sfrom\s/) {
		# We already have "from <table>" in the SQL
		print " from $tn";
	}
	print $fh "\n";
}

# add a row of elements to a table specified by tn.
# The number of elements passed is checked against the length specified
# during create_table. tn must be one of the keys passed to create_table.

sub add_row {
	my ($self,$tn,@r)=@_;
	my ($v,$c,$fh);
	croak "unknown table $tn" unless ($v=$self->{FH}->{$tn});
	$c=$v->[1];
	croak "number of columns does not match specification ". @r+0 ." != ".$c
		if ($c!=@r);
	$fh=$v->[0];
	print $fh join('|',@r), "\n"; 
}

sub DESTROY {
	my ($self)=@_;
	my $v;
	close $self->{CFH};
	close $self->{VFH};
	for $v (values %{$self->{FH}}) {
		close $v->[0];
	}
}

1;
