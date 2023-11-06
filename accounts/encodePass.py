import jwt

def encode(rawpass):
    return jwt.encode(payload={'encpass':rawpass},key='huihui',algorithm="HS256")

def decode(jwtToken):
    return jwt.decode(jwt=jwtToken,key='huihui',algorithms="HS256")


password = "huihui"

print(encode(password))

print(decode(encode(password)).get('encpass'))