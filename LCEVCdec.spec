# TODO: complete apidocs
#
# Conditional build:
%bcond_with	apidocs		# API documentation
#
Summary:	LCEVC Decoder SDK library
Summary(pl.UTF-8):	Biblioteka SDK dekodera LCEVC
Name:		LCEVCdec
Version:	3.3.4
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/v-novaltd/LCEVCdec/releases
Source0:	https://github.com/v-novaltd/LCEVCdec/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5bb2d7180bfa231cf1a4273a7831b6eb
Patch0:		%{name}-includes.patch
Patch1:		%{name}-libdir.patch
URL:		https://github.com/v-novaltd/LCEVCdec
BuildRequires:	cmake >= 3.19.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	nlohmann-json-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	java-plantuml
BuildRequires:	jre
BuildRequires:	python3-breathe >= 4.35.0
BuildRequires:	python3-sphinx_rtd_theme >= 1.2.0
BuildRequires:	python3-sphinxcontrib-plantuml >= 0.25
BuildRequires:	sphinx-pdg >= 6.2.1
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
%patch -P0 -p1
%patch -P1 -p1

# fake for git archive, not checkout
printf RELEASE > .githash
printf RELEASE > .gitlonghash
printf RELEASE > .gitbranch
printf %{version} > .gitversion
printf %{version} > .gitshortversion
printf 2025-03-17 > .gitdate

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING LICENSE.md README.md
%attr(755,root,root) %{_libdir}/liblcevc_dec_api.so
%attr(755,root,root) %{_libdir}/liblcevc_dec_core.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblcevc_dec_api_utility.a
%attr(755,root,root) %{_libdir}/liblcevc_dec_core_sequencing.a
%{_includedir}/LCEVC
%{_pkgconfigdir}/lcevc_dec.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/sphinx/docs/*
%endif
