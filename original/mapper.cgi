#!/usr/bin/perl
################################################################################
#                                                                              #
#  (c) Michael R. Davis 2000, 2001, 2024                                       #
#                                                                              #
#  This program was written by Michael R. Davis
#                                                                              #
#  Parameters: [default]          type                                         #
#    data      [copyright]        colon separated vals x0,y0[,x1,y1] floats    #
#    datatype  [line]             varchar (line,vert)                          #
#    width     [640]              int                                          #
#    height    [480]              int                                          #
#    bgcolor   [green=>CACE7F]    char(6)                                      #
#    fgcolor   [black=>000000]    char(6)                                      #
#    border0   [gray=>888888]     char(6)                                      #
#    border1   [dkgray=>6C6C6C]   char(6)                                      #
#    border2   [gray=>888888]     char(6)                                      #
#    size      [2]                int                  Line draw thickness     #
#    scale     [none=>0]          int                  standard scale types    #
#    unit      []                 vchar                display in scale        #
#    scaletext [black=>000000]    char(6)                                      #
#    scaleline [black=>000000]    char(6)                                      #
#                                                                              #
#  Versions:                                                                   #
#    1.3 December 13, 2001  Added datatype "vert" so that I could cut down on  #
#                           half of the data that I have to pass to the mapper.#
#                                                                              #
#    1.2 January 7, 2001    Added scale not quite prefected but it works       #
#                                                                              #
#    1.1 January 4, 2001    Security review and fixes                          #
#                           Removed unused colors                              #
#                           Added this comment section                         #
#                           Custom border colors feature                       #
#                                                                              #
#    1.0 December 25, 2000  Original version ready for Christmas               #
#                                                                              #
################################################################################
use strict;
use warnings;
use GD;
use CGI qw(:standard :html3);
my $query = CGI->new;

my $test=$query->param('test') || undef;
print "Content-type: text/plain\n\n" if $test;
        
# create a new image
my $width  = abs(int($query->param('width')  || 640)); #+int here for security
my $height = abs(int($query->param('height') || 480)); #+int here for security
my $im     = GD::Image->new($width, $height);

# allocate some colors
my %color=(
  scaletext=>$im->colorAllocate(hexcolor($query->param('scaletext') || '000000')),
  scaleline=>$im->colorAllocate(hexcolor($query->param('scaleline') || '000000')),
  border0  =>$im->colorAllocate(hexcolor($query->param('border0')   || '888888')),
  border1  =>$im->colorAllocate(hexcolor($query->param('border1')   || '6C6C6C')),
  border2  =>$im->colorAllocate(hexcolor($query->param('border2')   || '888888')),
  bgcolor  =>$im->colorAllocate(hexcolor($query->param('bgcolor')   || 'CACE7F')),
);

$im->interlaced(undef);

my $border;
# Put a frame around the picture
$border=0;
$im->rectangle($border, $border, $width-1-$border, $height-1-$border, $color{'border0'});

$border=1;
$im->rectangle($border, $border, $width-1-$border, $height-1-$border, $color{'border1'});

$border=2;
$im->rectangle($border, $border, $width-1-$border, $height-1-$border, $color{'border2'});
$im->fill(50, 50, $color{'bgcolor'});

$border=10;

#draw lines

# Create brush
my $size=int(abs($query->param('size'))) || 2;
my $brush = new GD::Image($size,$size);
my $color = $brush->colorAllocate(hexcolor($query->param('fgcolor') || '000000'));
$brush->filledRectangle(0, 0, $size-1, $size-1, $color);

# Set the brush
$im->setBrush($brush);

my $data=$query->param('data');
my @data=();
if ($data) {
  @data=split(":", $data);
  #I added this sprintf here for security purposes. I didn't really want to
  #sacrifice the performance but I guess it's a must in today's world.
  @data=map {[map {sprintf("%g", $_)} split(",", $_)]} @data;
  my $datatype=$query->param('datatype') || 'line';
  if ($datatype=~m/^vert$/i) {
    foreach (0..$#data-1) {
      $data[$_]=[$data[$_][0], $data[$_][1], $data[$_+1][0], $data[$_+1][1]];
      print "$data[$_]=[$data[$_][0], $data[$_][1], $data[$_+1][0], $data[$_+1][1]];\n" if $test;
    }
    pop @data; #get rid of last data record
  }
} else {
    @data=(
          #copy => o
          [-1,1,-1,4],
          [-1,4,0,5],
          [0,5,3,5],
          [3,5,4,4],
          [4,4,4,1],
          [4,1,3,0],
          [3,0,0,0],
          [0,0,-1,1],

          #copy => c
          [3,2,2,1],
          [2,1,1,1],
          [1,1,0,2],
          [0,2,0,3],
          [0,3,1,4],
          [1,4,2,4],
          [2,4,3,3],
          
          #M
          [7,0,7,5],
          [7,5,9,0],
          [9,0,11,5],
          [11,5,11,0],
          
          #i => l
          [13,0,13,3],
          
          #i => .
          [12.75,3.75,12.75,4.25],
          [12.75,4.25,13.25,4.25],
          [13.25,4.25,13.25,3.75],
          [13.25,3.75,12.75,3.75],
          
          #c
          [18,1,17,0],
          [17,0,16,0],
          [16,0,15,1],
          [15,1,15,2],
          [15,2,16,3],
          [16,3,17,3],
          [17,3,18,2],
          
          #h => l
          [20,0,20,5],
          
          #h => n
          [20,2,21,3],
          [21,3,23,3],
          [23,3,23,2],
          [23,2,23,0],
          
          #a => r
          [25,2,26,3],
          [26,3,27,3],
          [27,3,28,2],
          [28,2,28,0],
          
          #a => c
          [28,2,26,2],
          [26,2,25,1],
          [25,1,26,0],
          [26,0,27,0],
          [27,0,28,1],
          
          #e
          [30,2,33,2],
          [33,2,32,3],
          [32,3,31,3],
          [31,3,30,2],
          [30,2,30,1],
          [30,1,31,0],
          [31,0,32,0],
          [32,0,33,1],

          #l
          [35,0,35,5],
          
          #R => P
          [38,0,38,5],
          [38,5,41,5],
          [41,5,42,4],
          [42,4,42,3],
          [42,3,41,2],
          [41,2,38,2],
          
          #R => \
          [40,2,42,0],
          
          #.
          [43,0,43,0.5],
          [43,0.5,43.5,0.5],
          [43.5,0.5,43.5,0],
          [43.5,0,43,0],

          #D
          [47,0,47,5],
          [47,5,50,5],
          [50,5,51,4],
          [51,4,51,1],
          [51,1,50,0],
          [50,0,47,0],
          
          #a => r
          [53,2,54,3],
          [54,3,55,3],
          [55,3,56,2],
          [56,2,56,0],
          
          #a => c
          [56,2,54,2],
          [54,2,53,1],
          [53,1,54,0],
          [54,0,55,0],
          [55,0,56,1],
          
          #v
          [58,3,59.5,0],
          [59.5,0,61,3],
          
          #i => l
          [63,0,63,3],

          #i = > .
          [62.75,3.75,62.75,4.25],
          [62.75,4.25,63.25,4.25],
          [63.25,4.25,63.25,3.75],
          [63.25,3.75,62.75,3.75],
          
          #s
          [65,1,66,0],
          [66,0,67,0],
          [67,0,68,1],
          [68,1,65,2],
          [65,2,66,3],
          [66,3,67,3],
          [67,3,68,2],
          
          #2
          [71,3,72,4],
          [72,4,73,4],
          [73,4,74,3],
          [74,3,74,2],
          [74,2,71,0],
          [71,0,74,0],
          
          #03
          [76,1,76,3],
          [76,3,77,4],
          [77,4,78,4],
          [78,4,79,3],
          [79,3,79,1],
          [79,1,78,0],
          [78,0,77,0],
          [77,0,76,1],

          #0
          [81,1,81,3],
          [81,3,82,4],
          [82,4,83,4],
          [83,4,84,3],
          [84,3,84,1],
          [84,1,83,0],
          [83,0,82,0],
          [82,0,81,1],

          #0
          [86,1,86,3],
          [86,3,87,4],
          [87,4,88,4],
          [88,4,89,3],
          [89,3,89,1],
          [89,1,88,0],
          [88,0,87,0],
          [87,0,86,1],
        );
        push @data, map {[$_->[0]+41, $_->[1]+10, $_->[2]+41, $_->[3]+10]} (
          #D
          [-1,3,3,5],
          [3,5,4,5],
          [4,5,5,3],
          [5,3,4,1],
          [4,1,3,0],
          [3,0,-1,-2],
          
          #N
          [0,-0.5,0,3],
          [0,3,2,0],
          [2,0,2,3.5],
        );
}
my ($Xmin, $Xmax, $Ymin, $Ymax);
($Xmin, $Xmax)=(sort({$a <=> $b} map({$_->[0], $_->[2]} @data)))[0,-1];
($Ymin, $Ymax)=(sort({$a <=> $b} map({$_->[1], $_->[3]} @data)))[0,-1];
print "Xmax-min $Xmax $Xmin\n" if $test;
print "Ymax-min $Ymax $Ymin\n" if $test;

my $scaleheight=0;
if ($query->param('scale')) {
  $scaleheight=8;
}

my $Xscale;
if ($Xmax-$Xmin == 0) {
  $Xscale=1E9;
} else {
  $Xscale=($width-$border*2)/($Xmax-$Xmin);
}
print "Xscale $Xscale\n" if $test;

my $Yscale;
if ($Ymax-$Ymin == 0) {
  $Yscale=1E9;
} else {
  $Yscale=($height-$border*2-$scaleheight)/($Ymax-$Ymin);
}
print "Yscale $Yscale\n" if $test;

my $scale;
$scale=$Xscale; $scale=$Yscale if ($Yscale < $Xscale);
my $Xoffset=$width/2-$border-($Xmax+$Xmin)/2*$scale;
my $Yoffset=$height/2-$border+$scaleheight-($Ymax+$Ymin)/2*$scale;

print "scale $scale\n" if $test;
print "Xoffset $Xoffset\n" if $test;
print "Yoffset $Yoffset\n" if $test;

foreach (@data) {
  $im->line($border+$Xoffset+($_->[0]*$scale),
            $height-1-$border-$Yoffset-($_->[1]*$scale),
            $border+$Xoffset+($_->[2]*$scale),
            $height-1-$border-$Yoffset-($_->[3]*$scale),
            gdBrushed);
  print join(":",
            "$border+$Xoffset+($_->[0]*$scale)",
            "$height-1-$border-$Yoffset-($_->[1]*$scale)",
            "$border+$Xoffset+($_->[2]*$scale)",
            "$height-1-$border-$Yoffset-($_->[3]*$scale)"),
            "\n" if $test; 
  print join(":",
            $border+$Xoffset+($_->[0]*$scale),
            $height-1-$border-$Yoffset-($_->[1]*$scale),
            $border+$Xoffset+($_->[2]*$scale),
            $height-1-$border-$Yoffset-($_->[3]*$scale)),
            "\n\n" if $test; 
}

my $ticklen=$scaleheight-2;
my $Ylocation=$border+$scaleheight/2;
my $scaletext=($width-$border*2)/$scale;
my @scaleticks=();
if ($scaletext >= 2) {
  my $scalemagnitude=10**int(log($scaletext/2)/log(10));
  print "scalemagnitude: $scalemagnitude\n" if $test;
  my $scaleticks=int($scaletext/$scalemagnitude);
  print "scaleticks: $scaleticks\n" if $test;
  $scaletext=$scaleticks*$scalemagnitude;
  print "scaletext: $scaletext\n" if $test;
  if ($scaleticks > 1) {
    @scaleticks=(1..$scaleticks-1);
    @scaleticks=map {$_*$scalemagnitude} @scaleticks;
    print '@scaleticks: '. join(":", @scaleticks). "\n" if $test;
  }
}
print '@scaleticks: '. join(":", @scaleticks). "\n" if $test;
my $Xscaleend=$scaletext*$scale+$border;

$scaletext.=" ". $query->param('unit') if $query->param('unit');
if ($query->param('scale')) {
  $im->line($border,
            $height-$Ylocation,
            $Xscaleend,
            $height-$Ylocation,
            gdBrushed);
  $im->line($border,
            $height-$Ylocation-$ticklen/2,
            $border,
            $height-$Ylocation+$ticklen/2,
            gdBrushed);
  $im->line($Xscaleend,
            $height-$Ylocation-$ticklen/2,
            $Xscaleend,
            $height-$Ylocation+$ticklen/2,
            gdBrushed);
  foreach (@scaleticks) {
    print "$_\n" if $test;
    $im->line($_*$scale+$border,
              $height-$Ylocation,
              $_*$scale+$border,
              $height-$Ylocation+$ticklen/2,
              gdBrushed);
  }
  $im->string(gdLargeFont,
            $border+2,
            $height-$Ylocation-$ticklen/2-12,
            $scaletext,
            $color{'scaletext'});
}

# Convert the image to GIF and print it on standard output
print "Content-type: image/gif\n\n" if not $test;
print $im->gif if not $test;

sub hexcolor {
  #Tested for security purposes
  #If passed bad color codes this returns valid colors
  $_=shift;
  m/(..)(..)(..)/;
  return (hex($1), hex($2), hex($3));
}
