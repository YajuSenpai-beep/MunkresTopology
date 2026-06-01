import glob
bs = chr(92)
for fn in sorted(glob.glob("../chapters/Chapter_*.tex")):
    with open(fn, encoding="utf-8") as f: c = f.read()
    while True:
        i = c.find(bs+"idx[");
        if i<0: break
        bd=c.find("]",i+4); b2=c.find("{",bd+1); b3=c.find("}",b2+1)
        if bd>0 and b3>0: c=c[:i]+bs+"index{"+c[b2+1:b3]+"}"+c[b3+1:]
    c=c.replace(bs+"idx{",bs+"index{")
    c=c.replace(bs+"idxmath{",bs+"index{")
    c=c.replace(bs+"idxsub{",bs+"index{")
    i=0
    while True:
        i=c.find(bs+"index{",i)
        if i<0: break
        b1=c.find("}",i+7)
        if b1<0: break
        if b1+1<len(c) and c[b1+1]=="{":
            b2=c.find("}",b1+2)
            if b2>0: c=c[:i]+bs+"index{"+c[i+7:b1]+"@"+c[b1+2:b2]+"}"+c[b2+1:]; i+=1
        i+=1
    with open(fn,"w",encoding="utf-8") as f: f.write(c)
print("Done.")
