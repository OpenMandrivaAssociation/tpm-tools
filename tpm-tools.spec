%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define srcversion 1.3.3-2

Summary:	Management tools for the TPM hardware
Name:		tpm-tools
Version:	1.3.3
Release:	%mkrel 3
Group:		System/Servers
License:	CPL
URL:		http://www.sf.net/projects/trousers
Source0:	http://downloads.sourceforge.net/trousers/%{name}-%{srcversion}.tar.gz
Patch0:		tpm-tools-linkage_fix.diff
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	trousers-devel
BuildRequires:	opencryptoki-devel
BuildRequires:	openssl-devel
Requires:       trousers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
tpm-tools is a group of tools to manage and utilize the Trusted Computing
Group's TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's
software state using cryptographic hashes and more.

%package -n	%{libname}
Summary:	Implementation of the TCG's Software Stack v1.1 Specification
Group:          System/Libraries

%description -n	%{libname}
tpm-tools is a group of tools to manage and utilize the Trusted Computing
Group's TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's
software state using cryptographic hashes and more.

%package -n	%{develname}
Summary:	Files to use the library routines supplied with tpm-tools
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n	%{develname}
tpm-tools-devel is a package that contains the libraries and headers
necessary for developing tpm-tools applications.

%package	pkcs11
Summary:	Data management tools that use a PKCS#11 interface to the TPM
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	opencryptoki >= 2.2.4

%description	pkcs11
tpm-tools-pkcs11 is a group of tools that uses the TPM PKCS#11 token
developed in the opencryptoki project.  All data contained in the
PKCS#11 data store is protected by the TPM (keys, certificates, etc.).
You can import keys and certificates, list out the objects in the data
store, and protect data.

%prep
%setup -q
%patch0 -p0
sed -i -e "s/-Wall -Werror//" configure*

%build
rm -rf autom4te.cache 
autoreconf --force --install

%configure2_5x \
    --disable-rpath

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/tpm_*
%attr(755,root,root) %{_sbindir}/tpm_*
%{_mandir}/man1/tpm_*
%{_mandir}/man8/tpm_*

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/*.so.%{major}*

%files pkcs11
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/tpmtoken_*
%{_mandir}/man1/tpmtoken_*

%files -n %{develname}
%defattr(-,root,root,-)
%dir %{_includedir}/tpm_tools
%{_includedir}/tpm_tools/*.h
%{_libdir}/*.so
%{_libdir}/*.la
%{_mandir}/man3/tpmUnseal*
