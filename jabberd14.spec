Summary:	Jabber messaging system server
Summary(pl):	Serwer systemu powiadamiania Jabber
Name:		jabber
Version:	1.4.1
Release:	1
License:	distributable
Group:		Applications/Communications
Group(de):	Applikationen/Kommunikation
Group(pl):	Aplikacje/Komunikacja
Source0:	http://download.jabber.org/dists/1.4/final/%{name}-%{version}.tar.gz
Source1:	http://docs.jabber.org/no-sgml/howto-1.4.html
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-FHS.patch
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
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
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
cp -f %{SOURCE1} .

%build
JHOME="%{_localstatedir}/lib/%{name}"; export JHOME
%configure \
	--enable-ssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_sbindir},/etc/rc.d/init.d,/etc/sysconfig}
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/spool
install -d $RPM_BUILD_ROOT{/var/log/%{name},%{_libdir}/%{name}}
install -d $RPM_BUILD_ROOT%{_includedir}/jabberd/lib

install jabberd/jabberd $RPM_BUILD_ROOT%{_sbindir}
install jabber.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install xdb_file/xdb_file.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install pthsock/pthsock_client.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install jsm/jsm.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install dialback/dialback.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install dnsrv/dnsrv.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install jabberd/*.h $RPM_BUILD_ROOT%{_includedir}/jabberd
install jabberd/lib/*.h $RPM_BUILD_ROOT%{_includedir}/jabberd/lib
install platform-settings $RPM_BUILD_ROOT%{_libdir}/%{name}/
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabberd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabberd

gzip -9nf README UPGRADE pthsock/README*

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
%doc *.gz howto*.html pthsock/*.gz
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(771,root,jabber) %{_localstatedir}/lib/%{name}
%attr(770,root,jabber) /var/log/%{name}
%dir %{_sysconfdir}/%{name}
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/*.xml
%attr(755,root,root) /etc/rc.d/init.d/jabberd
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jabberd

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/%{name}/platform-settings
