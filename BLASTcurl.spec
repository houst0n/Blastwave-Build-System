# spec file for package BLASTcurl
#
# includes module(s): curl

%include Solaris.inc
%include opt-blast.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use curl_64 = curl.spec
%endif

%include base.inc
%use curl = curl.spec

Name:                    BLASTcurl
Summary:                 CURL URL
Version:                 7.24.0
Source:			 http://curl.haxx.se/download/curl-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


Requires:		 BLASTzlib


%prep
rm -rf curl-%{version}
mkdir curl-%{version}

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
mkdir curl-%version/%_arch64
%curl_64.prep -d curl-%version/%_arch64
%endif

mkdir curl-%version/%{base_arch}
%curl.prep -d curl-%version/%{base_arch}

%build
if [ "x`basename $CC`" != xgcc ]
then
        FLAG64="-xarch=generic64"
else
        FLAG64="-m64"
fi

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
%curl_64.build -d curl-%version/%_arch64
%endif

export LDFLAGS=
%curl.build -d curl-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%curl_64.install -d %name-%version/%_arch64
# 64-bit binaries are of no benefit
rm -rf $RPM_BUILD_ROOT%{_bindir}/%_arch64
%endif

%curl.install -d curl-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun March 11 2012 - Initial SPEC - nh

