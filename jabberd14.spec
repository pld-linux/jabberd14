#
# Conditional build:
# _without_ipv6 - without IPv6 support
#
Summary:	Jabber messaging system server
Summary(pl):	Serwer systemu powiadamiania Jabber
Name:		jabber
Version:	1.4.2
Release:	4
License:	distributable
Group:		Applications/Communications
Source0:	http://download.jabber.org/dists/1.4/final/%{name}-%{version}.tar.gz
Source1:	http://docs.jabber.org/no-sgml/howto-1.4.html
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-ssl_dos_fix.patch
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
URL:		http://www.jabber.org/
BuildRequires:	pth-devel
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jabber is an XML-based, client-server, open-source presence and
messaging system that uses a network of distributed servers to pass
data between servers and ultimately to Jabber clients.

%description -l pl
Jabber to oparty o XML, architekturê klient-server oraz filozofiê
open-source system powiadamiania, który wykorzystuje rozproszon± sieæ
serwerów, do przekazywania danych pomiêdzy nimi i klientami Jabber.

%package devel
Summary:	Header and library files for Jabber development
Summary(pl):	Pliki nag³ówkowe i biblioteki dla tworzenia us³ug Jabber
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package provides the files necessary to develop Jabber
extensions.

%description devel -l pl
Ten pakiet zawiera pliki niezbêdne do tworzenia rozszerzeñ serwera
Jabber.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

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

cp -f %{SOURCE1} .

%build
JHOME="%{_localstatedir}/lib/%{name}"; export JHOME
%configure \
	--enable-ssl \
	--%{?!_without_ipv6:enable}%{?_without_ipv6:disable}-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabberd,%{_sbindir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/spool \
	$RPM_BUILD_ROOT{/var/log/%{name},%{_libdir}/jabberd} \
	$RPM_BUILD_ROOT%{_includedir}/jabberd/lib

install jabberd/jabberd $RPM_BUILD_ROOT%{_sbindir}
install jabber.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabberd
install xdb_file/xdb_file.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install pthsock/pthsock_client.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install jsm/jsm.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install dialback/dialback.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install dnsrv/dnsrv.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install jabberd/*.h $RPM_BUILD_ROOT%{_includedir}/jabberd
install jabberd/lib/*.h $RPM_BUILD_ROOT%{_includedir}/jabberd/lib
install platform-settings $RPM_BUILD_ROOT%{_libdir}/jabberd/
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabberd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabberd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" = 1 ] ; then
	if [ ! -n "`getgid jabber`" ]; then
		%{_sbindir}/groupadd -f -g 74 jabber
	fi
	if [ ! -n "`id -u jabber 2>/dev/null`" ]; then
		%{_sbindir}/useradd -g jabber -d /var/lib/jabber -u 74 -s /bin/false jabber 2>/dev/null
	fi
fi

%post
/sbin/chkconfig --add jabberd
if [ -r /var/lock/subsys/jabberd ]; then
        /etc/rc.d/init.d/jabberd restart >&2
else
        echo "Run \"/etc/rc.d/init.d/jabberd start\" to start Jabber server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabberd ]; then
		/etc/rc.d/init.d/jabberd stop >&2
	fi
	/sbin/chkconfig --del jabberd
fi

%postun
# If package is being erased for the last time.
if [ "$1" = "0" ]; then
	%{_sbindir}/userdel jabber 2> /dev/null
	%{_sbindir}/groupdel jabber 2> /dev/null
fi

%files
%defattr(644,root,root,755)
%doc README UPGRADE howto*.html pthsock/README*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/jabberd
%{_libdir}/jabberd/*.so
%attr(771,root,jabber) %{_localstatedir}/lib/%{name}
%attr(770,root,jabber) /var/log/%{name}
%dir %{_sysconfdir}/jabberd
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabberd/*.xml
%attr(755,root,root) /etc/rc.d/init.d/jabberd
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jabberd

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/jabberd/platform-settings
