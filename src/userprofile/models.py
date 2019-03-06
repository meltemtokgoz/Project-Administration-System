from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

################################################################################
class CompanyQuerySet(models.QuerySet):
    def Companys(self):
        return self.filter(role='Company')

    def Customers(self):
        return self.filter(role='Customer')
#############################################################################

#############################################################################
class CompanyManager(models.Manager):
     def get_queryset(self):
         return super(CompanyManager, self).get_queryset().filter(active=True)
###############################################################################

###############################################################################
class CustomerUser(models.Manager):
    def get_queryset(self):
        return super(CustomerUser, self).get_queryset().filter(role='Customer')
    #eOther = models.ForeignKey(Employee, unique=True, primary_key=True, serialize=False, verbose_name='Employee')
################################################################################

################################################################################
class CompanyUser(models.Manager):
    def get_queryset(self):
        return super(CompanyUser, self).get_queryset().filter(role='Company')
################################################################################

class Company(models.Model):
    roles_choices = (
        ("Customer", "Customer"),
        ("Company", "Company"),
    )
    user = models.OneToOneField(User)
    c_id = models.AutoField(primary_key=True, verbose_name='User ID')
    c_name = models.CharField(max_length=30, verbose_name='User Name')
    c_email = models.EmailField(verbose_name='User E-mail')
    c_address = RichTextField(verbose_name='User Address')
    c_phone = models.CharField(max_length=20, verbose_name = 'User Phone')
    c_password = models.CharField(max_length=6,  verbose_name='User Password')
    role = models.CharField(max_length=30, choices=roles_choices, default="Customer")
    objects = models.Manager()
    all_employees = CompanyManager()
    Companys = CompanyUser()
    Customers = CustomerUser()

    def __str__(self):
        return self.c_name

    def get_company_url(self):
        return reverse('app:detailCompany', kwargs={'c_id': self.c_id})

    def get_updateC_url(self):
        return reverse('app:updateCompany', kwargs={'c_id': self.c_id})

    def get_deleteC_url(self):
        return reverse('app:deleteCompany', kwargs={'c_id': self.c_id})

    class Meta:
        ordering = ['user','c_name']

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Company.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)
#################################################################################

#################################################################################
class Department(models.Model):
    d_id = models.AutoField(primary_key=True, verbose_name='Department ID')
    d_name = models.CharField(max_length=30, verbose_name='Department Name')
    d_capacity = models.IntegerField(verbose_name='Department Capacity')
    d_phone = models.IntegerField(verbose_name='Department Phone')
    d_password = models.CharField(max_length=6, verbose_name='Department Password')
    dCompany = models.ForeignKey(Company, verbose_name='Company Name')
    d_slug = models.SlugField(unique=True,editable=False, max_length=130)

    def __str__(self):
        return self.d_name

    def get_department_url(self):
        return reverse('app:detailD', kwargs={'d_slug': self.d_slug})

    def get_createD_url(self):
        return reverse('app:createD')

    def get_updateD_url(self):
        return reverse('app:updateD', kwargs={'d_slug': self.d_slug})

    def get_deleteD_url(self):
        return reverse('app:deleteD', kwargs={'d_slug': self.d_slug})

    def get_unique_D_slug(self):
        d_slug = slugify(self.d_name.replace('ı', 'i'))
        unique_slug = d_slug
        counter = 1
        while Department.objects.filter(d_slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(d_slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.d_slug = self.get_unique_D_slug()
        return super(Department, self).save(*args, **kwargs)

    class Meta:
        ordering = ['dCompany']
#############################################################################

#############################################################################
class EmployeeQuerySet(models.QuerySet):
    def heads(self):
        return self.filter(role='Head')

    def others(self):
        return self.filter(role='Other')
#############################################################################

#############################################################################
class EmployeeManager(models.Manager):
     def get_queryset(self):
         return super(EmployeeManager, self).get_queryset().filter(active=True)
###############################################################################

###############################################################################
class Other(models.Manager):
    def get_queryset(self):
        return super(Other, self).get_queryset().filter(role='Other')
    #eOther = models.ForeignKey(Employee, unique=True, primary_key=True, serialize=False, verbose_name='Employee')
################################################################################

################################################################################
class Head(models.Manager):
    def get_queryset(self):
        return super(Head, self).get_queryset().filter(role='Head')
################################################################################

################################################################################
class Employee(models.Model):
    roles_choices = (
        ("Head", "head"),
        ("Other", "other"),
    )
    e_id = models.AutoField(primary_key=True, serialize=False, verbose_name='Employee ID')
    e_name = models.CharField(max_length=30, verbose_name='Name')
    e_surname = models.CharField(max_length=30, verbose_name='Surname')
    e_password = models.CharField(max_length=6, verbose_name='Password')
    e_email = models.EmailField(verbose_name='Email')
    e_phone = models.IntegerField(verbose_name='Phone')
    e_degree = models.IntegerField(verbose_name='Degree')
    e_salary = models.IntegerField(verbose_name='Salary')
    role = models.CharField(max_length=30, choices=roles_choices, default="Other")
    eDepartment = models.ForeignKey(Department, verbose_name="Department Name")
    eCompany = models.ForeignKey(Company, verbose_name="Company Name")
    Image = models.ImageField(null=True, blank=True)
    e_slug = models.SlugField(unique=True,editable=False, max_length=130)
    active = models.BooleanField(default=True)
    objects = models.Manager()
    all_employees = EmployeeManager()
    heads=Head()
    others=Other()

    def __str__(self):
        return "{} {}".format(self.e_name, self.e_surname)

    def get_absolute_url(self):
        return reverse('app:detail', kwargs={'e_slug': self.e_slug})

    def get_create_url(self):
        return reverse('app:create')

    def get_update_url(self):
        return reverse('app:update', kwargs={'e_slug': self.e_slug})

    def get_delete_url(self):
        return reverse('app:delete', kwargs={'e_slug': self.e_slug})

    def get_unique_E_slug(self):
        e_slug = slugify(self.e_name.replace('ı', 'i'))
        unique_slug = e_slug
        counter = 1
        while Employee.objects.filter(e_slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(e_slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.e_slug = self.get_unique_E_slug()
        return super(Employee, self).save(*args, **kwargs)

    class Meta:
        ordering = ['eCompany', 'eDepartment', '-e_degree']
###################################################################################

###################################################################################
class Project(models.Model):
    p_id = models.AutoField(primary_key=True, verbose_name='Project ID')
    p_startdate = models.DateTimeField(verbose_name='Project Start Date')
    p_enddate = models.DateTimeField(verbose_name='Project End Date')
    p_title = models.CharField(max_length=75, verbose_name='Project Title')
    p_situation = models.CharField(max_length=20, verbose_name='Project Situation')
    cProject = models.ForeignKey(Company, verbose_name='Company Name')
    dProject = models.ForeignKey(Department, verbose_name='Department Name')
    eProject = models.ForeignKey(Employee, null=True, related_name='eProject', verbose_name='Project Manager')
    sProject = models.ForeignKey(Employee, null=True, related_name='sProject')
    image = models.ImageField(null=True, blank=True)
    p_slug = models.SlugField(unique=True,editable=False, max_length=130)

    def __str__(self):
        return self.p_title

    def get_project_url(self):
        return reverse('app:detailP', kwargs={'p_slug': self.p_slug})

    def get_createP_url(self):
        return reverse('app:createP')

    def get_updateP_url(self):
        return reverse('app:updateP', kwargs={'p_slug': self.p_slug})

    def get_deleteP_url(self):
        return reverse('app:deleteP', kwargs={'p_slug': self.p_slug})

    def get_deletePC_url(self):
        return reverse('app:deletePC', kwargs={'p_slug': self.p_slug})

    def get_unique_P_slug(self):
        p_slug = slugify(self.p_title.replace('ı', 'i'))
        unique_slug = p_slug
        counter = 1
        while Project.objects.filter(p_slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(p_slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.p_slug = self.get_unique_P_slug()
        return super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['p_enddate']
###################################################################################

####################################################################################
class Issue(models.Model):
    i_id = models.AutoField(unique=True, primary_key=True, verbose_name='Issue ID')
    i_type = models.CharField(max_length=30, verbose_name='Issue Type')
    i_extra = RichTextField(verbose_name='Issue Notes')
    i_content = RichTextField(verbose_name='Issue Content')
    cIssue = models.ForeignKey(Company, verbose_name='Company Name')
    pIssue = models.ForeignKey(Project, verbose_name='Project Name')
    i_work = models.ForeignKey(Employee, null=True, related_name='i_work', verbose_name='Assign Employee 1')
    i_work2 = models.ForeignKey(Employee, blank=True, related_name='i_work2', verbose_name='Assign Employee 2')
    def __str__(self):
        return self.i_type

    def get_issue_url(self):
        return reverse('app:detailI', kwargs={'id': self.i_id})

    def get_createI_url(self):
        return reverse('app:createI')

    def get_updateI_url(self):
        return reverse('app:updateI', kwargs={'id': self.i_id})

    def get_deleteI_url(self):
        return reverse('app:deleteI', kwargs={'id': self.i_id})

    class Meta:
        ordering = ['i_id','pIssue']
#######################################################################################

#######################################################################################
class Subtask(models.Model):
    sub_id = models.AutoField(unique=True, primary_key=True, verbose_name='Subtask ID')
    sub_content = RichTextField(verbose_name='Subtask Content')
    sCompany = models.ForeignKey(Company, verbose_name='Company Name')
    iIssue = models.ForeignKey(Issue, verbose_name='Issue ID')
    s_work = models.ForeignKey(Employee, verbose_name='Assign Employee')

    def __str__(self):
        return self.sub_id

    def get_subtask_url(self):
        return reverse('app:detailSub', kwargs={'id': self.sub_id})

    def get_createSub_url(self):
        return reverse('app:createSub')

    def get_updateSub_url(self):
        return reverse('app:updateSub', kwargs={'id': self.sub_id})

    def get_deleteSub_url(self):
        return reverse('app:deleteSub', kwargs={'id': self.sub_id})

    class Meta:
        ordering = ['sub_id','iIssue']
#########################################################################################

#########################################################################################
class Plan(models.Model):
    plan_id = models.AutoField(unique=True, primary_key=True, verbose_name='Plan ID')
    plan_type = models.CharField(max_length=30, verbose_name='Plan Type')
    plan_date = models.DateTimeField(verbose_name='Plan Date')
    headMakes = models.ForeignKey(Employee, verbose_name='Employee ID')
    pPlan = models.ForeignKey(Project, verbose_name='Project ID')

    def __str__(self):
        return self.plan_id

    def get_plan_url(self):
        return reverse('app:detailPlan', kwargs={'id': self.plan_id})

    def get_createPlan_url(self):
        return reverse('app:createPlan')

    def get_updatePlan_url(self):
        return reverse('app:updatePlan', kwargs={'id': self.plan_id})

    def get_deletePlan_url(self):
        return reverse('app:deletePlan', kwargs={'id': self.plan_id})

    class Meta:
        ordering = ['plan_id','plan_type']
##########################################################################################

##########################################################################################
class WorkFlow(models.Model):
    w_id = models.AutoField(primary_key=True, verbose_name='Workflow ID')
    w_type = models.CharField(max_length=30, verbose_name='Workflow Type')
    w_date = models.DateTimeField(verbose_name='Workflow Date')
    w_content = RichTextField(verbose_name='Workflow')
    def __str__(self):
        return self.w_id

    def get_workflow_url(self):
        return reverse('app:detailW', kwargs={'id': self.w_id})

    def get_createW_url(self):
        return reverse('app:createW')

    def get_updateW_url(self):
        return reverse('app:updateW', kwargs={'id': self.w_id})

    def get_deleteW_url(self):
        return reverse('app:deleteW', kwargs={'id': self.w_id})

    class Meta:
        ordering = ['w_id','w_type']

##########################################################################################

##########################################################################################
class Report(models.Model):
    r_type = models.CharField(max_length=30, verbose_name='Report Type')
    r_version = models.CharField(max_length=5, verbose_name="Report Version")
    r_createdate = models.DateTimeField(verbose_name='Report Create Date')
    pReport = models.ForeignKey(Project, verbose_name='Project ID')
    oReport = models.ForeignKey(Employee, verbose_name='Prepare Employee ID')
###########################################################################################
