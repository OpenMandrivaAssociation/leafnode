%global commit 66da754d164983fde96ae391ddfda53a0b74e51b
Summary:	Leafsite NNTP server
Name:		leafnode
Version:	2.0.0
Release:	2
License:	Artistic
Group:		System/Servers
# Last official source:
# Url:		http://leafnode.sourceforge.io/
# Tree that has seen a little development in the last 2 decades:
Url:		https://gitlab.com/leafnode-2/leafnode-2/
Source0:	https://gitlab.com/leafnode-2/leafnode-2/-/archive/%{commit}/leafnode-%{version}.tar.bz2
Source2:	%{name}.texpire
Source3:	%{name}.filters
Source4:	%{name}.xinetd
Source5:        %{name}-tmpfiles.conf
BuildRequires:	pkgconfig(libpcre)
Requires:	xinetd
Conflicts:	inn

%description
Leafnode is a small NNTP server for leaf sites without permanent
connection to the internet. It supports a subset of NNTP and is able to
automatically fetch the newsgroups the user reads regularly from the
newsserver of the ISP.

%prep
%autosetup -p1 -n leafnode-2-%{commit}
aclocal
autoheader
automake -a
autoconf

%build
%configure \
	--with-spooldir=/var/spool/news \
	--with-lockfile=/run/lock/news/%{name} \
	--sysconfdir=%{_sysconfdir}/%{name}
%make 

%install
%makeinstall_std
install -d %{buildroot}%{_sysconfdir}/{cron.daily,leafnode}
install -m 755 %SOURCE2 %{buildroot}%{_sysconfdir}/cron.daily/texpire
#install -m 600 config.example %{buildroot}%{_sysconfdir}/leafnode/config
install -m 600 %SOURCE3 %{buildroot}%{_sysconfdir}/leafnode/filters
install -D -m644 %{SOURCE4} %{buildroot}/etc/xinetd.d/%{name}
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf

cp doc_german/README doc_german/README.de

# Install the man pages
install -d %{buildroot}%{_mandir}/{,de}/man{1,3,8}
install -m 644 doc_german/man/man1/*.1 %{buildroot}%{_mandir}/de/man1
install -m 644 doc_german/man/man8/*.8 %{buildroot}%{_mandir}/de/man8
rm -rf doc_german/man
install -m 644 `find . -name "*.1"` %{buildroot}%{_mandir}/man1
install -m 644 `find . -name "*.8"` %{buildroot}%{_mandir}/man8
rm -f %{buildroot}%{_mandir}/man?/pcre*
mkdir -p %{buildroot}/var/spool/news/message.id/{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}{0,1,2,3,4,5,6,7,8,9}

%pre
if [ -f %{_sysconfdir}/cron.daily/texpire.cron ] ; then
        rm -f %{_sysconfdir}/cron.daily/texpire.cron
fi

%post
systemd-tmpfiles --create %{name}.conf

%files
%doc COPYING CREDITS INSTALL tools/archivefaq.pl update.sh
#%doc doc_german/README.de doc_german/txt/*
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/texpire
%attr (644,root,man) %{_mandir}/man1/*
%attr (644,root,man) %{_mandir}/de/man1/*
%attr (644,root,man) %{_mandir}/man5/*
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
%{_tmpfilesdir}/%{name}.conf
%dir /var/spool/news
%dir /var/spool/news/*
%dir /var/spool/news/message.id/*

