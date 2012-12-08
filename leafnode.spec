%define name	leafnode
%define version	1.11.8
%define release %mkrel 3

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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.11.8-2mdv2011.0
+ Revision: 666068
- mass rebuild

* Sun Oct 24 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.11.8-1mdv2011.0
+ Revision: 587905
- update to 1.11.8

* Fri Feb 12 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.11.7-1mdv2010.1
+ Revision: 504431
- update to 1.11.7

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.11.6-5mdv2010.0
+ Revision: 425505
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.11.6-4mdv2009.1
+ Revision: 351350
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.11.6-3mdv2009.0
+ Revision: 222384
- rebuild

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.11.6-2mdv2008.1
+ Revision: 150442
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Jul 07 2007 Funda Wang <fwang@mandriva.org> 1.11.6-1mdv2008.0
+ Revision: 49358
- New version


* Thu Apr 13 2006 Jerome Soyer <saispo@mandriva.org> 1.11.5-1mdk
- New release 1.11.5

* Mon Jan 30 2006 Jerome Soyer <saispo@mandriva.org> 1.11.4-1mdk
- New release 1.11.4

* Sat Oct 08 2005 Michael Scherer <misc@mandriva.org> 1.11.3-1mdk
- New release 1.11.3
- mkrel
- erase RPM_BUILD_ROOT is for %%install

* Tue Aug 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.10.4-1mdk
- new release

* Thu Jul 29 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.10.3-1mdk
- new release

* Thu Jul 01 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.10.1-1mdk
- new release

* Fri Apr 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9.51-1mdk
- new release

* Fri Nov 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9.46-1mdk
- new release

* Thu Aug 07 2003 Florin <florin@mandrakesoft.com> 1.9.42-1mdk
- 1.9.42

* Thu Jun 05 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9.41-2mdk
- fix conflict with libpcre0

* Mon Jun 02 2003 Florin <florin@mandrakesoft.com> 1.9.41-1mdk
- 1.9.41
- add the asc source

