Name:                zlib
Summary:             A free, lossless data compression lib
Version:             1.2.6
Source:              http://zlib.net/zlib-%{version}.tar.gz
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
	    --libdir=%{_libdir}	

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Initial spec - March 11 / 2012 - NH
