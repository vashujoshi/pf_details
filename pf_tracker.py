import os
from django.db import models
from django.core.management.base import BaseCommand
from django.shortcuts import render
from nanodjango import Django

# Initialize nanodjango app
app = Django(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'pf_tracker.db',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        'django.contrib.admin',  # Admin functionality
        'django.contrib.auth',  # Required for permissions and users
        'django.contrib.sessions',  # Session management
        'django.contrib.messages',  # Required for messages framework
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'templates')],  # Path to templates folder
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',  # Required for messages
                ],
            },
        }
    ],
    STATICFILES_DIRS=[
        os.path.join(os.getcwd(), 'static'),
    ],
    STATIC_URL='/static/',  # Specify static URL
)

# Models
@app.admin
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    hello = models.TextField(blank=True)

    def __str__(self):
        return self.name

@app.admin
class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=200)
    pf_number = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.pf_number})"

@app.admin
class PFPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payments')
    month = models.DateField()
    employee_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    employer_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    total_contribution = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('employee', 'month')

    def save(self, *args, **kwargs):
        self.total_contribution = self.employee_contribution + self.employer_contribution
        super().save(*args, **kwargs)


# Management Command for PF Data Fetching
class Command(BaseCommand):
    help = 'Fetch and store PF data from a hypothetical API'

    def handle(self, *args, **options):
        # Simulated data fetching
        sample_data = [
            {
                'company': {
                    'name': 'Tech Innovations Pvt Ltd',
                    'registration_number': 'COMP12345',
                    'address': '123 Tech Park, Bangalore'
                },
                'employees': [
                    {
                        'name': 'John Doe',
                        'pf_number': 'PF98765',
                        'date_of_joining': '2020-01-15',
                        'payments': [
                            {
                                'month': '2024-01-01',
                                'employee_contribution': 1500,
                                'employer_contribution': 1500
                            }
                        ]
                    }
                ]
            }
        ]

        for company_data in sample_data:
            company, _ = Company.objects.get_or_create(
                registration_number=company_data['company']['registration_number'],
                defaults=company_data['company']
            )

            for emp_data in company_data['employees']:
                employee, _ = Employee.objects.get_or_create(
                    pf_number=emp_data['pf_number'],
                    defaults={
                        'name': emp_data['name'],
                        'company': company,
                        'date_of_joining': emp_data['date_of_joining']
                    }
                )

                for payment_data in emp_data['payments']:
                    PFPayment.objects.get_or_create(
                        employee=employee,
                        month=payment_data['month'],
                        defaults={
                            'employee_contribution': payment_data['employee_contribution'],
                            'employer_contribution': payment_data['employer_contribution']
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored PF data'))

# Web Views
@app.route("/")
def home(request):
    companies = Company.objects.all()
    return render(request, 'home.html', {'companies': companies})

@app.route("/company/<int:company_id>/")
def company_detail(request, company_id):
    company = Company.objects.get(id=company_id)
    employees = company.employees.all()
    return render(request, 'company_detail.html', {'company': company, 'employees': employees})

@app.route("/employee/<int:employee_id>/")
def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    payments = employee.payments.all()
    return render(request, 'employee_detail.html', {'employee': employee, 'payments': payments})

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0:8000")
