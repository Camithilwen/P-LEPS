def load_numpy(finder, module):
    """Find the numpy core extensions"""
    finder.IncludePackage("numpy.core._multiarray_umath")
    finder.IncludePackage("numpy.core._multiarray_tests")
    finder.IncludePackage("numpy.core._rational_tests")
    finder.IncludePackage("numpy.core._struct_ufunc_tests")
    finder.IncludePackage("numpy.core._umath_tests")
    finder.IncludePackage("numpy.random")
