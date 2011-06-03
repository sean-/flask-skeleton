	This is a "LAMP" stack done right... but using *NIX (FreeBSD/Mac),
	nginx, memcache, python and postgresql. :~]

There are several goals with this Skeleton:

1) To demonstrate Flask in action in a complete context, as opposed to the
fragmented set of tools that comprise Flask. Flask as a collection of modules
is great, btw!, but it means you have to bootstrap constantly. Skeleton is
out to combat that.

2) To demonstrate various best practices and combat the effects of the MySQL
stupid juice. Use of MySQL has led to some incredibly bad examples for how to
do things that end up being adopted by organizations and developers as "the
way" for open source products, but in professional development land, there
are diverging strategies. Document and exhibit an increasing number of them
here. Over time, I'd like to incorporate improved practices as they become
known.

3) Maintain Skeleton once the items in the TODO list are complete and shift
it in to maintenance mode. Specifically, I don't want to see it advance
beyond being a good starting point for developers (myself included).

So what started this?

Recently several people asked me for framework recommendations (it feels like
I've tried them all and have developed a few opinions along the way). As of
May 2011 it's Flask, but explaining the bootstrapping process required to get
a decent app up and running is high enough that you can't easily expect a new
programmer to figure it out before their attention span begins to drift. At
the same time I was giving out recommendations and fielding questions
regarding Flask, I also had a flurry of applications that I needed to
write. Ugh.

Bootstrapping any framework is typically a tremendous pain in the ass (and it
shouldn't have to be, but still is). So instead of constantly wasting various
evenings or afternoons looking up the required implementation details to
stitch components that every application needs (e.g. a database, static
files, caching), I started Flask-Skeleton.

I'd been hanging on to a "skeleton" app in my ~/src/template_app directory
for long enough and that I finally decided to kick something out that was
usable and documented. See the TODO for details on what has been completed,
but it was initially released to support structured development with a common
set of design patterns already implemented (i.e. it shouldn't take hours of
research to figure out how to do a mechanical task or get some piece of
infrastructure integrated). All of the provided "scaffolding" resides
somewhere under 'skeleton/' so that your friendly `egrep -r` command can find
the desired string and cement your understanding of the layout (i.e. don't do
the django thing and attempt to be clever by stashing application logic in
random libraries).

With Flask being the awesomest awesomesauce around (at least as of May 2011),
hopefully this contribution from your neighborhood ghost in the machine will
make Flask development a bit easier to get started with and will have a
positive impact on your future application development.

If you find new tricks that are sensible, straightforward and will help other
developers setup their apps in a non-fail way, let me know[1] and I'll
incorporate your changes (including improved documentation, unit tests and
comments).  Cheers and good luck.

To begin making use of this skeleton, step through the instructions in
INSTALL.

[1] https://github.com/sean-/flask-skeleton
