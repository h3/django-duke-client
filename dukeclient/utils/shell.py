import re

def confirm(message, default=False, yes=['y', 'yes'], no=['n', 'no'], 
        yn='Y/n', ny='[y/N]'):

    if default: yn = yn
    else:       yn = ny

    rs = raw_input('%s %s: ' % (message, yn))

    if rs == '': return default
    elif rs not in yes + no:
        return confirm(message, default)
    else: return rs in yes 


# Borrowed from fabric

def prompt(text, default='', validate=None):
    """
Prompt user with ``text`` and return the input (like ``raw_input``).

A single space character will be appended for convenience, but nothing
else. Thus, you may want to end your prompt text with a question mark or a
colon, e.g. ``prompt("What hostname?")``.

If ``default`` is given, it is displayed in square brackets and used if the
user enters nothing (i.e. presses Enter without entering any text).
``default`` defaults to the empty string. If non-empty, a space will be
appended, so that a call such as ``prompt("What hostname?",
default="foo")`` would result in a prompt of ``What hostname? [foo]`` (with
a trailing space after the ``[foo]``.)

The optional keyword argument ``validate`` may be a callable or a string:

* If a callable, it is called with the user's input, and should return the
value to be stored on success. On failure, it should raise an exception
with an exception message, which will be printed to the user.
* If a string, the value passed to ``validate`` is used as a regular
expression. It is thus recommended to use raw strings in this case. Note
that the regular expression, if it is not fully matching (bounded by
``^`` and ``$``) it will be made so. In other words, the input must fully
match the regex.

Either way, `prompt` will re-prompt until validation passes (or the user
hits ``Ctrl-C``).

.. note::
`~fabric.operations.prompt` honors :ref:`env.abort_on_prompts
<abort-on-prompts>` and will call `~fabric.utils.abort` instead of
prompting if that flag is set to ``True``. If you want to block on user
input regardless, try wrapping with
`~fabric.context_managers.settings`.

Examples::

# Simplest form:
environment = prompt('Please specify target environment: ')

# With default, and storing as env.dish:
prompt('Specify favorite dish: ', 'dish', default='spam & eggs')

# With validation, i.e. requiring integer input:
prompt('Please specify process nice level: ', validate=int)

# With validation against a regular expression:
release = prompt('Please supply a release name',
validate=r'^\w+-\d+(\.\d+)?$')

# Prompt regardless of the global abort-on-prompts setting:
with settings(abort_on_prompts=False):
prompt('I seriously need an answer on this! ')

"""
    # Set up default display
    default_str = ""
    if default != '':
        default_str = " [%s] " % str(default).strip()
    else:
        default_str = " "
    # Construct full prompt string
    prompt_str = text.strip() + default_str
    # Loop until we pass validation
    value = None
    while value is None:
        # Get input
        value = raw_input(prompt_str) or default
        # Handle validation
        if validate:
            # Callable
            if callable(validate):
                # Callable validate() must raise an exception if validation
                # fails.
                try:
                    value = validate(value)
                except Exception, e:
                    # Reset value so we stay in the loop
                    value = None
                    print("Validation failed for the following reason:")
                    print(indent(e.message) + "\n")
            # String / regex must match and will be empty if validation fails.
            else:
                # Need to transform regex into full-matching one if it's not.
                if not validate.startswith('^'):
                    validate = r'^' + validate
                if not validate.endswith('$'):
                    validate += r'$'
                result = re.findall(validate, value)
                if not result:
                    print("Regular expression validation failed: '%s' does not match '%s'\n" % (value, validate))
                    # Reset value so we stay in the loop
                    value = None
    # And return the value, too, just in case someone finds that useful.
    return value
