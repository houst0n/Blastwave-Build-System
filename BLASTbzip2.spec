#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include opt-blast.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use bzip2_64 = bzip2.spec
%endif

%include base.inc
%use bzip2 = bzip2.spec

Name:		     bzip2
Summary:             High quality, open source data compression
Version:	     1.0.6
Source:		     http://www.bzip.org/1.0.6/bzip2-%{version}.tar.gz
Patch1:		     bzip2-64-bin.patch 
Patch2:		     bzip2-64-lib.patch
Patch3:		     bzip2-32-bin.patch
Patch4:		     bzip2-32-lib.patch
SUNW_BaseDir:	     %{_basedir}
BuildRoot:	     %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

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
%bzip2_64.prep -d %name-%version/%_arch64
%patch1 -p0
%patch2 -p0
%endif

mkdir %name-%version/%{base_arch}
%bzip2.prep -d %name-%version/%{base_arch}
%patch3 -p0
%patch4 -p0

%build

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
%bzip2_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS=
%bzip2.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%bzip2.install -d %name-%version/%{base_arch}

%ifarch amd64 sparcv9
%bzip2_64.install -d %name-%version/%_arch64
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Mar 12 2012 - neil.a.houston@gmail.com
- Initial SPEC
