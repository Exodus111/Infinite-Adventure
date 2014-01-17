
mydict = {"add":"stuff"}

x= 1

for i in xrange(10):
    z = "added{0}".format(x)
    mydict[z] = "Stuffier"
    x += 1

for k in mydict.keys():
    if "add" in k:
        print mydict[k]



