#!/usr/bin/python

import os
import re
import click
import requests
import subprocess
from bs4 import BeautifulSoup

def get_problem_tests(contest, problem):
	url = "http://codeforces.com/contest/%s/problem/%s" % (contest, problem)
	response = requests.get(url)
	status = response.status_code
	if status == 200:
		page = BeautifulSoup(response.text, "lxml")
		inputs = page.select("div.input pre")
		outputs = page.select("div.output pre")
		for i in xrange(1, len(inputs)+1):
			s = '\n'.join([line for line in inputs[i-1].strings])
			infname = "%s%s%d.in" % (contest, problem, i)
			inf = open(infname, "w")
			inf.write(s + "\n")
			inf.close()
			s = '\n'.join([line for line in outputs[i-1].strings])
			outfname = "%s%s%d.out" % (contest, problem, i)
			outf = open(outfname, "w")
			outf.write(s + "\n")
			outf.close()
		print("%d test files written." % len(inputs))
	elif status == 404:
		print("Requested problem not found (404)")

def run_tests(contest, problem, language):
	pcode = contest+problem
	if language == 'cpp':
                srcfile = pcode + '.cpp'
        elif language == 'python':
                srcfile = pcode + '.py'
	files = os.listdir('.')
	inputs = filter(lambda x: re.match(pcode + "\d*\.in", x), files)
	outputs = filter(lambda x: re.match(pcode + "\d*\.out", x), files)
	if len(inputs) == 0:
		print('Tests not present')
		opt = raw_input('Want to download [Y/N]? ')
		opt = opt.upper()
		if opt == 'Y':
			get_problem_tests(contest, problem)
			files = os.listdir('.')
			inputs = filter(lambda x: re.match(pcode + "\d*\.in", x), files)
			outputs = filter(lambda x: re.match(pcode + "\d*\.out", x), files)
		else: return
	if not os.path.isfile(srcfile):
		print('%s doesn\'t exist' % srcfile)
		exit(1)
	if language == 'cpp':
		os.system("g++ %s -o %s" % (srcfile, pcode))
	tests = zip(inputs, outputs)
	for i in xrange(len(tests)):
		inf, outf = tests[i]
		if language == 'cpp':
			res = subprocess.check_output('./%s < %s' % (pcode, inf), shell=True)
		elif language == 'python':
                        res = subprocess.check_output('python %s < %s' % (srcfile, inf), shell=True)
		res = res.strip()
		f = open(outf, "r")
		expected = f.read().strip()
		f.close()
		verdict = "PASS" if res == expected else "FAIL"
		print("Test case #%d: %s" % (i+1, verdict))
	if language == 'cpp':	
		os.remove(pcode)

@click.command()
@click.option('--get', '-g', flag_value=True, help='Download test cases')
@click.argument('contest')
@click.argument('problem')
@click.argument('language', required=False, default='cpp')
def main(get, contest, problem, language):
	""" Codeforces tools by BKC """
	if not contest.isdigit():
		print("Not a valid contest number")
		exit(1)
	if len(problem) != 1:
		print("Not a valid problem code")
		exit(1)
	problem = problem.upper()

	if get: get_problem_tests(contest, problem)
	else: run_tests(contest, problem, language)

if __name__ == '__main__':
	main()
