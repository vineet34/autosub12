from django import template
from django.contrib.auth.models import User

register = template.Library()
@register.simple_tag
def getFileURL(dict, key, qid):
	return dict.get(str(qid)+'_'+str(key)+'_url', '')
	
@register.simple_tag
def getFileName(dict, key, qid):
	return dict.get(str(qid)+'_'+str(key)+'_name', '')
	
@register.simple_tag
def getProfileStatus(username):
	if User.objects.filter(username=username)[0].is_active:
		return 'Y'
	else:
		return 'N'