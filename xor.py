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
    # return b64.b64encode( "".join( secret ).encode() ).decode()
    return "".join( secret )


def xor_decrypt(secret,key):
    # tips = b64.b64decode( secret.encode() ).decode()
    tips = secret
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

# test1 = "testasdfsfasdfsadf"
# test2 = "keyafdsafdsafs"
# test = xor_encrypt(test1,test2)
# print test
# test = xor_decrypt(test, test2)
# print test
