from django.shortcuts import render
from django.shortcuts import redirect ,HttpResponse
from django.contrib.auth import get_user
import datetime
from datetime import date
import time
from django.core.files.storage import FileSystemStorage
from .models import login as log,Staff as stf,User as usr,Report as rep,Fine as fin, Payment as pay,Complaint as comp,Detect as dt,bank as bnk
import cv2
import pyaudio
from django.contrib import messages
import dlib
import pydub
from pydub.playback import play
import imutils
from scipy.spatial import distance as dist
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    if(request.session.get('role', ' ')=="admin"):
            response = redirect('/AdminHome')
            return response
    elif (request.session.get('role', ' ')== "staff"):
            response = redirect('/StaffHome')
            return response
    elif (request.session.get('role', ' ')== "user"):
            response = redirect('/UserHome')
            return response
    else:
            return render(request,"index.html",{"msg":""})

def AdminHome(request):
    return render(request,"adminhome.html",{"msg":""})
def pays(request):
        msg = "Paid Successfully"

        amt=request.GET["fine_amount"]
        ids=request.GET["detect_id"]
        if request.POST:
                t1=request.POST["t1"]
                t2=request.POST["t2"]
                t3=request.POST["t3"]
                today = date.today()
                datax=usr.objects.get(Log_id=request.session["id"])
                datay=fin.objects.get(fine_id=ids)
                fin.objects.filter(fine_id=ids).update(Fine_status="paid")
                pay.objects.create(Fine_id=datay,Pay_amount=t3,Pay_on=today,Pay_status="pending",User_id=datax)
        return render(request,"pay.html",{"msg":msg,"amt":amt,"id":ids})

def alert(request):
        msg="report generated"
        t1=request.GET["id"]
        datau=usr.objects.get(User_id=t1)
        today = date.today()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        rep.objects.create(User_id=datau ,Report_date=today,Report_time=current_time,Report_status="pending")
        return HttpResponse(msg) 
def UserHome(request):
    return render(request,"userhome.html",{"msg":""})

def StaffHome(request):
    return render(request,"staffhome.html",{"msg":""})

# @never_cache
# def Logout(request):
#     try:
#         del request.session['id']
#         del request.session['role']
#         del request.session['username']
#         # Logout(request)
#         response = redirect("/index")
#         return response
#     except:
#         response = redirect("/index")
#         return response

def Logout(request):
    logout(request)
    return redirect("/index")
    
def Our_Staff(request):
        msg = ""
        data1=stf.objects.all()
        return render(request,"View_staff.html",{"msg":msg,"data":data1})
def Our_Users(request):
        msg = ""
        data1=usr.objects.all()
        return render(request,"View_user.html",{"msg":msg,"data":data1})

def delete_staff(request):
    stf.objects.filter(Staff_id=request.GET["id"]).delete()
    response = redirect('/Our_Staff')
    return response

def delete_user(request):
    usr.objects.filter(User_id=request.GET["id"]).delete()
    response = redirect('/Our_Users')
    return response
def Current_Users(request):
        msg = ""
        data1=usr.objects.all()
        return render(request,"View_user1.html",{"msg":msg,"data":data1})
def delete_user1(request):
    usr.objects.filter(User_id=request.GET["id"]).delete()
    response = redirect('/Current_Users')
    return response
    
def Appoint_Staff(request):
    msg=""
    if request.POST:
        t1 = request.POST["t1"]
        t2 = request.POST["t2"]
        t3 = request.POST["t3"]
        t4 = request.POST["t4"]
        t5 = request.POST["t5"]
        t6=",".join(request.POST.getlist('t6'))
        
    
        t8 = request.FILES["t8"]
        fs = FileSystemStorage()
        fs.save(t8.name, t8)
        t9 = request.POST["t9"]
        t10 = request.POST["t10"]
        log.objects.create(username=t9, password=t10, role="staff")
        data=log.objects.last()
        stf.objects.create(Staff_name=t1,Staff_address=t2,Staff_email=t3,Staff_phone=t4,Staff_qualification=t6, Staff_designation=t5,Staff_photo=t8,Staff_status="approved",Staff_logid=data)
        messages.success(request,'Submitted')
        #return HttpResponse(t6)
    else:    
        messages.warning(request,'Failed submission')
    
    return render(request,"Add_staff.html",{"msg":msg}) 
def Login(request):
    if request.POST:
        user = request.POST["t1"]
        password = request.POST["t2"]
        try:
            data = log.objects.get(username=user, password=password)
            request.session['username'] = data.username
            request.session['role'] = data.role
            request.session['id'] = data.log_id
            
            if data.role == "admin":
                response = redirect('/AdminHome')
            elif data.role == "user":
                response = redirect('/UserHome')
            elif data.role == "staff":
                response = redirect('/StaffHome')
            else:
                return render(request, "index.html", {"msg": "invalid account Details"})
            
            return response
        except log.DoesNotExist:
            return render(request, "index.html", {"msg": "Invalid username or password"})
        except Exception as e:
            return render(request, "index.html", {"msg": f"An error occurred: {e}"})
    else:
        response = redirect('/index')
        return response


def Register_vehicle(request):
        msg=""
        if request.POST:
                t1 = request.POST["t1"]
                t2 = request.POST["t2"]
                t3 = request.POST["t3"]
                t4 = request.POST["t4"]
                t5 = request.POST["t5"]
                t6 = request.POST["t6"]
                t7 = request.POST["t7"]
        
    
                log.objects.create(username=t5, password=t4, role="user")
                data = log.objects.last()
                usr.objects.create(Owner_name=t1,Owner_address=t2,Owner_email=t3,Owner_phone=t4,Vechile_no=t5,Vechile_type=t6,Vechile_details=t7,Log_id=data)
                messages.success(request,'Submitted')
        else:    
                messages.warning(request,'Failed submission')
    
        return render(request,"Add_vehicle.html",{"msg":msg}) 

def Privacy(request):
    msg=""
    if request.POST:
        t1=request.POST["t1"]
        t2=request.POST["t2"]
        id=request.session["id"]
        data=log.objects.get(log_id=id)
        if data.password==t1:
            msg="sucessfully updated"
            log.objects.filter(log_id=id).update(password=t2)
        else:
            msg="invalid current password"
    returnpage="adminhead.html"
    if request.session["role"] == "user":
        returnpage="userhead.html"
    elif request.session["role"] =="staff":
        returnpage="staffhead.html"
    return render(request, "privacy.html",{"role":returnpage,"msg":msg})

def Manage_complaints(request):
        msg=""
        #datay=log.objects.get(log_id=request.session["id"])
        datax=usr.objects.get(Log_id=request.session["id"])
        if request.POST:
                t1 = request.POST["t1"]
                t2 = request.POST["t2"]
                today = date.today()
                
                msg="posted sucessfully"
                comp.objects.create(Complaint_subject=t1,Complaint_message=t2,Complaint_date=today,Complaint_reply="not yet Seen",User_id=datax)
        data1=comp.objects.filter(User_id=datax)
        #.filter(User_id=datax)
        return render(request, "Add_complaints.html",{"msg":msg,"data":data1})

def complaints(request):
        msg=""
        #datax=usr.objects.get(Log_id=request.session["id"])
        if request.POST:
                t1 = request.POST["t1"]
                t2 = request.POST["t2"]
                
                msg="updated sucessfully"
                comp.objects.filter(Complaint_id=t1).update(Complaint_reply=t2)
        data1=comp.objects.all()
        return render(request, "Answer_Queries.html",{"msg":msg,"data":data1})

def my_reports(request):
        msg=""
        datax=usr.objects.get(Log_id=request.session["id"])
        
        data1=fin.objects.filter(User_id=datax).all()
        return render(request, "View_reports.html",{"msg":msg,"data":data1})

def my_Payemnts(request):
        msg=""
        datax=usr.objects.get(Log_id=request.session["id"])
        #data1=rep.objects.get(User_id=datax)
        data1=dt.objects.filter(user_id=datax,Fine_status="completed").all()
        return render(request, "View_payments.html",{"msg":msg,"data":data1})

def fine_pay(request):
        msg=""
      
        data1=dt.objects.filter(Fine_status="completed")
        return render(request, "all_payments.html",{"msg":msg,"data":data1})

def reports(request):
        msg=""
        if request.POST:
                t1 = request.POST["t1"]
                t2 = request.POST["t2"]
                t3 = request.POST["t3"]
                t4 = request.POST["t4"]
                today = date.today()
                datax=usr.objects.get(User_id=t2)
                dataz=rep.objects.get(Report_id=t1)
                datay=stf.objects.get(Staff_logid=request.session["id"])
                msg="updated sucessfully"
                rep.objects.filter(Report_id=t1).update(Report_status="verifyed")
                fin.objects.create(Report_id=dataz,Fine_amount=t3,Fine_date=today,Fine_details=t4, Staff_id=datay,Fine_status="pending",User_id=datax)
        
        data1=rep.objects.filter(Report_status="pending").all()
        return render(request, "all_report.html",{"msg":msg,"data":data1})
def fine_report(request):
        # msg=""
        # datay=stf.objects.get(Staff_logid=request.session["id"])
        # data1=fin.objects.filter(Staff_id=datay).all()
        # return render(request, "all_fine.html",{"msg":msg,"data":data1})
        msg=""
      
        data1=dt.objects.filter(Fine_status="completed")
        return render(request, "all_fine.html",{"msg":msg,"data":data1})


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Define the sleep detection function


def detect_sleep(request):
    # Load the face detector

    detector = dlib.get_frontal_face_detector()
    audio_file_path = "alarm.mp3"
    audio_file = pydub.AudioSegment.from_file(audio_file_path)
    # Load the facial landmark predictor
    predictor_path = os.path.join(settings.BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(predictor_path)

    # Initialize the eye aspect ratio threshold
    EAR_THRESHOLD = 0.25

    # Initialize the number of consecutive frames with a low EAR to indicate drowsiness
    CONSEC_FRAMES = 50

    # Initialize the frame counter, the total number of blinks, and the total number of frames
    COUNTER = 0
    TOTAL_BLINKS = 0
    TOTAL_FRAMES = 0
#     if request.user.is_authenticated:
#         current_user_id = request.user.User_id
      
    # Start the video stream
    vs = cv2.VideoCapture(0)

    # Loop over the frames from the video stream
    while True:
        # Read the next frame from the video stream
        rect, frame = vs.read()

        # Resize the frame
        frame = imutils.resize(frame, width=450)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = detector(gray, 0)

        # Loop over the face detections
        for rect in rects:
            # Determine the facial landmarks for the face region
            shape = predictor(gray, rect)
            shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            # Extract the left and right eye coordinates
            left_eye = shape[36:42]
            right_eye = shape[42:48]

            # Compute the eye aspect ratio for each eye
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # Average the eye aspect ratio together for both eyes
            ear = (left_ear + right_ear) / 2.0

            # Check if the eye aspect ratio is below the threshold
            if ear < EAR_THRESHOLD:
                COUNTER += 1

                # If the eyes have been closed for a sufficient number of frames, consider the user to be sleepy
                if COUNTER >= CONSEC_FRAMES:
                    TOTAL_BLINKS += 1
                    # Play the audio file
                    play(audio_file)
                   
                    screenshot_folder = "media"
                    if not os.path.exists(screenshot_folder):
                        os.makedirs(screenshot_folder)

                    # Save the screenshot in the "screenshot" folder
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    screenshot_file = os.path.join(screenshot_folder, 'screenshot_{}.png'.format(timestamp))
                    cv2.imwrite(screenshot_file, frame)
                    #userid = request.user.User_id if request.user.is_authenticated else None
                    #detected = dt(screenshot=screenshot_file, user_id=userid, timestamp=datetime.datetime.now())
                    #detected.save()
                    timestamp = datetime.datetime.now()
                    
                    id=request.session['id']
                    datal=log.objects.get(log_id=id)
                    datau=usr.objects.get(Log_id=datal)
                    dt.objects.create(user=datau,screenshot=screenshot_file,timestamp=timestamp,Fine_status="waiting")
                                    #    
            # Otherwise, the eye aspect ratio is above the threshold, so reset the frame counter
            else:
                COUNTER = 0

            # Increment the total number of frames
            TOTAL_FRAMES += 1

        # Draw the total number of blinks and frames on the frame
        cv2.putText(frame, "Blinks: {}".format(TOTAL_BLINKS), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Frames: {}".format(TOTAL_FRAMES), (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        # If the 'q' key was pressed, break from the loop
        if key == ord("q"):
         vs.release()
         cv2.destroyAllWindows()
         return redirect('/UserHome')
        
def scrsht(request):
      id=request.session['id']
      datal=log.objects.get(log_id=id)
      datau=usr.objects.get(Log_id=datal)
      scrsht=dt.objects.filter(user=datau)
      context={
            'scrsht':scrsht
      }
      return render(request,"scrsht.html",context)

def screensht(request):
      scrsht=dt.objects.all()
      context={
            'scrsht':scrsht
      }
      return render(request,"screensht.html",context)

def adminscreensht(request):
      scrsht=dt.objects.all()
      context={
            'scrsht':scrsht
      }
      return render(request,"adminreportall.html",context)


def add_fine(request):
    if request.method == 'POST':
        fine_amount = request.POST["fine_amount"]
        detect_id = request.POST["detect_id"]

        dt.objects.filter(detect_id=detect_id).update(fine_amount=fine_amount)

        return redirect("screensht")


def payment_request(request):
    id=request.session['id']
    datal=log.objects.get(log_id=id)
    datau=usr.objects.get(Log_id=datal)
    msg=""
    if request.POST:
        t1=request.POST["lid"]
        t2=request.POST["holder"]
        t3=request.POST["card"]
        t4=request.POST["cvv"]
        t5=request.POST["exp"]
        t6=int(request.POST["amt"])
        bcc=bnk.objects.filter(holder=t2,card=t3,cvv=t4,exp=t5).count()
        if bcc==1:
            datb=bnk.objects.get(holder=t2,card=t3,cvv=t4,exp=t5)
            bal=int(datb.bank_bal)
            if bal < t6 :
                msg="insufficient Balance"
            else:
                bmt=bal-t6
                bnk.objects.filter(holder=t2,card=t3,cvv=t4,exp=t5).update(bank_bal=bmt)
                dt.objects.filter(detect_id=t1).update(Fine_status="completed",payment_timestamp=datetime.datetime.now())
                msg="payment successfull"
        else :
            msg="invalid account details"


    datag=dt.objects.filter(Fine_status="waiting",user=datau).all()
    datac=dt.objects.filter(Fine_status="waiting",user=datau).count()
#     print(datac)
    return render(request,"scrsht.html",{"data":datag,"datac":datac,"msg":msg})

def admin_payment(request):
      scrsht=dt.objects.filter(Fine_status="waiting")
      context={
            'scrsht':scrsht
      }
      return render(request,"admin_payment.html",context)


      

    # Release the video stream and close any open windows
       
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User  # Import the User model

# @login_required
# def your_view_function(request):
#     # Assuming the currently logged-in user's vehicle number is stored as the username
#     vehicle_number = request.User.Owner_name

#     try:
#         # Retrieve the user's name from the User table based on their vehicle number (username)
#         owner_name = User.objects.get(username=vehicle_number).Owner_name
#         return render(request, 'userhome.html', {'owner_name': owner_name})
#     except User.DoesNotExist:
#         # Handle the case when the user is not found based on the vehicle number (username)
#         return render(request, 'index.html')
