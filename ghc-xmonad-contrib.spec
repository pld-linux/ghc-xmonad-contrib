%define		pkgname	xmonad-contrib
Summary:	Third party extensions for xmonad
Name:		ghc-%{pkgname}
Version:	0.12
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	39345f462f069f2f0e4a488f7e435dbb
Patch0:		net_wm_state_fullscreen.patch
URL:		http://www.xmonad.org
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-X11 >= 1.6.1
BuildRequires:	ghc-extensible-exceptions
BuildRequires:	ghc-mtl
BuildRequires:	ghc-random
BuildRequires:	ghc-utf8-string
BuildRequires:	rpmbuild(macros) >= 1.608
BuildRequires:	xmonad >= 0.12
%requires_eq	ghc
Requires:	ghc-X11 >= 1.6.1
Requires:	ghc-extensible-exceptions
Requires:	ghc-mtl
Requires:	ghc-random
Requires:	ghc-utf8-string
Requires:	xmonad >= 0.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
Third party extensions for xmonad.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p0

%build
runhaskell Setup.lhs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
