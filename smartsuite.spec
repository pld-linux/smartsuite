Summary:	UCSC SMART suite - S.M.A.R.T. utility for Linux
Summary(pl):	UCSC SMART suite - obs�uga S.M.A.R.T. dla Linuksa
Name:		smartsuite
Version:	2.1
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://prdownloads.sourceforge.net/smartsuite/%{name}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://csl.cse.ucsc.edu/smart.shtml
Prereq:		/sbin/chkconfig
BuildRequires:	kernel-headers
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	smartctl
Obsoletes:	ucsc-smartsuite

%description
UCSC SMART suite controls and monitors storage devices uning the
Self-Monitoring, Analysis and Reporting Technology System (S.M.A.R.T.)
build into ATA and SCSI Hard Drives. This is used to check the
reliability of the hard drive and predict drive failures. The suite
contents two utilities, smartctl is a command line utility designed to
perform simple S.M.A.R.T. tasks. And smartd is a daemon that
periodically monitors smart status and reports errors to syslog.

%description -l pl
USCS SMART suite s�u�y do kontroli i monitorowania urz�dze� z systemem
S.M.A.R.T., takich jak dyski ATA i SCSI. System ten pozwala okre�la�
wiarygodno�� dysk�w i przewidywa� awarie. Pakiet zawiera dwa programy:
smartctl (obs�ugiwany z linii polece�) i smartd (demon regularnie
monitoruj�cy stan dysk�w).

%prep
%setup -q

%build
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -fsigned-char -DLINUX"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smartd
install smartd smartctl $RPM_BUILD_ROOT%{_sbindir}
install smartd.8 smartctl.8 $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf CHANGELOG README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smartd
if [ -f /var/lock/subsys/smartd ]; then
        /etc/rc.d/init.d/smartd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/smartd start\" to start smartd service."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/smartd ]; then
                /etc/rc.d/init.d/smartd stop 1>&2
        fi
        /sbin/chkconfig --del smartd
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/smartd
%{_mandir}/man8/*
