%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name: transbot
Version: 0.1
Release: 4%{?dist}
Summary: Small irc bot designed to translate between languages in irc channels
Group: Development/Libraries
License: GPL+
URL:	http://git.fedorahosted.org/git/lingobot.git
Source0:	http://jesusfreak91.googlepages.com/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	python, python-devel
Requires:	python-irclib

%description
An irc bot designed to translate between languages on separate irc channels. 
It takes input from one channel, translates it, and outputs the translated 
text into other channels in that channel's specified language.  
Handles public messages, topic changes, mode changes, join/leave events, 
and auto-joins to invited channels.  Supports utf-8 characters 
and multiple languages.  

%prep
%setup -q

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} 

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/*
%{_mandir}/man1/*
%{python_sitelib}/*
%config(noreplace) %{_sysconfdir}/transbot.conf

%changelog
* Mon Aug 04 2008 John McLean <jesusfreak91@gmail.com> - 0.1-4
-fixed licensing issues
-fixed rpmlint issues
-fixed %%defattr
-modified setup.py

* Fri Aug 01 2008 John McLean <jesusfreak91@gmail.com> - 0.1-3
-added support for utf-8 characters
-updated spec %%description

* Thu Jul 31 2008 John McLean <jesusfreak91@gmail.com> - 0.1-2
-fixed two bugs in transbot.py

*Sat Jul 05 2008 John McLean <jesusfreak91@gmail.com> - 0.1-1
-initial spec
