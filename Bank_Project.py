from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from pro_captcha_test import generate_captcha
from PIL import Image,ImageTk #Image works both show image & open image,while ImageTk convert image in photo
import time,random
from table_creation import generate
import sqlite3
from email_test import send_open_ackn,send_otp,send_otp_4_pass
from tktable import Table
import re
generate()

def show_dt():
    dt=time.strftime("%A %d-%m-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt)  #show time in ms(after 1 sec)

list_imgs=['Image_pro/logo1.jpg','Image_pro/logo2.png','Image_pro/logo3.jpg','Image_pro/logo4.jpg','Image_pro/logos.jpg']
def image_animation():
    index=random.randint(0,4)
    img=Image.open(list_imgs[index]).resize((230,95))
    imgtk=ImageTk.PhotoImage(img,master=root)
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)
    logo_lbl.image=imgtk
    logo_lbl.after(500,image_animation)

root=Tk()
root.state('zoomed')
root.configure(bg='pink')

title_lbl=Label(root,text="Banking Automation",bg='pink',fg='blue',font=('Arial',40,'underline'))
title_lbl.pack()

dt_lbl=Label(root,font=('Arial',15),bg='pink')
dt_lbl.pack(pady=5) #pady maintain gap 
show_dt()

img=Image.open("Image_pro/logos.jpg").resize((230,105))
imgtk=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=imgtk)
logo_lbl.place(relx=0,rely=0)
image_animation()

footer_lbl=Label(root,text="Developed By:\nFaisal Ansari @ 6394009960",bg='pink',fg='blue',font=('Arial',20))
footer_lbl.pack(side='bottom')

code_captcha=generate_captcha()

def main_screen():
    def refresh_captcha():
        global code_captcha
        code_captcha=generate_captcha()
        cap_value.configure(text=code_captcha)

    frm=Frame(root)
    frm.configure(bg='powder blue',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.76)

    def forgot():
        frm.destroy()
        fp_screen()
   
    def login():
        utype=acntype_cb.get()    
        uacn=acno_e.get()
        upass=pass_e.get()     #upass= user password
        
        ucaptcha=cap_e.get()
        global code_captcha
        code_captcha==code_captcha.replace(' ','')
        
        if utype=='Admin':
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid Captcha')
            else:
                messagebox.showerror("Login","You are not Admin!")              
        else:
            if code_captcha==ucaptcha:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacn,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login","Invalid ACN or PASS")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])
            else:
                messagebox.showerror('Login','Invalid Captcha')

    acntype_lbl=Label(frm,font=('Arial',15),text="ACN. Type",bg='powder blue')
    acntype_lbl.place(relx=.4,rely=.1)
    
    acntype_cb=Combobox(frm,values=['Users','Admin'])
    acntype_cb.current(0)
    acntype_cb.place(relx=.5,rely=.1)

    acno_lbl=Label(frm,font=('Arial',15),text="ACN.",bg='powder blue')
    acno_lbl.place(relx=.4,rely=.2)

    acno_e=Entry(frm,font=('Arial',15),bd=5)
    acno_e.place(relx=.5,rely=.2)
    acno_e.focus()

    pass_lbl=Label(frm,font=('Arial',15),text="Password",bg='powder blue')
    pass_lbl.place(relx=.4,rely=.3)

    pass_e=Entry(frm,font=('Arial',15),bd=5,show='*') #show maintain writing way as given str
    pass_e.place(relx=.5,rely=.3)

    cap_lbl=Label(frm,font=('Arial',15),text="Captcha",bg='powder blue')
    cap_lbl.place(relx=.4,rely=.4)

    cap_value=Label(frm,text=code_captcha,font=('Arial',15),bg='green',fg='white')
    cap_value.place(relx=.5,rely=.4)

    refresh_button=Button(frm,text='refresh',command=refresh_captcha)
    refresh_button.place(relx=.6,rely=.4)

    cap_e=Entry(frm,font=('Arial',15),bd=5)
    cap_e.place(relx=.5,rely=.5)
    
    submit_button=Button(frm,text='Login',width=15,command=login,bd=5,font=('Arial',15),bg='pink',fg='black')
    submit_button.place(relx=.51,rely=.6)

    forgot_button=Button(frm,text='Forgot Pass',width=15,command=forgot,bd=5,font=('Arial',15),bg='pink',fg='black')
    forgot_button.place(relx=.51,rely=.7)


def fp_screen():  #forgot password
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.76)

    def back():
        frm.destroy()
        main_screen()

    def fp_pass():
        uemail=email_e.get()
        uacn=acno_e.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))            
        torow=curobj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Password","ACN does not exist")
        else:
            if uemail==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_4_pass(uemail,otp,)
                messagebox.showinfo("Forgot Password","OTP sent to registered email,kindly verify")
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='select acn_pass from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo("Forgot Password",f"Your Password is {curobj.fetchone()[0]}")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Invalid OTP","Invalid OTP")
    
                otp_e=Entry(frm,font=('Arial',15),bd=5)
                otp_e.place(relx=.47,rely=.65)
                otp_e.focus()

                verify_btn=Button(frm,text='Verify',bd=5,font=('Arial',15),bg='pink',fg='black',command=verify_otp)
                verify_btn.place(relx=.47,rely=.80)
            
            else:
                messagebox.showerror("Forgot Password","Email is not matched") 

    back_button=Button(frm,text='Back',bd=5,font=('Arial',15),bg='pink',fg='black',command=back)
    back_button.place(relx=0,rely=0)

    acno_lbl=Label(frm,font=('Arial',15),text="ACN.",bg='powder blue')
    acno_lbl.place(relx=.4,rely=.2)

    acno_e=Entry(frm,font=('Arial',15),bd=5)
    acno_e.place(relx=.5,rely=.2)
    acno_e.focus()

    email_lbl=Label(frm,font=('Arial',15),text="Emial I'd",bg='powder blue')
    email_lbl.place(relx=.4,rely=.3)

    email_e=Entry(frm,font=('Arial',15),bd=5)
    email_e.place(relx=.5,rely=.3)

    submit_button=Button(frm,text='Submit',bd=5,font=('Arial',15),bg='pink',fg='black',command=fp_pass)
    submit_button.place(relx=.56,rely=.4)

def admin_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='yellow')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.76)
    
    def logout():
        frm.destroy()
        main_screen()
    logout_btn=Button(frm,text='Log Out',bd=5,font=('Arial',15),bg='pink',fg='black',command=logout)
    logout_btn.place(relx=.9,rely=0)

    def open():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.13,rely=.2,relwidth=.8,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',15),text="This open account screen",bg='powder blue')
        t_lbl.pack()

        def openac():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            uadhar=adhr_e.get()
            uadr=adr_e.get()
            udob=dob_e.get()
            upass=generate_captcha()
            upass=upass.replace(' ','')
            ubal=0
            uopendata=time.strftime("%A %d-%b-%Y")

            #empty validation 
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0 or len(upass)==0:
                messagebox.showerror("Open Accounts","Empty fields are not allowed")
                return
              
            #email validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]\.+[a-zA-Z]+",uemail)
            if match==None:
                messagebox.showerror("Open Accounts","Kindly check formate of Email")
                return
            #mob validation
            match=re.fullmatch(r"[6-9][0-9]{9}",umob)
            if match==None:
                messagebox.showerror("Open Accounts","Incorrect Mobile NO.")
                return
            #adhar validation
            match=re.fullmatch(r"[0-9]{12}",uadhar)
            if match==None:
                messagebox.showerror("Open Accounts","Incorrect Adhar")
                return
            #dob validation {Please do it}
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendata))
            conobj.commit()
            conobj.close()
           
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select max(acn_acno) from accounts")
            uacn=curobj.fetchone()[0]
            conobj.close()
            
            send_open_ackn(uemail,uname,uacn,upass)
            messagebox.showinfo("Account","Account opened and details sent email")
            frm.destroy()
            main_screen()

        name_lbl=Label(ifrm,font=('Arial',15),text="Name",bg='white')
        name_lbl.place(relx=.15,rely=.3)

        name_e=Entry(ifrm,font=('Arial',15),bd=5)
        name_e.place(relx=.27,rely=.3)
        name_e.focus()
        
        email_lbl=Label(ifrm,font=('Arial',15),text="Email I'd",bg='white')
        email_lbl.place(relx=.15,rely=.45)

        email_e=Entry(ifrm,font=('Arial',15),bd=5)
        email_e.place(relx=.27,rely=.45)
      
        mob_lbl=Label(ifrm,font=('Arial',15),text="Mob. No.",bg='white')
        mob_lbl.place(relx=.15,rely=.60)

        mob_e=Entry(ifrm,font=('Arial',15),bd=5)
        mob_e.place(relx=.27,rely=.60)
 
        adhr_lbl=Label(ifrm,font=('Arial',15),text="Adhar",bg='white')
        adhr_lbl.place(relx=.53,rely=.3)

        adhr_e=Entry(ifrm,font=('Arial',15),bd=5)
        adhr_e.place(relx=.65,rely=.3)

        adr_lbl=Label(ifrm,font=('Arial',15),text="Adress",bg='white')
        adr_lbl.place(relx=.53,rely=.45)

        adr_e=Entry(ifrm,font=('Arial',15),bd=5)
        adr_e.place(relx=.65,rely=.45)

        dob_lbl=Label(ifrm,font=('Arial',15),text="DOB",bg='white')
        dob_lbl.place(relx=.53,rely=.6)

        dob_e=Entry(ifrm,font=('Arial',15),bd=5)
        dob_e.place(relx=.65,rely=.6)
      
        open_button=Button(ifrm,text='Open ACN.',command=openac,width=10,bd=5,font=('Arial',15),bg='green',fg='black')
        open_button.place(relx=.45,rely=.77)

    def close():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.13,rely=.2,relwidth=.8,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',15),text="This close account screen",bg='powder blue')
        t_lbl.pack()

        def sent_close_otp():
            uacn=acno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))            
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Close Account","ACN does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_4_pass(torow[3],otp)
                messagebox.showinfo("Close Account","OTP sent to registered email,kindly verify")
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='delete from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            messagebox.showinfo("Close Account","Account Closed")
                            conobj.commit()
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Invalid OTP","Invalid OTP")
    
                otp_e=Entry(frm,font=('Arial',15),bd=5)
                otp_e.place(relx=.47,rely=.65)
                otp_e.focus()

                verify_btn=Button(frm,text='Verify',bd=5,font=('Arial',15),bg='pink',fg='black',command=verify_otp)
                verify_btn.place(relx=.47,rely=.80)

        acno_lbl=Label(ifrm,font=('Arial',15),text="ACN.",bg='white')
        acno_lbl.place(relx=.4,rely=.3)

        acno_e=Entry(ifrm,font=('Arial',15),bd=5)
        acno_e.place(relx=.5,rely=.3)
        acno_e.focus()

        open_button=Button(ifrm,text='Send OTP',command=sent_close_otp,width=10,bd=5,font=('Arial',15),bg='green',fg='black')
        open_button.place(relx=.5,rely=.45)

    def view():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.13,rely=.2,relwidth=.8,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',15),text="This view account screen",bg='powder blue')
        t_lbl.pack()
        
        table_headers = ("ACN.", "NAME", "EMAIL", "MOB", "OPEN DATE", "BALANCE")
        mytable = Table(ifrm, table_headers,headings_bold=True)
        mytable.place(relx=.1,rely=.1,relwidth=.8,relheight=.4)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts"
        curobj.execute(query)
        for tup in curobj.fetchall():
            mytable.insert_row(tup)
        conobj.close()

    open_button=Button(frm,text='Open ACN.',width=10,command=open,bd=5,font=('Arial',15),bg='pink',fg='black')
    open_button.place(relx=.01,rely=.1)

    close_button=Button(frm,text='Close ACN.',width=10,command=close,bd=5,font=('Arial',15),bg='red',fg='black')
    close_button.place(relx=.01,rely=.3)

    view_button=Button(frm,text='View ACN.',width=10,command=view,bd=5,font=('Arial',15),bg='blue',fg='black')
    view_button.place(relx=.01,rely=.5)

def user_screen(uacn,uname):
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.76)

    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacn,))
    row=curobj.fetchone()
    conobj.close()

    def logout():
        frm.destroy()
        main_screen()
    
    def check():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.20,rely=.2,relwidth=.7,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',20),text="This check details screen",bg='white',fg='purple')
        t_lbl.pack()

        acn_lbl=Label(ifrm,font=('Arial',15),text=f"Account No\t=\t{row[0]}",bg='white',fg='black')
        acn_lbl.place(relx=.20,rely=.13)

        bal_lbl=Label(ifrm,font=('Arial',15),text=f"Account Bal\t=\t{row[8]}",bg='white',fg='black')
        bal_lbl.place(relx=.20,rely=.23)
        
        open_lbl=Label(ifrm,font=('Arial',15),text=f"Open Date\t=\t{row[9]}",bg='white',fg='black')
        open_lbl.place(relx=.20,rely=.33)
 
        dob_lbl=Label(ifrm,font=('Arial',15),text=f"Date of birth\t=\t{row[7]}",bg='white',fg='black')
        dob_lbl.place(relx=.20,rely=.43)
 
        adhar_lbl=Label(ifrm,font=('Arial',15),text=f"Adhar No \t=\t{row[5]}",bg='white',fg='black')
        adhar_lbl.place(relx=.20,rely=.53)

    def update():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.20,rely=.2,relwidth=.7,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',20),text="This update details screen",bg='white',fg='purple')
        t_lbl.pack()

        def Update_details():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            upass=pass_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_name=?,acn_email=?,acn_mob=?,acn_pass=?'
            curobj.execute(query,(uname,uemail,umob,upass))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")
            frm.destroy()
            user_screen(uacn,None)


        name_lbl=Label(ifrm,font=('Arial',15),text="Name",bg='white')
        name_lbl.place(relx=.15,rely=.3)

        name_e=Entry(ifrm,font=('Arial',15),bd=5)
        name_e.place(relx=.27,rely=.3)
        name_e.focus()
        name_e.insert(0,row[1])

        email_lbl=Label(ifrm,font=('Arial',15),text="Email I'd",bg='white')
        email_lbl.place(relx=.15,rely=.45)

        email_e=Entry(ifrm,font=('Arial',15),bd=5)
        email_e.place(relx=.27,rely=.45)
        email_e.insert(0,row[3])
      
        mob_lbl=Label(ifrm,font=('Arial',15),text="Mob. No.",bg='white')
        mob_lbl.place(relx=.53,rely=.45)

        mob_e=Entry(ifrm,font=('Arial',15),bd=5)
        mob_e.place(relx=.65,rely=.45)
        mob_e.insert(0,row[4])
 
        pass_lbl=Label(ifrm,font=('Arial',15),text="Pass",bg='white')
        pass_lbl.place(relx=.53,rely=.3)

        pass_e=Entry(ifrm,font=('Arial',15),bd=5)
        pass_e.place(relx=.65,rely=.3)
        pass_e.insert(0,row[2])

        update_btn=Button(ifrm,text='Update',bd=5,font=('Arial',15),bg='pink',fg='black',command=Update_details)
        update_btn.place(relx=.45,rely=.80)


    def deposite():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.20,rely=.2,relwidth=.7,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',20),text="This deposite details screen",bg='white',fg='purple')
        t_lbl.pack()

        def deposite_amt():
            uamt=float(amt_e.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_bal=? where acn_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposite",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn,None)


        amt_lbl=Label(ifrm,font=('Arial',15),text="Amount",bg='white')
        amt_lbl.place(relx=.35,rely=.3)

        amt_e=Entry(ifrm,font=('Arial',15),bd=5)
        amt_e.place(relx=.47,rely=.3)
        amt_e.focus()

        deposite_btn=Button(ifrm,text='Deposite',bd=5,font=('Arial',15),bg='pink',fg='black',command=deposite_amt)
        deposite_btn.place(relx=.45,rely=.80)

    def withraw():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.20,rely=.2,relwidth=.7,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',20),text="This withraw details screen",bg='white',fg='purple')
        t_lbl.pack()

        def withraw_amt():
            uamt=float(amt_e.get())
            if row[8]>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withraw",f"{uamt} Amount Withrawn")
                frm.destroy()
                user_screen(uacn,None)
            else:
                messagebox.showerror("Withraw","Insufficiant Balance ")

        amt_lbl=Label(ifrm,font=('Arial',15),text="Amount",bg='white')
        amt_lbl.place(relx=.35,rely=.3)

        amt_e=Entry(ifrm,font=('Arial',15),bd=5)
        amt_e.place(relx=.47,rely=.3)
        amt_e.focus()

        withraw_btn=Button(ifrm,text='Withraw',bd=5,font=('Arial',15),bg='pink',fg='black',command=withraw_amt)
        withraw_btn.place(relx=.45,rely=.80)

    def transfer():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.20,rely=.2,relwidth=.7,relheight=.6)
        
        t_lbl=Label(ifrm,font=('Arial',20),text="This transfer details screen",bg='white',fg='purple')
        t_lbl.pack()

        def transfer_amt():
            toacn=int(to_e.get())
            uamt=float(amt_e.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(toacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Transfer","To ACN does not exist")
            else:
                if row[8]>=uamt:
                    otp=random.randint(1000,9999)
                    send_otp(row[3],otp,uamt)
                    messagebox.showinfo("Transfer","OTP sent to registered email,kindly verify")
                    def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                            query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                            curobj.execute(query1,(uamt,uacn))
                            curobj.execute(query2,(uamt,toacn))
                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo("Transfer",f"{uamt} Amount Transfered")
                            frm.destroy()
                        else:
                            messagebox.showerror("Transfer","Invalid OTP")
                    otp_lbl=Label(ifrm,font=('Arial',15),bd=5,text='OTP')
                    otp_lbl.place(relx=.35,rely=.65)

                    otp_e=Entry(ifrm,font=('Arial',15),bd=5)
                    otp_e.place(relx=.47,rely=.65)
                    otp_e.focus()

                    verify_btn=Button(ifrm,text='Verify',bd=5,font=('Arial',15),bg='pink',fg='black',command=verify_otp)
                    verify_btn.place(relx=.47,rely=.80)
                else:
                    messagebox.showerror("Transfer","Insufficiant Balance")

        to_lbl=Label(ifrm,font=('Arial',15),text="To ACN",bg='white')
        to_lbl.place(relx=.35,rely=.2)

        to_e=Entry(ifrm,font=('Arial',15),bd=5)
        to_e.place(relx=.47,rely=.2)
        to_e.focus()

        amt_lbl=Label(ifrm,font=('Arial',15),text="Amount",bg='white')
        amt_lbl.place(relx=.35,rely=.4)

        amt_e=Entry(ifrm,font=('Arial',15),bd=5)
        amt_e.place(relx=.47,rely=.4)

        transfer_btn=Button(ifrm,text='Transfer',bd=5,font=('Arial',15),bg='pink',fg='black',command=transfer_amt)
        transfer_btn.place(relx=.80,rely=.80)

    logout_btn=Button(frm,text='Log Out',bd=5,font=('Arial',15),bg='pink',fg='black',command=logout)
    logout_btn.place(relx=.92,rely=0)
    
    wel_lbl=Label(frm,font=('Arial',15),text=f"Welcome,Mr.{row[1]}",bg='powder blue',fg='purple')
    wel_lbl.place(relx=0,rely=0)

    check_button=Button(frm,text='Check Details',command=check,width=15,bd=5,font=('Arial',15),bg='white',fg='brown')
    check_button.place(relx=.01,rely=.1)

    update_button=Button(frm,text='Update Details',width=15,command=update,bd=5,font=('Arial',15),bg='white',fg='blue')
    update_button.place(relx=.01,rely=.3)

    deposite_button=Button(frm,text='Deposite',width=15,bd=5,command=deposite,font=('Arial',15),bg='white',fg='green')
    deposite_button.place(relx=.01,rely=.5)

    withraw_button=Button(frm,text='Withraw',width=15,bd=5,command=withraw,font=('Arial',15),bg='white',fg='red')
    withraw_button.place(relx=.01,rely=.7)

    transfer_button=Button(frm,text='Transfer',width=15,command=transfer,bd=5,font=('Arial',15),bg='white',fg='black')
    transfer_button.place(relx=.01,rely=.9)

main_screen()
root.mainloop()