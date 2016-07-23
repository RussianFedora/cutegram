%global decname Cutegram

%global commit 7294861b65861adb401668291d85970c5900fc5b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:         cutegram
Version:      3.0
Release:      0.1git%{shortcommit}%{?dist}
Summary:      Cutegram is a telegram client by Aseman Land

# Bundled JS stuff:
# js-linkify: MIT
# js-twemoji: MIT and CC-BY-4.0
License:        GPLv3+ and MIT and CC-BY-4.0
URL:            https://github.com/Aseman-Land/%{decname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# https://github.com/Aseman-Land/Cutegram/pull/233
Patch0001:      0001-Install-cutegram-binary-when-BinaryMode-is-enabled.patch
Patch0002:      0002-desktop-Exec-cutegram-when-binaryMode-is-enabled.patch

BuildRequires:  gcc-c++

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  /usr/bin/desktop-file-validate

Provides:       bundled(js-linkify)
Provides:       bundled(js-twemoji)

Requires:       hicolor-icon-theme

Requires:       aseman-qt-tools%{?_isa}
Requires:       telegramqml%{?_isa}

%description
A different telegram client from Aseman team. Cutegram forked from Sigram
by Sialan Labs. Cutegram project are released under the terms of the GPLv3
license.

%prep
%autosetup -n %{decname}-%{commit} -p1
mkdir %{_target_platform}

%build
pushd %{_target_platform}
  %qmake_qt5 PREFIX=%{_prefix} CONFIG+=binaryMode ..
popd
%make_build -C %{_target_platform}

%install
%make_install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{decname}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license GPL.txt
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{decname}.desktop

%changelog
* Sat Jul 23 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 3.0-0.1git7294861
- Initial commit.
