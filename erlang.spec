%undefine _missing_build_ids_terminate_build

Summary: Erlang OTP package
Name: marksteele-erlang
Version: 17.5.6.8
Release: 1
License: ASL 2.0
Group: "Development/Languages"
Source: %{_tarname}
URL: http://www.erlang.org
Packager:  <mark@control-alt-del.org>
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
%global conf_flags --enable-shared-zlib --without-javac --without-odbc --enable-dirty-schedulers
./otp_build autoconf
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %configure %{conf_flags}
make clean
touch lib/cosEvent/SKIP
touch lib/cosEventDomain/SKIP
touch lib/cosFileTransfer/SKIP
touch lib/cosNotification/SKIP
touch lib/cosProperty/SKIP
touch lib/cosTime/SKIP
touch lib/cosTransactions/SKIP
touch lib/jinterface/SKIP
touch lib/megaco/SKIP
touch lib/odbc/SKIP
touch lib/orber/SKIP
touch lib/test_server/SKIP
make -j4

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir}/erlang -type f -name info -delete
rm -rf %{buildroot}%{_libdir}/erlang/erts-*/man
rm -rf %{buildroot}%{_libdir}/erlang/Install

for exe in %{buildroot}%{_libdir}/erlang/erts-*/bin/*
do
    base="$(basename "$exe")"
    next="%{buildroot}%{_libdir}/erlang/bin/${base}"
    rel="$(echo "$exe" | sed "s,^%{buildroot}%{_libdir}/erlang/,../,")"
    if cmp "$exe" "$next"; then
        ln -sf "$rel" "$next"
        fi
done
for exe in %{buildroot}%{_libdir}/erlang/bin/*
do
    base="$(basename "$exe")"
    next="%{buildroot}%{_bindir}/${base}"
    rel="$(echo "$exe" | sed "s,^%{buildroot},,")"
    if cmp "$exe" "$next"; then
        ln -sf "$rel" "$next"
        fi
done

chrpath -d %{buildroot}%{_libdir}/erlang/lib/crypto-*/priv/lib/crypto.so

%post
echo "Erlang OTP %{version} installed"

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_bindir}/*

%clean
rm -rf %{buildroot}
