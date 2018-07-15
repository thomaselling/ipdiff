# ipdiff
diffs and checks ips with a given scope/classification csv

## Run
Requires the following parameters:

- -o, Text file of old scope, one IP per line.
- -n, Text file of new scope, one IP per line.
- -c, CSV file of IP mapping. IP address in column1 and partner/group in column2.

The script outputs:

- Text file containing all the IP addresses found in the new group, but not in the old group.
- CSV file containing the new IP addresses and the associated group (pulled from csv input flag).

```
PS C:\ipdiff> python .\ipdiff.py -o .\old.txt -n .\new.txt -c .\test.csv
new ips found
=============
10

Breakdown by partner
====================
Test1 6
Test2 3
None 1
```
