# This is an updated version of the work done by Peter Robinson and
# Dave Olsthoorn in https://bugzilla.redhat.com/show_bug.cgi?id=1738290

# Upstream is https://git.linuxtv.org/libcamera.git, but using the
# Github mirror allows easy use of the forgemeta macros
#
# Upstream is still under development so they're not tagging releases yet
%global forgeurl https://github.com/libcamera-org/libcamera
%global commit   0445a2dc02e8d686566553c50e89a7e873a964aa
%forgemeta

Name:    libcamera
Version: 0.0.0
Release: 10%{?dist}
Summary: A library to support complex camera ISPs

# Library is LGPLv2.1+ and the cam tool is GPLv2
License: LGPLv2.1+ and GPLv2
URL:     http://libcamera.org/

Source0: %{forgesource}

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
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Small utilities for %{name}

%package utils-gui
Summary: GUI Utilities for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils-gui
Utillities that require a GUI to use

%package gstreamer
Summary: Gstreamer plugin to use %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gstreamer
Gstreamer plugins for using cameras with %{name}

%package ipa-rpi
Summary: rpi ipa module for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description ipa-rpi
Raspberry Pi Image Processing Algorithm module for %{name}

%package ipa-vimc
Summary: vimc ipa module for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description ipa-vimc
Vimc Image Processing Algorithm module for %{name}

%package ipa-rkisp1
Summary: rkisp1 ipa module for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description ipa-rkisp1
RkISP1 Image Processing Algorithm module for %{name}

%package ipa-ipu3
Summary: ipu3 ipa module for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description ipa-ipu3
IPU3 Image Processing Algorithm module for %{name}

%prep
%forgeautosetup -p1

%build
# TODO: LTO breaks %%meson_test find out why
%define _lto_cflags %{nil}

# Unbreak the build on Fedora 34
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"

%meson -Dv4l2=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING.rst
%dir %{_libdir}/%{name}/
%{_libdir}/libcamera.so
%{_libdir}/v4l2-compat.so
%{_libexecdir}/%{name}/

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/camera.pc

%files doc
%doc %{_docdir}/%{name}-%{version}/

%files utils
%{_bindir}/cam
%{_bindir}/lc-compliance

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
* Thu May 13 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-10.20210513git0445a2
- Updated to latest upstream snapshot

* Thu Apr 22 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-9.20210422git9e1bd62
- Add lc-complicance to %%files

* Thu Apr 22 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-8.20210422git9e1bd62
- Updated to latest upstream snapshot

* Wed Apr 07 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-7.20210407git76a5861
- Updated to latest upstream snapshot

* Fri Mar 19 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-6.20210319git79b4822
- Updated to latest upstream snapshot

* Wed Mar 10 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-5.20210310gitd3cf0fe
- Updated to latest upstream snapshot

* Sat Feb 27 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-4.20210227gitcc22d22
- Updated to latest upstream snapshot

* Tue Feb 23 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-3.20210223git1612841
- Add Requires to the subpackages
- Fix description of ipu3 package
- Build v4l2 compat layer

* Tue Feb 23 2021 Dorian Stoll <dorian.stoll@tmsp.io> - 0.0.0-2.20210223git1612841
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
