#
# Conditional build:
# _with_ipv6 - with IPv6 support
#
Summary:	Old "jabber.org" Jabber server daemon
Summary(pl):	Stary serwer Jabbera "z jabber.org"
Name:		jabberd14
Version:	1.4.2
Release:	1
License:	distributable
Group:		Applications/Communications
Source0:	http://download.jabber.org/dists/1.4/final/jabber-%{version}.tar.gz
# Source0-md5:	10780dbdb93926ea5bb360e1186b939c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-ssl_dos_fix.patch
Patch2:		%{name}-mod_disco.patch
Patch3:		%{name}-mod_stats.patch
Patch4:		%{name}-register-deny_new.patch
Patch5:		%{name}-browse.patch
Patch6:		%{name}-detach_from_terminal.patch
# Patches from jabberd CVS follow
Patch10:	%{name}-IPv6.patch
Patch11:	%{name}-SRV.patch
Patch12:	%{name}-deadlock.patch
Patch13:	%{name}-dlopen.patch
Patch14:	%{name}-dos.patch
Patch15:	%{name}-double_connect.patch
Patch16:	%{name}-groups.patch
Patch17:	%{name}-messages_are_equal.patch
Patch18:	%{name}-presence.patch
Patch19:	%{name}-pth.patch
Patch20:	%{name}-route.patch
Patch21:	%{name}-allow_sslonly.patch
Patch22:	%{name}-xdbcache_lock.patch
URL:		http://www.jabber.org/
BuildRequires:	pth-devel
BuildRequires:	openssl-devel >= 0.9.7
PreReq:		rc-scripts
Requires(pre):	jabber-common
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
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
Requires:	%{name} = %{version}
Obsoletes:	jabber

%description server
Jabber server based on jabberd v. 1.4.x.

%package devel
Summary:	Header and library files for jabberd14 component development
Summary(pl):	Pliki nag³ówkowe i biblioteki dla komponentów jabberd14
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package provides the files necessary to develop jabberd-1.4.x
extensions.

%description devel -l pl
Ten pakiet zawiera pliki niezbêdne do tworzenia rozszerzeñ serwera
jabberd-1.4.x.

%prep
%setup -qn jabber-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1

%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0
%patch21 -p0
%patch22 -p0

%build
JHOME="%{_localstatedir}/lib/%{name}"; export JHOME
%configure \
	--enable-ssl \
	--%{?_with_ipv6:enable}%{?!_with_ipv6:disable}-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,%{_sbindir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/spool \
	$RPM_BUILD_ROOT{/var/log/%{name},%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT%{_includedir}/%{name}/lib

install jabberd/jabberd $RPM_BUILD_ROOT%{_sbindir}/%{name}
install jabber.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber/jabberd14.xml
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

%pre

%post server
/sbin/chkconfig --add %{name}
if [ -r /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start Jabber server."
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%postun

%files
%defattr(644,root,root,755)
%doc README UPGRADE pthsock/README*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(771,root,jabber) %{_localstatedir}/lib/%{name}
%attr(770,root,jabber) /var/log/%{name}

%files server
%defattr(644,root,root,755)
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/*.xml
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/%{name}/platform-settings
