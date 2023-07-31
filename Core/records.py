def savefunc(img, profile, user):
    with open('photo.txt', 'a') as file:
        file.write(img +' '+ profile + ' ' + user + '\n')
    file.close()

def image(user):
    from PIL import Image
    with open('photo.txt', 'r') as file:
        images = file.read()
        images = images.split()
        found = False
        for i in range(len(images)):
            username = images[i]
            if username == user:
                image = images[i-2]
                ppic = images[i-1]
                im = Image.open(image)
                img = im.resize((250,250))
                img.save('im_250.png')
                img = 'im_250.png'
                profile = im.resize((101,91))
                profile.save('im_101.png')
                profile = 'im_101.png'
                found = True
                continue
            else:
                pass
        if found == True:
            pass
        else:
            img = 'placeholder.png'
            profile = 'profile.png'
    return img, profile
