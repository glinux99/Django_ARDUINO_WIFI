from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from gateway.models import View_lp, autorisation
from gateway.form import DataSend
from datetime import datetime
k=str(datetime.now().time())
tp=k.split(':')
obj=View_lp.objects.all()
alarme=0
for obj in obj:
      tp1= obj.date_alum
      tp2= obj.date_ext
      tp1 = tp1.split(':')
      tp2 = tp2.split(':')
      if( tp[0]>= tp1[0]):
         if( tp[1] >=tp1[1]):
            obj.status = True
            obj.save()
      if( tp[0]>= tp2[0]):
         if( tp[1]>= tp2[1]):
            obj.status = False
            obj.save()
def status():
       lampe=autorisation.objects.get(id=1)
       if(lampe.alarme_on):
          return 1
       else:
           return 0
def HomeP1(request, lampe):
     if (lampe == 22):
          alarme=autorisation.objects.get(id=1)
          alarme.alarme_on= False
          alarme.save()
     if (lampe != 0 and lampe != 22):
          lampe=View_lp.objects.get(id_int=lampe)
          
          if (lampe.status ==  True):
               lampe.status = False
               lampe.save()
          else :
               lampe.status = True
               lampe.save()
     lampe=View_lp.objects.all()
     
     return render(request,  'gateway/index.html', {'lampe': lampe,'alarme':status()})
def HomeP(request):
    lampe=View_lp.objects.all()
    return render(request,  'gateway/index.html', {'lampe': lampe})
def Connect(request, lampe):
    return render(request,  'gateway/index.html', {'lampe': lampe,'alarme':status()})
def fermer(request):
    return render(request,  'gateway/lock.html')
def essaie(request):
    return render(request,  'gateway/essaie.html', {'alarme':status()})
def Lampes(request):
    lampe=View_lp.objects.all()
    return render(request,  'gateway/lampes.html', {'lampe':lampe,'alarme':status()})
def PlanHome(request):
    return render(request,  'gateway/planHome.html', {'alarme':status()})
    
def securite(request):
    lampe=View_lp.objects.all()
    if request.POST:
        if(request.POST.get('psswd')):
            req1= request.POST.get('psswd')
            try:
               auto=autorisation.objects.get(psswd=req1)
               alarme=autorisation.objects.get(id=1)
               alarme.alarme_on= True
               alarme.save()
            
            except Exception as e:
               auto=autorisation.objects.all()
               return render(request,  'gateway/autorisations.html', {'autorisations': auto, 'alarme':status()})
        else: 
             return render(request,  'gateway/index.html')   
    return render(request,  'gateway/index.html',{'lampe': lampe,'alarme':status()})
def auto(request):
    if request.POST:
         req1= request.POST.get('consomation')
         temp1=request.POST.get('temp1')
         temp2=request.POST.get('temp2')
         select=request.POST.get('select')
         if(select=="1"):
             req1=req1.replace(',','.')
             req1=float(req1)
             lampe=View_lp.objects.get(consomation=req1)
             lampe.date_alum=temp1
             lampe.date_ext=temp2
             lampe.consomation_f=req1
             lampe.save()
    automate=View_lp.objects.all()
    return render(request,  'gateway/automatisation.html', {'automate':automate, 'alarme':status()})
def statistiques(request):
    labels=[]
    data=[]
    cons=View_lp.objects.all()
    for x in cons:
        y=x.consomation
        
        data.append(y)
    return render(request,  'gateway/statistiques.html', {'alarme':status(), 'cons': data})
def autorisations(request):
    auto=autorisation.objects.all()
    return render(request,  'gateway/autorisations.html', {'autorisations': auto, 'alarme':status()})
def autres(request):
    return render(request,  'gateway/autres.html', {'alarme':status()})
# Create your views here.
