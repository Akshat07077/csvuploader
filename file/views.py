from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CSVForm,CSVUpdateForm
from .models import CSVfiles,CSVData
from django.core.paginator import Paginator
import csv
from django.contrib import messages
from django.contrib.auth import login, authenticate
from io import TextIOWrapper
from .serializers import UserSerializer, LoginSerializer, CSVFileSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import CSVfiles
from .serializers import UserSerializer, LoginSerializer, CSVFileSerializer

class SignupAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CSVUploadAPIView(generics.CreateAPIView):
    serializer_class = CSVFileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#Functionsss
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'registration/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')



@login_required
def upload_file(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save(commit=False)
            csv_file.user = request.user
            csv_file.save()

            # Parse the CSV file and save its data
            handle_uploaded_csv(csv_file)

            return redirect('file_list')
    else:
        form = CSVForm()
    return render(request, 'uploadFile.html', {'form': form})

def handle_uploaded_csv(csv_file):
    try:
        with open(csv_file.file.path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row_number, row in enumerate(reader):
                CSVData.objects.create(file=csv_file, row_number=row_number, data=row)
    except UnicodeDecodeError:
        with open(csv_file.file.path, newline='', encoding='latin-1') as file:
            reader = csv.reader(file)
            for row_number, row in enumerate(reader):
                CSVData.objects.create(file=csv_file, row_number=row_number, data=row)
@login_required
def exportCsv(request,file_id):
    csvFile = CSVfiles.objects.get(id=file_id, user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csvFile.file.name}"'
    
    with open(csvFile.file.path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(response)
        for row in reader:
            writer.writerow(row)

    return response
@login_required
def file_list(request):
    files = CSVfiles.objects.filter(user=request.user)
    paginator = Paginator(files, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fileList.html', {'page_obj': page_obj})

@login_required
def view_csv(request, file_id):
    csv_file = get_object_or_404(CSVfiles, id=file_id, user=request.user)
    data = []
    columns = []

    # Read the CSV file into memory
    with open(csv_file.file.path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
        if data:
            columns = data[0]

    # Handle form submission
    if request.method == 'POST':
        form = CSVUpdateForm(request.POST)
        if form.is_valid():
            row_data = form.cleaned_data['row_data']
            column_name = form.cleaned_data['column_name']

            # Add new column if provided
            if column_name:
                columns.append(column_name)
                for row in data:
                    row.append('')  # Add empty cell for new column

            # Add new row if provided
            if row_data:
                row_data_list = row_data.split(',')
                while len(row_data_list) < len(columns):
                    row_data_list.append('')  # Add empty cells to match column count
                data.append(row_data_list)

            # Write updated CSV back to file
            with open(csv_file.file.path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)

            return redirect('view_csv', file_id=file_id)
    else:
        form = CSVUpdateForm()

    return render(request, 'viewCsv.html', {'data': data, 'columns': columns, 'file_id': file_id, 'form': form})


@login_required
def edit_csv_row(request, file_id, row_index):
    csv_file = get_object_or_404(CSVfiles, id=file_id, user=request.user)
    data = []
    columns = []

    with open(csv_file.file.path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
        if data:
            columns = data[0]

    # Handle form submission
    if request.method == 'POST':
        form = CSVUpdateForm(request.POST)
        if form.is_valid():
            row_data = form.cleaned_data['row_data']
            row_data_list = row_data.split(',')

            # Update the specified row
            while len(row_data_list) < len(columns):
                row_data_list.append('')  # Add empty cells to match column count
            data[row_index] = row_data_list

            # Write updated CSV back to file
            with open(csv_file.file.path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)

            return redirect('view_csv', file_id=file_id)
    else:
        initial_data = ','.join(data[row_index])
        form = CSVUpdateForm(initial={'row_data': initial_data})

    return render(request, 'edit_csv_row.html', {'columns': columns, 'file_id': file_id, 'form': form, 'row_index': row_index})

@login_required
def delete_csv(request, file_id):
    csv_file = get_object_or_404(CSVfiles, id=file_id, user=request.user)
    csv_file.delete()
    messages.success(request, 'CSV file deleted successfully.')
    return redirect('file_list')