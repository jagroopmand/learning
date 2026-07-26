import subprocess

exit_code = subprocess.call(["ls", "-l"])
print "exit_code: ", exit_code

output = subprocess.check_output(["ls", "-l"])
print "output: ", output
jag@osboxes:~/python/interview$ 
