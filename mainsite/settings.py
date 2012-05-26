from local_settings import *

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'zioj1_5=%w6z!bgr6$h%3#%f3usw1bp%f_n2_cxudt0%=02!)j'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mainsite.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'mainsite.users',
	'mainsite.Assignment',
	'mainsite.customtags',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

FILE_UPLOAD_DIR = MEDIA_ROOT + 'uploads/'
PROFILE_PIC_DIR = FILE_UPLOAD_DIR + 'dp/'
QUES_FILES_DIR = FILE_UPLOAD_DIR + 'ques_files/'
ANS_FILES_DIR = FILE_UPLOAD_DIR + 'ans_files/'
ALLOWED_FILE_TYPES = ['.txt','.pdf','.doc','.docx','.tiff','.jpeg','.gif','.jpg','.png','.bmp','.ppt','.pptx','.xls','.xlsx','.zip','.rar','.7z','.tar','.gz','.bz2']
IMAGE_FILE_TYPES = ['.tiff','.jpeg','.gif','.jpg','.png','.bmp']
FILE_MAX_SIZE = 5242880
IMAGE_MAX_SIZE = 2621440