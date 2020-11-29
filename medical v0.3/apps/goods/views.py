from rest_framework.views import APIView
from rest_framework.response import Response
from medicine.models import Medicine
from store.models import medstore
from django.forms.models import model_to_dict
from goods.serializer import detailSerializer

class index(APIView):
    def get(self,request):
        datalist=[]
        all_medicine=Medicine.objects.all()
        for medicine in all_medicine:
            medicine = model_to_dict(medicine)
            datalist.append(medicine)
        return Response({"dataList": datalist})

class detail(APIView):
    def get(self,request):
        ser = detailSerializer(data=request.query_params)
        id = ser.initial_data.get('id')
        medicine = Medicine.objects.get(id=id)
        store=medicine.drugstore.name
        medicine = model_to_dict(medicine)
        print(store)
        return Response({"medicine_info": medicine,"store":store})

