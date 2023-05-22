import os
li = os.listdir("./assets")
inc=0
for i in range(len(li)):
    if li[i][:3]=="img":
        os.rename(f'./assets/{li[i]}',f'./assets/img{inc}.png')
        inc+=1
    print(type(i))