#
# spec file for package: [pkg name]
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): [pkg module(s)]
# 

# Definition of path to STDCXX

%define with_sfestdcxx %(pkginfo -q BLASTstdcxx && echo 1 || echo 0)

%if %with_sfestdcxx
%define stdcxx_dir /usr/stdcxx 
%define stdcxx_lib %{stdcxx_dir}/lib
%define stdcxx_include %{stdcxx_dir}/include
%else
%define stdcxx_dir /usr
%define stdcxx_lib %{stdcxx_dir}/lib
%define stdcxx_include %{stdcxx_dir}/include/stdcxx4
%endif
%define stdcxx_version 4.2.1

%if %with_sfestdcxx
%define stdcxx_cxxflags %{cxx_optflags} -library=no%Cstd -mt -L%{stdcxx_lib} -R%{stdcxx_lib} -I%{stdcxx_include}
%define stdcxx_ldflags %{_ldflags} -library=no%Cstd -mt -L%{stdcxx_dir} -R%{stdcxx_dir} -lstdcxx4
%else
%define stdcxx_cxxflags %{cxx_optflags} -library=no%Cstd -mt -I%{stdcxx_include}
%define stdcxx_ldflags %{_ldflags} -library=no%Cstd -lstdcxx4 -mt
%endif
