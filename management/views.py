from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.serializers import *
from .serializers import *
from .models import *


@api_view(['GET', 'POST'])
def user(request):
    userx=[]

    if request.method == 'GET':
        users = User.objects.all()
        for user in users:
            branch=None
            try:
                branch = Branch.objects.get(code=user.branch_code)
            except Branch.DoesNotExist:pass
            details = {
            'branch': branch.name if branch else None,
            'branch_code':user.branch_code,
            'contact':user.contact,
            'date_joined':user.date_joined.date(),
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'gender':user.gender,
            'profile':user.profile,
            'role':user.role,
            'staff_id':user.staff_id,   
            }
            userx.append(details)
        serializer = UserSerializer(users, many=True)
        
        return Response(userx, status=status.HTTP_200_OK)

    if request.method == 'POST':
        
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        contact = request.data.get('contact')
        gender = request.data.get('gender')
        staff_id = request.data.get('staff_id')
        role = request.data.get('role')
        profile = request.data.get('profile')
        password = request.data.get('password')
        branch = request.data.get('branch')
        try:
            user = User.objects.get(email=email)
            branch = Branch.objects.get(code=branch)
            return Response({'error':'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                contact=contact,
                gender=gender,
                staff_id=staff_id,
                role=role,
                profile=profile,
                branch_code = branch
            )
            user.set_password(password)
            user.save()
        # print(user)
    return Response({'success':'Created Successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT','DELETE'])
def staff_details(request, staff_id):
    try:
        user = User.objects.get(staff_id=staff_id)
        branch = Branch.objects.get(code=user.branch_code)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # context = {
    #     'branch_name':branch.name,
    # }

    if request.method == 'GET':
        serializer = UserSerializer(user)
        
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    try:
        branch = Branch.objects.get(code=request.data.get('branch'))
    except Branch.DoesNotExist:
        pass
 
    if request.method == 'PUT':
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.email = request.data.get('email')
        user.contact = request.data.get('contact')
        user.gender = request.data.get('gender')
        user.staff_id = request.data.get('staff_id')
        user.role = request.data.get('role')
        user.profile = request.data.get('profile')
        user.branch_code = str(branch.code)
        user.save()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        user.delete()
        return Response({'success':'Deleted User'})


@api_view(['POST', 'GET'])
def branch(request):
    if request.method == 'GET':
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST', 'GET'])
# def branch_details(request, code):
#     if request.method == 'GET':
#         branch = Branch.objects.get(code=code)
#         staffs = User.objects.filter(branch_code=code)
#         serializer = BranchSerializer(branch)
#         return Response({
#             'name':branch.name,
#             'staffs_no':staffs.count()
#         }, status=status.HTTP_200_OK)


    if request.method == 'POST':
        serializer = AddBranchSerializer(data=request.data)
        if serializer.is_valid():
            name = str(request.data.get('name')).upper()

            try:
                branch = Branch.objects.get(name=name)
                return Response({'error':'A branch with name ' + name + ' already exists'})
            except Branch.DoesNotExist:
                branch = Branch.objects.create(name=name)
                branch.created_by = request.user
                branch.save()
                    
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def delete_branch(request,id):
    if request.method == 'POST':
        branch = Branch.objects.get(id=id)
        branch.delete()
        return Response({'success':'Deleted branch'})
