%define version 0.0.14
%define release %mkrel 2

%define libggz_version %{version}
%define ggz_client_libs_version %{version}
%define games_list chess ttt

Name:		ggz-grubby
Summary:	GGZ Gaming Zone - Grubby, the chat bot
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://www.ggzgamingzone.org/

Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2
# (Abel) 0.0.9-1mdk fix libperl detection
Patch0:		%name-0.0.9-check-perl.patch
BuildRequires:	popt-devel
BuildRequires:	expat-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	ruby-devel
BuildRequires:	libggz-devel = %{libggz_version}
BuildRequires:	ggz-client-libs-devel = %{ggz_client_libs_version}
Requires(pre):	libggz = %{libggz_version}
Requires(pre):	ggz-client-libs = %{ggz_client_libs_version}


%description
This package contains grubby, a chatbot for GGZ Gaming Zone. It's
a single binary, but it is very flexible and extensible by plugins
and scripts.

Grubby is intended to be used on servers so it doesn't miss players,
but it is in fact a client program. It reads all necessary startup
information from your home folder and runs as long as it isn't shut
down by its owner. See the Setup file to view a common setup, or
generate one using grubby-config.

%package	embed
Summary:	Scripting functionality for Grubby, the GGZ Gaming Zone chat bot
Group:		Games/Other
Requires:	%{name} = %{version}-%{release}

%description	embed
This package contains module and scripts for grubby, the chatbot
for GGZ Gaming Zone. Please install this package if you want grubby
to support perl, python and ruby scripting.

%prep
%setup -q
%patch0 -p1

# Needed for patches
#libtoolize -c -f
#ACLOCAL=aclocal-1.7 AUTOMAKE=automake-1.7 autoreconf --force --install

%build
%configure --with-libggz-libraries=%{_libdir} --with-ggzmod-libraries=%{_libdir} --with-ggzcore-libraries=%{_libdir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm %{buildroot}%{_sysconfdir}/ggz.modules
rmdir %{buildroot}%{_sysconfdir}

# Get a copy of all of our .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz/ggz-config
for i in %games_list; do
  install -m 0644 games/guru-$i/module.dsc %{buildroot}%{_datadir}/ggz/ggz-config/guru-$i.dsc
done

%find_lang grubby

# remove unneeded files
rm -f %{buildroot}%{_libdir}/grubby/{,core}modules/*.{a,la}

%clean
rm -rf %{buildroot}

%post
# Run ggz-config vs. all installed games
if [ -f %{_sysconfdir}/ggz.modules ]; then
  for i in %games_list; do
    ggz-config --install --modfile=%{_datadir}/ggz/ggz-config/guru-$i.dsc --force
  done
fi


%preun
# Run ggz-config to uninstall all the games
if [ "$1" = "0" ]; then
  if [ -f %{_sysconfdir}/ggz.modules ]; then
    for i in %games_list; do
      ggz-config --remove --modfile=%{_datadir}/ggz/ggz-config/guru-$i.dsc
    done
  fi
fi

%files -f grubby.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README

%{_bindir}/*
%{_datadir}/ggz/ggz-config/*.dsc
%{_libdir}/ggz/*
%{_libdir}/grubby
%exclude %{_libdir}/grubby/modules/libgurumod_embed.so
%{_mandir}/man?/*
%lang(de) %{_mandir}/de/man?/*
%files embed
%defattr(-,root,root)
%{_libdir}/grubby/modules/libgurumod_embed.so
%{_datadir}/grubby


