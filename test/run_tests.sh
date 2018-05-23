#!/bin/bash

# test both the installed and non-installed versions

if [ "$1" = "--local" ]
then
	ALL_COMMANDS="./fairyc.py"
	shift
else
	ALL_COMMANDS="./fairyc.py fairyc"
fi

if [ -n "$1" ]
then
	ALL_TESTS="$1"
else
	ALL_TESTS="test_analyze test_analyze_order_usage test_analyze_order_name test_renpy test_lex test_ast test_docx"
fi


compiler_version=$(grep -E '^\s*__version__\s*=\s*' fairyscript/version.py | cut -d '=' -f 2 | awk '{printf $1}' | sed 's/'\''//g' | sed 's/"//g')
compiler_version_ticks=""
for x in $(seq ${#compiler_version})
do
	compiler_version_ticks="$compiler_version_ticks="
done
echo $compiler_version_ticks


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


create_template() {
	local input="$1"
	local output="$2"
	sed -e 's/__version__/'$compiler_version'/g' "$input" | sed -e 's/__version_ticks__/'$compiler_version_ticks'/g' > "$output"
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
	create_template test/expected/expected.ana test_output/expected.ana
	actual=$(checksum test_output/test.ana)
	expected=$(checksum test_output/expected.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test_output/expected.ana test_output/test.ana >&2
		return 1
	fi
}

test_analyze_order_usage() {
	local cmd="$1"
	"$cmd" analyze --order usage -o test_output/test_usage_order.ana test/sources/full_test.fey
	create_template test/expected/expected_usage_order.ana test_output/expected_usage_order.ana
	actual=$(checksum test_output/test_usage_order.ana)
	expected=$(checksum test_output/expected_usage_order.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test_output/expected_usage_order.ana test_output/test_usage_order.ana >&2
		return 1
	fi
}

test_analyze_order_name() {
	local cmd="$1"
	"$cmd" analyze --order name -o test_output/test_name_order.ana test/sources/full_test.fey
	create_template test/expected/expected_name_order.ana test_output/expected_name_order.ana
	actual=$(checksum test_output/test_name_order.ana)
	expected=$(checksum test_output/expected_name_order.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test/output_expected_name_order.ana test_output/test_name_order.ana >&2
		return 1
	fi
}

test_analyze_order_name_no_sources() {
	local cmd="$1"
	"$cmd" analyze --order name --no-source-info -o test_output/test_name_order_no_sources.ana test/sources/full_test.fey
	create_template test/expected/expected_name_order_no_sources.ana test_output/expected_name_order_no_sources.ana
	actual=$(checksum test_output/test_name_order_no_sources.ana)
	expected=$(checksum test_output/expected_name_order_no_sources.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test_output/expected_name_order_no_sources.ana test_output/test_name_order_no_sources.ana >&2
		return 1
	fi
}

test_analyze_order_usage_no_sources() {
	local cmd="$1"
	"$cmd" analyze --order usage --no-source-info -o test_output/test_usage_order_no_sources.ana test/sources/full_test.fey
	create_template test/expected/expected_usage_order_no_sources.ana test_output/expected_usage_order_no_sources.ana
	actual=$(checksum test_output/test_usage_order_no_sources.ana)
	expected=$(checksum test_output/expected_usage_order_no_sources.ana)
	if [ "$actual" != "$expected" ]
	then
		echo "Static analysis output differs from expected" >&2
		diff -u test_output/expected_usage_order_no_sources.ana test_output/test_usage_order_no_sources.ana >&2
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

test_ast_inline_sources() {
	local cmd="$1"
	"$cmd" ast --pretty --inline-sources -o test_output/test_inline.ast test/sources/full_test.fey
	actual=$(checksum test_output/test_inline.ast)
	expected=$(checksum test/expected/expected_inline.ast)
	if [ "$actual" != "$expected" ]
	then
		echo "Parsed AST output differs from expected" >&2
		diff -u test/expected/expected_inline.ast test_output/test_inline.ast >&2
		return 1
	fi
}

test_ast_no_debug_symbols() {
	local cmd="$1"
	"$cmd" ast --pretty --no-debug-symbols -o test_output/test_no_debug_symbols.ast test/sources/full_test.fey
	actual=$(checksum test_output/test_no_debug_symbols.ast)
	expected=$(checksum test/expected/expected_no_debug_symbols.ast)
	if [ "$actual" != "$expected" ]
	then
		echo "Parsed AST output differs from expected" >&2
		diff -u test/expected/expected_no_debug_symbols.ast test_output/test_no_debug_symbols.ast >&2
		return 1
	fi
}

test_ast_strip_debug() {
	local cmd="$1"
	"$cmd" ast --pretty --no-debug-symbols -f ast -o test_output/test_strip_debug.ast test/sources/debug_symbols.ast
	actual=$(checksum test_output/test_strip_debug.ast)
	expected=$(checksum test/expected/expected_strip_debug.ast)
	if [ "$actual" != "$expected" ]
	then
		echo "Parsed AST output differs from expected" >&2
		diff -u test/expected/expected_strip_debug.ast test_output/test_strip_debug.ast >&2
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

test_lex_to_ast() {
	local cmd="$1"
	"$cmd" ast -f lex --pretty -o test_output/test_lex_to_ast.ast test/sources/lexed_input.lex
	actual=$(checksum test_output/test_lex_to_ast.ast)
	expected=$(checksum test/expected/expected_from_lex.ast)
	if [ "$actual" != "$expected" ]
	then
		echo "Lexer symbol output differs from expected" >&2
		diff -u test/expected/expected_from_lex.ast test_output/test_lex_to_ast.ast >&2
		return 1
	fi
}

test_lex_to_renpy() {
	local cmd="$1"
	"$cmd" renpy -f lex -o test_output/test_lex_to_renpy.rpy test/sources/lexed_input.lex
	actual=$(checksum test_output/test_lex_to_renpy.rpy)
	expected=$(checksum test/expected/expected_from_lex.rpy)
	if [ "$actual" != "$expected" ]
	then
		echo "Lexer symbol output differs from expected" >&2
		diff -u test/expected/expected_from_lex.rpy test_output/test_lex_to_renpy.rpy >&2
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
		printf 'Running test "%s - %s"...' "$cmd" "$test"
		failed=
		"$test" "$cmd" > test_output/.temp_output 2>&1 || failed=1
		if [ -n "$failed" ]
		then
			failures="$(expr $failures + 1)"
			printf 'FAIL\n'
		else
			printf 'PASS\n'
		fi
		cat test_output/.temp_output >&2
	done
done

passes=$(expr $total_tests - $failures)

echo "$passes/$total_tests passed"

if [ "$failures" -gt 0 ]
then
	echo "$failures failed" >&2
	exit 1
fi
