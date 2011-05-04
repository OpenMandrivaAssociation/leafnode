%define name	leafnode
%define version	1.11.8
%define release %mkrel 2

Summary:	Leafnode - a leafsite NNTP server
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	Artistic
Group: 		System/Servers
URL:		http://www.leafnode.org
Source: 	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2.asc
Source2:	%{name}.texpire
Source3:	%{name}.filters
Source4: 	%{name}.xinetd
Conflicts:	inn
BuildRequires:	libpcre-devel
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	xinetd

%description
Leafnode is a small NNTP server for leaf sites without permanent
connection to the internet. It supports a subset of NNTP and is able to
automatically fetch the newsgroups the user reads regularly from the
newsserver of the ISP.

%prep

%setup -q -n %name-%version

%build
%configure --with-spooldir=/var/spool/news \
	   --with-lockfile=/var/lock/news/%name \
	   --sysconfdir=%{_sysconfdir}/%name
make 

#perl -p -i -e 's|/etc/inetd.conf|/etc/xinetd.d/leafnode|' `grep -r /etc/inetd.conf ../$RPM_BUILD_dir/%{name}-%{version}.rel|awk '{print $1}'| sed 's|^..\/BUILD\/||'|sed -e 's|:.*$|\1|'`

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cron.daily,leafnode}
install -m 755 %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/texpire
install -m 600 $RPM_BUILD_DIR/%name-%version/config.example $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/config
install -m 600 %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/leafnode/filters
install -D -m644 %{SOURCE4} %buildroot/etc/xinetd.d/%{name}

cp doc_german/README doc_german/README.de

# Install the man pages
install -d $RPM_BUILD_ROOT%{_mandir}/{,de}/man{1,3,8}
install -m 644 doc_german/*.1 $RPM_BUILD_ROOT%{_mandir}/de/man1
rm -rf doc_german/*.1
install -m 644 doc_german/*.8 $RPM_BUILD_ROOT%{_mandir}/de/man8
rm -rf doc_german/*.8
install -m 644 `find . -name "*.1"` $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 `find . -name "*.8"` $RPM_BUILD_ROOT%{_mandir}/man8
rm -f $RPM_BUILD_ROOT%{_mandir}/man?/pcre*
mkdir -p $RPM_BUILD_ROOT/var/spool/news/message.id/{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}

%pre
if [ -f %{_sysconfdir}/cron.daily/texpire.cron ] ; then
        rm -f %{_sysconfdir}/cron.daily/texpire.cron
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (644,root,root,755)
%doc COPYING CREDITS INSTALL README tools/archivefaq.pl update.sh
#%doc doc_german/README.de doc_german/txt/*
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/texpire
%attr (644,root,man) %{_mandir}/man1/*
%attr (644,root,man) %{_mandir}/de/man1/*
%attr (644,root,man) %{_mandir}/man8/*
%attr (644,root,man) %{_mandir}/de/man8/*
#%attr (644,root,man) %{_mandir}/de/man1/*
#%attr (644,root,man) %{_mandir}/de/man8/*
%defattr (644,news,news,755)
%dir %{_sysconfdir}/leafnode
%attr(600,news,news) %config(noreplace) %{_sysconfdir}/leafnode/*
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%attr(750,news,news) %{_sbindir}/*
%attr(755,news,news) %{_bindir}/*
%dir /var/lock/news
%dir /var/spool/news
%dir /var/spool/news/*
%dir /var/spool/news/message.id/*
