%global vernumber 149

Name:           mame-data-extras
Version:        0.%{vernumber}
Release:        2%{?dist}
Summary:        Extra data files for MAME

License:        Freely redistributable without restriction
URL:            http://mamedev.org
Source1:        http://www.arcade-history.com/dats/history%{vernumber}.7z
Source2:        http://www.mameworld.info/mameinfo/download/Mameinfo0%{vernumber}.zip
Source3:        http://www.kutek.net/mame_roms_pinball/mame32_config_files/ctrlr.rar
# 0.149
Source4:        http://www.progettoemma.net/public/cat/catveren.zip
Source5:        http://nplayers.arcadebelgium.be/files/nplayers0%{vernumber}.zip
Source6:        http://cheat.retrogames.com/download/cheat0%{vernumber}.zip
# 0.148
Source7:        http://www.progettoemma.net/mess/zips/sysinfo.zip
# 0.149
Source8:        http://www.progettosnaps.net/messinfo/messinfo.zip
# 0.148. Get from https://sites.google.com/site/steashii/Home/ and zip
Source9:        category.zip
Source10:       http://mamedev.org/roms/robby/robby.zip

BuildArch:      noarch

BuildRequires:  p7zip
BuildRequires:  unrar

Requires:       mame-data >= %{version}

Provides:       sdlmame-data = 0%{vernumber}-%{release}
Obsoletes:      sdlmame-data < 0146-2

%description
%{summary}.

%package -n mess-data-extras
Summary:        Extra data files for MESS

Requires:       mess-data >= %{version}

%description -n mess-data-extras
%{summary}.

%package robby
Summary:        Robby Roto ROM
License:        Free for no-commercial use

Requires:       mame-data

%description robby
%{summary}.

%prep
%setup -qcT

# extract DAT files
7za x %{SOURCE1}
unzip -qa %{SOURCE2} -d .
7za x Mameinfo0%{vernumber}.7z
mv docs mameinfo
unzip -qaj %{SOURCE4} -d .
mv readme.txt readme-catlist.txt
unzip -qa %{SOURCE5} -d .
mv docs nplayers
unzip -qa %{SOURCE6}
unzip -qa %{SOURCE7} -d .
unzip -qa %{SOURCE8} -d .
7za x pS_messinfo.dat.7z
unzip -qa %{SOURCE9} -d .
unzip -qa %{SOURCE10} readme.txt
mv readme.txt readme-robby.txt

# make it clear what messinfo.dat documentation is
mv pS_messinfo.dat/docs pS_messinfo.dat/messinfo

# clean up extraneous docs
rm -rf pS_messinfo.dat/messinfo/DRIVERs

# fix permissions and line endings
for i in mameinfo pS_messinfo.dat/messinfo
do
    chmod 0755 $i
done 
find . -name \*.txt -and -not -name nplayers.txt -exec sed -i 's/\r//' {} \;

#fix encoding
find *info* -name \*.txt > filelist
while read i
do
    /usr/bin/iconv -f iso8859-1 -t utf-8 "$i" > "$i".conv && /bin/mv -f "$i".conv "$i";
done < filelist


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/mame
install -pm 644 history.dat mameinfo.dat Catver.ini nplayers.ini cheat.7z \
    $RPM_BUILD_ROOT%{_datadir}/mame
install -d $RPM_BUILD_ROOT%{_datadir}/mess
install -pm 644 pS_messinfo.dat/"messinfo.dat Unicode, UTF-8 version (for QMC2)"/messinfo.dat \
    pS_messinfo.dat/folders/version.ini category.ini sysinfo.dat \
    $RPM_BUILD_ROOT%{_datadir}/mess
# The following might be ugly, but it is way simpler than creating a -common
# subpackage and symlinks
install -d $RPM_BUILD_ROOT%{_datadir}/mame/ctrlr
unrar x %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/mame
install -d $RPM_BUILD_ROOT%{_datadir}/mess/ctrlr
unrar x %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/mess
install -d $RPM_BUILD_ROOT%{_datadir}/mame/roms
install -pm 644 %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/mame/roms


%files
%doc nplayers/nplayers.txt mameinfo cheat.txt readme-catlist.txt
%{_datadir}/mame/Catver.ini
%{_datadir}/mame/cheat.7z
%{_datadir}/mame/history.dat
%{_datadir}/mame/mameinfo.dat
%{_datadir}/mame/nplayers.ini
%{_datadir}/mame/ctrlr/*

%files -n mess-data-extras
%doc pS_messinfo.dat/messinfo
%{_datadir}/mess/category.ini
%{_datadir}/mess/messinfo.dat
%{_datadir}/mess/sysinfo.dat
%{_datadir}/mess/version.ini
%{_datadir}/mess/ctrlr/*

%files robby
%doc readme-robby.txt
%{_datadir}/mame/roms/robby.zip


%changelog
* Sun Jun 30 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.149-2
- Updated everything except sysinfo.dat and category.ini to 0.149

* Tue Feb 05 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148-1
- Updated everything except cheats and catlist to 0.148
- %%define → %%global
- Fixed robby.zip permissions
- Killed superfluous messinfo.dat documentation

* Mon Oct 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147-2
- Updated everything to 0.147
- Added Robby Roto ROM

* Fri Sep 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147-1
- Rebooted as mame-data-extras, incorporating mess support files
