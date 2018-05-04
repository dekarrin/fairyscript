#!/bin/bash

#
./scpcompile.py -i test/full_test.scp -o test.rpy
./scpcompile.py -i test/full_test.scp -o test.docx --word

# test installed version as well
scpcompile -i test/full_test.scp -o test.rpy
scpcompile -i test/full_test.scp -o test.docx --word
