17_sites_monitoring
===================

This script takes as input the list of urls and checks for each url that
the server responds with 200 and the domain is paid for the month ahead.

Usage
-----

```
~$ python3 check_sites_health.py 'urls.txt'
server works: Yes, domain is paid for a month ahead: No data  https://www.google.ru/
server works: Yes, domain is paid for a month ahead: Yes  https://vk.com/
server works: Yes, domain is paid for a month ahead: Yes  https://habrahabr.ru/feed/
```

Requirements
------------

- Python >= 3.4
