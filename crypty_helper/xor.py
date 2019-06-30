import base64 as b64

def xor_encrypt(tips,key):
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num>=lkey:
            num=num%lkey
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1
    return b64.b64encode( "".join( secret ).encode() ).decode()


def xor_decrypt(secret,key):
    tips = b64.b64decode( secret.encode() ).decode()
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num>=lkey:
            num=num%lkey
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1
    return "".join( secret )

# test1 = "test"
# test2 = "keyafdsafdsafs"
# test = xor_encrypt(test1,test2)
# print test
# test = xor_decrypt(test, test2)
# print test
