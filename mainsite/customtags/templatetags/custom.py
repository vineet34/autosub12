from django import template

register = template.Library()
@register.simple_tag
def getFileURL(dict, key, qid):
	return dict.get(str(qid)+'_'+str(key)+'_url', '')
	
@register.simple_tag
def getFileName(dict, key, qid):
	return dict.get(str(qid)+'_'+str(key)+'_name', '')