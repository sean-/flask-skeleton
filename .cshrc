# Sean's .cshrc file: http://sean.chittenden.org/pubfiles/dot.cshrc.txt
#
# System-wide /etc/csh.cshrc or ~/.cshrc file for tcsh(1).

# UTF-8 or go home.
setenv LC_TYPE en_US.utf-8

### Set various path bits
if ( ! $?newpath ) set newpath
foreach d ($path /usr/local/sbin /usr/pkg/sbin /opt/local/sbin /usr/local/bin /usr/pkg/bin /opt/local/bin $HOME/sbin $HOME/bin $path)
	if ( -d $d ) then
		set -f newpath = ( $newpath $d )
	endif
end
set path = ( $newpath )
unset d
unset newpath

### Handle various interactive components
if ($?prompt) then
	# Do the tcsh auto-source tab completion thang
	foreach f (/opt/local/share/mercurial/contrib/tcsh_completion /usr/local/share/mercurial/contrib/tcsh_completion )
		if ( -s $f ) then
			source $f
		endif
	end

	### Begin the autohost completion thang
	set noglob
	if ( ! $?hosts ) then
		set hosts
	endif

	foreach f ($HOME/.hosts /usr/local/etc/csh.hosts $HOME/.rhosts /etc/hosts.equiv)
		if ( -s $f ) then
			set hosts = ($hosts `grep -v "+" $f | grep -E -v "^#" | tr -s " " "	" | cut -f 1`)
		endif
	end
	if ( -s $HOME/.netrc ) then
		set f=`awk '/machine/ { print $2 }' < $HOME/.netrc` >& /dev/null
		set hosts=($hosts $f)
	endif
	foreach f (/etc/ssh/known_hosts /etc/ssh_known_hosts $HOME/.ssh/known_hosts )
		if ( -s $f ) then
			set ssh_hosts=`grep -v '^#' $f | perl -p -e 's#\[([^\]]*)\]:(\d)#$1:$2#g' | cut -f 1 -d , | cut -f -1 -d ' '` >& /dev/null
			set hosts=($hosts $ssh_hosts)
			unset ssh_hosts
		endif
	end
	unset f
	unset noglob
	### End autohost-ification foo

	# environment variables
	complete unsetenv 'p/1/e/'
	complete setenv 'p/1/e/'
	#(kinda cool: complete first arg with an env variable, and add an =,
	# continue completion of first arg with a filename.  complete 2nd arg
	# with a command)
	complete env 'c/*=/f/' 'p/1/e/=/' 'p/2/c/'

	# Ahh... the keystroke savings!!!
	complete sysctl 'n/*/`sysctl -Na`/'
	complete mtr 'p/1/$hosts/'
	complete ssh 'p/1/$hosts/' 'p/2/c/'
	complete scp "c,*:/,F:/," "c,*:,F:$HOME," 'c/*@/$hosts/:/'


	# Aliases
	alias ll ls -lAG
	alias rm rm -i
	alias cp cp -i
	alias mv mv -i
	alias fs fossil
	alias emacs emacs --no-splash
	alias dmalloc 'eval `\dmalloc -C \!*`'

	# mmm... Kerberos
	alias kscp scp -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes
	alias kssh ssh -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes

	alias altq_see pfctl -vvsq
	alias pflog tcpdump -X -vvv -n -e -ttt -i pflog0
	alias asterisk_cli asterisk -r

	# An interactive shell -- set some stuff up
	set autolist
	set autocorrect
	set autoexpand
	set color
	set colorcat
	set complete = 'enhance'
	set echo_stype = 'both'
	set filec
	set fignore = (\~ .svn CVS .o .bak)
	set histdup = 'erase'
	set history = 10000
	set implicitcd
	set listjobs = long

	/bin/mkdir -pm 0700 /tmp/tmp

	if ( -d ~/Mail/inbox/new/ ) then
		set mail = ~/Mail/inbox/new/
	endif

	set printexitvalue
	set promptchars = '%#'
	set prompt = "%T %B%n%b@%m %# %L"
	set rmstar
#	set rprompt = "%~"
	set savehist = 10000 merge
	set time=(8 "\
Time spent in user mode   (CPU seconds) : %Us\
Time spent in kernel mode (CPU seconds) : %Ss\
Total time                              : %Es\
CPU utilisation (percentage)            : %P\
Times the process was swapped           : %W\
Times of major page faults              : %F\
Times of minor page faults              : %R")

	set watch=(0 any any)
	set who="%n has %a %l from %M."

	if ( $?tcsh ) then
		bindkey "^W" backward-delete-word
		bindkey -k up history-search-backward
		bindkey -k down history-search-forward
	endif

	setenv SVN_EDITOR vi
	setenv CVS_RSH ssh
	setenv M ~/src/stackjet/mercury
	setenv MO $M/obj/contrib-`uname -s`-`uname -m`

	# Change the behavior of the shell/environment based on the current directory
	alias cwdcmd 'if (-o .enter.tcsh) source .enter.tcsh'
	alias popd 'if ("\!*" == "" && -o .exit.tcsh) source .exit.tcsh; ""popd \!*'
	alias cd 'if (-o .exit.tcsh) source .exit.tcsh; chdir \!*'
	alias pushd 'if (-o .exit.tcsh) source .exit.tcsh; ""pushd \!*'
endif
