#!/usr/bin/perl  

# CGI Wrapper for IPv4 Calculator
# 
# Copyright (C) Krischan Jodies 2000 - 2005
# krischan()jodies.de, http://jodies.de/ipcalc
# 
# Copyright (C) for the graphics ipcalc.gif and ipcalculator.png 
# Frank Quotschalla. 2002 
#  
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


# 0.14.3
# 0.15   25.09.2000 Added link to this wrapper
# 0.16   07.11.2000 Get version from ipcalc
# 0.17   09.01.2001 Added screenshot
# 0.18   02.02.2001 Played with the html
# 0.18.1 03.02.2001 Played even more with the html
# 0.19   01.04.2001 Help text for wildcard netmask / Credits
# 0.20   20.05.2001 Changed error messages
# 0.21   19.06.2001 Adapted to new -c option
# 0.22   30.07.2002 Stole javascript at dict.leo.org
# 0.23	 28.10.2004 Remove whitespace in input fields
#                   Idea by David Shirlay David.Shirley(a)team.telstra.com
# 0.24   07.07.2005 Added license text to cgi-wrapper. Add style into cgi script
# 0.25	 11.01.2006 Link to screenshot was wrong.
# 0.26   27.07.2006 Replaced REQUEST_URI with SCRIPT_URL to prevent cross-site-scripting attacks

$|=1;
$ipcalc = "/usr/local/bin/ipcalc";
$MAIL_ADDRESS="ipcalc-200502&#64;jodies.de";
# history:
# 200404 
$actionurl = $ENV{'SCRIPT_URL'};
$actionurl =~ s/&/&amp;/g;
use CGI;
$query = new CGI;
$host  = $query->param('host');
$mask1 = $query->param('mask1');
$mask2 = $query->param('mask2');
$help  = $query->param('help');

$host  =~ s/ //g;
$mask1 =~ s/ //g;
$mask2 =~ s/ //g;


$version = qx($ipcalc -v);
chomp $version;

if (! defined $host) {
	$host = '';
}

if (! defined $mask1) {
	$mask1 = '';
	$help = 1;
}

if (! defined $mask2) {
	$mask2 = '';
}

if ($mask2 eq $mask1) {
	$mask2 = '';
}

if ($host eq '') {
	$error .= "&nbsp;No host given\n";
	$host = '192.168.0.1';
}

$testhost = $host;
$testhost =~ s/\.//g;
if ($testhost !~ /^\d+$/) {
	$error .= "&nbsp;Illegal value for host ('$host')\n";
	$host = '192.168.0.1';
}


if ($mask1 eq '') {
	$error .= "&nbsp;No netmask given (using default netmask of your network's class)\n";
	$mask1 = qx($ipcalc -c $host);
}


$testhost = $mask1;
$testhost =~ s/\.//g;
if ($testhost !~ /^\d+$/) {
	$error .= "&nbsp;Illegal value for netmask ('$mask1')\n";
	$mask1 = 24;
}

if ($mask2 ne '') {
	$testhost = $mask2;
	$testhost =~ s/\.//g;
	if ($testhost !~ /^\d+$/) {
		$error .= "&nbsp;Illegal value for netmask for sub/supernet ('$mask2')\n";
		$mask2 = '';
	}
}


print $query->header;
print << "EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">
<html>
   <head> 
   <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15">
   <title>IP Calculator / IP Subnetting</title>
   <link rel="shortcut icon" href="http://jodies.de/favicon.ico">
   <script language="JavaScript" type="text/javascript">
      <!-- 
      function setFocus()
      {
         document.form.host.focus();
         document.form.host.select();
      }
      // -->
   </script>

<style>
<!--
body {
   background-color: white;
   background-image: url("bg.gif");
   color: black;
   font-family: "Trebuchet MS", Verdana, Geneva, Helvetica, sans-serif;
   l//ine-height: 110%;
   l//ine-height: 1.4em;
}

A {text-decoration:none; color:#003CD7; }
A:visited {color:#003CD7;}
A:hover {background-color:#dddddd;}

h1 {
   margin-bottom: 30px;
}

table {
	border-spacing: 1px;
	border-style: solid;
	border-color: #888888;
	border-width: 0px;
}


input.text {
   border: solid 1px #000000;
}

.help {
   cursor:help;
}

input:focus, textarea:focus {
   background-color: #e9edf5;
}

div#help {
   border-color: black;
   border-style: dotted;
   border-width: 0px;
   border-spacing: 5px;
   margin: 5px;
   margin-bottom: 10px;
}

div#formfield {
   border-color: black;
   border-style: dotted;
   border-width: 1px;
   border-spacing: 5px;
   margin: 5px;
   padding: 5px;
}

-->
</style>
</head>
<body onLoad="setFocus()">
EOF
#print "$ENV{HTTP_USER_AGENT}<br>\n";

print << "EOF";
<center>


<table cellpadding=15 border=0 cellspacing=50><tr><td bgcolor="#ffffff">
<table border=0 width="100%">
<tr>
<td valign="top">&nbsp;</td>
<td><a href="http://jodies.de/ipcalc"><img src="ipcal03.gif" align=right width=100 height=95 border=0 alt=""></a></td></tr>
</table>
EOF
if ($help) {
print << "EOF";
<div id="help">
   <table border=0 bgcolor="#000000" cellpadding=0 cellspacing=1>
   <tr>
      <td>
         <table bgcolor="#e9edf5" border=0 width=550 cellpadding=10 cellspacing=1>
	    <tr>
	       <td>
<h1>IP Calculator</h1>

<p><a href="http://jodies.de/ipcalc">ipcalc</a> takes an IP address and netmask and calculates the resulting broadcast,
network, Cisco wildcard mask, and host range. By giving a second netmask, you
can design subnets and supernets. It is also intended to be a teaching tool
and presents the subnetting results as easy-to-understand binary values.</p>

<p>Enter your netmask(s) in <a href="http://www.ietf.org/rfc/rfc1517.txt">CIDR</a> notation (/25) or dotted decimals (255.255.255.0). 
Inverse netmasks are recognized.
If you omit the netmask ipcalc uses the default netmask for the class of your network.</p>

<p>Look at the space between the bits of the addresses: The bits before it are
the network part of the address, the bits after it are the host part. You can
see two simple facts: In a network address all host bits are zero, in a
broadcast address they are all set.</p>

<p>The class of your network is determined by its first <font color="#009900">bits</font>.</p>

<p>If your network is a private internet according to RFC 1918 this is remarked.
When displaying subnets the new bits in the network part of the netmask are
marked in a <font color="#663366">different color</font></p>

<p>The <a href="http://www.cisco.com/univercd/cc/td/doc/product/software/ssr83/ptc_r/22057.htm">wildcard</a> is the inverse
netmask as used for access control lists in Cisco routers.</p>

<p>Do you want to split your network into subnets? Enter the address and netmask
of your original network and play with the second netmask until the result matches your needs.</p>


<p>You can have all this fun at your shell prompt. Originally ipcalc was not intended for 
creating HTML and still works happily in /usr/local/bin/ :-)</p>

<p>Questions? Comments? Drop me a <a href="mailto:$MAIL_ADDRESS">mail</a>...</p>

<p>Thanks for your ideas and help to make this tool more useful:</p>

<pre>
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
Tim Brown


</pre>
               </td>
	    </tr>
	 </table>
      </td>
   </tr>
   </table>
</div>
EOF
}

print <<"EOF";
<div id="formfield">
   <form action="$actionurl" method="get" name="form" id="form">
   <table border=0>
   <tr>
      <td><b>Address</b> (Host or Network)</td>
      <td><b>Netmask</b> (i.e. 24)</td>
      <td><b>Netmask</b> for sub/supernet (optional)</td>
   </tr>
   <tr>
   <td nowrap><input class=text name=host value="$host"> / </td>
   <td nowrap><input class=text name=mask1 value="$mask1"></td>
   <td nowrap> move to: <input class=text name=mask2 value="$mask2"></td>
   </tr>
   <tr>
      <td colspan=3>
      <input class=submit type="submit" value="Calculate">
EOF
if (! $help) {
   print '&nbsp;<input name=help class=help type="submit" value="Help">';
}
print <<"EOF"; 
      </td>
   </tr>
   </table>
   </form>
</div>

<p>

EOF

if (defined $error) {
	$error =~ s/</&lt;/gm;
	$error =~ s/>/&gt;/gm;
	$error =~ s/\n/<br>/g;
	print qq(<font color="#ff0000"><tt>\n);
	print "$error<br>";
	print qq(</tt><font color="#000000">\n);
	
}

system("$ipcalc -h $host $mask1 $mask2");

print <<"EOF";
<br>
<table border=0 width="100%" cellspacing=10>
 <tr>
  
  <td nowrap valign=top>
   <a href="http://jodies.de/ipcalc">
   <img src="ipcalculator.png" alt="Thanks to http://www.netzwerkinfo.de/daemons/ for this ip calculator icon :-)" border=0></a><br>
   <tt><span style="font-size: 8pt;">Version $version</span></tt></td>
 </tr>
</table>
<hr>
<a href="http://jodies.de/ipcalc-archive/">Download</a><br>
<a href="ipcalc.png">Screenshot</a> (ipcalc works also at the prompt)<br>
<a href="http://jodies.de/ipcalc_cgi">CGI wrapper that produced this page</a>.<br>
<a href="ipcalc-archive">Archive</a><br>
Have a look in the archives for the <b>new version 0.38</b>, with the capability to deaggregate network ranges<br>
<a href="ipcalc-faq/win32.html">How to run this under windows</a><br>
Debian users can apt-get install ipcalc<br>
2000-2004 <a href="mailto:$MAIL_ADDRESS">Krischan Jodies</a>

</td></tr></table>
</center>
</body>
</html>
EOF
