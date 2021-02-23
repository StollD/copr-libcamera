# This is an updated version of the work done by Peter Robinson and
# Dave Olsthoorn in https://bugzilla.redhat.com/show_bug.cgi?id=1738290

# Upstream is https://git.linuxtv.org/libcamera.git, but using the
# Github mirror allows easy use of the forgemeta macros
#
# Upstream is still under development so they're not tagging releases yet
%global forgeurl https://github.com/libcamera-org/libcamera
%global commit   1612841ff156023ff23ae5c8f4d68eeb09840a2a
%forgemeta

Name:    libcamera
Version: 0.0.0
Release: 2%{?dist}
Summary: A library to support complex camera ISPs

# Library is LGPLv2.1+ and the cam tool is GPLv2
License: LGPLv2.1+ and GPLv2
URL:     http://libcamera.org/

Source0: %{forgesource}
Patch1: 0001-GCC-11.patch

# Tools
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: openssl
BuildRequires: ninja-build
BuildRequires: python3-yaml
BuildRequires: python3-jinja2
BuildRequires: python3-ply

# Docs
BuildRequires: python3-sphinx

# Dependencies
BuildRequires: boost-devel
BuildRequires: libatomic
BuildRequires: systemtap-sdt-devel
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(lttng-ust)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libevent_pthreads)
BuildRequires: pkgconfig(glib-2.0)

# Dependencies qcam
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)

# Dependencies gstreamer plugin
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(gstreamer-allocators-1.0)

%description
libcamera is a library that deals with heavy hardware image processing
operations of complex camera devices that are shared between the linux host all
while allowing offload of certain aspects to the control of complex camera
hardware such as ISPs.

Hardware support includes USB UVC cameras, libv4l cameras as well as more
complex ISPs (Image Signal Processor).

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package doc
Summary: %{name} Documentation Files
BuildArch: noarch

%description doc
Documentation files for %{name}

%package utils
Summary: Utilities for %{name}

%description utils
Small utilities for %{name}

%package utils-gui
Summary: GUI Utilities for %{name}

%description utils-gui
Utillities that require a GUI to use

%package gstreamer
Summary: Gstreamer plugin to use %{name}

%description gstreamer
Gstreamer plugins for using cameras with %{name}

%package ipa-rpi
Summary: rpi ipa module for %{name}

%description ipa-rpi
Raspberry Pi Image Processing Algorithm module for %{name}

%package ipa-vimc
Summary: vimc ipa module for %{name}

%description ipa-vimc
Vimc Image Processing Algorithm module for %{name}

%package ipa-rkisp1
Summary: rkisp1 ipa module for %{name}

%description ipa-rkisp1
RkISP1 Image Processing Algorithm module for %{name}

%package ipa-ipu3
Summary: rkisp1 ipa module for %{name}

%description ipa-ipu3
RkISP1 Image Processing Algorithm module for %{name}

%prep
%forgeautosetup -p1

%build
# TODO: LTO breaks %%meson_test find out why
%define _lto_cflags %{nil}

# Unbreak the build on Fedora 34
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"

%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING.rst
%dir %{_libdir}/%{name}/
%{_libdir}/libcamera*.so
%{_libexecdir}/%{name}/

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/camera.pc

%files doc
%doc %{_docdir}/%{name}-%{version}/

%files utils
%{_bindir}/cam

%files utils-gui
%{_bindir}/qcam

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files ipa-rpi
%{_libdir}/%{name}/ipa_rpi.so
%{_libdir}/%{name}/ipa_rpi.so.sign
%{_datadir}/%{name}/ipa/raspberrypi/

%files ipa-vimc
%{_libdir}/%{name}/ipa_vimc.so
%{_libdir}/%{name}/ipa_vimc.so.sign
%{_datadir}/%{name}/ipa/vimc

%files ipa-rkisp1
%{_libdir}/%{name}/ipa_rkisp1.so
%{_libdir}/%{name}/ipa_rkisp1.so.sign

%files ipa-ipu3
%{_libdir}/%{name}/ipa_ipu3.so
%{_libdir}/%{name}/ipa_ipu3.so.sign

%changelog
* Tue Feb 23 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-1.20210223git1612841
- Add systemdtap-sdt-devel to BuildRequires to fix F32 build
- Add small patch to make it build with GCC 11
- Build with -Wno-deprecated-declarations to get the gst plugin to build on F34

* Mon Feb 22 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-1.20210222git1612841
- Updated to latest upstream snapshot
- Included IPA module for IPU3
- Updated BuildRequires

* Sat Sep 12 2020 Dave Olsthoorn <dave@bewaar.me> 0.0.0-0.2.6f09a61
- Rebase to new snapshot
- Include openssl as dependency for signing ipa modules
- Split out to different packages like ipa modules, docs and utils
- Build gstreamer plugin
- Add %%check
- Disable LTO, it makes %%check fail

* Sat Jul 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.0-0.1.36d6229
- Initial package