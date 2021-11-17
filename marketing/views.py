from django.shortcuts import render
from .models import *
from management.models import *
from marketing.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime, timedelta
import time
from isoweek import Week
from django.http import HttpResponse,FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4


@api_view(['GET','POST'])
def attendances_feedback(request):
    today = date.today()
    currentWeek = date(today.year, today.month, today.day).strftime('%V')
    # for first_day for previous week it will be {int(currentWeek)-1}-1
    first_day= datetime.strptime(f"{today.year}-W{int(currentWeek)}-1", "%Y-W%W-%w").date()
    # last_day for previous week
    last_day = first_day + timedelta(days=6.9)
    attendances_list=[]
    if request.method =="GET":
        attendances = Attendance.objects.filter(created_at__date__range=[first_day,last_day])
        for attendance in attendances:
            details = {
            'name':attendance.patient.full_name(),
            'contact':attendance.patient.contact,
            'branch': Branch.objects.get(code=attendance.branch).name,
            'date':attendance.created_at.date(),
            'feedback':attendance.feedback.id,
            'feedback_status':attendance.feedback.is_complete
            }
            attendances_list.append(details)
        return Response(attendances_list, status=status.HTTP_200_OK)

    if request.method =="POST":
        branch = request.data['branch']
        attendances=[]
        if request.data['branch'] == 'all':
            attendances = Attendance.objects.filter(created_at__date__range=[first_day,last_day])
            for attendance in attendances:
                details = {
                'name':attendance.patient.full_name(),
                'contact':attendance.patient.contact,
                'branch': Branch.objects.get(code=attendance.branch).name,
                'date':attendance.created_at.date(),
                'feedback':attendance.feedback.id,
                'feedback_status':attendance.feedback.is_complete
                }
                attendances_list.append(details)
        else:
            attendances = Attendance.objects.filter(branch=branch,created_at__date__range=[first_day,last_day])
            for attendance in attendances:
                details = {
                'name':attendance.patient.full_name(),
                'contact':attendance.patient.contact,
                'branch': Branch.objects.get(code=branch).name,
                'date':attendance.created_at.date(),
                'feedback':attendance.feedback.id,
                'feedback_status':attendance.feedback.is_complete
                }
                attendances_list.append(details)
        return Response(attendances_list, status=status.HTTP_200_OK)


@api_view(['GET','PUT'])
def feedback(request, id):
    try:
        feedback = Feedback.objects.get(id=id)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        return Response({
            'patient': feedback.attendance.patient.full_name(),
            'date': feedback.attendance.created_at.date()
        })

    if request.method == 'PUT':
        reception = request.data.get('reception')
        nurse = request.data.get('nurse')
        doctor = request.data.get('doctor')
        lab = request.data.get('lab')
        pharmacy = request.data.get('pharmacy')
        cashier = request.data.get('cashier')
        house_keeper = request.data.get('house_keeper')
        overall = request.data.get('overall')
        opinion = request.data.get('opinion')
        best_staff = request.data.get('best_staff')
        referal= request.data.get('referal')
        
        feedback.reception=reception
        feedback.nurse=nurse
        feedback.doctor=doctor
        feedback.lab=lab
        feedback.pharmacy=pharmacy
        feedback.cashier=cashier
        feedback.house_keeper=house_keeper
        feedback.overall=overall
        feedback.opinion=opinion
        feedback.best_staff=best_staff
        feedback.how_did_you_hear_abt_rabito=referal
        feedback.created_by = request.user 
        feedback.is_complete = True
        feedback.save()
        

        return Response({
            'patient': feedback.attendance.patient.full_name(),
            'date': feedback.attendance.created_at.date()
        })

@api_view(['GET','POST'])
def analyses(request):
    if request.method == 'GET':
        branches=Branch.objects.all()
        today = date.today()
        currentWeek = date(today.year, today.month, today.day).strftime('%V')
        # for first_day for previous week it will be {int(currentWeek)-1}-1
        first_day_currentWeek= datetime.strptime(f"{today.year}-W{int(currentWeek)}-1", "%Y-W%W-%w").date()
        last_day_currentWeek = first_day_currentWeek + timedelta(days=6.9)
        first_day_previousWeek= datetime.strptime(f"{today.year}-W{int(currentWeek)-1}-1", "%Y-W%W-%w").date()
        last_day_previousWeek = first_day_previousWeek + timedelta(days=6.9)
        attendances_currentWeek = Attendance.objects.filter(created_at__date__range=[first_day_currentWeek,last_day_currentWeek])
        attendances_currentWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_currentWeek,last_day_currentWeek], feedback__is_complete=True)
        attendances_previousWeek = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek])
        patient_count_data=[]
        total_patient_count_data=[]
        satisfied_list=[]
        unsatisfied_list=[]
        all_satisfied_list=[]
        all_unsatisfied_list=[]
        pie_chart =[]
        report_summary=[]
        branch_summary={}
        satisfied=0
        unsatisfied=0
        
        for attendance in attendances_currentWeek_feedback:
            try:
                if attendance.feedback.overall >= 4:
                    all_satisfied_list.append(attendance)
                elif attendance.feedback.overall < 4:
                    all_unsatisfied_list.append(attendance)
            except:pass
        
        try:
            satisfied=(len(all_satisfied_list)/len(attendances_currentWeek_feedback))*100
        except ZeroDivisionError:
            pass

        try:
            unsatisfied=(len(all_unsatisfied_list)/len(attendances_currentWeek_feedback))*100
        except ZeroDivisionError:
            pass

        satisfied_per = {'name':'Satisfied', 'value':satisfied}
        unsatisfied_per = {'name':'Unsatisfied', 'value':unsatisfied}
        pie_chart.append(satisfied_per)
        pie_chart.append(unsatisfied_per)

        total_patient_count = {
            'name': 'Overall Patient Count',
            'current': len(attendances_currentWeek) if attendances_currentWeek else 0,
            'previous': len(attendances_previousWeek) if attendances_previousWeek else 0,
            }
        total_patient_count_data.append(total_patient_count)

        for branch in branches:
            first_time = []
            patients_reached = []
            current_very_good_list=[]
            current_good_list=[]
            current_fair_list=[]
            current_bad_list=[]
            current_excellent_list=[]
            previous_very_good_list=[]
            previous_good_list=[]
            previous_fair_list=[]
            previous_bad_list=[]
            previous_excellent_list=[]
            feedback_comments=[]
            attendances_currentWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_currentWeek,last_day_currentWeek],branch=branch.code, feedback__is_complete=True)
            attendances_previousWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek], branch=branch.code, feedback__is_complete=True)
            attendances_previousWeek = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek], branch=branch.code)
            attendances_currentWeek = Attendance.objects.filter(created_at__date__range=[first_day_currentWeek,last_day_currentWeek],branch=branch.code)

            for attendance in attendances_currentWeek_feedback:
                try:
                    if attendance.feedback.overall > 3:
                        satisfied_list.append(attendance)
                    elif attendance.feedback.overall < 4:
                        unsatisfied_list.append(attendance)
                    
                    if attendance.feedback.overall == 5:
                        current_excellent_list.append(attendance)
                    elif attendance.feedback.overall == 4:
                        current_very_good_list.append(attendance)
                    elif attendance.feedback.overall == 3:
                        current_good_list.append(attendance)
                    elif attendance.feedback.overall == 2:
                        current_fair_list.append(attendance)
                    elif attendance.feedback.overall == 1:
                        current_bad_list.append(attendance)
                except:pass

                if attendance.is_first_time:
                    first_time.append(attendance)
                try:
                    if attendance.feedback.is_complete:
                        patients_reached.append(attendance)
                except:pass
                if attendance.feedback.opinion:
                    details = {
                        'branch':branch.name,
                        'comment': attendance.feedback.opinion,
                        'patient': attendance.patient.full_name(),
                    }
                    feedback_comments.append(details)   
            
            for attendance in attendances_previousWeek_feedback:
                try:
                    # if attendance.feedback.overall > 3:
                    #     satisfied_list.append(attendance)
                    # elif attendance.feedback.overall < 4:
                    #     unsatisfied_list.append(attendance)
                    
                    if attendance.feedback.overall == 5:
                        previous_excellent_list.append(attendance)
                    elif attendance.feedback.overall == 4:
                        previous_very_good_list.append(attendance)
                    elif attendance.feedback.overall == 3:
                        previous_good_list.append(attendance)
                    elif attendance.feedback.overall == 2:
                        previous_fair_list.append(attendance)
                    elif attendance.feedback.overall == 1:
                        previous_bad_list.append(attendance)
                except:pass
            

            #FEEDBACK HIGHLIGHTS
            cur_excellent_per= (len(current_excellent_list)/len(attendances_currentWeek_feedback))*100 if current_excellent_list else 0
            pre_excellent_per= (len(previous_excellent_list)/len(attendances_previousWeek_feedback))*100 if previous_excellent_list else 0
            excellent_comment = ''
            if cur_excellent_per > pre_excellent_per:
                if pre_excellent_per == 0:
                    excellent_comment = "Previous value was 0%"
                else:
                    excellent_comment = f"Increase by {round((cur_excellent_per-pre_excellent_per),1)}%"
            elif cur_excellent_per < pre_excellent_per:
                excellent_comment = f"Decrease by {round((pre_excellent_per-cur_excellent_per),1)}%"
            elif cur_excellent_per == pre_excellent_per:
                excellent_comment= 'No percentage difference'

            cur_very_good_per= (len(current_very_good_list)/len(attendances_currentWeek_feedback))*100 if current_very_good_list else 0
            pre_very_good_per= (len(previous_very_good_list)/len(attendances_previousWeek_feedback))*100 if previous_very_good_list else 0
            very_good_comment = ''
            if cur_very_good_per > pre_very_good_per:
                if pre_very_good_per == 0:
                    very_good_comment = "Previous value was 0%"
                else:
                   very_good_comment = f"Increase by {round((cur_very_good_per-pre_very_good_per),1)}%" 
            elif cur_very_good_per < pre_very_good_per:
                very_good_comment = f"Decrease by {round((pre_very_good_per-cur_very_good_per),1)}%"
            elif cur_very_good_per == pre_very_good_per:
                very_good_comment= 'No percentage difference'
            
            cur_fair_per= (len(current_fair_list)/len(attendances_currentWeek_feedback))*100 if current_fair_list else 0
            pre_fair_per= (len(previous_fair_list)/len(attendances_previousWeek_feedback))*100 if previous_fair_list else 0
            fair_comment = ''
            if cur_fair_per > pre_fair_per:
                if pre_fair_per ==0:
                    fair_comment="Previous value was 0%"
                else:
                    fair_comment = f"Increase by {round((cur_fair_per-pre_fair_per),1)}%"
            elif cur_fair_per < pre_fair_per:
                fair_comment = f"Decrease by {round((pre_fair_per-cur_fair_per),1)}%"
            elif cur_fair_per == pre_fair_per:
                fair_comment= 'No percentage difference'
            
            cur_good_per= (len(current_good_list)/len(attendances_currentWeek_feedback))*100 if current_good_list else 0
            pre_good_per= (len(previous_good_list)/len(attendances_previousWeek_feedback))*100 if previous_good_list else 0
            good_comment = ''
            if cur_good_per > pre_good_per:
                if pre_good_per == 0:
                    good_comment="Previous value was 0%"
                else:
                    good_comment = f"Increase by {round((cur_good_per-pre_good_per),1)}%"
            elif cur_good_per < pre_good_per:
                good_comment = f"Decrease by {round((pre_good_per-cur_good_per),1)}%"
            elif cur_good_per == pre_good_per:
                good_comment= 'No percentage difference'
            
            cur_bad_per= (len(current_bad_list)/len(attendances_currentWeek_feedback))*100 if current_bad_list else 0
            pre_bad_per= (len(previous_bad_list)/len(attendances_previousWeek_feedback))*100 if previous_bad_list else 0
            bad_comment = ''
            if cur_bad_per > pre_bad_per:
                if pre_bad_per == 0:
                    bad_comment = "Previous value was 0%"
                else:
                    bad_comment = f"Increase by {round((cur_bad_per-pre_bad_per),1)}%"
            elif cur_bad_per < pre_bad_per:
                bad_comment = f"Decrease by {round((pre_bad_per-cur_bad_per),1)}%"
            elif cur_bad_per == pre_bad_per:
                bad_comment= 'No percentage difference'

            branch_summary= {
                'branch':branch.name,
                'total_visits': attendances_currentWeek.count(),
                'first_time': len(first_time),
                'patients_reached':len(patients_reached),
                'excellent_feedback': cur_excellent_per,
                'excellent_comment': excellent_comment,
                'very_good_feedback': cur_very_good_per,
                'very_good_comment': very_good_comment,
                'good_feedback': cur_good_per,
                'good_comment': good_comment,
                'fair_feedback': cur_fair_per,
                'fair_comment': fair_comment,
                'bad_feedback': cur_bad_per,
                'bad_comment': bad_comment,
                'current_patient_count': len(attendances_currentWeek) if attendances_currentWeek else 0,
                'previous_patient_count': len(attendances_previousWeek) if attendances_previousWeek else 0,
                'feedback_comments':feedback_comments
            }
            report_summary.append(branch_summary)

            patient_count = {
                'name': branch.name,
                #patient count branch by branch
                'current': attendances_currentWeek.count() if attendances_currentWeek.count() else 0,
                'previous': attendances_previousWeek.count() if attendances_previousWeek.count() else 0,
                #patient satisfaction branch by branch
                'satisfied': len(satisfied_list),
                'unsatisfied':len(unsatisfied_list),
            }
            patient_count_data.append(patient_count)

        return Response({
            'patient_count': patient_count_data,
            'pie_chart':pie_chart,
            'total_patient_count_data':total_patient_count_data,
            'report_summary':report_summary
        })

    if request.method == 'POST':
        today = date.today()
        date_input = request.data['date']
        week_input=None
        selected_date=None
        if date_input != 'current':
            selected_date = datetime.strptime(date_input, '%Y-%m-%d')
        currentWeek = date(today.year, today.month, today.day).strftime('%V')
        if date_input == 'current':
            week_input = currentWeek
        else:
            week_input = date(selected_date.year, selected_date.month, selected_date.day).strftime('%V') 
        first_day_selectedWeek= datetime.strptime(f"{today.year}-W{int(week_input)}-1", "%Y-W%W-%w").date()
        last_day_selectedWeek = first_day_selectedWeek + timedelta(days=6.9)
        branches=Branch.objects.all()
        
        first_day_previousWeek= datetime.strptime(f"{today.year}-W{int(week_input)-1}-1", "%Y-W%W-%w").date()
        last_day_previousWeek = first_day_previousWeek + timedelta(days=6.9)
        attendances_currentWeek = Attendance.objects.filter(created_at__date__range=[first_day_selectedWeek,last_day_selectedWeek])
        attendances_currentWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_selectedWeek,last_day_selectedWeek], feedback__is_complete=True)
        attendances_previousWeek = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek])

        patient_count_data=[]
        total_patient_count_data=[]
        satisfied_list=[]
        unsatisfied_list=[]
        all_satisfied_list=[]
        all_unsatisfied_list=[]
        pie_chart =[]
        report_summary=[]
        branch_summary={}
        satisfied=0
        unsatisfied=0


        for attendance in attendances_currentWeek_feedback:
            try:
                if attendance.feedback.overall >= 4:
                    all_satisfied_list.append(attendance)
                elif attendance.feedback.overall < 4:
                    all_unsatisfied_list.append(attendance)
            except:pass
        
        try:
            satisfied=(len(all_satisfied_list)/len(attendances_currentWeek_feedback))*100
        except ZeroDivisionError:
            pass

        try:
            unsatisfied=(len(all_unsatisfied_list)/len(attendances_currentWeek_feedback))*100
        except ZeroDivisionError:
            pass

        satisfied_per = {'name':'Satisfied', 'value':satisfied}
        unsatisfied_per = {'name':'Unsatisfied', 'value':unsatisfied}
        pie_chart.append(satisfied_per)
        pie_chart.append(unsatisfied_per)

        total_patient_count = {
            'name': 'Overall Patient Count',
            'current': len(attendances_currentWeek) if attendances_currentWeek else 0,
            'previous': len(attendances_previousWeek) if attendances_previousWeek else 0,
            }
        total_patient_count_data.append(total_patient_count)

        for branch in branches:
            first_time = []
            patients_reached = []
            current_very_good_list=[]
            current_good_list=[]
            current_fair_list=[]
            current_bad_list=[]
            current_excellent_list=[]
            previous_very_good_list=[]
            previous_good_list=[]
            previous_fair_list=[]
            previous_bad_list=[]
            previous_excellent_list=[]
            feedback_comments=[]
            attendances_currentWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_selectedWeek,last_day_selectedWeek],branch=branch.code, feedback__is_complete=True)
            attendances_currentWeek = Attendance.objects.filter(created_at__date__range=[first_day_selectedWeek,last_day_selectedWeek],branch=branch.code)
            attendances_previousWeek_feedback = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek], branch=branch.code, feedback__is_complete=True)
            attendances_previousWeek = Attendance.objects.filter(created_at__date__range=[first_day_previousWeek,last_day_previousWeek], branch=branch.code)

            for attendance in attendances_currentWeek_feedback:
                try:
                    if attendance.feedback.overall > 3:
                        satisfied_list.append(attendance)
                    elif attendance.feedback.overall < 4:
                        unsatisfied_list.append(attendance)
                   
                    if attendance.feedback.overall == 5:
                        current_excellent_list.append(attendance)
                    elif attendance.feedback.overall == 4:
                        current_very_good_list.append(attendance)
                    elif attendance.feedback.overall == 3:
                        current_good_list.append(attendance)
                    elif attendance.feedback.overall == 2:
                        current_fair_list.append(attendance)
                    elif attendance.feedback.overall == 1:
                        current_bad_list.append(attendance)
                except:pass

                if attendance.is_first_time:
                    first_time.append(attendance)
                try:
                    if attendance.feedback.is_complete:
                        patients_reached.append(attendance)
                except:pass

                if attendance.feedback.opinion:
                    details = {
                        'branch':branch.name,
                        'comment': attendance.feedback.opinion,
                        'patient': attendance.patient.full_name(),
                    }
                    feedback_comments.append(details)
          
            for attendance in attendances_previousWeek_feedback:
                try:
                    # if attendance.feedback.overall > 3:
                    #     satisfied_list.append(attendance)
                    # elif attendance.feedback.overall < 4:
                    #     unsatisfied_list.append(attendance)
                    
                    if attendance.feedback.overall == 5:
                        previous_excellent_list.append(attendance)
                    elif attendance.feedback.overall == 4:
                        previous_very_good_list.append(attendance)
                    elif attendance.feedback.overall == 3:
                        previous_good_list.append(attendance)
                    elif attendance.feedback.overall == 2:
                        previous_fair_list.append(attendance)
                    elif attendance.feedback.overall == 1:
                        previous_bad_list.append(attendance)
                except:pass

            cur_excellent_per= (len(current_excellent_list)/len(attendances_currentWeek_feedback))*100 if current_excellent_list else 0
            pre_excellent_per= (len(previous_excellent_list)/len(attendances_previousWeek_feedback))*100 if previous_excellent_list else 0
            excellent_comment = ''
            if cur_excellent_per > pre_excellent_per:
                if pre_excellent_per == 0:
                    excellent_comment = f"Previous value was 0%"
                else:
                    excellent_comment = f"Increase by {round((cur_excellent_per-pre_excellent_per),1)}%"
            elif cur_excellent_per < pre_excellent_per:
                if pre_excellent_per == 0:
                    excellent_comment = f"Previous value was 0%"
                else:
                    excellent_comment = f"Decrease by {round((pre_excellent_per-cur_excellent_per),1)}%"
                excellent_comment = f"Decrease by {round((pre_excellent_per-cur_excellent_per),1)}%"
            elif cur_excellent_per == pre_excellent_per:
                excellent_comment= 'No percentage difference'

            cur_very_good_per= (len(current_very_good_list)/len(attendances_currentWeek_feedback))*100 if current_very_good_list else 0
            pre_very_good_per= (len(previous_very_good_list)/len(attendances_previousWeek_feedback))*100 if previous_very_good_list else 0
            very_good_comment = ''
            if cur_very_good_per > pre_very_good_per:
                if pre_very_good_per == 0:
                    very_good_comment = f"Previous value was 0%"
                else:
                   very_good_comment = f"Increase by {round((cur_very_good_per-pre_very_good_per),1)}%" 
            elif cur_very_good_per < pre_very_good_per:
                if pre_very_good_per == 0:
                    very_good_comment = f"Previous value was 0%"
                else:
                    very_good_comment = f"Decrease by {round((pre_very_good_per-cur_very_good_per),1)}%"
            elif cur_very_good_per == pre_very_good_per:
                very_good_comment= 'No percentage difference'
            
            cur_fair_per= (len(current_fair_list)/len(attendances_currentWeek_feedback))*100 if current_fair_list else 0
            pre_fair_per= (len(previous_fair_list)/len(attendances_previousWeek_feedback))*100 if previous_fair_list else 0
            fair_comment = ''
            if cur_fair_per > pre_fair_per:
                if pre_fair_per ==0:
                    fair_comment=f"Previous value was 0%"
                else:
                    fair_comment = f"Increase by {round((cur_fair_per-pre_fair_per),1)}%"
            elif cur_fair_per < pre_fair_per:
                if pre_fair_per ==0:
                    fair_comment=f"Previous value was 0%"
                else:
                    fair_comment = f"Decrease by {round((pre_fair_per-cur_fair_per),1)}%"
            elif cur_fair_per == pre_fair_per:
                fair_comment= 'No percentage difference'
            
            cur_good_per= (len(current_good_list)/len(attendances_currentWeek_feedback))*100 if current_good_list else 0
            pre_good_per= (len(previous_good_list)/len(attendances_previousWeek_feedback))*100 if previous_good_list else 0
            good_comment = ''
            if cur_good_per > pre_good_per:
                if pre_good_per == 0:
                    good_comment=f"Previous value was 0%"
                else:
                    good_comment = f"Increase by {round((cur_good_per-pre_good_per),1)}%"
            elif cur_good_per < pre_good_per:
                if pre_good_per == 0:
                    good_comment=f"Previous value was 0%"
                else:
                    good_comment = f"Decrease by {round((pre_good_per-cur_good_per),1)}%"
            elif cur_good_per == pre_good_per:
                good_comment= 'No percentage difference'
            
            cur_bad_per= (len(current_bad_list)/len(attendances_currentWeek_feedback))*100 if current_bad_list else 0
            pre_bad_per= (len(previous_bad_list)/len(attendances_previousWeek_feedback))*100 if previous_bad_list else 0
            bad_comment = ''
            if cur_bad_per > pre_bad_per:
                if pre_bad_per == 0:
                    bad_comment = f"Previous value was 0%"
                else:
                    bad_comment = f"Increase by {round((cur_bad_per-pre_bad_per),1)}%"
            elif cur_bad_per < pre_bad_per:
                if pre_bad_per == 0:
                    bad_comment = f"Previous value was 0%"
                else:
                    bad_comment = f"Decrease by {round((pre_bad_per-cur_bad_per),1)}%"
            elif cur_bad_per == pre_bad_per:
                bad_comment= 'No percentage difference'
            
            branch_summary= {
                'branch':branch.name,
                'total_visits': attendances_currentWeek.count(),
                'first_time': len(first_time),
                'patients_reached':len(patients_reached),
                'excellent_feedback': cur_excellent_per,
                'excellent_comment': excellent_comment,
                'very_good_feedback': cur_very_good_per,
                'very_good_comment': very_good_comment,
                'good_feedback': cur_good_per,
                'good_comment': good_comment,
                'fair_feedback': cur_fair_per,
                'fair_comment': fair_comment,
                'bad_feedback': cur_bad_per,
                'bad_comment': bad_comment,
                'current_patient_count': len(attendances_currentWeek) if attendances_currentWeek else 0,
                'previous_patient_count': len(attendances_previousWeek) if attendances_previousWeek else 0,
                'feedback_comments':feedback_comments
            }
            report_summary.append(branch_summary)

            patient_count = {
                'name': branch.name,
                #patient count branch by branch
                'current': attendances_currentWeek.count() if attendances_currentWeek.count() else 0,
                'previous': attendances_previousWeek.count() if attendances_previousWeek.count() else 0,
                #patient satisfaction branch by branch
                'satisfied': len(satisfied_list),
                'unsatisfied':len(unsatisfied_list),
            }
            patient_count_data.append(patient_count)
        

        return Response({
            'patient_count': patient_count_data,
            'pie_chart':pie_chart,
            'total_patient_count_data':total_patient_count_data,
            'report_summary':report_summary
        })

# Gettting all weeks in the year
def dateRange(year,week):
  firstday= datetime.strptime(f"{year}-W{int(week)-1}-1", "%Y-W%W-%w").date()
  lastday = firstday + timedelta(days= 6.9)
  return firstday, lastday 

@api_view(['GET','POST'])
def feedback_reports(request):
    today = date.today()
    # currentWeek = date(today.year, today.month, today.day).strftime('%V')
    # first_day_currentWeek= datetime.strptime(f"{today.year}-W{int(currentWeek)}-1", "%Y-W%W-%w").date()
    # last_day_currentWeek = first_day_currentWeek + timedelta(days=6.9)
    branches = Branch.objects.all()
    week_list = []
    very_good_list=[]
    good_list=[]
    fair_list=[]
    bad_list=[]
    excellent_list=[]
    satisfied_list=[]
    unsatisfied_list=[]
    if request.method == 'GET':
        v = Week.last_week_of_year(2021).week

        for i in range(1,v+1):
            week = {
                "week": (dateRange(timezone.now().year, i)),
                'number' : i
                }
            week_list.append(week)
        return Response({"week_list": week_list})
    
    if request.method == 'POST':
        date_input = request.data['date']
        selected_date = datetime.strptime(date_input, '%Y-%m-%d')
        week_input = date(selected_date.year, selected_date.month, selected_date.day).strftime('%V')
        first_day_selectedWeek= datetime.strptime(f"{today.year}-W{int(week_input)}-1", "%Y-W%W-%w").date()
        last_day_selectedWeek = first_day_selectedWeek + timedelta(days=6.9)
        

        for branch in branches:
                attendances_selectedWeek = Attendance.objects.filter(created_at__date__range=[first_day_selectedWeek,last_day_selectedWeek],branch=branch.code)

                for attendance in attendances_selectedWeek:
                    
                    if attendance.feedback.overall > 3:
                        satisfied_list.append(attendance)
                    elif attendance.feedback.overall < 4:
                        unsatisfied_list.append(attendance)
                    elif attendance.feedback.overall == 5:
                        excellent_list.append(attendance)
                    elif attendance.feedback.overall == 4:
                        very_good_list.append(attendance)
                    elif attendance.feedback.overall == 3:
                        good_list.append(attendance)
                    elif attendance.feedback.overall == 2:
                        fair_list.append(attendance)
                    elif attendance.feedback.overall == 1:
                        bad_list.append(attendance)


def days_of_week():
    today = date.today()
    currentWeek = date(today.year, today.month, today.day).strftime('%V')
    firstday= datetime.strptime(f"{today.year}-W{int(currentWeek)-1}-1", "%Y-W%W-%w").date()
    second=firstday + timedelta(days= 1.9)
    third=firstday + timedelta(days= 2.9)
    fourth=firstday + timedelta(days= 3.9)
    fith=firstday + timedelta(days= 4.9)
    six=firstday + timedelta(days= 5.9)
    seven = firstday + timedelta(days= 6.9)
    return ([firstday,second, third, fourth, fith, six,seven])


@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        weekly_data = []
        monthly_data = []
        today = date.today()
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
        old_clients_number=0
        walk_in_number=0
        currentWeek = date(today.year, today.month, today.day).strftime('%V')
        firstday= datetime.strptime(f"{today.year}-W{int(currentWeek)}-1", "%Y-W%W-%w").date()
        second=firstday + timedelta(days= 1.9)
        third=firstday + timedelta(days= 2.9)
        fourth=firstday + timedelta(days= 3.9)
        fifth=firstday + timedelta(days= 4.9)
        six=firstday + timedelta(days= 5.9)
        seven = firstday + timedelta(days= 6.9)
        days_of_week = [firstday,second, third, fourth, fifth, six,seven]
        for day in days_of_week:
           attendances= Attendance.objects.filter(created_at__date=day) 
           weekly_data.append(len(attendances))
           
        jan_month = Attendance.objects.filter(created_at__month=1)
        monthly_data.append(len(jan_month) if jan_month else 0)
        feb_month = Attendance.objects.filter(created_at__month=2)
        monthly_data.append(len(feb_month) if feb_month else 0)
        mar_month = Attendance.objects.filter(created_at__month=3)
        monthly_data.append(len(mar_month) if mar_month else 0)
        apr_month = Attendance.objects.filter(created_at__month=4)
        monthly_data.append(len(apr_month) if apr_month else 0)
        may_month = Attendance.objects.filter(created_at__month=5)
        monthly_data.append(len(may_month) if may_month else 0)
        jun_month = Attendance.objects.filter(created_at__month=6)
        monthly_data.append(len(jun_month) if jun_month else 0)
        jul_month = Attendance.objects.filter(created_at__month=7)
        monthly_data.append(len(jul_month) if jul_month else 0) 
        aug_month = Attendance.objects.filter(created_at__month=8)
        monthly_data.append(len(aug_month) if aug_month else 0)
        sept_month = Attendance.objects.filter(created_at__month=9)
        monthly_data.append(len(sept_month) if sept_month else 0)
        oct_month = Attendance.objects.filter(created_at__month=10)
        monthly_data.append(len(oct_month) if oct_month else 0)
        nov_month = Attendance.objects.filter(created_at__month=11)
        monthly_data.append(len(nov_month) if nov_month else 0)
        dec_month = Attendance.objects.filter(created_at__month=12)
        monthly_data.append(len(dec_month) if dec_month else 0)

        total_visits = Attendance.objects.filter(created_at__date = today)
        
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
            
            consultaion_number=len(consultation_list)
            old_clients_number = len(subsequent_time_list)
            new_clients_per = new_clients_number/total_visits_number * 100
            sub_clients_per = len(subsequent_time_list)/total_visits_number * 100
            walk_in_number_per = walk_in_number/total_visits_number * 100
            consultaion_number_per = len(consultation_list)/total_visits_number * 100
        else:
            total_visits_number=0
            new_clients_number=0
            old_clients_number=0
            walk_in_number=0
            consultaion_number=0
            new_clients_per=0
            sub_clients_per=0
            walk_in_number_per=0
            consultaion_number_per=0
        

        return Response({
            'weekly_data':weekly_data,
            'monthly_data':monthly_data,
            'total_visitors':total_visits_number,
            'new_clients':new_clients_number,
            'old_clients':old_clients_number,
            'walk_ins':walk_in_number,
            'consultaion_number':consultaion_number,
            'new_clients_per':new_clients_per,
            'sub_clients_per':sub_clients_per,
            'walk_in_number_per':walk_in_number_per,
            'consultaion_number_per':consultaion_number_per,
            'profile':request.user.profile,
            'user':request.user.get_full_name()
        })
        