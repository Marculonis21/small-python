#!/usr/bin/env python3

f = open("wp_rm_submission_fields.csv", "r")

l = f.readlines()

people = []

lastUse = 0
it = -1
for i in l:
    x = i.split(',')
    try:
        userID = int(x[1][1:-1])
        fieldID = int(x[2][1:-1])
        value = x[4].split('"')[1]

        if(userID < 100):
            while True:
                if(lastUse == userID):
                    if(fieldID == 14):
                        d['name'] = value

                    if(fieldID == 13):
                        d['mail'] = value

                    if(fieldID == 26):
                        d['triko'] = value

                    if(fieldID == 27):
                        d['velikost'] = value

                    break
                else:
                    try:
                        people.append(d)
                    except:
                        pass

                    d = {'id': "", 'name': "", 'mail': "", 'triko': "", 'velikost': ""}
                    d['id'] = userID
                    lastUse = userID
    except:
        pass


people = sorted(people, key= lambda x: x['name'].split(' ')[-1])

rmlist = []
for p in range(len(people)):
    #print("{}: {}".format(p,people[p]))
    try:
        if(people[p]['name'] == people[p+1]['name'] or people[p]['name'] == ''):
            rmlist.append(p)
    except:
        pass

for i in reversed(rmlist):
    del(people[i]) 
    
#print()

#for p in people:
#    print(p)
#print(len(people))
