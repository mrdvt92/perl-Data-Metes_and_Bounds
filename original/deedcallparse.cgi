#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard :html3);
use CGI::Carp;
my $query        = CGI->new;

my $mapper       = 'mapper.cgi';
my $method       = 'POST';
$method          = 'GET' if ($query->param('get'));
my $htmltitle    = 'Metes and Bounds Plotting Tool (Deed Calls)';
my $authorname   = 'Michael R. Davis';
my $authoremail  = 'davis@davisnetworks.com';
my $bgcolor      = $query->param('bgcolor')      || 'FFFFFF';
my $fgcolor      = $query->param('fgcolor')      || '000000';
my $width        = $query->param('width')        || 640;
my $height       = $query->param('height')       || 480;
$width           = 54 if $width  < 54;
$height          = 54 if $height < 54;
my $scale        = $query->param('scale')        || 1;
my $parsedisplay = $query->param('parsedisplay') || 0;
my $box          = $query->param('box')          || '';

#-------------------------------------------------------------------------------
my $error=0;
my @output=();
if ( $box ) {
 my @box=split("\n", $box);
 foreach (@box) {
  my @tmp=();
  chomp;
  s/#.*//;  #Remove Comments
  if (m/\S/) {
    push @tmp, $_;
    my ($match, $ns, $deg, $min, $sec, $ew, $len, $unit);
    if (m/^\s*([NSns])\s+([\d\.]+)\s+([\d\.]*)\s*([\d\.]*)\s*([EWew])\s+([\d\.]+)\s+(\w+)\s*$/) {
    #Format S|N Deg [Min [Sec]] E|W Len unit
      $match=1;
      $ns=$1;
      $deg=$2;
      $min=$3 || 0; #default
      $sec=$4 || 0; #default
      $ew=$5;
      $len=$6;
      $unit=$7;
    } elsif (m/^\s*([NSns])\s+([\d\.]+)\s+(\w+)\s*$/) {
    #Format S|N Len unit
      $match=1;
      $ns=$1;
      $deg=0;
      $min=0;
      $sec=0;
      $ew="E";
      $len=$2;
      $unit=$3;
    } elsif (m/^\s*([EWew])\s+([\d\.]+)\s+(\w+)\s*$/) {
    #Format E|W Len unit
      $match=1;
      $ns="N";
      $deg=90;
      $min=0;
      $sec=0;
      $ew=$1;
      $len=$2;
       $unit=$3;
    } else {
      $match=0;
    }
    if ($unit=~m/^f((ee|oo)?t)?$/i) {
      $unit="ft";
    } elsif ($unit=~m/^y((ar)?ds?)?$/i) {
      $len*=3;
      $unit="ft";
    } elsif ($unit=~m/^(p(oles?)?|r(ods?)?)$/i) {
      $len*=16.5;
      $unit="ft";
    } elsif ($unit=~m/^m(eters?)?$/i) {
      $len*=3.28;
      $unit="ft";
    } else {
      $unit.=" (unknown)";
      $error=1;
    }
    if ($match) {
      $ns=~s/(.*)/uc($1)/e;
      $ew=~s/(.*)/uc($1)/e;
      push @tmp, $ns, $deg, $min, $sec, $ew, $len, $unit,;
    } else {
      push @tmp, ('-') x 7;
      $error=1;
    }
    push @output, [@tmp]; #must be an anonymous array [] indstead \@ because we keep changing the array.
  } #end \S
 } #end foreach
} #end param

print $query->header, 
      $query->start_html(-title=>$htmltitle,
                         -author=>$authoremail,
                        #-onload=>'document.form1.box.focus();'
                        ), "\n",
      $query->h1($htmltitle), "\n",
      $query->hr({-width=>'85%'}), "\n",
      $query->start_form(-name=>'form1',
                         -method=>$method,
                         -action=>$query->script_name()), "\n",
      $query->table({-align=>'center'},
        $query->Tr(
          $query->td({valign=>'top'},
            $query->textarea(-name=>'box',
                             -rows=>15,
                             -columns=>50)
          ),
          $query->td({valign=>'top'},
            $query->p('Enter data in one of the following formats.'),
            $query->table(
              $query->Tr([map {$query->td('&nbsp;'. $_)} 
                $query->b('N|S deg [min [sec]] E|W len unit'),
                'N 65 35 46.7 W 179.39 ft',
                'S 52.5 W 12.1 rods',
                $query->b('N|E|S|W len unit'),
                'S 175 Feet',
                'E 19.5 Poles',
                'N 222.42 ft',
                $query->b('#Comment'),
              ])
            ),
            $query->submit(-name=>'submit',
                           -value=>'Verify')
          ),
        ),
        $query->Tr(
          $query->td({valign=>'top'},
            $query->p(
              $query->b('Options')
            ),
            $query->table(
              $query->Tr([
                $query->td([
                  'Show Parser Output Table: ',
                  $query->checkbox(-name=>'parsedisplay',
			           -checked=>undef,
		                   -value=>1,
		                   -label=>''),
                  '&nbsp;&nbsp;&nbsp;',
                  'Image Scale Display: ',
                  $query->popup_menu({-name=>'scale',
                                      -default=>1,
                                      -values=>[0, 1],
                                      -labels=>{0=>'--none--', 1=>'Type 1'}})
                ]),
                $query->td([
                  'Image Background Color: ',
                  $query->input({-name=>'bgcolor', -value=>$bgcolor, -size=>8}),
                  '&nbsp;&nbsp;&nbsp;',
                  'Image Width: ',
                  $query->input({-name=>'width', -value=>$width, -size=>8})
                ]),
                $query->td([
                  'Image Foreground Color: ',
                  $query->input({-name=>'fgcolor', -value=>$fgcolor, -size=>8}),
                  '&nbsp;&nbsp;&nbsp;',
                  'Image Height: ',
                  $query->input({-name=>'height', -value=>$height, -size=>8})
                ])
              ])
            )
          )
        )
      ),
      $query->end_form, "\n",
      $query->hr({-width=>'85%'}), "\n";

if (scalar(@output)) {      
  if ($parsedisplay || $error) {
    print $query->table({-align=>'center', -border=>1, -cellpadding=>5},
            $query->Tr(
              $query->td({-align=>'center'}, $query->b(q/Input/)), 
              $query->td({-align=>'center', -colspan=>7}, $query->b(q/Output/))
            ),
            $query->Tr([
              $query->td([
                map {$query->b($_)}
                  qw/Call NS Degrees Minutes Seconds EW Length Units/
              ])
            ]),
            $query->Tr([
              map {
                $query->td([
                  $query->b($_->[0]),
                  &{sub{shift;return(@_)}}(@{$_})
                ])
              } @output
            ]),
          ), "\n",
          $query->hr({-width=>'85%'}), "\n";
  }

  if ($error) {
    print $query->p($query->b(q/Data Contains Errors!/)), "\n",
          $query->hr({-width=>'85%'}), "\n"; 
  } else {
    my $datatype='vert';
    my @points=vector2points(@output);
    my $data=join(":", map {join(",", @{$_})} @points);
    my $unit='ft';
    my $url="$mapper?width=$width&height=$height&scale=$scale&unit=$unit&bgcolor=$bgcolor&fgcolor=$fgcolor&datatype=$datatype&data=$data";
    if (length($url) > 2048) { #MSIE sucks and can only handle a 2k url!
      print $query->table({-align=>'center'},
              $query->Tr(
                $query->td(
                  $query->start_form(-name=>'form2',
                                     -action=>$mapper,
                                     -method=>'POST'),
                  $query->hidden(-name=>'width', -value=>$width),
                  $query->hidden(-name=>'height', -value=>$height),
                  $query->hidden(-name=>'scale', -value=>$scale),
                  $query->hidden(-name=>'unit', -value=>$unit),
                  $query->hidden(-name=>'bgcolor', -value=>$bgcolor),
                  $query->hidden(-name=>'fgcolor', -value=>$fgcolor),
                  $query->hidden(-name=>'datatype', -value=>$datatype),
                  $query->hidden(-name=>'data', -value=>$data),
                  $query->submit(-name=>'submit2', 
                                 -value=>'Plot'),
                  $query->end_form(),
                ),
              ),
            ),
            $query->hr({-width=>'85%'}), "\n"; 
    } else {
      print $query->table({-align=>'center'},
              $query->Tr(
                $query->td(
                  $query->a({-href=>$url},
                    $query->img({-src=>$url,
                                 -width=>$width,
                                 -height=>$height,
                                 -border=>0
                                }),
                  ),
                ),
              ),
            ),
            $query->hr({-width=>'85%'}), "\n"; 
    }
    my ($closex, $closey)=@{$points[-1]};
    my $angle=$closex ? 90 : 0;
    $angle=abs(atan2($closex/$closey, 1)*180/atan2(0,-1)) if $closey;
    my $ns=$closey>0 ? 'S' : 'N';
    my $ew=$closex>0 ? 'W' : 'E';
    my $deg=sprintf('%02d',   int($angle));
    my $min=sprintf('%02d',   int(($angle-$deg)*60));
    my $sec=sprintf('%02.5f', ($angle-$deg-$min/60)*60*60);
    my $len=sprintf('%.5f',   sqrt($closex**2+$closey**2));
    my $per=0;
    $per+=$_->[6] foreach (@output);
    $per=sprintf('%.5f', $per);
    my $area=sprintf('%.5f', abs(calcarea(@points))/43560); # 1 acre=43560 sqft
    my $unitarea="acres";
    #my $unit='ft';
    print $query->p("Vector of Closure:",
                    qq{<VectorOfClosure format="N|S dd mm ss E|W nn.nn ft">},
                    qq{<vocns>$ns</vocns>},
                    qq{<vocdeg>$deg</vocdeg>},
                    qq{<vocmin>$min</vocmin>},
                    qq{<vocsec>$sec</vocsec>},
                    qq{<vocew>$ew</vocew>},
                    qq{<voclen units="$unit">$len</voclen>},
                    qq{<vocunit>$unit</vocunit>},
                    qq{</VectorOfClosure>}),
          #$query->p("Distance from Closure: $len $unit"),
          $query->p("Perimeter:",
                    qq{<perimeter units="$unit">$per</perimeter>},
                    $unit),
          $query->p(qq{Area: <area units="$unitarea">$area</area> $unitarea}),
          $query->hr({-width=>'85%'}), "\n";
  }
}

#-------------------------------------------------------------------------------

print $query->p({-align=>'center'},
        'Copyright &copy; 2001',
        $query->a({-href=>"mailto:$authoremail"}, "$authorname."),
        'All rights reserved.'
      ), "\n",
      $query->end_html, "\n";

sub vector2points {
  my $pi=atan2(0,-1); # =~3.1415...
  my @pt=(0,0); #default start coordinates 0,0
  my $x;
  my $y;
  my $angle;
  my @data=([@pt]);
  foreach (@_) {
    my ($comment, $ns, $deg, $min, $sec, $ew, $len, $unit)=@{$_};
    my $xsgn=1;
    $xsgn=-1 if ($ew=~m/W/i);
    my $ysgn=1;
    $ysgn=-1 if ($ns=~m/S/i);
    $angle=$deg+($min+$sec/60)/60;
    $x=$pt[0] + $len * $xsgn * sin($angle/180*$pi);
    $y=$pt[1] + $len * $ysgn * cos($angle/180*$pi);
    $x=0 if (abs($x) < 1e-10);  #I added this because I was tired
    $y=0 if (abs($y) < 1e-10);  #of the 1e-15 numbers digital math!
    @pt=($x,$y);
    push @data, [@pt];
  }
  return @data;
}

sub calcarea {
#from http://www.geocities.com/SiliconValley/Lakes/2160/gis/compgra.htm#201
#
#Subject 2.01: How do I find the area of a polygon?
#
#    The signed area can be computed in linear time by a simple sum.
#    The key formula is this:
#
#        If the coordinates of vertex v_i are x_i and y_i,
#        twice the signed area of a polygon is given by
#
#        2 A( P ) = sum_{i=0}^{n-1} (x_i y_{i+1} - y_i x_{i+1}).
#
#    Here n is the number of vertices of the polygon.
#    References: [O' Rourke] pp. 18-27; [Gems II] pp. 5-6:
#    "The Area of a Simple Polygon", Jon Rokne.
#
#  @poly=([x0,y0],[x1,y1],...,[xn,yn],[x0,y0]);

  my @poly=@_;
  my $area=0;
  foreach (0..$#poly-1) {
    $area+=$poly[$_][0] * $poly[$_+1][1] - $poly[$_][1] * $poly[$_+1][0];
  }
  return $area/2;
}
