f=open("urls.txt", "r")
fw = open("recipe_urls.txt", "w")
fl = f.readlines()

# for x in fl:
#     print(x)
#     break

for s in fl:
    st = s[3:-3:1]
    if st != '':
        fw.write(st + "\n")