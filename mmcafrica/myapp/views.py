from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, User, Tender, Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages

#LOGIN

def login_view(request):
    if request.method == "POST":
        Username = request.POST.get("Username")
        Password = request.POST.get("Password")

        user = authenticate(request, Username=Username, Password=Password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.Username}!")
            return redirect("home")  # change to your dashboard/home page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

def insertuser(request):
    if request.method == 'POST':
            Username = request.POST.get('Username')
            Email = request.POST.get('Email')
            Password = request.POST.get('Password')

            User.objects.create(
                Username=Username,
                Email=Email,
                Password=Password
            )
            return redirect('user_success')  # Redirect after POST
    return render(request, 'register.html')
def registered(request):
    return HttpResponse("Task created successfully!")


#home
def home_view(request):
    return render(request, 'home.html')
def invoices_view(request):
    return render(request, 'invoices.html')

#tasks
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date
        )

        return redirect('task_success')  # Redirect after POST
    return render(request, 'task_form.html')

def task_success(request):
    return HttpResponse("Task created successfully!")

#TENDERS
def tender_create(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            tender = Tender.objects.create(
                tender_name=request.POST.get("tender_name"),
                ref_no=request.POST.get("ref_no"),
                issue_date=request.POST.get("issue_date"),
                submission_date=request.POST.get("submission_date"),
                #assigned_to=request.POST.get("assigned_to"),
                status=request.POST.get("status"),
                comments=request.POST.get("comments"),
            )
            return JsonResponse({
                "success": True,
                "id": tender.id,
                "tender_name": tender.tender_name,
                "ref_no": tender.ref_no,
                "issue_date": tender.issue_date,
                "submission_date": tender.submission_date,
                #"assigned_to": tender.assigned_to,
                "status": tender.status,
                "comments": tender.comments or "",
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    tenders = Tender.objects.all()
    return render(request, "tenders/tender_form.html", {"tenders": tenders})

# CLIENTS

def client_create(request):
    # Handle AJAX POST request
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            client = Client.objects.create(
                client_name=request.POST.get("client_name"),
                project_name=request.POST.get("project_name"),
                client_year=request.POST.get("client_year"),
                contact_person=request.POST.get("contact_person"),
                email=request.POST.get("email"),
                phone_number=request.POST.get("phone_number"),
                client_image=request.FILES.get("client_image")
            )
            return JsonResponse({
                "success": True,
                "id": client.id,
                "client_name": client.client_name,
                "project_name": client.project_name,
                "client_year": client.client_year,
                "contact_person": client.contact_person,
                "email": client.email,
                "phone_number": client.phone_number,
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    # For GET request → load all clients
    clients = Client.objects.all()
    return render(request, "client.html", {"clients": clients})

#CLIENT DETAIL

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "client": {
                "client_name": client.client_name,
                "project_name": client.project_name,
                "client_year": client.client_year,
                "contact_person": client.contact_person,
                "email": client.email,
                "phone_number": client.phone_number,
                "client_image": client.client_image.url if client.client_image else None,
            }
        })
    return JsonResponse({"success": False, "error": "Invalid request"})

import csv
from django.http import HttpResponse
from .models import Client

# DOWNLOAD CLIENT LIST
def download_clients_csv(request):
    # Create the HttpResponse object with CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="clients.csv"'

    writer = csv.writer(response)
    # Write header row
    writer.writerow([
        "ID", "Client Name", "Project Name", "Year",
        "Contact Person", "Email", "Phone Number"
    ])

    # Write data rows
    for client in Client.objects.all():
        writer.writerow([
            client.id,
            client.client_name,
            client.project_name,
            client.client_year,
            client.contact_person,
            client.email,
            client.phone_number,
        ])

    return response


# TENDER DOWNLOAD
import io
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import Tender


def tender_export_excel(request):
    tenders = Tender.objects.all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Tenders"

    # Headers
    headers = ["#", "Tender Name", "Ref No.", "Issue Date", "Submission Date", "Assigned To", "Status", "Comments"]
    ws.append(headers)

    # Data
    for idx, t in enumerate(tenders, start=1):
        ws.append([
            idx,
            t.tender_name,
            t.ref_no,
            t.issue_date.strftime("%Y-%m-%d") if t.issue_date else "",
            t.submission_date.strftime("%Y-%m-%d") if t.submission_date else "",
            t.status,
            t.comments,
        ])

    # Response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="tenders.xlsx"'
    wb.save(response)
    return response


def tender_export_pdf(request):
    tenders = Tender.objects.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 50, "Tender List")

    p.setFont("Helvetica", 10)
    y = height - 100
    headers = ["#", "Tender Name", "Ref No.", "Issue Date", "Submission Date", "Assigned To", "Status", "Comments"]

    # Header row
    x_positions = [40, 70, 200, 280, 360, 450, 520, 580]
    for i, header in enumerate(headers):
        p.drawString(x_positions[i], y, header)
    y -= 20

    # Data rows
    for idx, t in enumerate(tenders, start=1):
        row = [
            str(idx),
            t.tender_name,
            t.ref_no,
            t.issue_date.strftime("%Y-%m-%d") if t.issue_date else "",
            t.submission_date.strftime("%Y-%m-%d") if t.submission_date else "",
            t.status,
            (t.comments[:15] + "...") if t.comments and len(t.comments) > 15 else (t.comments or ""),
        ]
        for i, col in enumerate(row):
            p.drawString(x_positions[i], y, str(col))
        y -= 20
        if y < 50:  # new page
            p.showPage()
            y = height - 100

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="tenders.pdf"'
    return response

#INVOICES
from .models import Invoice

# CREATE INVOICE
def invoice_create(request):
    # Handle AJAX POST request
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            invoice = Invoice.objects.create(
                invoice_no=request.POST.get("invoice_no"),
                client=request.POST.get("client"),
                project=request.POST.get("project"),
                amount=request.POST.get("amount"),
                status=request.POST.get("status"),
                due_date=request.POST.get("due_date"),
            )
            return JsonResponse({
                "success": True,
                "id": invoice.id,
                "invoice_no": invoice.invoice_no,
                "client": invoice.client,
                "project": invoice.project,
                "amount": str(invoice.amount),  # Decimal to string for JSON
                "status": invoice.status,
                "due_date": invoice.due_date.strftime("%Y-%m-%d"),
            })
        except Exception as e:
            # In your invoice_create view
            return JsonResponse({
                # ...
                "status": invoice.get_status_display(), # This returns "Fully Paid", "Partially Paid", etc.
                # ...
            })

    # For GET request → load all invoices
    invoices = Invoice.objects.all()
    return render(request, "invoices.html", {"invoices": invoices})


# INVOICE DETAIL
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "invoice": {
                "invoice_no": invoice.invoice_no,
                "client": invoice.client,
                "project": invoice.project,
                "amount": str(invoice.amount),
                "status": invoice.status,
                "due_date": invoice.due_date,
            }
        })
    return JsonResponse({"success": False, "error": "Invalid request"})
