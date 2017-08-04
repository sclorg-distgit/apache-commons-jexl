%{?scl:%scl_package apache-%{jarname}}
%{!?scl:%global pkg_name %{name}}

%global jarname commons-jexl
%global compatver 2.1.0

Name:           %{?scl_prefix}apache-%{jarname}
Version:        2.1.1
Release:        18.2%{?dist}
Summary:        Java Expression Language (JEXL)
License:        ASL 2.0
URL:            http://commons.apache.org/jexl
BuildArch:      noarch

Source0:        http://www.apache.org/dist/commons/jexl/source/%{jarname}-%{version}-src.tar.gz

# Patch to fix test failure with junit 4.11
Patch0:         001-Fix-tests.patch
# Fix javadoc build
Patch1:         apache-commons-jexl-javadoc.patch
Patch2:         0001-Port-to-current-javacc.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(commons-logging:commons-logging)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.mojo:javacc-maven-plugin)

Provides:       %{?scl_prefix}%{jarname} = %{version}-%{release}

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
Requires:       %{?scl_prefix}jpackage-utils
Provides:       %{?scl_prefix}%{jarname}-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{jarname}-%{version}-src
%patch0 -p1 -b .test
%patch1 -p1 -b .javadoc
%patch2 -p1

# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +

# Drop "-SNAPSHOT" from version
%pom_xpath_set "pom:project/pom:version" %{compatver} jexl2-compat
%pom_xpath_set "pom:dependency[pom:artifactId='commons-jexl']/pom:version" %{version} jexl2-compat

echo "
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.fedoraproject</groupId>
  <artifactId>commons-jexl-aggegator</artifactId>
  <version>%{version}</version>
  <packaging>pom</packaging>
  <modules>
    <module>.</module>
    <module>jexl2-compat</module>
  </modules>
</project>" >>aggregator-pom.xml
%mvn_package :commons-jexl-aggegator __noinstall

%build
%mvn_build -- -f aggregator-pom.xml

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 2.1.1-18.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 2.1.1-18.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 07 2016 Michael Simacek <msimacek@redhat.com> - 2.1.1-17
- Port to current javacc

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-16
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 27 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-14
- Build compat package in the same reactor as main module

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-12
- Add patch to fix javadoc build

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-10
- Use Requires: java-headless rebuild (#1067528)

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.1.1-9
- Build JEXL 1.x compat artifact
- Fix directory ownership

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-7
- Install NOTICE file with javadoc package

* Fri Jun 28 2013 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-6
- Update to current maven spec guidelines to fix build (bug 979497)
- Add patch to fix test with junit 4.11

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
