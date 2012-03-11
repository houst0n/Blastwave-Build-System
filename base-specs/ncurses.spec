# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# Relegating to /opt/blast to avoid name collisions with regular curses files

Name:                ncurses
Summary:             Emulation of SVR4 curses
Version:             5.9
Source:              http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir} $LDFLAGS"

./configure --prefix=%{_prefix}	\
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --with-shared	\
	    --enable-rpath	\
            --mandir=%{_mandir}

# The following hack sets LD_LIBRARY_PATH in run_tic.sh. It's necessary
# because that script -- which is only run during make install -- fails
# to find the ncurses .so libraries when the install is being done with 
# DESTDIR set. If, for your purposes, /opt/blast is not the ultimate destination 
# for installation of this package, you need to adjust this accordingly.

perl -i.orig -lne 'print ; if (/^test -z "\${DESTDIR}" \&\& DESTDIR/) {print q^LD_LIBRARY_PATH="$DESTDIR%{_libdir}"; export LD_LIBRARY_PATH^}' misc/run_tic.sh

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Mar 11 2012 - neil.a.houston@gmail.com
- Bump to 5.9
* Sat Nov 3 2007 - markwright@internode.on.net
- Bump to 5.6.  Set LDFLAGS=-m64 for 64 bit build.
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
