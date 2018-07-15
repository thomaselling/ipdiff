import argparse
import csv
import netaddr
import collections

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--old')
	parser.add_argument('-n', '--new')
	parser.add_argument('-c', '--csv')
	args = parser.parse_args()

	if args.old is None or args.new is None or args.csv is None:
		parser.print_help()
		exit()

	# create sets of old scope and new scope
	old = loadfile(args.old)
	new = loadfile(args.new)

	# get diff between the two sets and write to file
	# diff is list of hosts that are present in "new" but NOT in "old"
	#diff = list(old.symmetric_difference(new))
	diff = list(new - old)
	print("new ips found\n=============\n%s\n" % len(diff))
	writefile(diff, 'diff.txt')

	# create scope map dict from given scope
	# csv needs to be formatted as ip address in column1 and parnter in column2
	scopemap = readcsv(args.csv)
	dictadd = {}

	# iterate through scopemap and breakout cidr addresses
	# make temp dict to hold breakout addresses
	for key, value in scopemap.items():
		try:
			ip = netaddr.IPNetwork(key)
			iplist = list(ip)
			for ip in iplist:
				dictadd.update({str(ip) : value})
		except Exception as e:
			#print(e)
			continue

	# add temp dict to master scopemap
	scopemap.update(dictadd)

	# format csv output
	csvfile = open('output.csv', 'w')
	csvfile.write("IP Address,Partner\n")
	partners = []

	# do dict lookup to get partner by diff'd ip
	# write values to csv
	for ip in diff:
		csvfile.write("%s,%s\n" % (ip, scopemap.get(ip)))
		partners.append(scopemap.get(ip))

	# print verbose to user
	c = collections.Counter(partners)
	print("Breakdown by partner\n====================")
	for key, value in c.items():
		print(key, value)

# load file content into a set
def loadfile(filename):
	with open(filename, 'r') as csv:
		return set(line.strip() for line in csv)

# write list to a file
def writefile(writelist, filename):
	with open(filename, 'w') as diff:
		for item in writelist:
			diff.write("%s\n" % item)

# read csv contents into dict
# csv needs to be formatted as ip address in column1 and parnter in column2
def readcsv(filename):
	with open(filename,newline='') as scopefile:
		reader = csv.reader(scopefile)
		next(reader)
		results = dict(reader)
		return results

if __name__ == "__main__":
    main()