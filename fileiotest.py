try:
    with open("FKE.xml",'r') as r:
        if r:
            print "EXISTS"
        else:
            print "APPARENTLY DOES NOT EXIST"
except IOError ["Errno 2"]:
    print "DOES NOT EXIST ERROR IOERROR"
except:
    print "OTHER ERROR"
with open("matches47199737.txt",'r') as r:
    if r:
        print "EXISTS"
    else:
        print "APPARENTLY DOES NOT EXIST"
