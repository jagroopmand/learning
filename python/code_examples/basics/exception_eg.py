import traceback

try:
  print "Raising fake exception"
  raise IOError, "Fake Exception"
except IOError as e:
  print "Exception: %s" % e
  traceback.print_exc()
