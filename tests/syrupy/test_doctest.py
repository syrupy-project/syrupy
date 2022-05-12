def doctest_fn():
    """a doctest in a function docstring
    >>> doctest_fn() == getfixture('snapshot')
    True
    """
    return "doc test fn return value"


class DocTestClass:
    """
    >>> DocTestClass() == getfixture('snapshot')
    True

    a doctest in a class docstring
    >>> DocTestClass() == getfixture('snapshot')
    True
    """

    obj_attr = "test class attr"

    def doctest_method(self):
        """a doctest in a method docstring
        >>> DocTestClass().doctest_method() == getfixture('snapshot')
        True
        """
        return "doc test method return value"

    class NestedDocTestClass:
        """a doctest in a nested class docstring
        >>> DocTestClass.NestedDocTestClass() == getfixture('snapshot')
        True
        """

        nested_obj_attr = "nested doc test class attr"

        def doctest_method(self):
            """a doctest in a nested method docstring
            >>> nested_obj = DocTestClass.NestedDocTestClass()
            >>> nested_obj.doctest_method() == getfixture('snapshot')
            True
            """
            return "nested doc test method return value"
