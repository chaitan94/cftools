CF-Tools
====

A small script to automatically download, manage and run test cases for a codeforces problem

## Usage

Put the file cftools.py in a directory included in your path, say /usr/bin and then
run

```
$ cftools.py 454 c
```

to download and run all test cases given on the website
Example output:
```
Tests not present
Want to download [Y/N]? y
3 test files written.
Test case #1: PASS
Test case #2: PASS
Test case #3: FAIL
```
or if you just wanted to download the test files you can run
`cftools.py --get 454 c` or just `cftools.py -g 454 c`

## Dependencies
 To download all dependencies, chage to repo directory and run 
 
 `pip install -r requirements.txt`

CF-Tools depends on [requests](https://github.com/kennethreitz/requests), [click](https://github.com/mitsuhiko/click) and [BeautifulSoup](https://launchpad.net/beautifulsoup)
