#!/usr/bin/env python3

import sys
from string import digits, ascii_uppercase, ascii_lowercase

MAX_LEN = 20280

class MaxLenException(Exception):
	pass

class NotFoundException(Exception):
	pass

def gen_pattern(length):
	pattern = ''

	if length > MAX_LEN:
		raise MaxLenException("! Error: Pattern length exceeds MAX_LEN ({0})".format(MAX_LEN))

	for upper in ascii_uppercase:
		for lower in ascii_lowercase:
			for digit in digits:
				if len(pattern) < length:
					pattern += upper+lower+digit
				else:
					return pattern[:length]

def search_pattern(needle):
	
	try:
		if needle.startswith('0x'):
			# convert to ascii and reverse (little-endian)
			needle = needle[2:]
			needle = bytearray.fromhex(needle).decode('ascii')
			needle = needle[::-1]
	except (ValueError, TypeError) as e:
		raise

	haystack = ''
	for upper in ascii_uppercase:
		for lower in ascii_lowercase:
			for digit in digits:
				haystack += upper+lower+digit
				index = haystack.find(needle)
				if index > -1:
					return index

	raise NotFoundException("Not found anywhere in pattern")

if __name__ == "__main__":
	if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == "--help":
		print("Usage: {0} <LEN>|<PATTERN>".format(sys.argv[0]))
		print("Generate a pattern of length LEN or search for a specific PATTERN")
		sys.exit(0)

	if sys.argv[1].isdigit():
		try:
			p = gen_pattern(int(sys.argv[1]))
			print(p)
		except MaxLenException as e:
			print(e)
	else:
		try:
			index = search_pattern(sys.argv[1])
			print("First occurence at index {0} in pattern".format(index))
		except NotFoundException as e:
			print(e)
			sys.exit(1)
		except (ValueError, TypeError):
			print("! Error: Check your input")
