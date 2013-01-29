=============
Customization
=============

.. content::
    :depth: 3


Intitialisation
===============

You can tweak your development environment quite alot. 

To do so, simply type this command:

.. code-block:: bash

    user@host$ duke customize
    Copying setup.py to ~/.duke/templates/
    Copying profile to ~/.duke/templates/
    Copying bootstrap.py to ~/.duke/templates/
    Copying gitignore to ~/.duke/templates/
    Copying buildout.cfg to ~/.duke/templates/
    Copying project_conf.yml to ~/.duke/templates/
    Copying dev to ~/.duke/templates/
    Copying env to ~/.duke/templates/
    Copying duke_conf.yml to ~/.duke/templates/
    Copying base.cfg to ~/.duke/templates/
    Copying svnignore to ~/.duke/templates/
    Copying dev.cfg to ~/.duke/templates/

Files
=====
In the same shell:

.. code-block:: bash

    user@host$ cd ~/.duke/templates
    user@host$ ls
    base.cfg  bootstrap.py  buildout.cfg  dev  dev.cfg  duke_conf.yml  env  gitignore  profile  project_conf.yml  setup.py  svnignore

The files `profile` and `env` are used to personalize your prompt, or to add commands (alias) .


Customize prompt
================

If you want to modify your duke prompt, (simply) you have to edit `profile`.

Here the default `profile` file:

.. code-block:: bash
    
    # Typing "--settings=projectname.settingsfile" is annoying.
    DJANGO_SETTINGS_MODULE=settings
    SEP="|"
    ENDCHAR="$ "
    DUKE_DIRTRIM=2
    DUKE_DJANGO_STR="django:"
    DUKE_SVN_STR="svn:"
    DUKE_GIT_STR="git:"
    DUKE_PS1="${NO_COLOR}\u@\h${SEP}${BOLD_CYAN}\$(__in_project)${CYAN}%(project_name)s${NO_COLOR}${SEP}${BOLD_YELLOW}\$(__vcs_status)${YELLOW}\w${NO_COLOR}${ENDCHAR}"

will produce the following prompt:

.. code-block:: bash

    user@host|projectname|svn:~/.../path/in/project$

You can change de value of the variable to personalize your prompt.

If it's not enough, you can edit the `env` file.

.. caution::
    all that you make in `profile` overwrite `env`


Here the default `env` file:

.. code-block:: bash

    . ~/.bashrc 
    # based on virtualenv's activate
    # This file must be used with "source bin/activate" *from bash*
    # you cannot run it directly

    # Shell colors
    BLACK="\[\e[0;30m\]"    BOLD_BLACK="\[\e[1;30m\]"   UNDER_BLACK="\[\e[4;30m\]"
    RED="\[\e[0;31m\]"      BOLD_RED="\[\e[1;31m\]"     UNDER_RED="\[\e[4;31m\]"
    GREEN="\[\e[0;32m\]"    BOLD_GREEN="\[\e[1;32m\]"   UNDER_GREEN="\[\e[4;32m\]"
    YELLOW="\[\e[0;33m\]"   BOLD_YELLOW="\[\e[1;33m\]"  UNDER_YELLOW="\[\e[4;33m\]"
    BLUE="\[\e[0;34m\]"     BOLD_BLUE="\[\e[1;34m\]"    UNDER_BLUE="\[\e[4;34m\]"
    PURPLE="\[\e[0;35m\]"   BOLD_PURPLE="\[\e[1;35m\]"  UNDER_PURPLE="\[\e[4;35m\]"
    CYAN="\[\e[0;36m\]"     BOLD_CYAN="\[\e[1;36m\]"    UNDER_CYAN="\[\e[4;36m\]"
    WHITE="\[\e[0;37m\]"    BOLD_WHITE="\[\e[1;37m\]"   UNDER_WHITE="\[\e[4;37m\]"
    NO_COLOR="\[\e[0m\]"

    parse_git_branch () {
      git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
    }

    parse_git_dirty () {
      [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
    }

    __vcs_status () {
        if [ -d "$PWD/.svn" ]; then
            echo "$DUKE_SVN_STR"
        elif [ -n "$(parse_git_branch)" ]; then
            echo "$DUKE_GIT_STR"
        fi
    }

    # Prefix the command prompt with %(project_name)s
    function __in_project {
        if [ "`pwd | xargs basename`" = "%(project_name)s" ] ; then
            echo "$DUKE_DJANGO_STR"
        else
            echo ""
        fi
    }

    # Duke client default environment variables

    DUKE_ENV="%(base_path)s"
    DUKE_DIRTRIM=2
    CUSTOM_TEMPLATES="~/.duke/templates"
    _DUKE_OLD_PATH="$PATH"


    # Add bin/ to the executable path to make them available
    # without having to type their path and make all scripts 
    # in it executables.
    PATH="$DUKE_ENV/.duke/bin:$PATH"
    export PATH
    chmod a+x $DUKE_ENV/.duke/bin/*

    # unset PYTHONHOME if set
    # this will fail if PYTHONHOME is set to the empty string (which is bad anyway)
    # could use `if (set -u; : $PYTHONHOME) ;` in bash
    if [ -n "$PYTHONHOME" ] ; then
        _DUKE_OLD_PYTHONHOME="$PYTHONHOME"
        unset PYTHONHOME
    fi
     
    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
        hash -r
    fi

    # set a fancy prompt (non-color, unless we know we "want" color)
    case "$TERM" in
        xterm-color) color_prompt=yes;;
    esac

    # Django commands

    function __django {
        if [ -e "settings.py" ] ; then
            django $@
        else
            echo "Error: You must be within a django project to use this command."
        fi
    }

    alias syncdb="__django syncdb"
    alias runserver="__django runserver"
    alias shell="__django shell"
    alias dbshell="__django dbshell"
    alias loaddata="__django loaddata"
    alias dumpdata="__django dumpdata"

    # Duke commands 

    function __duke {
        if [ -e "buildout.cfg" ] ; then
            $@
        else
            echo "Error: You must be within a duke project to use this command."
        fi
    }

    # FIXME: The -vv flag is only a dirty hack to workaround a suspected 
    # threading issue with python. For some reason, on a fast machine with 
    # multiple cores, buildout hangs randomly. Increasing buildout's output
    # solves this issue. If you are still experiencing this problem, consider
    # using -vvv for even more output.
    # https://github.com/fschulze/mr.developer/pull/76
    alias buildout='__duke buildout -c dev.cfg -vv'
    alias dev='__duke develop'

    # Python commands

    # Make sure that while within the dev environment we only
    # use the sandboxed python interpreter.
    alias python="$DUKE_ENV/.duke/bin/python -S" 
    alias ipython="$DUKE_ENV/.duke/bin/ipython --autoindent --no-banner --deep-reload"

    # Prompt

    function __duke_prompt {
        if [ -z "$DUKE_ENV_DISABLE_PROMPT" ] ; then
            _DUKE_OLD_PS1="$PS1"
            _DUKE_OLD_DIRTRIM="$PROMPT_DIRTRIM"
            . profile
            
            if [ "x" != x ] ; then
                PS1="$PS1"
            elif [ "`basename \"$DUKE_ENV\"`" = "__" ] ; then
                # special case for Aspen magic directories
                # see http://www.zetadev.com/software/aspen/
                PS1="(%(project_name)s$(in_project)) $PS1"
                PROMPT_DIRTRIM="$PROMPT_DIRTRIM"
            else
                PROMPT_DIRTRIM="$DUKE_DIRTRIM"
                PS1="$DUKE_PS1"
            fi
            export PS1
            export PROMPT_DIRTRIM
        fi
    }
    __duke_prompt




In this file you can creat / modify some variable.
For exemple if you want toi create a new alias for the django collectstatic commande, you juste have to add this line::

    alias collectstatic="__django collectstatic"
