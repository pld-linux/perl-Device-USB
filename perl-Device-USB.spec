#
# Conditional build:
%bcond_with	tests		# perform "make test"

%define		pdir	Device
%define		pnam	USB
%include	/usr/lib/rpm/macros.perl
Summary:	Device::USB - Use libusb to access USB devices
Name:		perl-Device-USB
Version:	0.36
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://search.cpan.org/CPAN/authors/id/G/GW/GWADEJ/Device-USB-%{version}.tar.gz
# Source0-md5:	aa91bee777f7ed7a18225a84f8795344
Patch0:		fix-buildsystem.patch
Patch1:		hardening-flags.patch
Patch2:		just-assume-libusb-is-there.patch
URL:		http://search.cpan.org/dist/Device-USB/
%if "%{pld_release}" == "ac"
BuildRequires:	libusb-devel < 1.0
%else
BuildRequires:	libusb-compat-devel
%endif
BuildRequires:	perl-Inline
BuildRequires:	perl-Inline-C
BuildRequires:	perl-Parse-RecDescent
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides a Perl interface to the C library libusb. This
library supports a relatively full set of functionality to access a
USB device. In addition to the libusb, functioality, Device::USB
provides a few convenience features that are intended to produce a
more Perl-ish interface.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# function names conflict with libusb-1.0
sed -e 's/libusb_/DeviceUSB_/g' -i lib/Device/USB.pm lib/Device/USB/Device.pm
rm USB.pm
ln -s lib/Device/USB.pm .

%build
export LIBUSB_LIBDIR="%{_libdir}"
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} -j1

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README dump_usb.pl
%{perl_vendorarch}/Device/*.pm
%{perl_vendorarch}/Device/USB
%dir %{perl_vendorarch}/auto/Device/USB
%attr(755,root,root) %{perl_vendorarch}/auto/Device/USB/*.so
%{_mandir}/man3/*
