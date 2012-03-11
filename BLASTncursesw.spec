#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include opt-blast.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use ncursesw_64 = ncursesw.spec
%endif

%include base.inc
%use ncursesw = ncursesw.spec

Name:                BLASTncursesw
Summary:             Emulation of SVR4 curses with wide-character support
Version:             %{ncursesw.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: BLASTncurses
Requires: BLASTncurses-devel


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%ncursesw_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%ncursesw.prep -d %name-%version/%{base_arch}

%build
if [ "x`basename $CC`" != xgcc ]
then
        FLAG64="-xarch=generic64"
else
        FLAG64="-m64"
fi

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
%ncursesw_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS=
%ncursesw.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ncursesw.install -d %name-%version/%{base_arch}

%ifarch amd64 sparcv9
%ncursesw_64.install -d %name-%version/%_arch64
# We don't need the ncursesw bins - they'll just conflict with ncurses
rm -rf $RPM_BUILD_ROOT%{_bindir}/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Mar 11 2012 - neil.a.houston@gmail.com
- Initial SPEC
