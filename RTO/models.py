from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Create your models here.
class login(models.Model):
    log_id = models.AutoField(primary_key=True)
    username = models.CharField("username", max_length=100)
    password = models.CharField("password", max_length=100)
    role = models.CharField("role", max_length=100)
#log_id,username,password,role
class Staff(models.Model):
   Staff_id= models.AutoField(primary_key=True)
   Staff_name= models.CharField("Name",max_length=100)
   Staff_address = models.CharField("Staff_address", max_length=500)
   Staff_email = models.EmailField("Staff_email", max_length=200)
   Staff_phone=models.CharField("Staff_phone",max_length=100)
   Staff_qualification = models.CharField("Staff_qualification", max_length=200)
   Staff_designation = models.CharField("Staff_designation", max_length=100)
   Staff_photo = models.FileField("Staff_photo", max_length=1000,upload_to='images/')
   Staff_status=models.CharField("Staff_status",max_length=50,default="")
   Staff_logid=models.ForeignKey(login, on_delete=models.CASCADE, null=True)
#Staff_id,Staff_name,Staff_address,Staff_email,Staff_phone,Staff_qualification,Staff_designation,Staff_photo,Staff_status,Staff_logid
class User(models.Model):
    User_id = models.AutoField(primary_key=True)
    Owner_name = models.CharField("Staff_qualification", max_length=200)
    Owner_address = models.CharField("Staff_qualification", max_length=200)
    Owner_email = models.CharField("Staff_qualification", max_length=100)
    Owner_phone = models.CharField("Staff_qualification", max_length=100)
    Vechile_no = models.CharField("Staff_qualification", max_length=100)
    Vechile_type = models.CharField("Staff_qualification", max_length=200)
    Vechile_details = models.CharField("Staff_qualification", max_length=1000)
    Log_id = models.ForeignKey(login, on_delete=models.CASCADE, null=True)

    # Specify the required fields

    #User_id,Owner_name,Owner_address,Owner_email,Owner_phone,Vechile_no,Vechile_type,Vechile_details,Log_id
class Report(models.Model):
    Report_id= models.AutoField(primary_key=True)
    User_id =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Report_date = models.CharField("Report_date", max_length=500)
    Report_time = models.CharField("Report_time", max_length=500)
    Report_status = models.CharField("Report_status", max_length=500)
#report_id,User_id ,report_date,report_time,report_status
class Fine(models.Model):
    fine_id	= models.AutoField(primary_key=True)
    Report_id	=models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    Fine_amount	=models.CharField("fine_amount", max_length=100)
    Fine_date	= models.CharField("fine_date", max_length=500)
    Fine_details =models.CharField("fine_details", max_length=1000)
    Staff_id	=models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    User_id =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Fine_status = models.CharField("Fine_status", max_length=500)
#fine_id,Report_id,	Fine_amount,Fine_date,Fine_details, Staff_id,Fine_status,User_id
class Payment(models.Model):
    Pay_id= models.AutoField(primary_key=True)
    Fine_id=models.ForeignKey(Fine, on_delete=models.CASCADE, null=True)
    Pay_amount	=models.CharField("pay_amount", max_length=100)
    Pay_on	=models.CharField("pay_on", max_length=100)
    Pay_status	=models.CharField("pay_status", max_length=100)
    User_id =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#  Pay_id,Fine_id,Pay_amount,Pay_on,Pay_status,
class Complaint(models.Model):
    Complaint_id= models.AutoField(primary_key=True)
    Complaint_subject= models.CharField("subject", max_length=100)
    Complaint_message= models.CharField("mesage", max_length=500)
    Complaint_date= models.CharField("date", max_length=100)
    Complaint_reply= models.CharField("replay", max_length=500)
    User_id =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#Complaint_id,Complaint_subject,Complaint_message,Complaint_date,Complaint_reply,User_id

class Detect(models.Model):
    detect_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screenshot = models.FileField("screenshot",max_length=100,upload_to='images/')
    timestamp = models.DateTimeField(null=True)
    fine_amount=models.CharField("fine_amount",max_length=20)
    Fine_status = models.CharField("Fine_status", max_length=500)
    payment_timestamp = models.DateTimeField(null=True)    # Log_id = models.ForeignKey(login, on_delete=models.CASCADE, null=True)
class bank(models.Model):
    bank_id=models.AutoField(primary_key=True)
    holder=models.CharField("holder",max_length=100)
    card=models.CharField("card",max_length=100)
    cvv=models.CharField("cvv",max_length=100)
    exp=models.CharField("exp",max_length=100) 
    bank_bal=models.CharField("bank",max_length=100) 
