#!/bin/bash

#
./scpcompile.py -o test.rpy renpy test/full_test.scp
./scpcompile.py -o test.docx docx test/full_test.scp

# test installed version as well
scpcompile -o test.rpy renpy test/full_test.scp
scpcompile -o test.docx docx test/full_test.scp
