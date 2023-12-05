%global optflags %{optflags} -Wno-error=unused-function
%define	major	2
%define	libname	%mklibname %{name}
%define	devname	%mklibname %{name} -d

%global __requires_exclude ^cmake\\(minizip-ng\\)

Summary:	Enables color transforms and image display across graphics apps
Name:		OpenColorIO
Version:	2.3.0
Release:	1
Group:		System/Libraries
License:	BSD
Url:		http://opencolorio.org/
Source0:        https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v%{version}/%{name}-%{version}.tar.gz
#Patch0:		OpenColorIO-1.1.0-compile.patch
#from mageia
#Patch0:		opencolorio-2.0.1-fix-install.patch
Patch0:		OpenColorIO-zlib-ng.patch
Patch1:		opencolorio-2.0.1-armh-multiple-definition.patch
Patch2:		OpenColorIO-2.2.1-minizip-ng-4.0.patch
# Upstream's attempt to locate yaml-cpp doesn't work with 0.8
Patch3:		ocio-find-yaml-cpp.patch

BuildRequires:	boost-devel
BuildRequires:	cmake ninja
BuildRequires:	git-core
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(pystring)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python-sphinx
#BuildRequires:	pkgconfig(OpenImageIO)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(glew)

# FIXME this is a workaround for incompatibility with current glew and
# glext.h -- should really be a BuildRequires, the BuildConflict works
# around the problem by disabling some optional components.
#BuildConflicts:	pkgconfig(glew)

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
Obsoletes:	%{mklibname %{name} 2} < %{EVRD}

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
%autosetup -p1
# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*
rm -f ext/dist

%if "%{_lib}" != "lib"
sed -i 's|DESTINATION lib|DESTINATION %_lib|' src/OpenColorIO/CMakeLists.txt
%endif

# Let's debug cmake failures instead of just getting weird errors...
find . -name "CMakeLists.txt" -o -name "*.cmake" |xargs sed -i -e 's, QUIET,,'

%build
%cmake \
	-DCMAKE_SKIP_RPATH=TRUE \
	-DOCIO_BUILD_STATIC=OFF \
	-DPYTHON_INCLUDE_LIB_PREFIX=OFF \
	-DOCIO_BUILD_DOCS=OFF \
	-DOCIO_BUILD_TESTS=ON \
	-DOCIO_LINK_PYGLUE=ON \
	-DOCIO_PYGLUE_SONAME=OFF \
	-DUSE_EXTERNAL_YAML=TRUE \
	-DUSE_EXTERNAL_TINYXML=TRUE \
	-DUSE_EXTERNAL_LCMS=TRUE \
%ifnarch %{x86_64}
	-DOCIO_USE_SSE=OFF \
%endif
	-DOCIO_USE_GLVND=ON \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-G Ninja

PYTHONDONTWRITEBYTECODE= %ninja_build

%install
%ninja_install -C build

# Fix location of cmake files.
mkdir -p %{buildroot}%{_datadir}/cmake/Modules
find %{buildroot} -name "*.cmake" -exec mv {} %{buildroot}%{_datadir}/cmake/Modules/ \;


%files
%doc LICENSE README.md
%{_bindir}/*
%{python_sitearch}/Py%{name}.so
%{_datadir}/ocio

%files -n %{libname}
%{_libdir}/libOpenColorIO.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/lib*helpers.a
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/cmake/Modules/
