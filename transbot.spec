%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name: transbot
Version: 0.1
Release: 1%{?dist}
Summary: Small irc bot designed to translate between languages in irc channels
Group: Development/Libraries
License: GPLv2+
URL:	http://git.fedorahosted.org/git/lingobot.git
Source0:	http://fedorahosted.org/lingobot/browser/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	python, python-devel
Requires:	python-irclib

%description
An irc bot designed to translate between languages on separate irc channels. 

%prep
%setup -q

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --record=installed_files 
sed -e 's/\.[0-9]$/&\*/' <installed_files >installed_files2

%clean
rm -rf %{buildroot}

%files -f installed_files2
%defattr(-,root,root)
%doc README LICENSE
%dir %{python_sitelib}/trans
%{python_sitelib}/trans/*.pyo
%config(noreplace) %{_sysconfdir}/transbot.conf

%changelog
*Sat Jul 05 2008 John McLean <jesusfreak91@gmail.com>
-Fixed the problems in the spec file
