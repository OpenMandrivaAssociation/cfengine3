%define	up_name	cfengine
%define	name	cfengine3
%define version 3.0.1
%define release %mkrel 1
%define _fortify_cflags %nil

%define major 1
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname -d %{name}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Cfengine helps administer remote BSD and System-5-like systems
License:	GPL
Group:		Monitoring
URL:		http://www.cfengine.org
Source0:	http://www.cfengine.org/downloads/%{up_name}-%{version}.tar.gz
Source4:	cfservd.init
Source5:	cfexecd.init
Source6:	cfenvd.init
Patch0:     cfengine-3.0.1-fix-buffer-size.patch
Patch1:     cfengine-3.0.1-fix-mandriva-detection.patch
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel
BuildRequires:	db4-devel
Requires(pre):	rpm-helper
Requires(preun):rpm-helper
Conflicts:      cfengine
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Cfengine, the configuration engine, is a very high level language for
simplifying the task of administrating and configuring large numbers
of workstations. Cfengine uses the idea of classes and a primitive
form of intelligence to define and automate the configuration of large
systems in the most economical way possible.

%package base
Summary:	Cfengine base files
Group:		Monitoring

%description base
This package contain the cfengine base files needed by all subpackages.

%package cfagent
Summary:	Cfengine agent
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}

%description cfagent
This package contain the cfengine agent.

%package cfservd
Summary:	Cfengine server daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):rpm-helper
Requires(preun):rpm-helper

%description cfservd
This package contain the cfengine server daemon.

%package cfexecd
Summary:	Cfengine agent execution wrapper
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description cfexecd
This package contain the cfengine agent execution wrapper.

%package cfenvd
Summary:	Cfengine anomaly detection daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(preun):rpm-helper

%description cfenvd
This package contain the cfengine anomaly detection daemon.

%package -n	%{libname}
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q -n %{up_name}-%{version}
%patch0 -p 0
%patch1 -p 1

%build
%serverbuild
export CFLAGS="$CFLAGS -fPIC"
%configure2_5x --with-workdir=%{_localstatedir}/lib/%{up_name} --enable-shared
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/cfservd
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/cfexecd
install -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/cfenvd

# everything installed there is doc, actually
rm -rf %{buildroot}%{_datadir}/%{up_name}
mv %{buildroot}%{_docdir}/%{up_name} %{buildroot}%{_docdir}/%{name}
install -m 644 inputs/*.cf %{buildroot}%{_docdir}/%{name}

%post base
if [ $1 = 1 ]; then
    [ -f "%{_localstatedir}/lib/%{up_name}/ppkeys/localhost.priv" ] || cf-key >/dev/null 2>&1
fi

%post cfexecd
%_post_service cfexecd

%preun cfexecd
%_preun_service cfexecd

%post cfenvd
%_post_service cfenvd

%preun cfenvd
%_preun_service cfenvd

%post cfservd
%_post_service cfservd

%preun cfservd
%_preun_service cfservd

%clean
rm -rf %{buildroot}

%files base
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_sbindir}/cf-key
%{_sbindir}/cf-promises
%{_localstatedir}/lib/%{up_name}
%{_mandir}/man8/cf-key.8*
%{_mandir}/man8/cf-promise.8*

%files cfagent
%defattr(-,root,root)
%{_sbindir}/cf-agent
%{_sbindir}/cf-know
%{_sbindir}/cf-report
%{_sbindir}/cf-runagent
%{_mandir}/man8/cf-agent.8*
%{_mandir}/man8/cf-know.8*
%{_mandir}/man8/cf-report.8*
%{_mandir}/man8/cf-runagent.8*
%{_infodir}/cf3-reference.info.*
%{_infodir}/cf3-reference.info-1.*
%{_infodir}/cf3-reference.info-2.*

%files cfservd
%defattr(-,root,root)
%{_initrddir}/cfservd
%{_sbindir}/cf-serverd
%{_mandir}/man8/cf-serverd.8*

%files cfenvd
%defattr(-,root,root)
%{_initrddir}/cfenvd
%{_sbindir}/cf-monitord
%{_mandir}/man8/cf-monitord.8*

%files cfexecd
%defattr(-,root,root)
%{_initrddir}/cfexecd
%{_sbindir}/cf-execd
%{_mandir}/man8/cf-execd.8*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
