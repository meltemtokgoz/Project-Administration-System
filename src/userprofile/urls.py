from django.conf.urls import url
from .views import *

app_name = 'app'

urlpatterns = [

    ######################################################################
    url(r'^home/$', company_view, name='homeC'),
    ######################################################################

    ######################################################################
    url(r'^homeCustomer/$', customer_view, name='homeCu'),
    ######################################################################

    ######################################################################
    url(r'^homeAdmin/$', admin_view, name='homeA'),
    ######################################################################

    ######################################################################
    url(r'^settings/$', setting_view, name='settings'),
    ######################################################################

    ######################################################################
    url(r'^companys/$', company_index, name='indexC'),
    url(r'^(?P<c_id>\d+)/detailCompany/$', company_detail, name='detailCompany'),
    url(r'^(?P<c_id>\d+)/updateCompany/$', company_update, name='updateCompany'),
    url(r'^(?P<c_id>\d+)/deleteCompany/$', company_delete, name='deleteCompany'),
    ######################################################################

    ######################################################################
    url(r'^employees/$', employee_index, name='index'),
    url(r'^employee/add/$', employee_create, name='create'),
    url(r'^(?P<e_slug>[\w-]+)/detail/$', employee_detail, name='detail'),
    url(r'^(?P<e_slug>[\w-]+)/update/$', employee_update, name='update'),
    url(r'^(?P<e_slug>[\w-]+)/delete/$', employee_delete, name='delete'),
    ######################################################################

    ######################################################################
    url(r'^heads/$', head_index, name='indexH'),
    ######################################################################

    ######################################################################
    url(r'^others/$', other_index, name='indexO'),
    ######################################################################

    ######################################################################
    url(r'^companyuser/$', companyuser_index, name='companyuser'),
    ######################################################################

    ######################################################################
    url(r'^companyuser2/$', companyuser2_index, name='companyuser2'),
    ######################################################################

    ######################################################################
    url(r'^customeruser/$', customeruser_index, name='customeruser'),
    ######################################################################

    ######################################################################
    url(r'^departments/$', department_index, name='indexD'),
    url(r'^department/add/$', department_create, name='createD'),
    url(r'^(?P<d_slug>[\w-]+)/detailD/$', department_detail, name='detailD'),
    url(r'^(?P<d_slug>[\w-]+)/updateD/$', department_update, name='updateD'),
    url(r'^(?P<d_slug>[\w-]+)/deleteD/$', department_delete, name='deleteD'),
    #######################################################################

    #######################################################################
    url(r'^projects/$', project_index, name='indexP'),
    url(r'^project/add/$', project_create, name='createP'),
    url(r'^(?P<p_slug>[\w-]+)/detailP/$', project_detail, name='detailP'),
    url(r'^(?P<p_slug>[\w-]+)/updateP/$', project_update, name='updateP'),
    url(r'^(?P<p_slug>[\w-]+)/deleteP/$', project_delete, name='deleteP'),
    url(r'^projectP/$', projectC_index, name='projectP'),
    url(r'^(?P<p_slug>[\w-]+)/deletePC/$', projectC_delete, name='deletePC'),
    #######################################################################

    #######################################################################
    url(r'^issues/$', issue_index, name='indexI'),
    url(r'^issue/add/$', issue_create, name='createI'),
    url(r'^(?P<id>\d+)/detailI/$', issue_detail, name='detailI'),
    url(r'^(?P<id>\d+)/updateI/$', issue_update, name='updateI'),
    url(r'^(?P<id>\d+)/deleteI/$', issue_delete, name='deleteI'),
    #######################################################################

    #######################################################################
    url(r'^subtasks/$', subtask_index, name='indexSub'),
    url(r'^subtask/add/$', subtask_create, name='createSub'),
    url(r'^(?P<id>\d+)/detailSub/$', subtask_detail, name='detailSub'),
    url(r'^(?P<id>\d+)/updateSub/$', subtask_update, name='updateSub'),
    url(r'^(?P<id>\d+)/deleteSub/$', subtask_delete, name='deleteSub'),
    #######################################################################

    #######################################################################
    url(r'^workflows/$', workflow_index, name='indexW'),
    url(r'^workflow/add/$', workflow_create, name='createW'),
    url(r'^(?P<id>\d+)/detailW/$', workflow_detail, name='detailW'),
    url(r'^(?P<id>\d+)/updateW/$', workflow_update, name='updateW'),
    url(r'^(?P<id>\d+)/deleteW/$', workflow_delete, name='deleteW'),
    #######################################################################

    #######################################################################
    url(r'^plans/$', plan_index, name='indexPlan'),
    url(r'^plan/add/$', plan_create, name='createPlan'),
    url(r'^(?P<id>\d+)/detailPlan/$', plan_detail, name='detailPlan'),
    url(r'^(?P<id>\d+)/updatePlan/$', plan_update, name='updatePlan'),
    url(r'^(?P<id>\d+)/deletePlan/$', plan_delete, name='deletePlan'),
    #######################################################################
]
