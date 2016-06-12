# takeoff ConnectionManager

Simple class to abstract SSH/Netconf sessions


example:


```python
  import ConnectionManager

  conn = ConnectionManager.connection(
      target=myhostname,
      user=user,
      password=password
      )

  if conn.open():
     res = conn.cli("show version")
     if 'errors' in res:
         pass # there were errors... handle?
     else:
         for result in res['results']:
             parse_result(result)
  else:
     pass # fail code here!
```

connection.cli returns dict, with 'error' populated if an error occurred.  Otherwise, 'results' is a list of strings representing the output from the CLI.   

connection.cli can take a str or list of str.  A list of str will return a list of results; if only a single str was passed, a list of length 1 will be returned.

connection.cli_batch will take a "batch" of newline-separated commands that will be executed in a single channel/shell session.   Output is more of a "screen scrape", and all the nuances of pagination, terminal widths, etc, are not handled.   Use sparingly.
