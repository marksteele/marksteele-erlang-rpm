%undefine _missing_build_ids_terminate_build
%define _libdir /usr/lib/erlang
%define _bindir /usr/bin

Summary: Erlang OTP package
Name: marksteele-erlang
Version: 17.5.6.8
Release: 1
License: ASL 2.0
Group: "Development/Languages"
Source: %{_tarname}
URL: http://www.erlang.org
Packager:  <mark@control-alt-del.org>
BuildRoot: %{_tmppath}/%{name}-%{_revision}-%{release}-root
BuildArch: x86_64
BuildRequires:ncurses-devel
BuildRequires:openssl-devel
BuildRequires:zlib-devel
BuildRequires:flex
BuildRequires:m4
BuildRequires:fop
BuildRequires:libxslt
BuildRequires:emacs
BuildRequires:emacs-el
BuildRequires:ed
BuildRequires:tcl-devel
BuildRequires:tk-devel
BuildRequires:java-devel
BuildRequires:unixODBC-devel
BuildRequires:wxGTK-devel
BuildRequires:freeglut-devel
BuildRequires:fop
BuildRequires:libxslt-devel
BuildRequires:chrpath
Vendor: Mark Steele

%description
This is an Erlang OTP %{version} package

%prep
%setup -q -n %{_tarname_base}

%build
./otp_build autoconf
./otp_build configure --enable-dirty-schedulers
./otp_build boot -a
./otp_build release -a

%install
%define buildroot_lib %{buildroot}/%{_libdir}
%define buildroot_bin %{buildroot}/%{_bindir}
mkdir -p %{buildroot_lib} %{buildroot_bin} %{buildroot}/usr/share

cp -r %{_builddir}/%{name}-%{_revision}/bin/{cerl,ct_run,dialyzer,erl,erlc,escript,typer,x86_64-unknown-linux-gnu/{beam,beam.smp,child_setup,dyn_erl,epmd,erlexec,heart,hipe_mkliterals,hipe_mkliterals.smp,inet_gethost,run_erl,to_erl}} %{buildroot_bin}/
cp -r %{_builddir}/%{name}-%{_revision}/release/*/* %{buildroot_lib}/

rm -rf %{buildroot_lib}/lib/*/doc

set +e
for i in `find . -wholename '*/bin/*'`; do
    objdump -G ${i}
    RETVAL=$?
    [ $RETVAL -eq 0 ] && strip ${i}
done
set -e
find . -iname '*.so' -exec strip --strip-unneeded {} \;

chrpath -d %{buildroot_lib}/lib/crypto-*/priv/lib/crypto.so
rm -rf %{buildroot_lib}/man/cat*

export QA_RPATHS=3

%post
echo "Erlang OTP %{version} installed"

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_bindir}/*

