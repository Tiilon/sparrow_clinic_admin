from django.shortcuts import render
from .models import *
from .serializer import *
from management.models import *
from marketing.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime, timedelta


@api_view(['GET', 'POST'])
def patient(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        first_name = str(request.data.get('first_name')).upper()
        last_name = str(request.data.get('last_name')).upper()
        gender = request.data.get('gender')
        marital_status = request.data.get('marital_status')
        date_of_birth = request.data.get('dob')
        contact = request.data.get('contact')

        try:
            patient = Patient.objects.get(first_name=first_name, last_name=last_name, contact=contact)
            return Response ({'error': 'Patient already exists'})
        except Patient.DoesNotExist:
            new_patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                contact=contact,
                gender=gender,
                marital_status=marital_status,
                date_of_birth=date_of_birth,
                created_by = request.user,
                )
    return Response(PatientSerializer(new_patient).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'})
    
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def vital_signs(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient cannot be found'})
    
    if request.method == 'GET':
        vital_signs = VitalSign.objects.filter(patient=patient)
        serializer=VitalSignSerializer(vital_signs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    if request.method == 'POST':
        weight = request.data.get('weight')
        sys = request.data.get('sys')
        dias = request.data.get('dias')
        respiration = request.data.get('respiration')
        temperature = request.data.get('temperature')
        pulse = request.data.get('pulse')

        bp = f"{sys}/{dias}"
        if request.method == 'POST':
            nvs = VitalSign.objects.create(
                patient=patient,
                diastolic=dias,
                systolic=sys,
                weight=weight,
                respiration=respiration,
                temperature=temperature,
                created_by=request.user,
                created_at=timezone.now().date(),
                pulse= pulse,
                attendance=attendance,
            )
        return Response({'success':'Created Successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def attendance(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error':'Patient Does Not Exist'})
    
    if request.method == 'GET':
        attendances = Attendance.objects.filter(patient=patient)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            branch = Branch.objects.get(code=request.user.branch_code)
        except Branch.DoesNotExist:pass
        try:
            attendances = Attendance.objects.filter(patient=patient)
            if attendances:
                patient.is_first_time = False
                patient.save()
        except Attendance.DoesNotExist:pass        

        patient.is_discharged = False
        new_attendance = Attendance.objects.create(
            patient=patient,
            branch = branch.code,
            is_recorded = True,
            created_by=request.user,
            is_first_time = False if attendances else True 
        )
        
        if request.data.get('walk_in'):
            new_attendance.is_walk_in = True
            new_attendance.save()
        
        Feedback.objects.create(attendance=new_attendance)
        patient.save()
        
        return Response({"Success":"It was successfully created"})


@api_view(['GET'])
def clinic_day_stats(request):
    if request.method == 'GET':
        total_visits_number=0
        first_time_list = []
        subsequent_time_list = []
        walk_in_list = []
        consultation_list = []
        new_clients_per = 0
        sub_clients_per=0
        walk_in_number_per=0
        consultaion_number_per=0
        new_clients_number=0
        walk_in_number=0

        try:
            branch = Branch.objects.get(code=request.user.branch_code)
            total_visits = Attendance.objects.filter(branch=branch.code, created_at__date = today)
        except Branch.DoesNotExist:pass
       
        if total_visits:
            total_visits_number = total_visits.count()
            for attendance in total_visits:
                if attendance.is_first_time:
                    first_time_list.append(attendance)
                else:
                    subsequent_time_list.append(attendance)
                if attendance.is_walk_in:
                    walk_in_list.append(attendance)
                elif not attendance.is_walk_in:
                    consultation_list.append(attendance)
            if len(first_time_list) >= 0:
                new_clients_number = len(first_time_list)
            
            
            new_clients_per = new_clients_number/total_visits_number * 100
            sub_clients_per = len(subsequent_time_list)/total_visits_number * 100
            walk_in_number_per = walk_in_number/total_visits_number * 100
            consultaion_number_per = len(consultation_list)/total_visits_number * 100
        
            return Response({
                'total_visitors':total_visits_number,
                'new_clients':new_clients_number,
                'old_clients':len(subsequent_time_list),
                'walk_ins':walk_in_number,
                'consultaion_number':len(consultation_list),
                'new_clients_per':new_clients_per,
                'sub_clients_per':sub_clients_per,
                'walk_in_number_per':walk_in_number_per,
                'consultaion_number_per':consultaion_number_per
            })
        else:
            return Response({
                'total_visitors':0,
                'new_clients':0,
                'old_clients':0,
                'walk_ins':0,
                'consultaion_number':0,
                'new_clients_per':0,
                'sub_clients_per':0,
                'walk_in_number_per':0,
                'consultaion_number_per':0
                })


