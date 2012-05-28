from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from mainsite import settings
from mainsite.users.views import registration_page_view, login, logout, Profile
from mainsite.Assignment.views import dashboard, CreateAssignment, AddQuestion, EditAssignment, PreviewAssignment, DeleteAssignment, SolveAssignment, ModifyAssignment, DeleteFile
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^register/$', registration_page_view),
    ('^$', login),
    ('^login/$', login),
    ('^logout/$', logout),
    ('^dashboard/$', dashboard),
    ('^assignment/create/$', CreateAssignment),
    (r'^assignment/add/question/(\d{1,4})/$', AddQuestion),
    (r'^assignment/preview/(\d{1,4})/$', PreviewAssignment),
    (r'^assignment/delete/(\d{1,4})/$', DeleteAssignment),
    (r'^assignment/modify/(\d{1,4})/$', ModifyAssignment),
    (r'^assignment/solve/$', SolveAssignment),
    (r'^assignment/add/question/$', EditAssignment),
    (r'^assignment/delete/$', EditAssignment),
    (r'^assignment/modify/$', EditAssignment),
    ('^assignment/edit/$', EditAssignment),
    ('^assignment/preview/$', PreviewAssignment),
    ('^user/profile/$', Profile),
	(r'^assignment/file/delete/(?P<assg_id>[\w\-]+)/(?P<qid>[\w\-]+)/(?P<fname>[\w\s\.-]+)/$', DeleteFile),
	(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

if settings.DEBUG:
	from django.views.static import serve
	_media_url = settings.MEDIA_URL
	if _media_url.startswith('/'):
		_media_url = _media_url[1:]
		urlpatterns += patterns('',
					(r'%s(?P<path>.*)$' % _media_url,
					serve,
					{'document_root':settings.MEDIA_ROOT}))
	del(_media_url, serve)