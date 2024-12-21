# **PF Tracker Application Documentation**

This application manages Provident Fund (PF) data for employees and companies. It involves the following key components:
1. **Database Models**: Company, Employee, and PFPayment.
2. **Management Command**: A custom Django management command (fetchpfdata) to fetch and store PF data from Excel and XML files.
3. **Web Views**: Routes that handle requests to fetch PF data and display company and employee information.

---
![image](https://github.com/user-attachments/assets/7dcae44c-8b7e-4511-90f9-c311e43b917e)
![image](https://github.com/user-attachments/assets/a7a267c9-7432-434a-bda7-7ef213046025)
![image](https://github.com/user-attachments/assets/ca8f432c-182f-448d-9ef5-7ec7fc9f4fb7)
![image](https://github.com/user-attachments/assets/d0e2c0df-34f0-417c-8f1d-d8c3451ab4a4)





### **1. Application Setup**
The app is initialized using **Nanodjango**, which allows us to manage a lightweight Django-like application with minimal configuration. The settings define:
- **DATABASES**: Uses SQLite as the database backend.
- **INSTALLED_APPS**: Includes essential Django apps such as auth, admin, sessions, and staticfiles.
- **TEMPLATES**: Specifies the path to HTML templates.
- **STATICFILES_DIRS**: Specifies the directory for static files (CSS, JavaScript, etc.).

The app is initialized like this:

python
app = Django(
    DATABASES={...},
    INSTALLED_APPS=[...],
    TEMPLATES=[...],
    STATICFILES_DIRS=[...],
    STATIC_URL='/static/',
)


---

### **2. Models: Company, Employee, and PFPayment**
The application uses three models to structure the data:

- **Company**:
  Represents a company. It has attributes like:
  - name (company name)
  - registration_number (unique company identifier)
  - address (company address)
  - pf_account_number (PF account number, optional)

  The __str__() method ensures that when a Company object is printed, it shows the company's name.

- **Employee**:
  Represents an employee. It has:
  - company (ForeignKey to Company)
  - name (employee name)
  - pf_number (unique Provident Fund number)
  - date_of_joining (employee's joining date)

  The __str__() method returns the employee's name and PF number.

- **PFPayment**:
  Represents PF payment details for employees. It stores:
  - employee (ForeignKey to Employee)
  - month (payment month)
  - employee_contribution (employee's PF contribution)
  - employer_contribution (employer's PF contribution)
  - total_contribution (sum of both contributions)

  The save() method calculates the total_contribution by summing the employee's and employer's contributions.

---

### **3. Management Command: fetchpfdata**
The fetchpfdata command is responsible for fetching PF data from an Excel file (pf_sample.xlsx) and an XML file (pf_details.xml). It processes the data and populates the Company, Employee, and PFPayment models.

#### **Steps Involved:**
1. **Excel Data Processing**:
   - The Excel file is read using pandas:
     - **Company Data**: Fetches details like company name, registration number, and address.
     - **Employee Data**: Fetches details like employee name, PF number, joining date, and the company they belong to.
     - **Payment Data**: Fetches details of employee contributions and employer contributions for each month.
   
   - The get_or_create() method ensures that duplicate data is not inserted into the database.

2. **XML Data Processing**:
   - The XML file is parsed using the xml.etree.ElementTree library.
   - The data is iterated and processed in a similar manner to the Excel data.
   - The companies, employees, and payment data are extracted and stored in the corresponding models.

3. **Execution**:
   - To execute this management command, run nanodjango manage <script_name>.py fetchpfdata.
   - This command populates the database with data from both the Excel and XML files.

#### **Example of Command Execution**:
bash
nanodjango manage pf_tracker.py fetchpfdata


#### **Excel File Format**:
The Excel file is expected to have three sheets:
- **Company Data**: Contains company-related information.
- **Employee Data**: Contains employee details linked to companies.
- **Payment Data**: Contains PF contribution data for employees.

---

### **4. Web Views (Routes)**
The web application exposes several views (routes) for displaying the data:

#### **Home Page (/)**:
- Displays a list of all companies.
- home(request) retrieves all companies and renders them using the home.html template.

python
@app.route("/")
def home(request):
    companies = Company.objects.all()
    return render(request, 'home.html', {'companies': companies})


#### **Company Detail Page (/company/<int:company_id>/)**:
- Displays detailed information about a specific company, including the employees associated with that company.
- company_detail(request, company_id) retrieves the company and its employees by the company_id and renders the company_detail.html template.

python
@app.route("/company/<int:company_id>/")
def company_detail(request, company_id):
    company = Company.objects.get(id=company_id)
    employees = company.employees.all()
    return render(request, 'company_detail.html', {'company': company, 'employees': employees})


#### **Employee Detail Page (/employee/<int:employee_id>/)**:
- Displays detailed information about a specific employee, including their PF payments.
- employee_detail(request, employee_id) retrieves the employee and their payments by the employee_id and renders the employee_detail.html template.

python
@app.route("/employee/<int:employee_id>/")
def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    payments = employee.payments.all()
    return render(request, 'employee_detail.html', {'employee': employee, 'payments': payments})


#### **Fetch PF Data View (/fetch_pf/)**:
- This view manually triggers the process of fetching and storing PF data from the Excel file.
- When a user accesses this route, it:
  - Attempts to read and process the pf_sample.xlsx file.
  - Stores the data in the database.
  - Returns a JSON response with the success or failure status and any relevant messages.

python
@app.route("/fetch_pf/")
def fetch_pf_data_excel(request):
    messages = []
    success = True

    excel_file = os.path.join(os.getcwd(), 'pf_sample.xlsx')
    
    if os.path.exists(excel_file):
        try:
            # Process Excel data and update models
            ...
        except Exception as e:
            success = False
            messages.append(f"Error processing Excel file: {str(e)}")
    else:
        success = False
        messages.append("Excel file 'pf_sample.xlsx' not found.")

    return JsonResponse({
        'success': success,
        'messages': messages
    })


---

### **5. How the Database is Populated**
The database is populated in two primary ways:
1. **By Running the fetchpfdata Management Command**: This is done via the command line using python <fetchpfdata>.py . This command processes the Excel and XML files and stores the data in the Company, Employee, and PFPayment models.
2. **By Triggering the /fetch_pf/ View**: This view allows the user to fetch and store PF data directly from the pf_sample.xlsx Excel file. The data is processed in real-time and stored in the database.

---

### **6. How to Run the Application**
1. Ensure that the necessary files (pf_sample.xlsx and pf_details.xml) are present in the project directory.
2. Start the server:
   
bash
     uv run pf_tracker.py

   
bash
   nanodjango manage pf_tracker.py runserver

3. Open the browser and visit http://localhost:8000 to view the application.

To manually fetch and populate the database with PF data, visit http://localhost:8000/fetch_pf/ or run the management command nanodjango manage pf_tracker.py fetchpfdata.

---

### **Conclusion**
This application provides a simple interface to manage and view Provident Fund data for employees and companies. The process of populating the database with PF data is streamlined using management commands and views, making it easy to integrate and store data from external sources like Excel and XML files. add this new change for running management command in my docs #for running management command     
#RUN SCRIPT
# rest of script
# if __name__ == "__main__":
#     app._prepare()
#     command = fetchpfdata()
#     command.handle(arg1='value')
