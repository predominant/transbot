%define name transbot
%define version 0.1
%define unmangled_version 0.1
%define release 1
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name: %{name}
Version: %{version}
Release: %{release}
Summary: Small irc bot designed to translate between languages in irc channels
Group: Development/Libraries
License: GPLv2+
URL:	http://fedoraproject.org/wiki/User:Mcleanj/
Source0:	http://fedorahosted.org/transbot/browser/transbot-0.1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	python
Requires:	python-irclib

%description
An irc bot designed to translate between different languages on separate irc channels.  Works for public/channel messages, topic changes, mode changes, and user join/quit instances.

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

%changelog
