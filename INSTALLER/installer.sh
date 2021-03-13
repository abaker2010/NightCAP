unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

OS="`uname`"
SEP=""
case $OS in
  'Linux')
    OS='Linux'
    SEP="/"
    alias ls='ls --color=auto'
    ;;
  'FreeBSD')
    OS='FreeBSD'
    SEP="/"
    alias ls='ls -G'
    ;;
  'WindowsNT')
    OS='Windows'
    SEP="\\"
    ;;
  'Darwin') 
    OS='Mac'
    SEP="/"
    ;;
  'SunOS')
    OS='Solaris'
    SEP="/"
    ;;
  'AIX') ;;
  *) ;;
esac



echo $OS
echo $SEP
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Installing nightcapcore plugin/requirements
echo "python3.8 -m pip install -e "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapcore"$SEP
core_installer="python3.8 -m pip install -e "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapcore"$SEP
core_re_installer="python3.8 -m pip install -r "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapcore"$SEP"requirements.txt"

# Installing nightcappackages plugin/requirements
packages_installer="python3.8 -m pip install -e "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcappackages"$SEP
packages_re_installer="python3.8 -m pip install -r "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcappackages"$SEP"requirements.txt"

# Installing nightcapserver plugin/requirements
packages_installer="python3.8 -m pip install -e "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapserver"$SEP
packages_re_installer="python3.8 -m pip install -r "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapserver"$SEP"requirements.txt"

# Installing nightcapcli plugin/requirements
packages_installer="python3.8 -m pip install -e "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapcli"$SEP
packages_re_installer="python3.8 -m pip install -r "$SCRIPTPATH$SEP".."$SEP"packages"$SEP"nightcapcli"$SEP"requirements.txt"

# Installing main requirements
main_re_installer="python3.8 -m pip install -r "$SCRIPTPATH$SEP".."$SEP"requirements.txt"

eval $core_installer
eval $core_re_installer
eval $packages_installer
eval $packages_re_installer
eval $main_re_installer