
class JackAnalyzer:
    """
    The analyzer program operates on a given source,
    where source is either a file name of the form Xxx.jack
    or a directory name containing one or more such files.

    For each source Xxx.jack file,
    the analyzer goes through the following logic:

    1. Create a JackTokenizer from the Xxx.jack input file.
    2. Create an output file called Xxx.xml and prepare it for writing.
    3. Use the CompilationEngine to compile the input JackTokenizer
       into the output file.

    """

    # todo add file handling stuff and logic from ex9

