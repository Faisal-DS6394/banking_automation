import gmail
#replace with your emial_id and app_pass
email_id="titani453@gmail.com"
app_pass="sdfg adfe eejd ergd"

def send_open_ackn(uemail,uname,uacn,upass): #ackn=acknowledgement
    con=gmail.GMail(email_id,app_pass)
    sub="Congrates😊,Account opened Successfully"
    upass=upass.replace(' ','')
    utext=f"""Hello,{uname}
Welcome to ABC Bank
Your Acn no. is {uacn}
Your Password is {upass}
Kindly change your password when login first

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp(uemail,otp,amt):
    con=gmail.GMail(email_id,app_pass)
    sub="OTP for transaction"
    
    utext=f"""Your OTP is {otp} to transfer amount {amt}

Kindly use this OTP to complete this transaction
Please don't share this OTP to anyone

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp_4_pass(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub="OTP for password recovery"
    
    utext=f"""Your OTP is {otp} to recover password
Please don't share this OTP to anyone

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)