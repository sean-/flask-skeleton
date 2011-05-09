# Sean's .cshrc file. Why? 'cause bash(1) sucks and you won't look back once
# you make the switch. Use sh(1) for scripts and tcsh(1) for your shell.
#
# Can be installed per-user at ~/.cshrc or system-wide at /etc/csh.cshrc

# UTF-8 or go home.
setenv LC_TYPE en_US.utf-8

### Set various path bits
if ( ! $?newpath ) set newpath
foreach d ($path /usr/local/sbin /opt/local/sbin /usr/local/bin /opt/local/bin $HOME/sbin $HOME/bin)
	if ( -d $d ) then
		set -f newpath = ( $newpath $d )
	endif
end
set path = ( $newpath )
unset d
unset newpath

### Handle various interactive components
if ($?prompt) then
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
	# This isn't perfect. If you've connected to a host via ssh on a
	# different port, you may see: example.com:1234. Need to clean this
	# up.
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


	# OS-specific aliases. Be sure to copy and port aliases on new OS
	# types.
	switch ($OSTYPE)
	case "freebsd":
	case "darwin":
		# FreeBSD's ls(1) uses the -G flag to enable color
		alias ll ls -lAG
		breaksw
	default:
		alias ll ls -lA
		breaksw
	endsw
	alias rm rm -i
	alias cp cp -i
	alias mv mv -i
	alias fs fossil
	alias emacs emacs --no-splash
	alias dmalloc 'eval `\dmalloc -C \!*`'

	# mmm... Kerberos
	alias kscp scp -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes
	alias kssh ssh -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes

	# A few handy BSD aliases that I refuse to retire
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
	set fignore = (\~ .bak .class CVS .git .o .pyc .svn)
	set histdup = 'erase'
	set histfile = ~/.history
	set history = 10000
	set implicitcd
	set listjobs = long

	# I like having a temp directory that I can stash things in knowing
	# that it will be blown away. Significantly helps reduce clutter.
	/bin/mkdir -pm 0700 /tmp/${USER}

	if ( -d ~/Mail/inbox/new/ ) then
		set mail = ~/Mail/inbox/new/
	endif

	set printexitvalue
	set promptchars = '%#'
	set prompt = "%T %B%n%b@%m %# %L"
	set rmstar
	# There are days when I like having a prompt to the right of my cursor.
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

	# I program using emacs and edit checkins or system files with
	# vi(1). As such, I don't set an EDITOR variable globally.
	setenv SVN_EDITOR vi
	setenv CVS_RSH ssh

	# Change the behavior of the shell/environment based on the current
	# directory.
	alias cwdcmd 'if (-o .enter.tcsh) source .enter.tcsh'
	alias popd 'if ("\!*" == "" && -o .exit.tcsh) source .exit.tcsh; ""popd \!*'
	alias cd 'if (-o .exit.tcsh) source .exit.tcsh; chdir \!*'
	alias pushd 'if (-o .exit.tcsh) source .exit.tcsh; ""pushd \!*'
endif
