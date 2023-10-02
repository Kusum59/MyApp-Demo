import logging

from django.contrib.auth.models import User 
from django.shortcuts import render
from django.http import JsonResponse 
from django.core.exceptions import ObjectDoesNotExist 

from rest_framework.decorators import APIView  
from rest_framework import status 
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from  rest_framework.permissions import IsAuthenticated

from newapp.models import Employee 
from newapp import global_msg 
from newapp.serializers import EmployeeSerializers 


logger = logging.getLogger('django')

class EmployeeCreateApiView(APIView):
    authentication_classes = []
    permission_classes = [] 
    '''This class creates new employee only'''
    def post(self, request):
        if not request.body:
            msg = {
                global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY : "Invalid Request Body."
            }
            return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND) 
        try:
            serializers = EmployeeSerializers(data = request.data)
            user = User.objects.get(username = 'kusum')
            if serializers.is_valid():
                serializers.save(created_by = user)
                msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Data Created Successfully."  
                } 
                return JsonResponse(msg, status=status.HTTP_200_OK)
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data.",
                    global_msg.ERROR_KEY : serializers.errors  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        try:
            employee = Employee.objects.filter(is_delete = False)  

            serializers = EmployeeSerializers(employee, many = True)
            msg = {
                global_msg.RESPONSE_CODE_KEY : global_msg.SUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY : "Successful.",  
                "data": serializers.data 
            } 
            return JsonResponse(msg, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
    
class EmployeeEditApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def put(self, request, pk):
        if not request.body:
            msg = {
                global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY : "Invalid Request Body."
            }
            return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND) 
        try:
            employee = Employee.objects.get(id = pk, is_delete = False)
            serializers = EmployeeSerializers(employee, data = request.data)
            user = User.objects.get(username = 'kusum')
            
            if serializers.is_valid():
                serializers.save()
                msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Data Updated Successfully."   
                } 
                return JsonResponse(msg, status=status.HTTP_200_OK)
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data.",
                    global_msg.ERROR_KEY : serializers.errors  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "No Data Found."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
class EmployeeDeleteApiView(APIView):
    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
            employee.is_delete = True 
            employee.save() 
            msg = {
                global_msg.RESPONSE_CODE_KEY : global_msg.SUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY : "Delete Successfully." 
            }
            return JsonResponse(msg, status=status.HTTP_200_OK) 

        except ObjectDoesNotExist as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "No Data Found."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e),exc_info=True) 
            msg = {
                    global_msg.RESPONSE_CODE_KEY : global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY : "Invalid Data."  
                } 
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)

        

