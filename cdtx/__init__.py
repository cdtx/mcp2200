# This is an implicit namespace package (https://www.python.org/dev/peps/pep-0420/)
# It's built with the help of the setuptools's functionality : (http://setuptools.readthedocs.io/en/latest/setuptools.html#namespace-packages)
__import__('pkg_resources').declare_namespace(__name__)

# No other code shall be written after.
