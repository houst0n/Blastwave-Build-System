#
# spec file for package BLASTvim
#
# includes module(s): vim
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    BLASTvim
Summary:                 Vi IMproved Text Editor
Version:                 7.3
Source:			 ftp://ftp.vim.org/pub/vim/unix/vim-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: BLASTncursesw

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%prep
rm -rf vim73
%setup -q -n vim73

%build
export CFLAGS="-m64 -I/opt/blast/include -I/opt/blast/include/ncursesw "
export CPPFLAGS="-m64 -I/opt/blast/include -I/opt/blast/include/ncursesw "
export LDFLAGS="-m64 -R/opt/blast/lib/amd64 -L/opt/blast/lib/amd64 -lncursesw"

./configure --prefix=%{_prefix}			\
                 --bindir=%{_bindir}			\
                 --mandir=%{_mandir}                 \
                 --sysconfdir=%{_sysconfdir}       \
		 --enable-gui=no \
		 --without-x \
		 --enable-multibyte \
		 --disable-xim \
		 --with-features=big

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_mandir}/fr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/vim
%{_datadir}/vim/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun March 11 2012 - Initial SPEC - nh

