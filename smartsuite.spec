Summary:	UCSC SMART suite - S.M.A.R.T. utility for Linux
Summary(pl.UTF-8):	UCSC SMART suite - obsługa S.M.A.R.T. dla Linuksa
Summary(pt_BR.UTF-8):	Conjunto de utilitários SMART para Linux
Name:		smartsuite
Version:	2.1
Release:	6
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/smartsuite/%{name}-%{version}.tar.gz
# Source0-md5:	f793fa1ed6419090af1c8e45cc052805
Source1:	%{name}.init
Patch0:		%{name}-u8.patch
URL:		http://csl.cse.ucsc.edu/smart.shtml
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	smartctl
Obsoletes:	smartmontools
Obsoletes:	ucsc-smartsuite
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UCSC SMART suite controls and monitors storage devices uning the
Self-Monitoring, Analysis and Reporting Technology System (S.M.A.R.T.)
build into ATA and SCSI Hard Drives. This is used to check the
reliability of the hard drive and predict drive failures. The suite
contents two utilities, smartctl is a command line utility designed to
perform simple S.M.A.R.T. tasks. And smartd is a daemon that
periodically monitors smart status and reports errors to syslog.

%description -l pl.UTF-8
USCS SMART suite służy do kontroli i monitorowania urządzeń z systemem
S.M.A.R.T., takich jak dyski ATA i SCSI. System ten pozwala określać
wiarygodność dysków i przewidywać awarie. Pakiet zawiera dwa programy:
smartctl (obsługiwany z linii poleceń) i smartd (demon regularnie
monitorujący stan dysków).

%description -l pt_BR.UTF-8
SMART suite controla e monitora dispositivos de armazenamento usando o
sistema de auto-monitoração e análise existente em discos rígidos ATA
e SCSI. Esse sistema é utilizado para verificar a confiabilidade do
disco e prever falhas no equipamento.

%prep
%setup -q
%patch -P0 -p1

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
%service smartd restart "smartd service"

%preun
if [ "$1" = "0" ]; then
	%service smartd stop
	/sbin/chkconfig --del smartd
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README TODO
%attr(755,root,root) %{_sbindir}/smartctl
%attr(755,root,root) %{_sbindir}/smartd
%attr(754,root,root) /etc/rc.d/init.d/smartd
%{_mandir}/man8/smartctl.8*
%{_mandir}/man8/smartd.8*
