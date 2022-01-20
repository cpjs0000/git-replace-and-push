#!/usr/bin/env python3

import os
import git
import re
import shutil
import datetime

#Path to git repositories. Must be set
git_repos_path = '/path/to/git/repositories'

def replace_content(dict_replace, target):

    #Based on dict, replaces key with the value on the target.
    for check, replacer in list(dict_replace.items()):
        target = re.sub(check, replacer, target)
    return target

repositories_list_file = open("repositories_list.txt", "r")
repositories_list = repositories_list_file.read().splitlines()
print ("List of repositories: ", repositories_list)
repositories_list_file.close()


credentials_file = open("credentials.txt", "r")
credentials = credentials_file.read().splitlines()
print ("Credntials: ", credentials)
credentials_file.close()

original_strings_file = open("original_strings.txt", "r")
original_strings = original_strings_file.read().splitlines()
print ("List of original strings: ", original_strings)
original_strings_file.close()

replaced_strings_file = open("replaced_strings.txt", "r")
replaced_strings = replaced_strings_file.read().splitlines()
print ("Listf strings for replace:", replaced_strings)
replaced_strings_file.close()

#Iterate over the original strings list and the list with lines for replace into dictionary
zip_iterator = zip(original_strings, replaced_strings)
replace_dict = dict(zip_iterator)
print ("Replacement dictionary: ", replace_dict)

#Main cycle, iterate over the list of repositories
for repo_url in repositories_list:
    repo = re.sub(r'^.+/([^/]+)$',r'\1',repo_url)
    repo_path = git_repos_path + repo
    repo_path = repo_path.rstrip("\n")
    g = git.Git(repo_url)
    print (repo_path)
    try:
        os.stat(repo_path)
        os.chdir(repo_path)
        g.pull('origin','main')
    except:
        os.mkdir(repo_path)
        os.chdir(git_repos_path)
        g.clone(repo_url.rstrip())
        os.chdir(repo_path)
    #Getting a list of files
    files = os.listdir(repo_path)
    files.sort()
    #Iterate over the list of files, processing each of them
    for file in files:
        if not file.startswith('.') and  not os.path.isdir(file):
            print ("Processing file: ", file)
            tmp_file = 'tmp.txt'
            file_open = open(file, 'r')
            tmp_file_open = open (tmp_file, 'w')
            file_read = file_open.read()
            file_open.close()
            new_content = replace_content (replace_dict, file_read)
            tmp_file_open.write (new_content)
            tmp_file_open.close()
            shutil.move(tmp_file,file)
    now = datetime.datetime.now()
    now = str(now.strftime("%Y-%m-%d %H:%M"))
    os.system("git add .")
    os.system("git commit -m 'commit at %s'"%now)
    os.system("git push -u origin main")
