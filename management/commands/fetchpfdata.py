import os
import pandas as pd
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from ...pf_tracker import Company, Employee, PFPayment

class Command(BaseCommand):
    help = 'Fetch and store PF details from Excel and XML'

    def handle(self, *args, **options):
        # Fetch data from Excel
        excel_file = os.path.join(os.getcwd(), 'pf_sample.xlsx')
        if os.path.exists(excel_file):
            company_data = pd.read_excel(excel_file, sheet_name='Company Data')
            employee_data = pd.read_excel(excel_file, sheet_name='Employee Data')
            payment_data = pd.read_excel(excel_file, sheet_name='Payment Data')

            # Process Company Data
            for _, row in company_data.iterrows():
                Company.objects.get_or_create(
                    registration_number=row['Registration Number'],
                    defaults={
                        'name': row['Company Name'],
                        'address': row['Address']
                    }
                )

            # Process Employee Data
            for _, row in employee_data.iterrows():
                company = Company.objects.get(registration_number=row['Company Registration Number'])
                Employee.objects.get_or_create(
                    pf_number=row['PF Number'],
                    defaults={
                        'name': row['Employee Name'],
                        'company': company,
                        'date_of_joining': pd.to_datetime(row['Date of Joining']).date()
                    }
                )

            # Process Payment Data
            for _, row in payment_data.iterrows():
                employee = Employee.objects.get(pf_number=row['PF Number'])
                PFPayment.objects.get_or_create(
                    employee=employee,
                    month=pd.to_datetime(row['Month']).date(),
                    defaults={
                        'employee_contribution': row['Employee Contribution'],
                        'employer_contribution': row['Employer Contribution']
                    }
                )

        # Fetch data from XML
        xml_file = os.path.join(os.getcwd(), 'pf_details.xml')
        if os.path.exists(xml_file):
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for company_elem in root.findall('Company'):
                company, _ = Company.objects.get_or_create(
                    registration_number=company_elem.find('RegistrationNumber').text,
                    defaults={
                        'name': company_elem.find('Name').text,
                        'address': company_elem.find('Address').text,
                    }
                )

                for employee_elem in company_elem.findall('Employee'):
                    employee, _ = Employee.objects.get_or_create(
                        pf_number=employee_elem.find('PFNumber').text,
                        defaults={
                            'name': employee_elem.find('Name').text,
                            'company': company,
                            'date_of_joining': employee_elem.find('DateOfJoining').text,
                        }
                    )

                    for payment_elem in employee_elem.findall('Payment'):
                        PFPayment.objects.get_or_create(
                            employee=employee,
                            month=payment_elem.find('Month').text,
                            defaults={
                                'employee_contribution': float(payment_elem.find('EmployeeContribution').text),
                                'employer_contribution': float(payment_elem.find('EmployerContribution').text),
                            }
                        )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored PF data from Excel and XML'))