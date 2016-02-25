%global pkg_name apache-commons-jexl
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global jarname commons-jexl

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.1.1
Release:        9.13%{?dist}
Summary:        Java Expression Language (JEXL)

License:        ASL 2.0
URL:            http://commons.apache.org/jexl
Source0:        http://www.apache.org/dist/commons/jexl/source/%{jarname}-%{version}-src.tar.gz
# Patch to fix test failure with junit 4.11
Patch0:         001-Fix-tests.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}apache-commons-parent >= 26-7
BuildRequires:  %{?scl_prefix}javacc-maven-plugin

BuildArch:      noarch


%description
Java Expression Language (JEXL) is an expression language engine which can be
embedded in applications and frameworks.  JEXL is inspired by Jakarta Velocity
and the Expression Language defined in the JavaServer Pages Standard Tag
Library version 1.1 (JSTL) and JavaServer Pages version 2.0 (JSP).  While
inspired by JSTL EL, it must be noted that JEXL is not a compatible
implementation of EL as defined in JSTL 1.1 (JSR-052) or JSP 2.0 (JSR-152).
For a compatible implementation of these specifications, see the Commons EL
project.

JEXL attempts to bring some of the lessons learned by the Velocity community
about expression languages in templating to a wider audience.  Commons Jelly
needed Velocity-ish method access, it just had to have it.


%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n %{jarname}-%{version}-src
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p1 -b .test
# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 2.1.1-9.13
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.1.1-9.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.1.1-9.11
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.1.1-9.9
- Mass rebuild 2015-01-13

* Thu Jan 08 2015 Michal Srb <msrb@redhat.com> - 2.1.1-9.8
- Use .mfiles wherever possible

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.1.1-9.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-9.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.1-9
- Mass rebuild 2013-12-27

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-8
- Add BuildRequires on apache-commons-parent >= 26-7

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-7
- Install NOTICE file with javadoc package

* Thu Jun 28 2013 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-6
- Update to current maven spec guidelines to fix build (bug 979497)
- Add patch to fix test with junit 4.11

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-1
- Update to 2.1.1

* Mon Dec 12 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1-1
- Update to 2.1
- Update bsf patch
- Add needed BRs

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.1-4
- Packaging fixes
- New maven macro for depmaps (include a compat depmap) #745118

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 6 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-3
- Use BR apache-commons-parent

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-2
- Add license to javadoc package

* Wed May 26 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-1
- Update to 2.0.1
- Require Java 1.6 or greater
- Drop language level patch
- Add patch to remove bsf-api 3.0 dependency from pom.xml as this is provided
  by Java 1.6
- Fix depmap group id

* Sat Jan 9 2010 Orion Poplawski <orion@cora.nwra.com> - 1.1-3
- Drop gcj support
- Fix javadoc group
- Bump java levels in pom.xml

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 1.1-2
- Rename to apache-commons-jexl

* Tue Oct 27 2009 Orion Poplawski <orion@cora.nwra.com> - 1.1-1
- Initial Fedora Package
