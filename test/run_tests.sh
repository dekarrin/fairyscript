#!/bin/bash

# test both the installed and non-installed versions

if [ "$1" = "--local" ]
then
	ALL_COMMANDS="./fairyc.py"
else
	ALL_COMMANDS="./fairyc.py fairyc"
fi

ALL_TESTS="test_analyze test_analyze_order_usage test_analyze_order_name test_renpy test_lex test_ast test_docx"



if command -v md5
then
	export has_md5=1
elif command -v md5sum
then
	export has_md5=
else
	echo "md5 and md5sum are both unavailable. Cannot run comparison. Abort." >&2
	exit 1
fi

checksum() {
	if [ -n "$has_md5" ]
	then
		echo "$(md5 "$1" | cut -d ' ' -f 4)"
	else
		echo "$(md5sum "$1" | cut -d ' ' -f 1)"
	fi
}

log_and_show() {
	echo '['$(date)']'" $1" >> test.log
	echo "$1"
}

log() {
	echo '['$(date)']'" $1" >> test.log
}

test_renpy() {
	local cmd="$1"
	"$cmd" renpy -o test_output/test.rpy test/sources/full_test.fey
	actual=$(checksum test_output/test.rpy)
	expected=$(checksum test/expected/expected.rpy)
	if [ "$actual" != "$expected" ]
	then
		echo "Ren'py output differs from expected" >&2
		diff -u test/expected/expected.rpy test_output/test.rpy >&2
		return 1
	fi
}

test_analyze() {
	local cmd="$1"
	"$cmd" analyze -o test_output/test.ana test/sources/full_test.fey
	actual=$(checksum test_output/test.ana)
	expected=$(checksum test/expected/expected.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test/expected/expected.ana test_output/test.ana >&2
		return 1
	fi
}

test_analyze_order_usage() {
	local cmd="$1"
	"$cmd" analyze --order usage -o test_output/test_usage_order.ana test/sources/full_test.fey
	actual=$(checksum test_output/test_usage_order.ana)
	expected=$(checksum test/expected/expected_usage_order.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test/expected/expected.ana test_output/test.ana >&2
		return 1
	fi
}

test_analyze_order_name() {
	local cmd="$1"
	"$cmd" analyze --order name -o test_output/test.ana test/sources/full_test.fey
	actual=$(checksum test_output/test.ana)
	expected=$(checksum test/expected/expected.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test/expected/expected.ana test_output/test.ana >&2
		return 1
	fi
}

test_ast() {
	local cmd="$1"
	"$cmd" ast --pretty -o test_output/test.ast test/sources/full_test.fey
	actual=$(checksum test_output/test.ast)
	expected=$(checksum test/expected/expected.ast)
	if [ "$actual" != "$expected" ]
	then
		echo "Parsed AST output differs from expected" >&2
		diff -u test/expected/expected.ast test_output/test.ast >&2
		return 1
	fi
}

test_lex() {
	local cmd="$1"
	"$cmd" lex --pretty -o test_output/test.lex test/sources/full_test.fey
	actual=$(checksum test_output/test.lex)
	expected=$(checksum test/expected/expected.lex)
	if [ "$actual" != "$expected" ]
	then
		echo "Lexer symbol output differs from expected" >&2
		diff -u test/expected/expected.lex test_output/test.lex >&2
		return 1
	fi
}

test_docx() {
	local cmd="$1"

	rm -rf test_output/docx
	mkdir test_output/docx
	mkdir test_output/docx/expected
	mkdir test_output/docx/actual

	"$cmd" docx -o test_output/docx/actual/test.docx test/sources/full_test.fey
	cp test/expected/expected.docx test_output/docx/expected/

	cd test_output/docx/expected
	unzip expected.docx > /dev/null 2>&1
	cd ../actual
	unzip test.docx > /dev/null 2>&1
	cd ../../..

	status=0

	actual_data=$(checksum test_output/docx/actual/word/document.xml)
	expected_data=$(checksum test_output/docx/expected/word/document.xml)
	if [ "$actual" != "$expected" ]
	then
		echo "DOCX document content differs from expected" >&2
		echo "(cannot show docx diffs)" >&2
		status=1
	fi

	actual_styles=$(checksum test_output/docx/actual/word/styles.xml)
	expected_styles=$(checksum test_output/docx/expected/word/styles.xml)
	if [ "$actual" != "$expected" ]
	then
		echo "DOCX document style differs from expected" >&2
		echo "(cannot show docx diffs)" >&2
		status=1
	fi

	return ${status}
}

echo "Starting tests..."

rm -rf test_output
mkdir test_output

count() { echo $#; }

total_tests=$(expr $(count $ALL_TESTS) \* $(count $ALL_COMMANDS))
failures=0

for cmd in $ALL_COMMANDS
do
	for test in $ALL_TESTS
	do
		echo "\"$cmd / $test\"..."
		"$test" "$cmd" || failures="$(expr $failures + 1)"
	done
done

passes=$(expr $total_tests - $failures)

echo "$passes/$total_tests passed"

if [ "$failures" -gt 0 ]
then
	echo "$failures failed" >&2
	exit 1
fi
