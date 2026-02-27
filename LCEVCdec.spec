# TODO: complete apidocs
#
# Conditional build:
%bcond_with	apidocs		# API documentation
#
Summary:	LCEVC Decoder SDK library
Summary(pl.UTF-8):	Biblioteka SDK dekodera LCEVC
Name:		LCEVCdec
Version:	4.0.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/v-novaltd/LCEVCdec/releases
Source0:	https://github.com/v-novaltd/LCEVCdec/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cceb6df703f1129173ec906a802c8945
Patch0:		%{name}-lib-utility.patch
Patch1:		%{name}-link.patch
URL:		https://github.com/v-novaltd/LCEVCdec
BuildRequires:	CLI11-devel
BuildRequires:	cmake >= 3.19.0
BuildRequires:	libfmt-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	nlohmann-json-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	java-plantuml
BuildRequires:	jre
BuildRequires:	python3-breathe >= 4.35.0
BuildRequires:	python3-sphinx_rtd_theme >= 3.0.1
BuildRequires:	python3-sphinxcontrib-plantuml >= 0.30
BuildRequires:	sphinx-pdg >= 8.0.2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Low Complexity Enhancement Video Codec Decoder (LCEVCdec) is the
primary MPEG-5 Part 2 decoder SDK maintained by V-Nova.

To learn what the LCEVC codec is and how it works, please refer to the
V-Nova documentation portal:
<https://docs.v-nova.com/v-nova/lcevc/lcevc-sdk-overview>.

%description -l pl.UTF-8
Dekoder kodeka LCEVC (Low Complexity Enhancement Video Codec), czyli
LCEVCdec, to główne SDK dekodera MPEG-5 Part 2 utrzymywane przez firmę
V-Nova.

Więcej o kodeku LCEVC i jego działaniu można dowiedzieć się z
dokumentacji V-Nova:
<https://docs.v-nova.com/v-nova/lcevc/lcevc-sdk-overview>.

%package devel
Summary:	Header files for LCEVC Decoder libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek dekodera LCEVC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LCEVC Decoder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek dekodera LCEVC.

%package static
Summary:	Static LCEVC Decoder libraries
Summary(pl.UTF-8):	Biblioteki statyczne dekodera LCEVC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LCEVC Decoder libraries.

%description static -l pl.UTF-8
Biblioteki statyczne dekodera LCEVC.

%package apidocs
Summary:	API documentation for LCEVC Decoder library
Summary(pl.UTF-8):	Dokumentacja API bibliotek dekodera LCEVC
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for LCEVC Decoder libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek dekodera LCEVC.

%prep
%setup -q
# patch0 to get liblcevc_dec_utility.a
%patch -P0 -p1
%patch -P1 -p1

# fake for git archive, not checkout
printf RELEASE > .githash
printf RELEASE > .gitlonghash
printf RELEASE > .gitbranch
printf %{version} > .gitversion
printf %{version} > .gitshortversion
printf 2026-02-09 > .gitdate

%build
install -d build
cd build
%cmake .. \
	-DVN_SDK_JSON_CONFIG=ON \
	%{?with_apidocs:-DVN_SDK_DOCS=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed if tests/examples SDK not enabled
cp -p build/lib/{liblcevc_dec_color_conversion,liblcevc_dec_overlay_images}.a $RPM_BUILD_ROOT%{_libdir}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/licenses/{COPYING,LICENSE.md}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING LICENSE.md README.md
%{_libdir}/liblcevc_dec_api.so.*.*.*
%ghost %{_libdir}/liblcevc_dec_api.so.4
%{_libdir}/liblcevc_dec_legacy.so.1
%{_libdir}/liblcevc_dec_pipeline_cpu.so.1
%{_libdir}/liblcevc_dec_pipeline_legacy.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblcevc_dec_api.so
%{_libdir}/liblcevc_dec_legacy.so
%{_libdir}/liblcevc_dec_pipeline_cpu.so
%{_libdir}/liblcevc_dec_pipeline_legacy.so
%{_libdir}/liblcevc_dec_color_conversion.a
%{_libdir}/liblcevc_dec_extract.a
%{_libdir}/liblcevc_dec_overlay_images.a
%{_libdir}/liblcevc_dec_utility.a
%{_includedir}/LCEVC
%{_pkgconfigdir}/lcevc_dec.pc
%{_pkgconfigdir}/lcevc_dec_extract.pc
%{_pkgconfigdir}/lcevc_dec_utility.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblcevc_dec_api_utility.a
%{_libdir}/liblcevc_dec_common.a
%{_libdir}/liblcevc_dec_enhancement.a
%{_libdir}/liblcevc_dec_pipeline.a
%{_libdir}/liblcevc_dec_pixel_processing.a
%{_libdir}/liblcevc_dec_sequencer.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/sphinx/docs/*
%endif
