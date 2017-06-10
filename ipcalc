#!/usr/bin/perl -w


#  IPv4 Calculator
#  Copyright (C) Krischan Jodies 2000 - 2004
#  krischan()jodies.de, http://jodies.de/ipcalc
#   
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#   
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use strict;

my $version = '0.41';

my @class   = qw (0 8 16 24 4 5 5);

my $quads_color = "\033[34m"; # dotted quads, blue
my $norml_color = "\033[m";   # normal, black
#my $binry_color = "\033[1m\033[46m\033[37m"; # binary, yellow
my $binry_color = "\033[33m"; # binary, yellow
my $mask_color = "\033[31m"; # netmask, red
my $class_color = "\033[35m"; # classbits, magenta
my $subnt_color = "\033[0m\033[32m"; # subnet bits, green
my $error_color = "\033[31m";
my $sfont  = "";
my $break  ="\n";

my $color_old = "";
my $color_actual = "";

my $opt_text        = 1;
my $opt_html        = 0;
my $opt_color       = 0;
my $opt_print_bits  = 1;
my $opt_print_only_class = 0;
my $opt_split       = 0;
my $opt_deaggregate   = 0;
my $opt_version     = 0;
my $opt_help        = 0;
my @opt_split_sizes;
my @arguments;
my $error = "";
my $thirtytwobits = 4294967295; # for masking bitwise not on 64 bit arch

main();
exit;

sub main 
{
   my $address  = -1;
   my $address2 = -1;
   my $network  = -1;
   my $mask1    = -1;
   my $mask2    = -1;

   if (! defined ($ARGV[0])) {
      usage();
      exit();
   }

   @ARGV = getopts();

   if ($opt_help) {
      help();
      exit;
   }

   if ($opt_version) {
      print "$version\n";
      exit;
   }

#print "opt_html   $opt_html\n";
#print "opt_color  $opt_color\n";
#print "opt_print_bits $opt_print_bits\n";
#print "opt_print_only_class $opt_print_only_class\n";
#print "opt_deaggregate $opt_deaggregate\n";

   if (! $opt_color) {
      $quads_color = '';
      $norml_color = '';
      $binry_color = '';
      $mask_color = '';
      $class_color = '';
      $subnt_color = '';
      $sfont  = '';
   }

   if ($opt_html) {
      $quads_color = '<font color="#0000ff">' ;
      $norml_color = '<font color="#000000">';
      $binry_color = '<font color="#909090">';
      $mask_color = '<font color="#ff0000">';
      $class_color = '<font color="#009900">';
      $subnt_color = '<font color="#663366">';
      $sfont  = '</font>';
      $break  = "<br>";
      #$private = "(<a href=\"http://www.ietf.org/rfc/rfc1918.txt\">Private Internet</a>)";
#      print "<pre>\n";
print << 'EOF';
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta HTTP-EQUIV="content-type" CONTENT="text/html; charset=UTF-8">
<title>Bla</title>
</head>
<body>
EOF
      print "<!-- Version $version -->\n";
   }

#   foreach (@arguments) {
#      print "arguments: $_\n";
#   }

#   foreach (@ARGV) {
#      print "ARGV: $_\n";
#   }
  
   # get base address
   if (defined $ARGV[0]) {
      $address = argton($ARGV[0],0);
   }
   if ($address == -1) {
      $error .= "INVALID ADDRESS: $ARGV[0]\n";
      $address = argton("192.168.1.1");
   }

   if ($opt_print_only_class) {
      print getclass($address,1);
      exit;
   }
  
   # if deaggregate get last address
   if ($opt_deaggregate) {
      if (defined $ARGV[1]) {
         $address2 = argton($ARGV[1],0);
      }
      if ($address2 == -1) {
        $error .= "INVALID ADDRESS2: $ARGV[1]\n";
        $address2 = argton("192.168.1.1");
      }
   }

   if ($opt_deaggregate) {
      if ($error) {
         print "$error\n";
      }
      print "deaggregate ".ntoa($address) . " - " . ntoa($address2)."\n";
      deaggregate($address,$address2);
      exit;
   }

   # get netmasks
   if (defined $ARGV[1]) {
      $mask1   = argton($ARGV[1],1);
   } else {
      #get natural mask ***
      $mask1 = argton(24);
   }
   if ($mask1   == -1) {
      $error .= "INVALID MASK1:   $ARGV[1]\n";
      $mask1   = argton(24);
   }

   if (defined $ARGV[2]) {
      $mask2   = argton($ARGV[2],1);
   } else {
      $mask2 = $mask1;
   }
   if ($mask2   == -1) {
      $error .= "INVALID MASK2:   $ARGV[2]\n";
      $mask2   = argton(24);
   }

   if ($error) {
      if ($opt_color) {
         print set_color($error_color);
      }
      print "$error\n";
   }

#   print "Address: ".ntoa($address)."\n";
#   print "mask1: ($mask1) ".ntoa($mask1)."\n";
#   print "mask2: ($mask2) ".ntoa($mask2)."\n";
   
   html('<table border="0" cellspacing="0" cellpadding="0">');
   html("\n");
   printline ("Address",   $address ,$mask1,$mask1,1);
   printline ("Netmask",   $mask1   ,$mask1,$mask1);
   printline ("Wildcard", ~$mask1   ,$mask1,$mask1);
   html("<tr>\n");
   html('<td colspan="3"><tt>');
   print "=>";
   html("</tt></td>\n");
   html("</tr>\n");
   print "\n";
   
   $network = $address & $mask1;
   printnet($network,$mask1,$mask1);
   html("</table>\n");
   if ($opt_deaggregate) {
      deaggregate();
   }
   if ($opt_split) {
      split_network($network,$mask1,$mask2,@opt_split_sizes);
      exit;
   }
   if ($mask1 < $mask2) {
      print "Subnets after transition from /" . ntobitcountmask($mask1);
      print " to /". ntobitcountmask($mask2) . "\n\n";
      subnets($network,$mask1,$mask2);
   }
   if ($mask1 > $mask2) {
      print "Supernet\n\n";
      supernet($network,$mask1,$mask2);
   }
   if ($opt_html) {
      print << 'EOF';
    <p>
      <a href="http://validator.w3.org/check/referer"><img border="0"
          src="http://www.w3.org/Icons/valid-html401"
          alt="Valid HTML 4.01!" height="31" width="88"></a>
    </p>
EOF
   }
   exit;

}

# ---------------------------------------------------------------------

sub end {
 if ($opt_html) {
#   print "\n</pre>\n";
print "<html>\n";
 }
 exit;
}

sub supernet {
    my ($network,$mask1,$mask2) = @_;
    $network = $network & $mask2;
    printline ("Netmask",   $mask2   ,$mask2,$mask1,1);
    printline ("Wildcard", ~$mask2   ,$mask2,$mask1);
    print "\n";
    printnet($network,$mask2,$mask1);
}

sub subnets 
{
   my ($network,$mask1,$mask2) = @_;
   my $subnet=0;
   my $bitcountmask1 = ntobitcountmask($mask1);
   my $bitcountmask2 = ntobitcountmask($mask2);

   html('<table border="0" cellspacing="0" cellpadding="0">');
   html("\n");
   printline ("Netmask",   $mask2   ,$mask2,$mask1,1);
   printline ("Wildcard", ~$mask2   ,$mask2,$mask1);
   html("</table>\n");

   print "\n";
  
   for ($subnet=0; $subnet < (1 << ($bitcountmask2-$bitcountmask1)); $subnet++)
   {
     my $net = $network | ($subnet << (32-$bitcountmask2));
     print " ". ($subnet+1) .".\n";
     html('<table border="0" cellspacing="0" cellpadding="0">');
     html("\n");
     printnet($net,$mask2,$mask1);
     html("</table>\n");
     if ($subnet >= 1000) {
        print "... stopped at 1000 subnets ...$break";
	last;
     }
   }
   $subnet = (1 << ($bitcountmask2-$bitcountmask1));
   my $hostn = ($network | ((~$mask2) & $thirtytwobits)) - $network - 1;
   if ($hostn > -1) {
      print "\nSubnets:   $quads_color$subnet";
      html('</font>');
      print "$norml_color$break";
      html('</font>');
   }
   if ($hostn < 1 ) {
      $hostn = 1;
   }
   print "Hosts:     $quads_color" . ($hostn * $subnet);
   html('</font>'); 
   print "$norml_color$break";
   html('</font>');
}


sub getclass {
   my $network = shift;
   my $numeric = shift;
   my $class = 1;
#   print "n $network bit ". (1 << (32-$class)) . " & " . 
   while (($network & (1 << (32-$class))) == (1 << (32-$class)) ) {
      $class++;
      if ($class > 5) {
	 return "invalid";
      }
   }
   if ($numeric) {
      return $class[$class]; 
   } else {
      return chr($class+64);
   }
}

sub printnet {
    my ($network,$mask1,$mask2) = @_;
    my $hmin;
    my $hmax; 
    my $hostn;
    my $mask;

    my $broadcast = $network | ((~$mask1) & $thirtytwobits);
    
    $hmin  = $network + 1;
    $hmax  = $broadcast - 1;
    $hostn =  $hmax - $hmin + 1;
    $mask  = ntobitcountmask($mask1);
    if ($mask == 31) {
       $hmax  = $broadcast;
       $hmin  = $network;
       $hostn = 2;
    }
    if ($mask == 32) {
       $hostn = 1;
    }
    

    #if ($hmax < $hmin) {
    #   $hmax = $hmin;
    #   $hostn = 1;
    #}
    

    #private...
    #$p = 0;
    #for ($i=0; $i<3; $i++) {
    #	if ( (&bintoint($hmax) <= $privmax[$i])  && 
    #         (&bintoint($hmin) >= $privmin[$i]) ) {
    #	    $p = $i +1;
    #	    last;
    #	}
    #}
    
    #if ($p) {
    #	$p = $private;
    #} else {
    #	$p = '';
    #}
 

    if ($mask == 32) {
       printline ("Hostroute", $network  ,$mask1,$mask2,1);
    } else {
       printline ("Network",   $network  ,$mask1,$mask2,1);
       printline ("HostMin",   $hmin     ,$mask1,$mask2); 
       printline ("HostMax",   $hmax     ,$mask1,$mask2);
       printline ("Broadcast", $broadcast,$mask1,$mask2) if $mask < 31;
    }
#    html("</table>\n");

#    html('<table border="0" cellspacing="0" cellpadding="0">');
#    html("\n");
    html("<tr>\n");
    html('<td valign="top"><tt>'); #label
    print set_color($norml_color);
    print "Hosts/Net: " ;
    html("</font></tt></td>\n");
    html('<td valign="top"><tt>');
#    printf $norml_color . "Hosts/Net: </tt>$quads_color%-22s",$hostn;
#    html("<td><tt>");   
    print set_color($quads_color);
    printf "%-22s",$hostn;
#    printf "%-22s", (ntoa($address).$additional_info);
    html("</font></tt></td>\n"); 
    html("<td>"); #label
    if ($opt_html) {
#warn "HTML\n";
       print wrap_html(30,get_description($network,$mask1));
    } else {
       print get_description($network,$mask1);
    }
    html("</font></td>\n");
    html("</tr>\n");   
    html("\n");
    text("\n");
    text("\n");
    
    ##printf "Class %s, ",getclass($network);
    ##printf "%s",netblock($network,$mask1);
#    my ($label,$address,$mask1,$mask2,$classbitcolor_on,$is_netmask) = @_;
#    print $sfont . $norml_color;
   
#    print "$break\n";
#   exit; 
   return $hostn;
}

sub get_description 
{
   my $network = shift;
   my $mask    = shift;
   my @description;
   my $field;
   # class
   if ($opt_color || $opt_html) {
      $field = set_color($class_color) . "Class " . getclass($network);
      if ($opt_html) {
         $field .= '</font>';
      }
      $field .= set_color($norml_color);
      push @description, $field
#      push @description, set_color($class_color) . "Class " . 
#                         getclass($network) . set_color($norml_color);
   } else {
      push @description, "Class " . getclass($network);
   }
   # netblock
   my ($netblock_txt,$netblock_url) = split ",",netblock($network,$mask);
   if (defined $netblock_txt) {
      if ($opt_html) {
         $netblock_txt = '<a href="' . $netblock_url . '">' .
                         $netblock_txt . '</a>';
      }
#warn "DESC: '$netblock_txt'";
      push @description,$netblock_txt;
   }
   # /31
   if (ntobitcountmask($mask) == 31) {
      if ($opt_html) { 
         push @description,"<a href=\"http://www.ietf.org/rfc/rfc3021.txt\">PtP Link</a>";
      } else {
         push @description,"PtP Link RFC 3021";
      }
   }
#$rfc3021 = "<a href=\"http://www.ietf.org/rfc/rfc3021.txt\">Point-to-Point
#Link</a>";
   return join ", ",@description;
}

sub printline
{
   my ($label,$address,$mask1,$mask2,$html_fillup) = @_;
   $mask1 = ntobitcountmask($mask1);
   $mask2 = ntobitcountmask($mask2);
   my $line = "";
   my $bit;
   my $newbitcolor_on = 0;
   my $toggle_newbitcolor = 0;
   my $bit_color;
   my $additional_info = '';
   my $classbitcolor_on;
   my $second_field;
   if ($label eq 'Netmask') {
      $additional_info = " = $mask1";
   }
   if ($label eq 'Network') {
      $classbitcolor_on = 1;
      $additional_info = "/$mask1";
   }
   if ($label eq 'Hostroute' && $mask1 == 32) {
      $classbitcolor_on = 1;
   }
   
   html("<tr>\n");   
   html("<td><tt>");   
   #label
   print set_color($norml_color);
   if ($opt_html && $html_fillup) {
      print "$label:";
      print "&nbsp;" x (11 - length($label));
   } else {
      printf "%-11s","$label:";
   }
   html("</font></tt></td>\n"); 
   #address
   html("<td><tt>");   
   print set_color($quads_color);
   #printf "%s-22s",(ntoa($address).$additional_info);

   #printf "%s%-11s$sfont%s",set_color($norml_color),"$label:",set_color($quads_color);
   $second_field = ntoa($address).$additional_info;
   if ($opt_html && $html_fillup) {
      print $second_field;
      print "&nbsp;" x (21 - length($second_field));
   } else {
      printf "%-21s", (ntoa($address).$additional_info);
   }
   html("</font></tt></td>\n"); 
   
   
   if ($opt_print_bits)
   {
      html("<td><tt>");
      $bit_color = set_color($binry_color);
      if ($label eq 'Netmask') {
         $bit_color = set_color($mask_color);
      }
      
      if ($classbitcolor_on) {
         $line .= set_color($class_color);
      } else {
         $line .= set_color($bit_color);
      }
      for (my $i=1;$i<33;$i++)
      {
         $bit = 0;
         if (($address & (1 << 32-$i)) == (1 << 32-$i)) {
            $bit = 1;
         }
         $line .= $bit;
         if ($classbitcolor_on && $bit == 0) {
            $classbitcolor_on = 0;
   	 if ($newbitcolor_on) {
   	    $line .= set_color($subnt_color);
   	 } else {
   	    $line .= set_color($bit_color);
   	 }
         }
#   print "$mask1 $i % 8 == " . (($i) % 8) . "\n";
         if ($i % 8 == 0 && $i < 32) {
            $line .= set_color($norml_color) . '.';
	    $line .= set_color('oldcolor');
         }
         if ($i == $mask1) {
            $line .= " "; 
         }
         if (($i == $mask1 || $i == $mask2) && $mask1 != $mask2) {
            if ($newbitcolor_on) {
               $newbitcolor_on = 0;
               $line .= set_color($bit_color) if ! $classbitcolor_on;
            } else {
               $newbitcolor_on = 1;
               $line .= set_color($subnt_color) if ! $classbitcolor_on;
            }
         }
      }
      $line .= set_color($norml_color);
      print "$line";
      html("</tt></font></td>\n"); 
   }
   html("</tr>\n");
html("\n");
text("\n");
   #print $sfont . $break;
}

sub text
{
   my $str = shift;
   if ($opt_text) {
      print "$str";
   }
}

sub html
{
   my $str = shift;
   if ($opt_html) {
      print "$str";
   }
}

sub set_color
{
   my $new_color = shift;
   my $return;
   if ($new_color eq $color_old) {
#      print "SETCOLOR saved one dupe\n";
   #   $return = 'x';
   $return = '';
   }
   if ($new_color eq 'oldcolor') {
      $new_color = $color_old;
   }
   $color_old = $color_actual;
   #$return .= "$color_actual" . "old";
   $color_actual = $new_color;
   #return $new_color;
   $return .= $new_color;
   return $return;
}

sub split_network
{
   my $network = shift;
   my $mask1   = shift;
   my $mask2   = shift;
   my @sizes = @_;
   
   my $first_address = $network;
   my $broadcast = $network | ((~$mask1) & $thirtytwobits);
   my @network;
   my $i=0;
   my @net;
   my @mask;
   my $needed_addresses = 0;
   my $needed_size;
   foreach (@sizes) {
      $needed_size = round2powerof2($_+2);
#      printf "%3d -> %3d -> %3d\n",$_,$_+2,$needed_size;
      push @network , $needed_size .":".$i++;
      $needed_addresses += $needed_size;
   }
   @network = sort { ($b =~ /(.+):/)[0] <=> ($a =~ /(.+):/)[0] } @network;
   foreach (@network) {
      my ($size,$nr) = split ":",$_;
      $net[$nr]=  $network;
      $mask[$nr]= (32-log($size)/log(2));
      $network += $size;
   }
   $i = -1;
   while ($i++ < $#sizes) {   
      printf "%d. Requested size: %d hosts\n", $i+1,$sizes[$i];
      ###$mask  = $mask[$i];
      #$mark_newbits = 1;
      ###print_netmask(bitcountmasktobin($mask[$i]),$mask);
      printline("Netmask",bitcountmaskton($mask[$i]),bitcountmaskton($mask[$i]),$mask2);
      printnet($net[$i],bitcountmaskton($mask[$i]),$mask2);
   }

   my $used_mask = 32-log(round2powerof2($needed_addresses))/log(2);
   if ($used_mask < ntobitcountmask($mask1)) {
      print "Network is too small\n";
   }
   print "Needed size:  ". $needed_addresses . " addresses.\n";
   print "Used network: ". ntoa($first_address) ."/$used_mask\n";
   print "Unused:\n";
   deaggregate($network,$broadcast);
   
}

sub round2powerof2 {
  my $i=0;
  while ($_[0] > ( 1 << $i)) {
     $i++;
  }
  return 1 << $i;
}

# Deaggregate address range
# expects: range: (dotted quads)start (dotted quads)end

sub deaggregate 
{
  my $start = shift;
  my $end   = shift;
  my $base = $start;
  my $step;
  while ($base <= $end)
  {
       $step = 0;
       while (($base | (1 << $step))  != $base) {
          if (($base | (((~0) & $thirtytwobits) >> (31-$step))) > $end) {
	     last;
	  }
          $step++;
       }
       print ntoa($base)."/" .(32-$step);
       print "\n";
       $base += 1 << $step;
  }
}

sub getopts 
   # expects nothing
   # returns @ARGV without options
   # sets global opt variables
   
   # -h --html 
   # -h without further opts -> help 
   #    (workaround: can't change meaning of -h since this would
   #     break old cgi_wrapper scripts)
   # --help 
   # -n --nocolor
   # -v --version
   # -c --class print natural class
   # -s --split
   # -b --nobinary
   # -d --deaggregate  
{  
   my @arguments;
   my $arg;
   my $prefix;
   my $nr_opts = 0;
   my @tmp;
   
   # opt_color defaults to 1 when connected to a terminal
   if (-t STDOUT) {
      $opt_color = 1;
   }
   
   while (has_opts()) {
     $arg = shift @ARGV;
     if ($arg =~ /^--(.+)/) {
         $nr_opts += read_opt('--',$1);
     }
     elsif ($arg =~ /^-(.+)/) {
	 $nr_opts += read_opt('-',split //,$1);
     } 
     else {
        push @tmp, $arg;
     }
   }

#   foreach (@arguments) {
#      print "arg: $_\n";
#   }

   foreach (@ARGV) {
      push @tmp,$_;
   }
   # extract base address and netmasks and ranges
   foreach (@tmp) {
      if (/^(.+?)\/(.+)$/) {
         push @arguments,$1;
         push @arguments,$2;
      }
      elsif (/^(.+)\/$/) {
         push @arguments,$1;
      }
      elsif (/^(.+)\-(.+)$/) {
         push @arguments,$1;
         push @arguments,$2;
         $opt_deaggregate = 1;
      }
      elsif (/^\-$/) {
         $opt_deaggregate = 1;
      }
      else {
         push @arguments, $_;
      }
   }
   if ($#arguments == 2 && $arguments[1] eq '-') {
      @arguments = ($arguments[0],$arguments[2]);
      $opt_deaggregate = 1;
   }
   
   
   # workaround for -h 
   if ($opt_html && $nr_opts == 1 && $#arguments == -1) {
      $opt_help = 1;
   }
 

   if ($error) {
      print "$error";
      exit;
   }
   return @arguments;

   sub read_opt {
     my $prefix = shift;
     my $opts_read = 0;
     foreach my $opt (@_) 
     {
        ++$opts_read;
        if    ($opt eq 'h' || $opt eq 'html') {
	   $opt_html = 1;
           $opt_text = 0;
	}
        elsif    ($opt eq 'help') {
	   $opt_help = 1;
	}
	elsif ($opt eq 'n' || $opt eq 'nocolor') {
	   $opt_color = 0;
	}
	elsif ($opt eq 'v' || $opt eq 'version') {
	   $opt_version = 1;
	}
	elsif ($opt eq 'b' || $opt eq 'nobinary') {
	   $opt_print_bits = 0;
	}
	elsif ($opt eq 'c' || $opt eq 'class') {
	   $opt_print_only_class =  1;
	}
	elsif ($opt eq 'r' || $opt eq 'range') {
           $opt_deaggregate =  1;
        }
	elsif ($opt eq 's' || $opt eq 'split') {
	   $opt_split = 1;
	   while (defined $ARGV[0] && $ARGV[0] =~ /^\d+$/) {
	      push @opt_split_sizes, shift @ARGV;
	   }
	   if ($#opt_split_sizes < 0) {
	      $error .= "Argument for ". $prefix . $opt . " is missing or invalid \n";
	   }
	}
	else {
	   $error .= "Unknown option: " . $prefix . $opt . "\n";
	   --$opts_read;
	}
     }
     return $opts_read;
   }

   sub has_opts {
      foreach (@ARGV) {
         return 1 if /^-/;
      }
      return 0;
   }
}


# expects int width
#         string  
# returns wrapped string
sub wrap_html
{ 
   my $width = shift;
   my $str   = shift;
#warn "WRAP: '$str'\n";
   my @str = split //,$str;
   my $result;
   my $current_pos = 0;
   my $start = 0;
   my $last_pos = 0;
   my $line;
   while ($current_pos < $#str) 
   {
#warn "$current_pos\n";
#warn "$current_pos: $str[$current_pos]\n";
      # find next blank
      while ($current_pos < $#str && $str[$current_pos] ne ' ') {
         # ignore tags
         if ($str[$current_pos] eq '<') {
            $current_pos++;
            while ($str[$current_pos] ne '>') {
               $current_pos++;
            }
         }
         $current_pos++;
      }
      # fits in one line?...
      $line = substr($str,$start,$current_pos-$start);
      $line =~ s/<.+?>//g;
      if ( length($line) <= $width) {
	 # ... yes. keep position in mind and try next
         $last_pos = $current_pos;
         $current_pos++;
         next;
      } else {
         # ...no. wrap at last position (if there was one,
         # otherwise wrap here)
         if ($last_pos ne $start) {
            $current_pos = $last_pos;
         }
         $line = substr($str,$start,$current_pos-$start);
         $current_pos++;
         $start = $current_pos;
         $last_pos = $start;
         # no output if end of string is reached because
         # rest of string is treated after this block
         if ($current_pos < $#str) {
#warn "RESULT+ '$line'\n";
            $result .= "$line<br>";
         }
         
      }  
   }
   $line = substr($str,$start,$current_pos-$start);
   $result .= "$line";
#warn "'return RESULT $result'\n";
   return $result;
}


# gets network address as dq
# returns string description,string url
sub netblock 
{
   my ($mynetwork_start,$mymask) = @_;
   my $mynetwork_end = $mynetwork_start | ((~$mymask) & $thirtytwobits);
   my %netblocks = ( "192.168.0.0/16" => "Private Internet,http://www.ietf.org/rfc/rfc1918.txt",
                     "172.16.0.0/12"  => "Private Internet,http://www.ietf.org/rfc/rfc1918.txt",
                     "10.0.0.0/8"     => "Private Internet,http://www.ietf.org/rfc/rfc1918.txt",
                     "169.254.0.0/16" => "APIPA,http://www.ietf.org/rfc/rfc3330.txt",
		     "127.0.0.0/8"    => "Loopback,http://www.ietf.org/rfc/rfc1700.txt",
		     "224.0.0.0/4"    => "Multicast,http://www.ietf.org/rfc/rfc3171.txt"
                   );
   my $match = 0;
   #
   foreach (keys %netblocks) {
      my ($network,$mask) = split "/",$_;
      my $start = argton($network);
      my $end   = $start + (1 << (32-$mask)) -1;
      # mynetwork starts within block
      if ($mynetwork_start >= $start && $mynetwork_start <= $end) {
         $match++;
      }
      # mynetwork ends within block
      if ($mynetwork_end >= $start && $mynetwork_end <= $end) {
         $match++;
      }
      # block is part of mynetwork
      if ($start > $mynetwork_start && $end < $mynetwork_end) {
         $match = 1;
      }
      if ($match == 1) {
         return "In Part ".$netblocks{$_};
      }
      if ($match == 2) {
         return $netblocks{$_};
      }
   }
   return "";
}

# ------- converter ---------------------------------------------

sub bitcountmaskton 
{
   my $bitcountmask = shift;
   my $n;
   for (my $i=0;$i<$bitcountmask;$i++) {
      $n |= 1 << (31-$i);
   }
   return $n;
}

sub argton
# expects 1. an address as dotted decimals, bit-count-mask, or hex
#         2. netmask flag. if set -> check netmask and negate wildcard
#            masks
# returns integer or -1 if invalid
{
   my $arg          = shift;
   my $netmask_flag = shift;
   
   my $i = 24;
   my $n = 0;
   
   # dotted decimals
   if    ($arg =~ /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/) {
      my @decimals = ($1,$2,$3,$4);
      foreach (@decimals) {
         if ($_ > 255 || $_ < 0) {
	    return -1;
	 }
	 $n += $_ << $i;
	 $i -= 8;
      }
      if ($netmask_flag) {
         return validate_netmask($n);
      }
      return $n;
   }
   
   # bit-count-mask (24 or /24)
   $arg =~ s/^\/(\d+)$/$1/;
   if ($arg =~ /^\d{1,2}$/) {
      if ($arg < 1 || $arg > 32) {
         return -1;
      }
      for ($i=0;$i<$arg;$i++) {
         $n |= 1 << (31-$i);
      }
      return $n;
   }
   
   # hex
   if ($arg =~   /^[0-9A-Fa-f]{8}$/ || 
       $arg =~ /^0x[0-9A-Fa-f]{8}$/  ) {
      if ($netmask_flag) {
         return validate_netmask(hex($arg));
      }
      return hex($arg);
   }

   # invalid
   return -1;
   
   sub validate_netmask
   {
      my $mask = shift;
      my $saw_zero = 0;
      # negate wildcard
      if (($mask & (1 << 31)) == 0) {
      print "WILDCARD\n";
         $mask = ~$mask;
      }
      # find ones following zeros 
      for (my $i=0;$i<32;$i++) {
         if (($mask & (1 << (31-$i))) == 0) {
            $saw_zero = 1;
         } else {
            if ($saw_zero) {
      print "INVALID NETMASK\n";
               return -1;
	    }
         }
      }
      return $mask;
   }
}

sub ntoa 
{
   return join ".",unpack("CCCC",pack("N",shift));
}

sub ntobitcountmask
# expects integer
# returns bitcountmask
{
   my $mask = shift;
   my $bitcountmask = 0;
   # find first zero
   while ( ($mask & (1 << (31-$bitcountmask))) != 0 ) {
      if ($bitcountmask > 31) {
         last;
      }
      $bitcountmask++;
   }
   return $bitcountmask;
}

# ------- documentation ----------------------------------------

sub usage {
    print << "EOF";
Usage: ipcalc [options] <ADDRESS>[[/]<NETMASK>] [NETMASK]

ipcalc takes an IP address and netmask and calculates the resulting broadcast, 
network, Cisco wildcard mask, and host range. By giving a second netmask, you 
can design sub- and supernetworks. It is also intended to be a teaching tool 
and presents the results as easy-to-understand binary values. 

 -n --nocolor  Don't display ANSI color codes.
 -b --nobinary Suppress the bitwise output.
 -c --class    Just print bit-count-mask of given address.
 -h --html     Display results as HTML (not finished in this version).
 -v --version  Print Version.
 -s --split n1 n2 n3
               Split into networks of size n1, n2, n3.
 -r --range    Deaggregate address range.
    --help     Longer help text.
 
Examples:

ipcalc 192.168.0.1/24
ipcalc 192.168.0.1/255.255.128.0
ipcalc 192.168.0.1 255.255.128.0 255.255.192.0
ipcalc 192.168.0.1 0.0.63.255


ipcalc <ADDRESS1> - <ADDRESS2>  deaggregate address range

ipcalc <ADDRESS>/<NETMASK> --s a b c
                                split network to subnets
				where a b c fits in.

! New HTML support not yet finished.

ipcalc $version
EOF
}

sub help {
    print << "EOF";
    
IP Calculator $version

Enter your netmask(s) in CIDR notation (/25) or dotted decimals (255.255.255.0).
Inverse netmask are recognized. If you mmit the netmask, ipcalc uses the default
netmask for the class of your network.

Look at the space between the bits of the addresses: The bits before it are 
the network part of the address, the bits after it are the host part. You can
see two simple facts: In a network address all host bits are zero, in a 
broadcast address they are all set. 

The class of your network is determined by its first bits. 

If your network is a private internet according to RFC 1918 this is remarked. 
When displaying subnets the new bits in the network part of the netmask are 
marked in a different color. 

The wildcard is the inverse netmask as used for access control lists in Cisco 
routers. You can also enter netmasks in wildcard notation. 

Do you want to split your network into subnets? Enter the address and netmask 
of your original network and play with the second netmask until the result 
matches your needs. 


Questions? Comments? Drop me a mail... 
krischan at jodies.de
http://jodies.de/ipcalc

Thanks for your nice ideas and help to make this tool more useful: 

Bartosz Fenski
Denis A. Hainsworth
Foxfair Hu
Frank Quotschalla
Hermann J. Beckers
Igor Zozulya
Kevin Ivory
Lars Mueller
Lutz Pressler
Oliver Seufer
Scott Davis
Steve Kent
Sven Anderson
Torgen Foertsch

EOF
usage();
exit;
}
