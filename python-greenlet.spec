#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	greenlet
Summary:	Lightweight in-process concurrent programming
Name:		python-%{module}
Version:	0.3.1
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		http://pypi.python.org/pypi/greenlet
Source0:	http://pypi.python.org/packages/source/g/greenlet/%{module}-%{version}.tar.gz
# Source0-md5:	8d75d7f3f659e915e286e1b0fa0e1c4d
# Based on https://bitbucket.org/ambroff/greenlet/changeset/2d5b17472757
# slightly fixed up to apply cleanly. Avoid rhbz#746771
Patch1:		get-rid-of-ts_origin.patch
# Apply https://bitbucket.org/ambroff/greenlet/changeset/25bf29f4d3b7
# to fix the i686 crash in rhbz#746771
Patch2:		i686-register-fixes.patch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%package devel
Summary:	C development headers for python-greenlet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files required for C modules development.

%prep
%setup -q -n greenlet-%{version}
%patch1 -p1
%patch2 -p1

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%if %{with tests}
# FIXME!!
# The checks segfault on ppc64. So this arch
# is essentially not supported until this is fixed
%ifnarch ppc ppc64 s390 s390x
# Run the upstream test suite:
%{__python} setup.py test

# Run the upstream benchmarking suite to further exercise the code:
PYTHONPATH=$(pwd) %{__python} benchmarks/chain.py
PYTHONPATH=$(pwd) %{__python} benchmarks/switch.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/greenlet.txt README benchmarks AUTHORS NEWS
%attr(755,root,root) %{py_sitedir}/%{module}.so
%{py_sitedir}/%{module}*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py_ver}/greenlet
