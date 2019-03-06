from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from .models import Employee
from .forms import EmployeeForm
from .models import Department
from .forms import DepartmentForm
from .forms import Project
from .forms import ProjectForm
from .forms import Issue
from .forms import IssueForm
from .forms import Subtask
from .forms import SubtaskForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db import transaction, IntegrityError
from .models import Company
from .forms import CompanyForm
from .forms import WorkFlow
from .forms import WorkflowForm
from .forms import Plan
from .forms import PlanForm
from django.utils.text import slugify
#########################################################################

#########################################################################
def company_index(request):
    companys_list = Company.objects.all()
    query = request.GET.get('q')
    if query:
        companys_list = companys_list.filter(c_name__icontains=query)
    paginator = Paginator(companys_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        companys = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companys = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companys = paginator.page(paginator.num_pages)
    return render(request, 'company/index.html', {'companys': companys})
#########################################################################

@transaction.atomic
def company_update(request, c_id):
    companys = get_object_or_404(Company, c_id=c_id)
    form = CompanyForm(request.POST or None, instance=companys)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Company is updated, successfully!")
        return HttpResponseRedirect(companys.get_company_url())
    context = {
        'form': form,
    }
    return render(request, 'company/form.html', context)

#########################################################################
def company_detail(request, c_id):
    companys = get_object_or_404(Company, c_id=c_id)

    context = {
        'company': companys,
    }

    return render(request, 'company/detail.html', context)
#########################################################################
def company_delete(request, c_id):
    companys = get_object_or_404(Company, c_id=c_id)
    companys.delete()
    return redirect('app:indexC')

#########################################################################
def employee_index(request):
    employees_list = Employee.objects.filter(eCompany__c_name__contains=request.user)
    query = request.GET.get('q')
    if query:
        employees_list = employees_list.filter(
            Q(e_name__icontains=query) |
            Q(e_surname__icontains=query) |
            Q(eDepartment__icontains=query)
            ).distinct()
    paginator = Paginator(employees_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)
    return render(request, 'employee/index.html', {'employees': employees})


def employee_detail(request, e_slug):
    employees = get_object_or_404(Employee, e_slug=e_slug)
    context = {
        'employee': employees,
    }

    return render(request, 'employee/detail.html', context)

@transaction.atomic
def employee_create(request):

    # if request.method == "POST":
    #     Formdan gelen bilgileri kaydet
    #    form = EmployeeForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    # else:
    #    formu kullanıcıya göster
    #    form = EmployeeForm()

    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        try:
            with transaction.atomic():
                employees = form.save(commit=True)
                messages.success(request, "Employee is created, successfully!")
                return HttpResponseRedirect(employees.get_absolute_url())
        except IntegrityError:
            messages.ValidationError(request, "Employee is not created!")
    context = {
        'form': form,
    }
    return render(request, 'employee/form.html', context)

@transaction.non_atomic_requests
def employee_update(request, e_slug):
    employees = get_object_or_404(Employee, e_slug=e_slug)
    form = EmployeeForm(request.POST or None, instance=employees)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Employee is updated, successfully!")
        return HttpResponseRedirect(employees.get_update_url())
    context = {
        'form': form,
    }
    return render(request, 'employee/update.html', context)


def employee_delete(request, e_slug):
    employees = get_object_or_404(Employee, e_slug=e_slug)
    employees.delete()
    return redirect('app:index')
############################################################################

############################################################################
def department_index(request):
    departments_list = Department.objects.filter(dCompany__c_name__contains=request.user)
    query = request.GET.get('q')
    if query:
        departments_list = departments_list.filter(d_name__icontains=query)
    paginator = Paginator(departments_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        departments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        departments = paginator.page(paginator.num_pages)
    return render(request, 'department/index.html', {'departments': departments})


def department_detail(request, d_slug):
    departments = get_object_or_404(Department, d_slug=d_slug)

    context = {
        'department': departments,
    }

    return render(request, 'department/detail.html', context)

@transaction.atomic
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        try:
            with transaction.atomic():
                departments = form.save(commit=True)
                messages.success(request, "Department is created, successfully!")
                return HttpResponseRedirect(departments.get_department_url())
        except IntegrityError:
            messages.ValidationError(request, "Department is not created!")


    context = {
        'form': form,
    }
    return render(request, 'department/form.html', context)

@transaction.non_atomic_requests
def department_update(request, d_slug):
    departments = get_object_or_404(Department, d_slug=d_slug)
    form = DepartmentForm(request.POST or None, instance=departments)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Department is updated, successfully!")
        return HttpResponseRedirect(departments.get_updateD_url())
    context = {
        'form': form,
    }
    return render(request, 'department/update.html', context)


def department_delete(request, d_slug):
    departments = get_object_or_404(Department, d_slug=d_slug)
    departments.delete()
    return redirect('app:indexD')
###########################################################################

###########################################################################
def project_index(request):
    projects_list = Project.objects.filter(cProject__c_name__contains=request.user)
    query = request.GET.get('q')
    if query:
        projects_list = projects_list.filter(p_title__icontains=query)
    paginator = Paginator(projects_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)
    return render(request, 'project/index.html', {'projects': projects})


def project_detail(request, p_slug):
    projects = get_object_or_404(Project, p_slug=p_slug)
    context = {
        'project': projects,
    }

    return render(request, 'project/detail.html', context)

@transaction.atomic
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        projects = form.save(commit=True)
        messages.success(request, "Project is created, successfully!")
        return HttpResponseRedirect(projects.get_project_url())
    context = {
        'form': form,
    }
    return render(request, 'project/form.html', context)

@transaction.non_atomic_requests
def project_update(request, p_slug):
    projects = get_object_or_404(Project, p_slug=p_slug)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=projects)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Project is updated, successfully!")
        return HttpResponseRedirect(projects.get_project_url())
    context = {
        'form': form,
    }
    return render(request, 'project/update.html', context)


def project_delete(request, p_slug):
    projects = get_object_or_404(Project, p_slug=p_slug)
    projects.delete()
    return redirect('app:indexP')
##########################################################################

##########################################################################
def issue_index(request):
    issues_list = Issue.objects.filter(cIssue__c_name__contains=request.user)
    query = request.GET.get('q')
    if query:
        issues_list = issues_list.filter(i_id__icontains=query)
    paginator = Paginator(issues_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        issues = paginator.page(paginator.num_pages)
    return render(request, 'issue/index.html', {'issues': issues})


def issue_detail(request, id):
    issues = get_object_or_404(Issue, i_id=id)
    context = {
        'issue': issues,
    }

    return render(request, 'issue/detail.html', context)

@transaction.atomic
def issue_create(request):
    form = IssueForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        issues = form.save(commit=True)
        messages.success(request, "Issue is created, successfully!")
        return HttpResponseRedirect(issues.get_issue_url())
    context = {
        'form': form,
    }
    return render(request, 'issue/form.html', context)

@transaction.non_atomic_requests
def issue_update(request, id):
    issues = get_object_or_404(Issue, i_id=id)
    form = IssueForm(request.POST or None, request.FILES or None, instance=issues)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Issue is updated, successfully!")
        return HttpResponseRedirect(issues.get_issue_url())
    context = {
        'form': form,
    }
    return render(request, 'issue/update.html', context)


def issue_delete(request, id):
    issues = get_object_or_404(Issue, i_id=id)
    issues.delete()
    return redirect('app:indexI')
##############################################################################

##############################################################################
def subtask_index(request):
    subtasks_list = Subtask.objects.filter(sCompany__c_name__contains=request.user)
    query = request.GET.get('q')
    if query:
        subtasks_list = subtasks_list.filter(sub_id__icontains=query)
    paginator = Paginator(subtasks_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        subtasks = paginator.page(page)
    except PageNotAnInteger:
        subtasks = paginator.page(1)
    except EmptyPage:
        subtasks = paginator.page(paginator.num_pages)
    return render(request, 'subtask/index.html', {'subtasks': subtasks})


def subtask_detail(request, id):
    subtasks = get_object_or_404(Subtask, sub_id=id)
    context = {
        'subtask': subtasks,
    }

    return render(request, 'subtask/detail.html', context)

@transaction.atomic
def subtask_create(request):
    form = SubtaskForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        subtasks = form.save()
        messages.success(request, "Subtask is created, successfully!")
        return HttpResponseRedirect(subtasks.get_subtask_url())
    context = {
        'form': form,
    }
    return render(request, 'subtask/form.html', context)

@transaction.non_atomic_requests
def subtask_update(request, id):
    subtasks = get_object_or_404(Subtask, sub_id=id)
    form = SubtaskForm(request.POST or None, request.FILES or None, instance=subtasks)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, "Subtask is updated, successfully!")
        return HttpResponseRedirect(subtasks.get_subtask_url())
    context = {
        'form': form,
    }
    return render(request, 'subtask/update.html', context)


def subtask_delete(request, id):
    subtasks = get_object_or_404(Subtask, sub_id=id)
    subtasks.delete()
    return redirect('app:indexSub')
#############################################################################

#############################################################################
def head_index(request):
    employees_list = Employee.objects.filter(eCompany__c_name__contains=request.user, role__contains='Head')
    query = request.GET.get('q')
    if query:
        employees_list = employees_list.filter(
            Q(e_name__icontains=query) |
            Q(e_surname__icontains=query) |
            Q(eDepartment__icontains=query)
            ).distinct()
    paginator = Paginator(employees_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)
    return render(request, 'employee/index.html', {'employees': employees})
#############################################################################

#############################################################################
def other_index(request):
    employees_list = Employee.objects.filter(eCompany__c_name__contains=request.user, role='Other')
    query = request.GET.get('q')
    if query:
        employees_list = employees_list.filter(
            Q(e_name__icontains=query) |
            Q(e_surname__icontains=query) |
            Q(eDepartment__icontains=query)
            ).distinct()
    paginator = Paginator(employees_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)
    return render(request, 'employee/index.html', {'employees': employees})
############################################################################

#########################################################################
def companyuser_index(request):
    companys_list = Company.objects.filter(role='Company')
    query = request.GET.get('q')
    if query:
        companys_list = companys_list.filter(c_name__icontains=query)
    paginator = Paginator(companys_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        companys = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companys = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companys = paginator.page(paginator.num_pages)
    return render(request, 'company/index.html', {'companys': companys})
#########################################################################
#########################################################################
def companyuser2_index(request):
    companys_list = Company.objects.filter(role='Company')
    query = request.GET.get('q')
    if query:
        companys_list = companys_list.filter(c_name__icontains=query)
    paginator = Paginator(companys_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        companys = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companys = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companys = paginator.page(paginator.num_pages)
    return render(request, 'company/indexuser.html', {'companys': companys})
#########################################################################

#########################################################################
def customeruser_index(request):
    companys_list = Company.objects.filter(role='Customer')
    query = request.GET.get('q')
    if query:
        companys_list = companys_list.filter(c_name__icontains=query)
    paginator = Paginator(companys_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        companys = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companys = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companys = paginator.page(paginator.num_pages)
    return render(request, 'company/index.html', {'companys': companys})
#########################################################################

############################################################################
def company_view(request):
    #return HttpResponse('<b>Welcome</b>')
    return render(request, 'company/company.html', {})
############################################################################

############################################################################
def customer_view(request):
    #return HttpResponse('<b>Welcome</b>')
    return render(request, 'customer/customer.html', {})
############################################################################

############################################################################
def admin_view(request):
    #return HttpResponse('<b>Welcome</b>')
    return render(request, 'admin/admin.html', {})
############################################################################
def projectC_index(request):
    projects_list = Project.objects.all()
    query = request.GET.get('q')
    if query:
        projects_list = projects_list.filter(p_title__icontains=query)
    paginator = Paginator(projects_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)
    return render(request, 'project/projectC.html', {'projects': projects})
############################################################################

##############################################################################

def workflow_index(request):
    workflows_list = WorkFlow.objects.all()
    query = request.GET.get('q')
    if query:
        workflows_list = workflows_list.filter(w_id__icontains=query)
    paginator = Paginator(workflows_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        workflows = paginator.page(page)
    except PageNotAnInteger:
        workflows = paginator.page(1)
    except EmptyPage:
        workflows = paginator.page(paginator.num_pages)
    return render(request, 'workflow/index.html', {'workflows': workflows})


def workflow_detail(request, id):
    workflows = get_object_or_404(WorkFlow, w_id=id)
    context = {
        'workflow': workflows,
    }

    return render(request, 'workflow/detail.html', context)


def workflow_create(request):
    form = WorkflowForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        workflows = form.save()
        messages.success(request, "Workflow is created, successfully!")
        return HttpResponseRedirect(workflows.get_workflow_url())
    context = {
        'form': form,
    }
    return render(request, 'workflow/form.html', context)


def workflow_update(request, id):
    workflows = get_object_or_404(WorkFlow, w_id=id)
    form = WorkflowForm(request.POST or None, request.FILES or None, instance=workflows)
    if form.is_valid():
        messages.success(request, "Workflow is updated, successfully!")
        return HttpResponseRedirect(workflows.get_workflow_url())
    context = {
        'form': form,
    }
    return render(request, 'workflow/update.html', context)


def workflow_delete(request, id):
    workflows = get_object_or_404(WorkFlow, w_id=id)
    workflows.delete()
    return redirect('app:indexW')
#############################################################################

##############################################################################

def plan_index(request):
    plans_list = Plan.objects.all()
    query = request.GET.get('q')
    if query:
        plans_list = plans_list.filter(plan_id__icontains=query)
    paginator = Paginator(plans_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        plans = paginator.page(page)
    except PageNotAnInteger:
        plans = paginator.page(1)
    except EmptyPage:
        plans = paginator.page(paginator.num_pages)
    return render(request, 'plan/index.html', {'plans': plans})


def plan_detail(request, id):
    plans = get_object_or_404(Plan, plan_id=id)
    context = {
        'plan': plans,
    }

    return render(request, 'plan/detail.html', context)


def plan_create(request):
    form = PlanForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        plans = form.save()
        messages.success(request, "Project Plan is created, successfully!")
        return HttpResponseRedirect(plans.get_plan_url())
    context = {
        'form': form,
    }
    return render(request, 'plan/form.html', context)


def plan_update(request, id):
    plans = get_object_or_404(Plan, plan_id=id)
    form = PlanForm(request.POST or None, request.FILES or None, instance=plans)
    if form.is_valid():
        messages.success(request, "Project Plan is updated, successfully!")
        return HttpResponseRedirect(plans.get_plan_url())
    context = {
        'form': form,
    }
    return render(request, 'plan/update.html', context)


def plan_delete(request, id):
    plans = get_object_or_404(Plan, plan_id=id)
    plans.delete()
    return redirect('app:indexPlan')
#############################################################################


############################################################################
def setting_view(request):
    #return HttpResponse('<b>Welcome</b>')
    return render(request, 'settings/settings.html', {})
#############################################################################

#############################################################################
def projectC_delete(request, p_slug):
    projects = get_object_or_404(Project, p_slug=p_slug)
    projects.delete()
    return redirect('app:projectP')
