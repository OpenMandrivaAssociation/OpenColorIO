%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Summary:	Enables color transforms and image display across graphics apps
Name:		OpenColorIO
Version:	1.0.9
Release:	1
Group:		System/Libraries
License:	BSD
Url:		http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.9
Source0:        %{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(zlib)

#######################
# Unbundled libraries #
#######################
BuildRequires:	tinyxml-devel
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(yaml-cpp)

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

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name} library.

%prep
%setup -q
%apply_patches

# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*

%build
%cmake \
	-DCMAKE_SKIP_RPATH=TRUE \
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
%{_libdir}/libOpenColorIO.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_includedir}/Py%{name}

