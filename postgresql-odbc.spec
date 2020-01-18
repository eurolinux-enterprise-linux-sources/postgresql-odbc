Name: postgresql-odbc
Summary: PostgreSQL ODBC driver
Version: 09.03.0100
Release: 2%{?dist}
License: LGPLv2+
Group: Applications/Databases
URL: http://psqlodbc.projects.postgresql.org/

Source0: http://ftp.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz

# CAUTION: acinclude.m4 has to be kept in sync with package's aclocal.m4.
# This is a kluge that ought to go away, but upstream currently isn't
# shipping their custom macros anywhere except in aclocal.m4.  (The macros
# actually come from the Postgres source tree, but we haven't got that
# available while building this RPM.)  To generate: in psqlodbc source tree,
#   aclocal -I . -I $PGSRC/config
# then strip aclocal.m4 down to just the PGAC macros.
# BUT: as of 09.01.0200, configure.ac hasn't been updated to use latest
# PG macros, so keep using the previous version of acinclude.m4.
Source1: acinclude.m4

BuildRequires: unixODBC-devel
BuildRequires: libtool automake autoconf postgresql-devel
BuildRequires: openssl-devel krb5-devel pam-devel zlib-devel readline-devel

# This spec file and ancillary files are licensed in accordance with 
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n psqlodbc-%{version}

# Some missing macros.  Courtesy Owen Taylor <otaylor@redhat.com>.
cp -p %{SOURCE1} .

# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4 config/libtool.m4

libtoolize --force  --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build

%configure --with-unixodbc --disable-dependency-tracking

make

%install

make DESTDIR=$RPM_BUILD_ROOT install

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file
pushd ${RPM_BUILD_ROOT}%{_libdir}
	ln -s psqlodbcw.so psqlodbc.so
	rm psqlodbcw.la
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%attr(755,root,root) %{_libdir}/psqlodbcw.so
%{_libdir}/psqlodbc.so
%doc license.txt readme.txt docs/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 09.03.0100-2
- Mass rebuild 2014-01-24

* Mon Jan 06 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0100-1
- update to new release

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 09.01.0200-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Tom Lane <tgl@redhat.com> 09.01.0200-2
- Update tarball URL in specfile (no actual package change)

* Mon Aug 20 2012 Tom Lane <tgl@redhat.com> 09.01.0200-1
- Update to version 09.01.0200
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 09.01.0100-1
- Update to version 09.01.0100

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.00.0200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 09.00.0200-1
- Update to version 09.00.0200

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 08.04.0200-2
- Correct Source0: tag and comment to reflect how to get the tarball

* Wed Dec 30 2009 Tom Lane <tgl@redhat.com> 08.04.0200-1
- Update to version 08.04.0200

* Fri Aug 28 2009 Tom Lane <tgl@redhat.com> 08.04.0100-2
- Rebuild with new openssl

* Tue Aug 18 2009 Tom Lane <tgl@redhat.com> 08.04.0100-1
- Update to version 08.04.0100

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 08.03.0200-2
- Rebuild for unixODBC 2.2.14.

* Tue Aug  5 2008 Tom Lane <tgl@redhat.com> 08.03.0200-1
- Update to version 08.03.0200

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 08.03.0100-1
- Update to version 08.03.0100
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.

* Fri Nov  2 2007 Tom Lane <tgl@redhat.com> 08.02.0500-1
- Update to version 08.02.0500

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 08.02.0200-2
- Update License tag to match code.

* Wed Apr 25 2007 Tom Lane <tgl@redhat.com> 08.02.0200-1
- Update to version 08.02.0200

* Mon Dec 11 2006 Tom Lane <tgl@redhat.com> 08.01.0200-4
- Rebuild for new Postgres libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-3.1
- rebuild

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 08.01.0200-3
- Fix BuildRequires: for mock build environment

* Wed Mar 22 2006 Tom Lane <tgl@redhat.com> 08.01.0200-2
- Change library name back to psqlodbc.so, because it appears that upstream
  will revert to that name in next release; no point in thrashing the name.
- Include documentation files unaccountably omitted before (bug #184158)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tom Lane <tgl@redhat.com> 08.01.0200-1
- Update to version 08.01.0200.
- Upstream now calls the library psqlodbcw.so ... add a symlink to avoid
  breaking existing odbc configuration files.

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 08.01.0102-1
- Update to version 08.01.0102.
- Add buildrequires postgresql-devel (bz #174505)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 08.01.0100-1
- Update to version 08.01.0100.

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 08.00.0100-1
- Update to version 08.00.0100.

* Fri Nov 12 2004 Tom Lane <tgl@redhat.com> 7.3-9
- back-port 64-bit fixes from current upstream (bug #139004)

* Tue Sep 21 2004 Tom Lane <tgl@redhat.com> 7.3-8
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com>
- Correct License: annotation.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 21 2003 David Jee <djee@redhat.com> 7.3-5
- rebuild

* Wed Nov 05 2003 David Jee <djee@redhat.com> 7.3-4
- import new community version 07.03.0200

* Mon Sep 15 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- autotools fixes (courtesy Alex Oliva <aoliva@redhat.com> and 
  Owen Taylor <otaylor@redhat.com>)

* Tue Jul 08 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- allow use with unixODBC (courtesy Troels Arvin) [Bug #97998]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 02 2003 Andrew Overholt <overholt@redhat.com> 7.3-1
- sync to new community version (07.03.0100 => v7.3, r1)

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 1-2
- rebuild

* Tue Jan 14 2003 Andrew Overholt <overholt@redhat.com>
- 1-1
- initial build (just took old package sections)
