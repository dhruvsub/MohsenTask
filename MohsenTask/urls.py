from django.conf.urls import url
from django.contrib import admin
import settings

from MohsenTaskApp.views import *

#admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
	#patterns('',
    #(r'^$', index),
	#(r'^EU/$', return_eu_survey_page),
	#(r'^SA/$', return_sa_survey_page),
	#(r'^AS/$', return_as_survey_page),
	#(r'^test/$', return_test_survey_page),
	#(r'^AMT/$', return_AMT_survey_page),
	#(r'^res_files/', show_result_files),
	#(r'^labeling_res_files/$', show_labeling_result_files),
	#(r'^AMT_grandLabeling_res_files/$', show_grandLabeling_result_files),
	#(r'^AMT_grandLabeling_startPage/$', return_AMT_grandLabel_survey_startPage),
	#(r'^AMT_grandLabeling_retrievePage/$', return_AMT_grandLabel_survey_retrievePage),
	#(r'^AMT_grandLabeling_initPage/$', return_AMT_grandLabel_survey_initPage),
	#(r'^AMT_grandLabeling_submitPage/$', return_AMT_grandLabel_survey_submitPage),
	#(r'^AMT_grandLabeling_savePage/$', return_AMT_grandLabel_survey_savePage),
	#(r'^AMT_labeling/$', return_AMT_label_survey_page),
	### survey -1: 1000w+1000t, anonymous or not
	#(r'^AMT_anonymity_survey1_startPage/$', return_AMT_anonymity_survey1_startPage),
	#(r'^AMT_anonymity_survey1_retrievePage/$', return_AMT_anonymity_survey1_retrievePage),
	#(r'^AMT_anonymity_survey1_submitPage/$', return_AMT_anonymity_survey1_submitPage),
	#(r'^AMT_anonymity_survey1_savePage/$', return_AMT_anonymity_survey1_savePage),
	### survey -2: 1000w categories
	#(r'^AMT_labeling_survey2_startPage/$', return_AMT_labeling_survey2_startPage),
	#(r'^AMT_labeling_survey2_retrievePage/$', return_AMT_labeling_survey2_retrievePage),
	#(r'^AMT_labeling_survey2_submitPage/$', return_AMT_labeling_survey2_submitPage),
	#(r'^AMT_labeling_survey2_savePage/$', return_AMT_labeling_survey2_savePage),
	### new survey -1: 500w+500t, anonymous or not, also collect the users demographics
	url(r'^AMT_anonymity_newSurvey1_startPage/$', return_AMT_anonymity_newSurvey1_startPage),
	url(r'^AMT_anonymity_newSurvey1_retrievePage/$', return_AMT_anonymity_newSurvey1_retrievePage),
	url(r'^AMT_anonymity_newSurvey1_submitPage/$', return_AMT_anonymity_newSurvey1_submitPage),
	url(r'^AMT_anonymity_newSurvey1_savePage/$', return_AMT_anonymity_newSurvey1_savePage),
	### new survey -2: 500w categories
	#(r'^AMT_labeling_newSurvey2_startPage/$', return_AMT_labeling_newSurvey2_startPage),
	#(r'^AMT_labeling_newSurvey2_retrievePage/$', return_AMT_labeling_newSurvey2_retrievePage),
	#(r'^AMT_labeling_newSurvey2_submitPage/$', return_AMT_labeling_newSurvey2_submitPage),
	#(r'^AMT_labeling_newSurvey2_savePage/$', return_AMT_labeling_newSurvey2_savePage),
	### delete survey -1: 1000 deleted tweets, spam, will post or will not post, also collect the users demographics
	#(r'^AMT_deletion_survey1_startPage/$', return_AMT_deletion_survey1_startPage),
	#(r'^AMT_deletion_survey1_retrievePage/$', return_AMT_deletion_survey1_retrievePage),
	#(r'^AMT_deletion_survey1_submitPage/$', return_AMT_deletion_survey1_submitPage),
	#(r'^AMT_deletion_survey1_savePage/$', return_AMT_deletion_survey1_savePage),



]
