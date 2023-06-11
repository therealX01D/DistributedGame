UN = ""


def cP():
    import eel
    eel.init('web')
    with open('username', 'r') as openfile:
        for o in openfile:
           global UN
           UN = o
    print(f"username@eel {UN}")
    @eel.expose
    def getUN():
        global UN
        print(f"USERNAMEto_return {UN}")
        return UN

    eel.start('index.html', size=(1000, 500),port=0)
