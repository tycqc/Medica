from rest_framework.views import APIView
from rest_framework.response import Response
from medicine.models import Medicine
from store.models import medstore
from django.forms.models import model_to_dict

class index(APIView):
    def get(self,request):
        datalist=[]
        all_medicine=Medicine.objects.all()
        for medicine in all_medicine:
            medicine = model_to_dict(medicine)
            datalist.append(medicine)
        print(datalist)
        return Response({"dataList": datalist})