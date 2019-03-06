from django import forms
from .models import Company
from .models import Employee
from .models import Department
from .models import Project
from .models import Issue
from .models import Subtask
from .models import WorkFlow
from .models import Plan

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'user',
            'c_id',
            'c_name',
            'c_email',
            'c_address',
            'c_phone',
            'role',
        ]

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [
            'e_id',
            'e_name',
            'e_surname',
            'e_password',
            'e_email',
            'e_phone',
            'e_degree',
            'e_salary',
            'role',
            'eCompany',
            'eDepartment',
            'Image',
            'active',
        ]
        
        
class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = [
            'd_id',
            'd_name',
            'd_capacity',
            'd_phone',
            'd_password',
            'dCompany',
        ]


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'p_id',
            'p_startdate',
            'p_enddate',
            'p_title',
            'p_situation',
            'cProject',
            'dProject',
            'eProject',
            'image',
        ]


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'i_id',
            'i_type',
            'i_extra',
            'i_content',
            'cIssue',
            'pIssue',
            'i_work',
            'i_work2',
        ]

class SubtaskForm(forms.ModelForm):

    class Meta:
        model = Subtask
        fields = [
            'sub_id',
            'sub_content',
            'sCompany',
            'iIssue',
            's_work',
        ]
class WorkflowForm(forms.ModelForm):

    class Meta:
        model = WorkFlow
        fields = [
            'w_id',
            'w_type',
            'w_date',
            'w_content',
        ]

class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = [
            'plan_id',
            'plan_type',
            'plan_date',
            'headMakes',
            'pPlan'
        ]
