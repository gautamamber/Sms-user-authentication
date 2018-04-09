from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from twilio.rest import Client
import os
import random
# Create your views here.

class MyForm(forms.Form):
	mobile_no = forms.CharField(max_length = 20)
class OTPForm(forms.Form):
	otp = forms.IntegerField()

def generate_otp(mobile_no):
	otp = random.randint(1000,9999)
	account_sid =  "Your account sid"
	auth_token = "Your auth token"
	client = Client(account_sid, auth_token)
	client.messages.create(
		to = mobile_no,
		from_ = "+17752389482'",
		body = "Your OTP is" + str(otp)

		)
	f = open('otp.txt' , 'w')
	f.write(str(otp))
	f.close()
def send_otp(request):
	form = MyForm(request.POST)
	otp_form  = OTPForm(request.POST)
	otp = 0
	if form.is_valid():
		cd = form.cleaned_data
		mobile_no = cd.get('mobile_no')
		if os.path.getsize('otp.txt') == 0:
			generate_otp(mobile_no)
	elif otp_form.is_valid():
		f = open('otp.txt' , 'r')
		otp = int(f.read())
		open('otp.txt' , 'w').close()
		cd2 = otp_form.cleaned_data
		entered_otp = cd2.get('otp')
		if otp == entered_otp:
			return HttpResponseRedirect(reverse('success'))
		else:
			return HttpResponseRedirect(reverse('failure'))
	return render(request,'phonesms/index.html',{'form':form,'otp_form':otp_form})

def success(request):
	return render(request, 'phonesms/success.html')
def failure(request):
	return render(request, 'phonesms/failure.html')

