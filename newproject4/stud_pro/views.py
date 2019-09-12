from django.shortcuts import render,redirect

from stud_pro.forms import teacherform,studentform,parentform
from stud_pro.models import *


def show(request):
	teachers = Teacher.objects.raw('SELECT * FROM stud_pro_teacher')
	return render(request,"show.html",{'teachers':teachers})

def class_combo(request):
	class_com = Class.objects.all()
	return render(request,"admin_add_student.html",{'class_com':class_com})

def student_profile(request):
	details = Student.objects.all()
	print(details)
	return render(request,"student/student_profile.html",{'details':details})

def teacher_classes(request):
	current_login_id=request.session['login_id']
	teachers = Teacher_Subject.objects.filter(teacher_id__exact=current_login_id)
	classt = Class_Teacher.objects.filter(sr_no__in= teachers)
	class_nm = Class.objects.filter(class_id__in = classt)
	#stud_nm = Student.objects.filter(class_id_id__in = class_nm)
	return render(request,"teacher/teacher_classes.html",{'class_nm':class_nm})

def teacher_students(request,class_id):
	#current_login_id=request.session['login_id']
	stud_from_cls = Student.objects.filter(class_id__exact=class_id)
	stud_from_cls[0].password=""
	print(class_id)
	print(stud_from_cls)
	#classt = Class_Teacher.objects.filter(sr_no__in= teachers)
	#class_nm = Class.objects.filter(class_id__in = classt)
	#stud_nm = Student.objects.filter(class_id_id__in = class_nm)
	return render(request,"teacher/teacher_students.html",{'stud_from_cls':stud_from_cls})	
# Create your views here.
def login(request):
	if ("session_on" in request.session):
		if (request.session["session_on"]=="student"):
			#print(request.session["login_id"])
			return redirect("/student/")
		elif (request.session["session_on"]=="parent"):
			return redirect("/parent/")


	elif (request.method == "GET"):
		return render(request,"login/login.html")

	elif (request.method == "POST"):
		current_login_id=request.POST['login_id']
		print(current_login_id)
		password=request.POST['pass_word']
		if (request.POST['type'] == "student"):
			request.session['session_on']="student"
			if (Student.objects.filter(student_id = current_login_id).exists() ):		#check in database
				request.session['login_id']=current_login_id
				print(current_login_id)
				student_det=Student.objects.filter(student_id__exact=current_login_id)
				#print(student_det["password"])
				if(password==student_det[0].password):
					del student_det[0].password
					return render(request,"student/student.html",{'student_det':student_det})
				else :
					request.session.clear()
					context = { 'invalid' : "invalid password " }
					return render(request,"login/login.html",context)
			else :
				request.session.clear()
				context1 = { 'invalid_id' : "invalid id " }
				return render(request,"login/login.html",context1)		
     
		elif (request.POST['type'] == "parent"):
			request.session['session_on']="parent"
			if (Parent.objects.filter(parent_id = current_login_id).exists() ):
				request.session['login_id']=current_login_id
				print(current_login_id)
				parent_det=Parent.objects.filter(parent_id__exact=current_login_id)
				if(password==parent_det[0].password):
					del parent_det[0].password
					return render(request,"parent/parent.html",{'parent_det':parent_det})
				else :
					request.session.clear()
					context = { 'invalid' : "invalid password " }
					return render(request,"login/login.html",context)
			else :
				request.session.clear()
				context1 = { 'invalid_id' : "invalid id " }
				return render(request,"login/login.html",context1)	
		elif(request.POST['type'] == "teacher"):
			request.session['session_on']="teacher"
			if (Teacher.objects.filter(teacher_id = current_login_id).exists() ):
				request.session['login_id']=current_login_id
				print(current_login_id)
				teacher_det=Teacher.objects.filter(teacher_id__exact=current_login_id)
				if(password==teacher_det[0].password):
					del teacher_det[0].password
					return render(request,"teacher/teacher.html",{'teacher_det':teacher_det})
				else :
					request.session.clear()
					context = { 'invalid' : "invalid password " }
					return render(request,"login/login.html",context)
			else :
				request.session.clear()
				context1 = { 'invalid_id' : "invalid id " }
				return render(request,"login/login.html",context1)	
	#request.session["invalid"]=login_id
	return render(request,"login/login.html")


def parent(request):
	if("session_on" in request.session):
		if(request.session["session_on"]=="parent"):
			login_id=request.session['login_id']
			
			# (to-do) parent dashboard
			return render(request,"parent/parent.html")
		else:
			request.session.clear()
			return redirect("/invalid/")
	else:
		return redirect("/login/")



def student(request):
	if("session_on" in request.session):
		if(request.session["session_on"]=="student"):
			login_id=request.session['login_id']

			# (to-do) student dashboard here
			return render(request,"student/student.html")
		else:
			request.session.clear()
			return redirect("/invalid/")
	else:
		return redirect("/login/")



def teacher(request):
	if("session_on" in request.session):
		if(request.session["session_on"]=="teacher"):
			login_id=request.session['login_id']

			# (to-do) teacher dashboard here
			return render(request,"teacher/teacher.html")
		else:
			request.session.clear()
			return redirect("/invalid/")
	else:
		return redirect("/login/")


def admin(request):
	if("session_on" in request.session):
		if(request.session["session_on"]=="admin"):
			login_id=request.session['login_id']
			# (to-do) admin dashboard
			return render(request,"admin/admin.html")
		else:
			request.session.clear()
			return redirect("/invalid/")
	else:
		return redirect("/login/")


def  admin_teacher(request):
	if request.method == "POST" :
		form = teacherform(request.POST)
		if form.is_valid():
			try :
				print(form.cleaned_data["teacher_name"])
				form.save()
				#return redirect("/show")
			except :
				pass
	else :
		form = teacherform()
	return render(request,"admin/admin_add_teacher.html",{'form':form})	

def  admin_student(request):
	if request.method == "POST" :
		form = studentform(request.POST)
#		if form.is_valid():
		try :
			print("sdjo")
			print(form.cleaned_data["cats"])
			form.save()
			#return redirect("/show")
		except :
			pass
	else :
		form = studentform()
	return render(request,"admin/admin_add_student.html",{'form':form})		

def  admin_parent(request):
	if request.method == "POST" :
		form = parentform(request.POST)
		if form.is_valid():
			try :
				form.save()
				#return redirect("/show")
			except :
				pass
	else :
		form = parentform()
	return render(request,"admin/admin_add_parent.html",{'form':form})
#	return redirect("/login/")




def logout(request):
	if("session_on" in request.session):	#deleate everything in the session
		request.session.clear()
	return redirect("/login/")

