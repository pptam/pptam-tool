# Results parser

This parser takes results stored by Faban and prepares it for the analysis. It is currently implmented in [Elixir](https://elixir-lang.org/).

It is implemented as a command line application, which can be compliled using ``mix escript.build`` in the main directory and executed as follows:

- on Windows: ``escript.exe parser --input=(folder name in which all the experiments are) --output=(csv file to which to write the result of the parsing)``
- on Linux/Mac: ``./parser --input=(folder name in which all the experiments are) --output=(csv file to which to write the result of the parsing)``

Example:

``./parser --input=../test_executor/executed --output=../analyzer/BenchflowOutput.csv``

