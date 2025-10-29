def generate_captcha():
    import random
    captcha=''
    a=str(random.randint(0,9))
    b=chr(random.randint(65,80))
    c=str(random.randint(0,9))
    d=chr(random.randint(97,122))
    captcha= a+b+c+d   #'  '+a+' '+b+' '+c+' '+d+'  '
    return captcha