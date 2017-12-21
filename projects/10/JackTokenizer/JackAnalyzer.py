import sys

import os

import JackTokenizer
import CompilationEngineXML
import CompilationEngineVM


XML_EXTENSION = "OUR.xml"

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

    def __init__(self,input_file):
        self.input_file = open(input_file,"r")
        self.output_file = open(input_file.split(".jack")[0] + XML_EXTENSION, 'w')
        self.tokenizer = None

    def compile_xml(self):
        self.tokenizer = JackTokenizer.JackTokenizer(self.input_file)
        CompilationEngineXML.CompilationEngineXML(self.tokenizer, self.output_file)

        self.input_file.close()
        self.output_file.close()

def parse_dir(dir_path):
    for f in os.listdir(dir_path):
        if f.endswith(".jack"):
            parse_file(dir_path + "/" + f)

def parse_file(abs_path):
    analyzer = JackAnalyzer(abs_path)
    analyzer.compile_xml()


def main():
    if len(sys.argv) != 2:
        print("USAGE: JackTokenizer ~directory/file")
        return exit(1)

    abs_path = str(os.path.abspath(sys.argv[1]))

    if os.path.isfile(abs_path):
       parse_file(abs_path)

    if os.path.isdir(abs_path):
        parse_dir(abs_path)


if __name__ == '__main__':
    main()
