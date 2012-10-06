%define		major		1
%define		libname		%mklibname %{name} %{major}
%define		develname	%mklibname %{name} -d

Name:		OpenColorIO
Version:	1.0.7
Release:	1
Summary:	Enables color transforms and image display across graphics apps
Group:		System/Libraries
License:	BSD
URL:		http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.7
Source0:	imageworks-%{name}-v%{version}-0-g87da508.tar.gz
# Dot set soname for python modules.
Patch0:		OpenColorIO-1.0.7-pylib_no_soname.patch
# Exclude hidden files from being packaged.
Patch1:		OpenColorIO-1.0.7-docfix.patch
BuildRequires:	cmake
BuildRequires:	python-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)

#######################
# Unbundled libraries #
#######################
BuildRequires:	tinyxml-devel
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	yaml-cpp-devel >= 0.3.0

%description
OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.

%package -n %{libname}
Summary:	Enables color transforms and image display across graphics apps
Group:		System/Libraries

%description -n %{libname}
Enables color transforms and image display across graphics apps.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for %{name} library.

%prep
%setup -q -n imageworks-%{name}-b3cb224
%patch0 -p1 -b .pylib
%patch1 -p1 -b .docfix

# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*

%build
%cmake	-DCMAKE_SKIP_RPATH=TRUE \
	-DOCIO_BUILD_STATIC=OFF \
	-DPYTHON_INCLUDE_LIB_PREFIX=OFF \
	-DOCIO_BUILD_DOCS=ON \
	-DOCIO_BUILD_TESTS=ON \
	-DOCIO_LINK_PYGLUE=ON \
	-DOCIO_PYGLUE_SONAME=OFF \
	-DUSE_EXTERNAL_YAML=TRUE \
	-DUSE_EXTERNAL_TINYXML=TRUE \
	-DUSE_EXTERNAL_LCMS=TRUE \
%ifnarch x86_64
	-DOCIO_USE_SSE=OFF
%endif
PYTHONDONTWRITEBYTECODE= %make

%install
%makeinstall_std -C build

%files
%doc ChangeLog LICENSE README
%{_bindir}/*
%{python_sitearch}/Py%{name}.so
%{_datadir}/ocio

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_includedir}/Py%{name}

