%define	up_name	cfengine
%define _fortify_cflags %nil

%define major 1
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname -d %{name}

Name:		cfengine3
Version:	3.1.2
Release:	%mkrel 0.1
Summary:	Cfengine helps administer remote BSD and System-5-like systems
License:	GPL
Group:		Monitoring
URL:		http://www.cfengine.org
Source0:	http://www.cfengine.org/tarballs/%{up_name}-%{version}.tar.gz
Source4:	cfengine-serverd.init
Source5:	cfengine-execd.init
Source6:	cfengine-monitord.init
Patch0:		cfengine-3.0.3-fix-str-fmt.patch
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel
BuildRequires:	db4-devel
BuildRequires:	graphviz-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	pcre-devel
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
Requires:	lsb-release

%description base
This package contain the cfengine base files needed by all subpackages.

%package agent
Summary:	Cfengine agent
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}

%description agent
This package contain the cfengine agent.

%package serverd
Summary:	Cfengine server daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):rpm-helper
Requires(preun):rpm-helper

%description serverd
This package contain the cfengine server daemon.

%package execd
Summary:	Cfengine agent execution wrapper
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description execd
This package contain the cfengine agent execution wrapper.

%package monitord
Summary:	Cfengine anomaly detection daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(preun):rpm-helper

%description monitord
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
%patch0 -p1

%build
%serverbuild
export CFLAGS="$CFLAGS -fPIC"
%configure2_5x --with-workdir=%{_localstatedir}/lib/%{up_name} --enable-shared
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -d -m 755 %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/bin
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/lastseen
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/modules
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/outputs
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{up_name}/ppkeys
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/randseed
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/reports
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{up_name}/rpc_in
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{up_name}/rpc_out
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{up_name}/rpc_state

mv %{buildroot}%{_docdir}/%{up_name}/inputs \
    %{buildroot}%{_sysconfdir}/%{up_name}

pushd %{buildroot}%{_localstatedir}/lib/%{up_name}
ln -sf ../../..%{_sysconfdir}/%{up_name} inputs
popd
pushd %{buildroot}%{_localstatedir}/lib/%{up_name}/bin
#ln -sf ../../../../%{_sbindir}/cf-promises .
for i in ../../../../%{_sbindir}/cf-*
do
ln -sf ../../../../%{_sbindir}/$i .
done
popd

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/cfengine-serverd
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/cfengine-execd
install -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/cfengine-monitord

mv %{buildroot}%{_docdir}/%{up_name} %{buildroot}%{_docdir}/%{name}

# compatibility purpose
pushd %{buildroot}%{_localstatedir}/lib/%{up_name}
ln -sf %{_localstatedir}/lib/%{up_name} ../../%{up_name}
popd

%post base
if [ $1 = 1 ]; then
    [ -f "%{_localstatedir}/lib/%{up_name}/ppkeys/localhost.priv" ] || cf-key >/dev/null 2>&1
fi

%post execd
%_post_service cfengine-execd

%preun execd
%_preun_service cfengine-execd

%post monitord
%_post_service cfengine-monitord

%preun monitord
%_preun_service cfengine-monitord

%post serverd
%_post_service cfengine-serverd

%preun serverd
%_preun_service cfengine-serverd

%clean
rm -rf %{buildroot}

%files base
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_sbindir}/cf-key
%{_sbindir}/cf-promises
%{_localstatedir}/lib/%{up_name}
%{_localstatedir}/%{up_name}
%config(noreplace) %{_sysconfdir}/%{up_name}
%{_mandir}/man8/cf-key.8*
%{_mandir}/man8/cf-promises.8*

%files agent
%defattr(-,root,root)
%{_sbindir}/cf-agent
%{_sbindir}/cf-know
%{_sbindir}/cf-report
%{_sbindir}/cf-runagent
%{_sbindir}/cf-hub
%{_mandir}/man8/cf-agent.8*
%{_mandir}/man8/cf-know.8*
%{_mandir}/man8/cf-report.8*
%{_mandir}/man8/cf-runagent.8*
%{_mandir}/man8/cf-hub.8*

%files serverd
%defattr(-,root,root)
%{_initrddir}/cfengine-serverd
%{_sbindir}/cf-serverd
%{_mandir}/man8/cf-serverd.8*

%files monitord
%defattr(-,root,root)
%{_initrddir}/cfengine-monitord
%{_sbindir}/cf-monitord
%{_mandir}/man8/cf-monitord.8*

%files execd
%defattr(-,root,root)
%{_initrddir}/cfengine-execd
%{_sbindir}/cf-execd
%{_mandir}/man8/cf-execd.8*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
