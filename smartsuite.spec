Summary:	UCSC SMART suite - S.M.A.R.T. utility for Linux
Summary(pl):	UCSC SMART suite - obs³uga S.M.A.R.T. dla Linuksa
Summary(pt_BR):	Conjunto de utilitários SMART para Linux
Name:		smartsuite
Version:	2.1
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/smartsuite/%{name}-%{version}.tar.gz
# Source0-md5:	f793fa1ed6419090af1c8e45cc052805
Source1:	%{name}.init
URL:		http://csl.cse.ucsc.edu/smart.shtml
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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
USCS SMART suite s³u¿y do kontroli i monitorowania urz±dzeñ z systemem
S.M.A.R.T., takich jak dyski ATA i SCSI. System ten pozwala okre¶laæ
wiarygodno¶æ dysków i przewidywaæ awarie. Pakiet zawiera dwa programy:
smartctl (obs³ugiwany z linii poleceñ) i smartd (demon regularnie
monitoruj±cy stan dysków).

%description -l pt_BR
SMART suite controla e monitora dispositivos de armazenamento usando o
sistema de auto-monitoração e análise existente em discos rígidos ATA e
SCSI. Esse sistema é utilizado para verificar a confiabilidade do disco
e prever falhas no equipamento.

%prep
%setup -q

%build
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -fsigned-char -DLINUX"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smartd
install smartd smartctl $RPM_BUILD_ROOT%{_sbindir}
install smartd.8 smartctl.8 $RPM_BUILD_ROOT%{_mandir}/man8

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
%doc CHANGELOG README TODO
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/smartd
%{_mandir}/man8/*
