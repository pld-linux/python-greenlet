#
# Conditional build:
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	tests		# unit tests and benchmarks (any)
%bcond_without	tests_py2	# CPython 2.x module tests

%if %{without tests}
%undefine	with_tests_py2
%endif

%define 	module	greenlet
Summary:	Lightweight in-process concurrent programming
Summary(pl.UTF-8):	Lekkie programowanie równoległe wewnątrz procesu
Name:		python-%{module}
Version:	0.4.14
Release:	1
License:	MIT, PSF (Stackless Python parts)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/greenlet/
Source0:	https://files.pythonhosted.org/packages/source/g/greenlet/%{module}-%{version}.tar.gz
# Source0-md5:	a87b6028c3b742b210bf5973939db595
URL:		https://pypi.org/project/greenlet/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-2to3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-modules >= 1:3.2
%endif
Requires:	python-modules >= 1:2.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# -fno-tree-dominator-opts because https://bugzilla.opensuse.org/show_bug.cgi?id=902146
%define		specflags_x32	-fno-tree-dominator-opts

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%description -l pl.UTF-8
Pakiet greenlet to odprysk projektu Stackless - wersji CPythona
obsługującej mikrowątki zwane "taskletami". Tasklety działają
pseudorównolegle (zwykle w jednym lub kilku wątkach na poziomie
systemu operacyjnego) i są synchronizowane przy wymianie danych
poprzez "kanały".

%package devel
Summary:	C development headers for Python 2 greenlet module
Summary(pl.UTF-8):	Pliki nagłówkowe C dla modułu Pythona 2 greenlet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel >= 1:2.4

%description devel
This package contains header files required for C modules development.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia modułów w
C.

%package -n python3-%{module}
Summary:	Lightweight in-process concurrent programming
Summary(pl.UTF-8):	Lekkie programowanie równoległe wewnątrz procesu
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%description -n python3-%{module} -l pl.UTF-8
Pakiet greenlet to odprysk projektu Stackless - wersji CPythona
obsługującej mikrowątki zwane "taskletami". Tasklety działają
pseudorównolegle (zwykle w jednym lub kilku wątkach na poziomie
systemu operacyjnego) i są synchronizowane przy wymianie danych
poprzez "kanały".

%package -n python3-%{module}-devel
Summary:	C development headers for Python 3 greenlet module
Summary(pl.UTF-8):	Pliki nagłówkowe C dla modułu Pythona 3 greenlet
Group:		Development/Libraries
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-devel >= 1:3.2

%description -n python3-%{module}-devel
This package contains header files required for C modules development.

%description -n python3-%{module}-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia modułów w
C.

%prep
%setup -q -n greenlet-%{version}

%build
%if %{with python2}
%py_build %{?with_tests_py2:test}

%if %{with tests_py2}
# Run the upstream benchmarking suite to further exercise the code:
PYTHONPATH=$(echo $(pwd)/build-2/lib.*-2.?) %{__python} benchmarks/chain.py
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with tests}
# Run the upstream benchmarking suite to further exercise the code:
mkdir -p benchmarks-3
2to3-%{py3_ver} -o benchmarks-3 -n -w --no-diffs benchmarks
PYTHONPATH=$(echo $(pwd)/build-3/lib.*-3.?) %{__python3} benchmarks-3/chain.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.rst doc/greenlet.txt benchmarks
%attr(755,root,root) %{py_sitedir}/greenlet.so
%{py_sitedir}/greenlet-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py_ver}/greenlet
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.rst doc/greenlet.txt benchmarks-3
%attr(755,root,root) %{py3_sitedir}/greenlet.cpython-*.so
%{py3_sitedir}/greenlet-%{version}-py*.egg-info

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{_includedir}/python%{py3_ver}*/greenlet
%endif
