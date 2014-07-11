Summary:	Leafsite NNTP server
Name:		leafnode
Version:	1.11.8
Release:	11
License:	Artistic
Group:		System/Servers
Url:		http://www.leafnode.org
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2.asc
Source2:	%{name}.texpire
Source3:	%{name}.filters
Source4:	%{name}.xinetd
BuildRequires:	pkgconfig(libpcre)
Requires:	xinetd
Conflicts:	inn

%description
Leafnode is a small NNTP server for leaf sites without permanent
connection to the internet. It supports a subset of NNTP and is able to
automatically fetch the newsgroups the user reads regularly from the
newsserver of the ISP.

%prep
%setup -q

%build
%configure2_5x \
	--with-spooldir=/var/spool/news \
	--with-lockfile=/var/lock/news/%{name} \
	--sysconfdir=%{_sysconfdir}/%{name}
%make 

%install
%makeinstall_std
install -d %{buildroot}%{_sysconfdir}/{cron.daily,leafnode}
install -m 755 %SOURCE2 %{buildroot}%{_sysconfdir}/cron.daily/texpire
install -m 600 %{_builddir}/%{name}-%{version}/config.example %{buildroot}%{_sysconfdir}/leafnode/config
install -m 600 %SOURCE3 %{buildroot}%{_sysconfdir}/leafnode/filters
install -D -m644 %{SOURCE4} %{buildroot}/etc/xinetd.d/%{name}

cp doc_german/README doc_german/README.de

# Install the man pages
install -d %{buildroot}%{_mandir}/{,de}/man{1,3,8}
install -m 644 doc_german/*.1 %{buildroot}%{_mandir}/de/man1
rm -rf doc_german/*.1
install -m 644 doc_german/*.8 %{buildroot}%{_mandir}/de/man8
rm -rf doc_german/*.8
install -m 644 `find . -name "*.1"` %{buildroot}%{_mandir}/man1
install -m 644 `find . -name "*.8"` %{buildroot}%{_mandir}/man8
rm -f %{buildroot}%{_mandir}/man?/pcre*
mkdir -p %{buildroot}/var/spool/news/message.id/{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}

%pre
if [ -f %{_sysconfdir}/cron.daily/texpire.cron ] ; then
        rm -f %{_sysconfdir}/cron.daily/texpire.cron
fi

%files
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

