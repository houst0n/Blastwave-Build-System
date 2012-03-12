# BZIP2 Base Spec

Name:                bzip2
Summary:             High quality, open source data compression
Version:             1.0.6
Source:              http://www.bzip.org/1.0.6/bzip2-%{version}.tar.gz
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

export PATH=/opt/csw/gcc4/bin:$PATH
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir} $LDFLAGS"

make 
make -f Makefile-libbz2_so 

%install
make install PREFIX=$RPM_BUILD_ROOT/opt/blast
%ifarch amd64 sparcv9
mkdir -p $RPM_BUILD_ROOT/opt/blast/lib/%_arch64
cp libbz2.so.1.0 $RPM_BUILD_ROOT/opt/blast/lib/%_arch64
cp libbz2.so.1.0.6 $RPM_BUILD_ROOT/opt/blast/lib/%_arch64
%endif

%ifarch i386 sparcv8
cp libbz2.so.1.0 $RPM_BUILD_ROOT/opt/blast/lib
cp libbz2.so.1.0.6 $RPM_BUILD_ROOT/opt/blast/lib
%endif

mkdir -p $RPM_BUILD_ROOT/opt/blast/share/man
cp -R $RPM_BUILD_ROOT/opt/blast/man $RPM_BUILD_ROOT/opt/blast/share/man
rm -rf $RPM_BUILD_ROOT/opt/blast/man

cd $RPM_BUILD_ROOT/opt/blast/bin
rm ./bzless ./bzcmp ./bzfgrep ./bzegrep
ln -s bzdiff bzcmp
ln -s bzgrep bzegrep 
ln -s bzgrep bzfgrep 
ln -s bzmore bzless 

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 12 2012 - neil.a.houston@gmail.com
- Initial SPEC
