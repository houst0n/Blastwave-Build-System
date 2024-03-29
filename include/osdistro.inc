#
#
#   STRONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO1: test logic for correctness
# TODO2: extend rules to match Solaris 10 / SVR4
# TODO3: add copyright (CDDL?)


#
# Macro definitions for Solaris OS build version and distribution detection
#

# note for new OS releases: Follow the marks NEWRELEASE in his include file
# to add new code for detection these new releases
# hint: use the search function of your editor with the pattern NEWRELEASE
#       and copy an old block, then edit. Keep the order to not break the logic

# note this fails havily if you are "BFU"ing your box
# (if you don't use BFU / don't know what BFU is, you don't need to take care of)


# detect OS distro and os build version if possible
# distinguish between SXCE and os20nn.nn, set distro numbers for "osbuild > nnn" logic
# try to detect the distro release in example of os20nn.nn
# and provide boolean flags e.g. %os200902  <0|1>
# and provide test numbers with a distro releasenumber %osdistrelnumber  201003
# and provide test strings with a short distro releasename %osdistrelname  "os2010.03"

# see also the include file "packagenamemakros.inc" for
# already predefined "BuildRequires" and "Requires" depending
# on the distro and build number, leveraging the detection from 
# this osversion.inc include file
# should simplify sharing spec files between SXCE and os20nn.nn


# usage/examples:
# if you depend on a package which for instance got some day a rename:
# (or dissapeared, newly introduced, merged into another package
# this is not limited to these examples (think of switching off SVR4 package
# scripting, ...).
#
# %if %( expr %{osbuild} '>=' 100 )
# BuildRequires: SUNWnewname
# %else
# BuildRequires: SUNWoldname
# %endif

#TO BE CHECKED # *if* we are on os20nn.nn *and* build is younger|equal then 118
#TO BE CHECKED # %if %os2nnn %( expr %osbuild '>=' 118 )
#TO BE CHECKED # BuildRequires: newpackagename
#TO BE CHECKED # %else
#TO BE CHECKED # BuildRequires: SUNWoldname
#TO BE CHECKED # %endif

#TO BE CHECKED # same as above but based on the os20nn.nn distro, example os2009.06 and above
#TO BE CHECKED # %if %( expr %os2nnndistro '>=' 200906 && echo 1 || echo 0 )
#TO BE CHECKED # BuildRequires: newpackagename
#TO BE CHECKED # %else
#TO BE CHECKED # BuildRequires: SUNWoldname
#TO BE CHECKED # %endif

### end of examples
### rules below need extensions with every major distro release

#osdistro.inc is included --- NOTE: this variable is primarily for internal use by osdistro.inc
%define osdistro 1

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')
#special handling for release builds: uname -v prints 11.0 or similar 
#which might correspond to build 175 (needs refinement)
%if %( uname -v | egrep '^11\.[0-9]' > /dev/null && echo 1 || echo 0 )
##TODO## be more precise later, for build 173 and 174 and later SRU
%define osbuild 175
%endif 

# see if we are on old SVR4 release
%define SXCE %( egrep "Solaris Express Community Edition" /etc/release > /dev/null 2>&1 && echo 1 || echo 0 )


#switches for major distro releases
# os2nnn is defined 1 if we can detect the OpenSolaris (IPS based) distro
# 
# an estimate is done to tell which distro release is present
#NEWRELEASE add to the table    (OpenSolaris releases as os2......)
# os2008.11    os2009.06    os2009.11    os2010.03    os2010.05  
# corresponds to:
# os200811     os200906     os200911     os201003     os201005   
#
# Solaris11Express_firstrelease Solaris11Express_following OpenIndiana147 OpenIndiana151
##TODO## replace the "*00" to be the real release month
# s11ex201011                   s11ex201000                oi201009       oi201100

#numbers for each major distro release are stored in %os2nnnversion

#Flags - who knows what that's worth for
#set defaults to null - reverse order to catch youngest distro first 
#and then used to skip the other detection rules for older releases
#NEWRELEASE add to the table

#boolean flags for major osdistro names
#no versioning here
%define openindiana 0
%define solaris11express 0

#boolean flags for major osdistro names - *with* versioning the releases
#use osbuild in addition to finer granularity, e.g. osbuild >= 148
#OpenSolaris and Solaris11Express below. We need something to tell the release as well
#Solaris11Express gets its own name prefix though it's close to what OpenSolaris was

#OpenIndiana
# could be oi201009 and oi201100 or something, the first development release and following
##TODO## replace oi201100
%define oi201100 0
%define oi201009 0

#Solaris 11 Express and OpenSolaris
##TODO## replace s11ex201100
%define s11ex201100 0
%define s11ex201011 0
#OpenSolaris
%define os201005 0
#never apperared: (this variable might go away some day)
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0


# one of the IPS style OpenSolaris distro releases is present if os2nnn set to "1"
# set default to "0" which is good
# includes OI
%define os2nnn        0

# make your logic work with the major distro number  %if %( expr %os2nnndistro '>=' 200906 )
# set default to "0" which is good
# includes OI
%define osdistrelnumber 0

# set readable name for this os distribution  (not for SXCE)
%define osdistrelname   "not detected"

# Note osdet299999 is a helper variable. Specs should use %if %os2nnn ... and %os2nnndistro
# Make default to "1" to enable the os20nn.nn detection steps below.
# for readability see separated %if where a present %SXCE resets this switch to "0" and disables all remaining checks
%define osdet299999 1

# we are on SXCE, so skip the all other os2nnn detection rules and leave %os**** defaults at "0"
%if %SXCE
#no more work to do
%define osdet299999 0
%define osdistrelname   "SXCE"
%endif


# try detecting the distro release we are on
# might need more fine grained rules some day?

#(os2010.03)
#e.g. OpenSolaris 2010.03 snv_134 X86

#NEWRELEASE carefull: add new releases *always* on top of the predecessor version.
#NEWRELEASE for that, copy the example from below (START to END) and change numbers
#NEWRELEASE you might need *many* places in the block edited. be *carefull* please and double-check and 
#NEWRELEASE do not forget to change the variables names too!

#NEWRELEASE *add* new version  *here* (below)



#note: build 166 (maybe earlier) does read "Oracle Solaris 11 snv_166 X86"
#note: build 160 (2010.11++) does read "Oracle Solaris 11 Express snv_160 X86"
#note: build 151a 2010.11 does read "Oracle Solaris 11 Express snv_156 X86"
#note: build 140 does read "Solaris Next Development"
#note: build 134 does read "OpenSolaris Development"
#below probably release of 2010.05 (was 2010.03 or whatever name)


##START build 151 and up, OpenIndiana
#NOTE: we try to set a resonable opensolaris/solaris express release
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
%if %( egrep 'OpenIndiana Development' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define openindiana 1
##TODO## replace oi201100
%define oi201100    1
%define osdistrelnumber 151
#                                below: subject to change!
%define osdistrelname   "OpenIndiana"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 147 and up, OpenIndiana
#NOTE: we try to set a resonable opensolaris/solaris express release
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 147 )
%if %( egrep 'OpenIndiana Development' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define openindiana 1
%define oi201009    1
%define osdistrelnumber 147
#                                below: subject to change!
%define osdistrelname   "OpenIndiana"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build *greater then* 151, this is 152 and up, detect "Oracle Solaris 11 snv_166 X86" aka 2011.00 as s11ex201100
#NOTE: s11ex201100 <- 00 - nothing is released, to use "00" as placeholder in year 2011
#NOTE: we try to set a resonable release number in %osdistrelnumber
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 152 )
%if %( egrep 'Oracle Solaris 11 ' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
##TODO## replace s11ex201100
%define s11ex201100 1
%define solaris11express 1
##TODO## replace 201100
%define osdistrelnumber 201100
#                                below: subject to change!
%define osdistrelname   "Solaris 11 Express"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 151 and up, detect "Oracle Solaris 11 Express snv_151a X86" aka 2010.11 as s11ex201011
#NOTE: we try to set a resonable release number in %osdistrelnumber
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
%if %( egrep 'Oracle Solaris 11 Express' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define s11ex201011 1
%define solaris11express 1
%define osdistrelnumber 201011
#                                below: subject to change!
%define osdistrelname   "Solaris 11 Express"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 134 and up, os2010.05 as os201005
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 134 )
%if %( egrep 'Solaris Develop|Solaris Next Develop' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
%define os201005 1
%define osdistrelnumber 201005
%define osdistrelname   "os2010.05"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 111 and up, os2009.06 as os200906
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 111 )
%if %( egrep "OpenSolaris 2[0-9][0-9][0-9]" /etc/release > /dev/null  && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os200906 1
%define osdistrelnumber 200906
%define osdistrelname   "os2009.06"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END



##START build 101 and up, os2008.11 as os200811
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 101 )
%if %( egrep "OpenSolaris Develop" /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os200911 1
%define osdistrelnumber 200811
%define osdistrelname   "os2008.11"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END



### bail out, detection of the os2... distribution failed!
###%if %{osdet299999}
###echo "Error. Detection of OS Distribution failed in osdistro.inc"
###exit 1
###%endif


%changelog
* Mon Nov  7 2011 - Thomas Wagner
- add Support for builds (173)(174) as osbuild=175 Oracle Solaris 11 11/11
* Fri Jun 17 2011 - Thomas Wagner
- changed osdistrelname "OI147" to read "OpenIndiana", "os2010.11" to read "Solaris11Express"
- added boolean flags for: openindiana solaris11express oi201009 oi201100 s11ex201011 s11ex201100
- removed boolean flags for: os201011 (renamed to s11ex201011), oi147 (renamed to oi201009)
- added OpenIndiana development release with build 151 number, faked distreleasenumber to oi201100 (00 to be changed later)
- make grep on /etc/release more relaxed on "Oracle Solaris 11 "
* Wed Mar 16 2011 - Thomas Wagner
- add Oracle Solaris 11 Express to the mix
* Sat Oct 20 2010 - Thomas Wagner
- add OI 147 to the mix
* May 31 2010 - Thomas Wagner
- rename 201003/2010.03 to 201005/2010.05 (speculative)
- change egrep for builds >=134 to match OpenSolaris Development and Solaris Next Development
- remove typo os2distrelname -> osdistrelname
- for SXCE %define osdistrelname   "SXCE"
* May  5 2010 - Thomas Wagner
- fix ifs to give echo 0 | echo 1 and not strings or exitcodes
- lot's of fixes over time, especially %if logic is non standard in spec files...
- initial - drafting the idea, bugs are the only feature of this include file
