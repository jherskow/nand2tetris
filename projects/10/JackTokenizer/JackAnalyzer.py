import sys
import os
import JackTokenizer
import CompilationEngineXML


XML_EXTENSION =".xml"

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

    def __init__(self, input_file):
        self.input_file = open(input_file,"r")
        self.output_file = open(input_file.split(".")[0] + XML_EXTENSION, "w")
        self.tokenizer = None

    def get_tokenizer(self):
        self.tokenizer = JackTokenizer.JackTokenizer(self.input_file)

    def jack_to_xml(self):
        self.get_tokenizer()
        CompilationEngineXML.CompilationEngineXML(self.tokenizer, self.output_file)

def main():
    input_file = sys.argv[1]
    if os.path.isfile(input_file):
        JackAnalyzer(input_file)


    if os.path.isdir(input_file):
        for f in os.listdir(input_file):
            if f.endswith(".jack"):
                JackAnalyzer(f)



if __name__ == '__main__':
   main()