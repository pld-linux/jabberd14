#
# Conditional build:
%bcond_with	ipv6	# - with IPv6 support

Summary:	Old "jabber.org" Jabber server daemon
Summary(pl):	Stary serwer Jabbera "z jabber.org"
Name:		jabberd14
Version:	1.4.3.1
Release:	2
License:	distributable
Group:		Applications/Communications
Source0:	http://jabberd.jabberstudio.org/1.4/dist/jabberd-1.4.3.tar.gz
# Source0-md5:	a3e964d6fa07b5d850302ae0512f94c6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-mod_stats.patch
Patch2:		%{name}-register-deny_new.patch
Patch3:		%{name}-browse.patch
Patch4:		%{name}-detach_from_terminal.patch
Patch5:		%{name}-opt.patch
# Patch6:	http://devel.amessage.info/jabberd14/jabberd-1.4.3.1.diff.bz2
Patch6:		%{name}-1.4.3.1.patch
URL:		http://jabberd.jabberstudio.org/1.4/
BuildRequires:	expat-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pth-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	jabber-common
Requires:	rc-scripts
Obsoletes:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jabber is an XML-based, client-server, open-source presence and
messaging system that uses a network of distributed servers to pass
data between servers and ultimately to Jabber clients.

This package contains old version of JSF jabberd Jabber server
software, mainly for use with some old Jabber services.

%description -l pl
Jabber to oparty o XML, architekturê klient-server oraz filozofiê
open-source system powiadamiania, który wykorzystuje rozproszon± sieæ
serwerów, do przekazywania danych pomiêdzy nimi i klientami Jabber.

Ten pakiet zawiera star± wersjê jabberd, g³ównie na potrzeby starszych
serwisów Jabbera.

%package server
Summary:	jabberd-1.4 based Jabber server
Summary(pl):	Serwer Jabbera oparty o jabberd-1.4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	jabber

%description server
Jabber server based on jabberd v. 1.4.x.

%description server -l pl
Serwer Jabbera oparty o jabberd-1.4.

%package devel
Summary:	Header and library files for jabberd14 component development
Summary(pl):	Pliki nag³ówkowe i biblioteki dla komponentów jabberd14
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel
Requires:	openssl-devel >= 0.9.7d
Requires:	pth-devel

%description devel
This package provides the files necessary to develop jabberd-1.4.x
extensions.

%description devel -l pl
Ten pakiet zawiera pliki niezbêdne do tworzenia rozszerzeñ serwera
jabberd-1.4.x.

%prep
%setup -qn jabberd-1.4.3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
JHOME="%{_localstatedir}/lib/%{name}"; export JHOME
%configure \
	--enable-ssl \
	--%{?with_ipv6:enable}%{?!with_ipv6:disable}-ipv6

%{__make} \
	CC="%{__cc}" \
	CCFLAGS="%{rpmcflags} -Wall -I. -I.. -I/usr/include/openssl -DHAVE_SSL -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,%{_sbindir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/spool \
	$RPM_BUILD_ROOT{/var/log/%{name},%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT%{_includedir}/%{name}/lib

install jabberd/jabberd $RPM_BUILD_ROOT%{_sbindir}/%{name}
sed -e 's,@libdir@,%{_libdir},g' jabber.xml > $RPM_BUILD_ROOT%{_sysconfdir}/jabber/jabberd14.xml
install xdb_file/xdb_file.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install pthsock/pthsock_client.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install jsm/jsm.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install dialback/dialback.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install dnsrv/dnsrv.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install jabberd/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install jabberd/lib/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/lib
install platform-settings $RPM_BUILD_ROOT%{_libdir}/%{name}/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add %{name}
%service %{name} restart "Jabber server"

%preun server
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README UPGRADE pthsock/README*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(771,root,jabber) %{_localstatedir}/lib/%{name}
%attr(770,root,jabber) /var/log/%{name}

%files server
%defattr(644,root,root,755)
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*.xml
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/%{name}/platform-settings
