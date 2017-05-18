# -*- coding: utf-8 -*-
import os
import sys
import commands
import string
import random
import urllib2
import uuid
import time
import glob
import csv

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.db import connections
from django.utils.http import urlquote
from django.views.decorators.cache import never_cache

import logging
from django.core import serializers
from models import *

import datetime
from urllib import urlencode
import base64
import hmac
import hashlib
try:
   import json
except ImportError:
   from django.utils import simplejson as json



htmlStringEnding='''
</body>
</html>
'''



@never_cache
def get_meta_refresh_page(request):
	if request.method=='GET':
		response=render_to_response('meta_refresh.html',{})
		return response

@never_cache
def get_test_landing_page(request):
	if request.method=='GET':
		response=render_to_response('redirect_land_page.html',{})
		return response
	
@never_cache
def get_http_redirect_page(request):
	if request.method=='GET':
		return HttpResponseRedirect('https://privacy-quiz.app-ns.mpi-sws.org/testland');


@never_cache
def index(request):
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		cursor = connections['default'].cursor()
		#cursor.execute("""insert into WeightwatcherAdIpaddr (ADCOUNTRY, IPADDR) values ('GET_REQUEST_INDEX', '%s');"""%(ip));
		#print cursor
		#response=render_to_response('index.html',{})
		response=render_to_response('index.html',{})
		return response



def checkDictkey(Dict, Key):
	try:
		a=Dict[Key]
		return True
	except:
		return False



@never_cache
@csrf_exempt
def return_eu_survey_page(request):
	cName='EU'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/results/%s_res.%d.txt'%(cName, ts)
		res=open(resFile, 'w')
		for i in range(1, 101):
			serialName= '%s_text%d'%(cName, i)
			try:
				a=paramDict[serialName]
			except:
				a='0'
			print>>res, '%s|%s'%(serialName,a)
		res.close()
		response=render_to_response('survey_done.html',{})
		return response
	
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response
	

@never_cache
@csrf_exempt
def return_as_survey_page(request):
	cName='AS'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/results/%s_res.%d.txt'%(cName, ts)
		res=open(resFile, 'w')
		for i in range(1, 101):
			serialName= '%s_text%d'%(cName, i)
			try:
				a=paramDict[serialName]
			except:
				a='0'
			print>>res, '%s|%s'%(serialName,a)
		res.close()
		response=render_to_response('survey_done.html',{})
		return response
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response
	
@never_cache
@csrf_exempt
def return_sa_survey_page(request):
	cName='SA'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/results/%s_res.%d.txt'%(cName, ts)
		res=open(resFile, 'w')
		for i in range(1, 101):
			serialName= '%s_text%d'%(cName, i)
			try:
				a=paramDict[serialName]
			except:
				a='0'
			print>>res, '%s|%s'%(serialName,a)
		res.close()
		response=render_to_response('survey_done.html',{})
		return response
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response

@never_cache
@csrf_exempt
def return_test_survey_page(request):
	cName='test'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(uuid.uuid4())
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/tokens")
		os.system("touch /var/www/checkanonsurvey/checkanonsurvey1/tokens/%s.%d.%s.token"%(cName, ts, randomNumber))
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/results/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		for i in range(1, 101):
			serialName= '%s_text%d'%(cName, i)
			try:
				a=paramDict[serialName]
			except:
				a='0'
			print>>res, '%s|%s'%(serialName,a)
		res.close()
		response=render_to_response('survey_done_amt.html', {'token':randomNumber})
		return response
	
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function_AMT(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response
	

@never_cache
@csrf_exempt
def return_AMT_label_survey_page(request):
	cName='AMT_labeling'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(uuid.uuid4())
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_tokens")
		os.system("touch /var/www/checkanonsurvey/checkanonsurvey1/grandLebeling_tokens/%s.%d.%s.token"%(cName, ts, randomNumber))
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_results/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		values=['Meetup', 'Confessions', 'Relationships', 'NSFW', 'QandAAdvice', 'LOL', 'CelebrityNewsGossip', 'LGBTQ', 'DrugsAlchoholBlackmarkets', 'other', 'otherText']
		for i in range(1, 112):
			serialName= '%s_text%d_'%(cName, i)
			keys=paramDict.keys()
			bigDict={'serialName': '%s_text%d'%(cName, i)}
			for k in keys:
				if serialName in k:
					if 'otherText' in k:
						if serialName+'other' in keys: 
							bigDict[k]=paramDict[k]
					else:
						bigDict[k]=paramDict[k]
			print>>res, json.dumps(bigDict)
		res.close()
		response=render_to_response('survey_done_amt_grandLabeling.html', {'token':randomNumber})
		return response
	
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function_AMT_grandLabeling(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response




@never_cache
@csrf_exempt
def return_AMT_survey_page(request):
	cName='AMT'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(uuid.uuid4())
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/tokens")
		os.system("touch /var/www/checkanonsurvey/checkanonsurvey1/tokens/%s.%d.%s.token"%(cName, ts, randomNumber))
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/results/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		for i in range(1, 101):
			serialName= '%s_text%d'%(cName, i)
			try:
				a=paramDict[serialName]
			except:
				a='0'
			print>>res, '%s|%s'%(serialName,a)
		res.close()
		response=render_to_response('survey_done_amt.html', {'token':randomNumber})
		return response
	
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function_AMT(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response


@never_cache
@csrf_exempt
def return_AMT_grandLabel_survey_page(request):
	cName='AMT_grandLabeling'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(uuid.uuid4())
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_tokens")
		os.system("touch /var/www/checkanonsurvey/checkanonsurvey1/grandLebeling_tokens/%s.%d.%s.token"%(cName, ts, randomNumber))
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_results/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		values=['Meetup', 'Confessions', 'Relationships', 'NSFW', 'QandAAdvice', 'LOL', 'CelebrityNewsGossip', 'LGBTQ', 'DrugsAlchoholBlackmarkets', 'other', 'otherText']
		for i in range(1, 112):
			serialName= '%s_text%d_'%(cName, i)
			keys=paramDict.keys()
			bigDict={'serialName': '%s_text%d'%(cName, i)}
			for k in keys:
				if serialName in k:
					if 'otherText' in k:
						if serialName+'other' in keys: 
							bigDict[k]=paramDict[k]
					else:
						bigDict[k]=paramDict[k]
			print>>res, json.dumps(bigDict)
		res.close()
		response=render_to_response('survey_done_amt_grandLabeling.html', {'token':randomNumber})
		return response
	
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_function_AMT_grandLabeling(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{})
		return response

@never_cache
@csrf_exempt
def  return_AMT_grandLabel_survey_initPage(request):
	cName='AMT_grandLabeling'
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		randomNumber=str(uuid.uuid4())
		cursor = connections['default'].cursor()
		res=get_function_AMT_grandLabelingInitPage(ts, cName)
		response=render_to_response('survey_%s_apache_initPage.html'%(cName),{'tsValue':ts, 'uuidValue':randomNumber})
		return response

@never_cache
@csrf_exempt
def return_AMT_grandLabel_survey_startPage(request):
	cName='AMT_grandLabeling'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(paramDict['uuidValue'])
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		cursor = connections['default'].cursor()
		res=get_AMT_grandLabel_survey_startPage(ts, cName)
		response=render_to_response('survey_%s_apache.html'%(cName),{'tsValue':ts, 'uuidValue':randomNumber})
		return response


@never_cache
@csrf_exempt
def return_AMT_grandLabel_survey_retrievePage(request):
	cName='AMT_grandLabeling'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(paramDict['tokenValueRetrieve'])
		randomNumber=randomNumber.strip()
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_savedSession/%s'%(randomNumber)
		if os.path.isfile(resFile)==False:
			response=render_to_response('tokenNotFound_apache.html',{'tsValue':ts, 'token':randomNumber})
			return response
		f=open(resFile, "r")
		l=f.read()
		savedParamDict=json.loads(l)
		f.close()
		ip=request.META['REMOTE_ADDR']
		res=get_AMT_grandLabel_survey_retrievePage(ts, cName, savedParamDict, randomNumber)
		#response=render_to_response("survey_%s_apache.%s.html"%(cName, randomNumber),{'tsValue':ts, 'uuidValue':randomNumber})
		return HttpResponse(res)


@never_cache
@csrf_exempt
def return_AMT_grandLabel_survey_savePage(request):
	cName='AMT_grandLabeling'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(paramDict['uuidValue'])
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_savedSession")
		os.system("chmod 777 -R /var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_savedSession")
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_savedSession/%s'%(randomNumber)
		res=open(resFile, 'w')
		print>>res,json.dumps(paramDict)
		response=render_to_response('survey_saved_amt_grandLabeling.html', {'token':randomNumber})
		return response


@never_cache
@csrf_exempt
def return_AMT_grandLabel_survey_submitPage(request):
	cName='AMT_grandLabeling'
	if request.method=='POST':
		paramDict=request.POST
		if 'Save' in paramDict.keys():
			return return_AMT_grandLabel_survey_savePage(request)

		ts=int(paramDict['time'])
		randomNumber=str(paramDict['uuidValue'])
		os.system("mkdir -p /var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_tokens")
		os.system("touch /var/www/checkanonsurvey/checkanonsurvey1/grandLebeling_tokens/%s.%d.%s.token"%(cName, ts, randomNumber))
		resFile='/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_results/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		for i in range(1, 1001):
			serialName= '%s_text%d_'%(cName, i)
			keys=paramDict.keys()
			bigDict={'serialName': '%s_text%d'%(cName, i)}
			for k in keys:
				if serialName in k:
					if 'otherText' in k:
						if serialName+'other' in keys: 
							bigDict[k]=paramDict[k]
					else:
						bigDict[k]=paramDict[k]
			print>>res, json.dumps(bigDict)
		res.close()
		response=render_to_response('survey_done_amt_grandLabeling.html', {'token':randomNumber})
		return response


def return_ping(request):
	rand_num=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
	response= HttpResponse(str(rand_num))
	return response

	
def show_result_files(request):
	if request.method=='GET':
		path="/var/www/checkanonsurvey/checkanonsurvey1/results/"  # insert the path to your directory   
		f_list =os.listdir(path)   
	    	return render_to_response('files.html', {'files': f_list})
	
	
def show_labeling_result_files(request):
	if request.method=='GET':
		path="/var/www/checkanonsurvey/checkanonsurvey1/labeling_results/"  # insert the path to your directory   
		f_list =os.listdir(path)   
	    	return render_to_response('labeling_files.html', {'files': f_list})
	
	
def show_grandLabeling_result_files(request):
	if request.method=='GET':
		path="/var/www/checkanonsurvey/checkanonsurvey1/grandLabeling_results_consolidated/"  # insert the path to your directory   
		f_list =os.listdir(path)   
	    	return render_to_response('grandLabeling_files.html', {'files': f_list})
	

#################################### BEGIN: Survey 1 #############################
####### BEGIN: HANDLER HELPERS #####################



####### END: HANDLER HELPERS #####################
##########################################################################
####### BEGIN: HANDLERS #####################

####### END: HANDLERS #####################
#################################### END: Survey 1 #############################


#################################### BEGIN: Survey 2 #############################
####### BEGIN: HANDLER HELPERS #####################



####### END: HANDLER HELPERS #####################
##########################################################################
####### BEGIN: HANDLERS #####################


#################################### END: Survey 2 #############################

#################################### BEGIN: New Survey demographics 1 #############################
########### BEGIN: HANDLER HELPERS ########################

htmlStringBeginingAnonNewSurvey1='''
<!DOCTYPE html> 
<html lang="en">
<head>
  <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
      <title>Survey: Anonymity Sensitivity of Social Media posts</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <style>
    		table {border:solid 1px;border-collapse:collapse; table-layout:fixed; width:100%;}
      		table td {border:solid 1px; width:100%; word-wrap:break-word;}
	
			    body{-webkit-font-smoothing:antialiased;font:normal .8764em/1.5em Arial,Verdana,sans-serif;margin:0}html>body{font-size:13px}li{font-size:110%}li li{font-size:100%}li p{font-size:100%;margin:.5em 0}h1{color:#000;font-size:2.2857em;line-h+eight:.6563em;margin:.6563em 0}h2{color:#111;font-size:1.7143em;line-height:.875em;margin:.875em 0}h3{color:#111;font-size:1.5em;line-height:1em;margin:1em 0}h4{color:#111;font-size:1.2857em;line-height:1.1667em;margin:1.1667em 0}h5{col+or:#111;font-size:1.15em;line-height:1.3em;margin:1.3em 0}h6{font-size:1em;line-height:1.5em;margin:1.5em 0}body,p,td,div{color:#111;font-family:"Helvetica Neue",Helvetica,Arial,Verdana,sans-serif;word-wrap:break-word}h1,h2,h3,h4,h5,h6{+line-height:1.5em}a{-webkit-transition:color .2s ease-in-out;color:#0d6ea1;text-decoration:none}a:hover{color:#3593d9}.footnote{color:#0d6ea1;font-size:.8em;vertical-align:super}#wrapper img{max-width:100%;height:auto}dd{margin-bottom:1+em}li>p:first-child{margin:0}ul ul,ul ol{margin-bottom:.4em}caption,col,colgroup,table,tbody,td,tfoot,th,thead,tr{border-spacing:0}table{border:1px solid rgba(0,0,0,0.25);border-collapse:collapse;display:table;empty-cells:hide;margin:-1+px 0 23px;padding:0;table-layout:fixed}caption{display:table-caption;font-weight:700}col{display:table-column}colgroup{display:table-column-group}tbody{display:table-row-group}tfoot{display:table-footer-group}thead{display:table-header-+group}td,th{display:table-cell}tr{display:table-row}table th,table td{font-size:1.1em;line-height:23px;padding:0 1em}table thead{background:rgba(0,0,0,0.15);border:1px solid rgba(0,0,0,0.15);border-bottom:1px solid rgba(0,0,0,0.2)}table+ tbody{background:rgba(0,0,0,0.05)}table tfoot{background:rgba(0,0,0,0.15);border:1px solid rgba(0,0,0,0.15);border-top:1px solid rgba(0,0,0,0.2)}figure{display:inline-block;margin-bottom:1.2em;position:relative;margin:1em 0}figcaption{+font-style:italic;text-align:center;background:rgba(0,0,0,.9);color:rgba(255,255,255,1);position:absolute;left:0;bottom:-24px;width:98%;padding:1%;-webkit-transition:all .2s ease-in-out}.poetry pre{display:block;font-family:Georgia,Gara+mond,serif!important;font-size:110%!important;font-style:italic;line-height:1.6em;margin-left:1em}.poetry pre code{font-family:Georgia,Garamond,serif!important}blockquote p{font-size:110%;font-style:italic;line-height:1.6em}sup,sub,a.fo+otnote{font-size:1.4ex;height:0;line-height:1;position:relative;vertical-align:super}sub{vertical-align:sub;top:-1px}p,h5{font-size:1.1429em;line-height:1.3125em;margin:1.3125em 0}dt,th{font-weight:700}table tr:nth-child(odd),table th:n+th-child(odd),table td:nth-child(odd){background:rgba(255,255,255,0.06)}table tr:nth-child(even),table td:nth-child(even){background:rgba(0,0,0,0.06)}@media print{body{overflow:auto}img,pre,blockquote,table,figure,p{page-break-inside:av+oid}#wrapper{background:#fff;color:#303030;font-size:85%;padding:10px;position:relative;text-indent:0}}@media screen{.inverted #wrapper,.inverted{background:rgba(37,42,42,1)}.inverted hr{border-color:rgba(51,63,64,1)!important}.inverted+ p,.inverted td,.inverted li,.inverted h1,.inverted h2,.inverted h3,.inverted h4,.inverted h5,.inverted h6,.inverted pre,.inverted code,.inverted th,.inverted .math,.inverted caption,.inverted dd,.inverted dt{color:#eee!important}.inver+ted table tr:nth-child(odd),.inverted table th:nth-child(odd),.inverted table td:nth-child(odd){background:0}.inverted a{color:rgba(172,209,213,1)}#wrapper{padding:20px}::selection{background:rgba(157,193,200,.5)}h1::selection{backgroun+d-color:rgba(45,156,208,.3)}h2::selection{background-color:rgba(90,182,224,.3)}h3::selection,h4::selection,h5::selection,h6::selection,li::selection,ol::selection{background-color:rgba(133,201,232,.3)}code::selection{background-color:rg+ba(0,0,0,.7);color:#eee}code span::selection{background-color:rgba(0,0,0,.7)!important;color:#eee!important}a::selection{background-color:rgba(255,230,102,.2)}.inverted a::selection{background-color:rgba(255,230,102,.6)}td::selection,th+::selection,caption::selection{background-color:rgba(180,237,95,.5)}}
			    </style>
			    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js" ></script>
			    <script>
			    var toprint = 1;
			    $(document).ready(function() {
				$('#doneSurvey').click(function(e){                 
				  var alldone = [];
				  var notdoneRadio=-1;
				  var click=0;
				  var totQuestion=0;
				  $('input[type="radio"]').each(function(){
				    if($(this).prop('name').search("AMT_anonymity") == 0)
				    {
				      totQuestion+=1;
				      if($(this).prop('checked')) {
				    	click+=1;
					alldone.push($(this).prop('name').split('_')[3]);
  				      }
				      else{
				    	var name = $(this).prop('name');
					var num=name.split('_')[3];
				    	notDoneRadio=num;
				      }
				    }
				  });

				  var totDem=0;
				  var doneDem=0;
				
				  var table0text = $('#table_0').html();
				  for(var l = 0; l < table0text.length; l++)
				  {
				    if(table0text.substring(l, l+5) == "</tr>")
				      totDem++;
				  }
				  totDem--;

				  $('option').each(function() {
				    if($(this).text() == "Select")
				      return;
				    if($(this).is(':selected'))
				      doneDem++;
				  });
				  $('input[type="radio"]').each(function() {
				    if($(this).is(':checked'))
				      doneDem++;
				  });
				  doneDem -= click;

				  //console.log(doneDem.toString() + " / " + totDem.toString());
				  totQuestion>>=1;
				  notDoneRadio=notDoneRadio.replace("text", "");

				  var notDoneRadio = [];
				  for(var mind = 1; mind <= totQuestion; mind++)
				    if(alldone.indexOf('text' + mind.toString()) == -1)
				    {
				      notDoneRadio.push(mind);
				    }
				  var stringNotDoneRadio = '';
				  var lim = 10;
				  if(notDoneRadio.length < lim)
				    lim = notDoneRadio.length;
				  if(lim == 1)
				    stringNotDoneRadio = notDoneRadio[0].toString();
				  else
				  {
				    for(var l = 0; l < lim; l++)
				    {
				      var toput = ', ';
				      if(l == lim - 1)
				        toput = ' and ';
				      stringNotDoneRadio += l ? (toput + notDoneRadio[l].toString()) : (notDoneRadio[l].toString());
				    }
				  }

				  var flag=0;
				  if(click != totQuestion)
				    flag = 1;
				  else if (totDem != doneDem)
				    flag = 2;

				  if (flag == 2){
				    //alert('Please enter all your demographic information!');
				  }
				  else if (flag == 1){
				    alert('Please tell for all '+ totQuestion.toString() +' texts whether you want to post it anonymous/non-anoymously. You have categorized ' + click +' text' + (click > 1 ? 's' : '') + '. For e.g., you have not categorized text with serial number' + (lim > 1 ? 's' : '') + ' '+stringNotDoneRadio+'!');
				  }

				  if (flag == 1){
				      e.preventDefault();
				  }
				 });
				});
				
				function showHide(id1, id2){
					id2num = "";
					for(var i = 0; i < id2.length; i++)
						if (id2[i] >= '0' && id2[i] <= '9')
							id2num = id2num + id2[i]
					id2num = parseInt(id2num);
					var stillOpen = 0;
					for(var i = id2num - 10; i >= 0; i -= 10)
					{
						if(document.getElementById("table_" + i.toString()).style.display == "block")
							stillOpen = 1;
					}
					if(!stillOpen)
					{
						document.getElementById(id2).style.display = "none";
						document.getElementById(id1).style.display = "block";
						$( '#' + id1 ).fadeTo( 0.0, 0);
						$( '#' + id1 ).fadeTo( 1.0, 10000);
					}
					if(id1 == "table_0")
					{
						document.getElementById("doneSurvey").style.display = "block";
						//document.getElementById("sttfrombeg").style.display = "inline-block";
					}
					else
					{
						document.getElementById("doneSurvey").style.display = "none";
						document.getElementById("sttfrombeg").style.display = "none";
					}
				}
			       function showToggle(id){var e = document.getElementById(id);if (e.style.display == '')e.style.display = 'none';else e.style.display = '';}
			   </script>
			    </head>
			    <body class="normal">
			    <div id="wrapper">
			            <p><img src="http://cdn.bleacherreport.net/images/team_logos/328x328/purdue.png" align="right"></p>
				            <h1 id="survey:name">Survey: Anonymity Sensitivity of Social Media posts</h1>
					            <!-- <h2 id="survey:description">Yadda yadda yadda</h2>
						            <p><strong>Bla bla bla ... </strong></p> -->
						    <p> In the survey below, you will be shown 1000 pieces of text with 10 texts on each page. These texts are collected from different social networking sites.</p>
						    <p> For each piece of text you have to tell &#8210; <strong>if you were sharing this information on a social networking site, would you post this piece of information anonymously (i.e., without real name and profile information) or non-anonymously?</strong> Once you finish labeling all 1000 pieces of text, click submit, and you will be given a token. Put the token in the Mechanical Turk survey page to claim your reward. 
						    </p>

						    <p>
						    At the end of the survey, you will see a page which requests your demographic information. This demographic information is highly valuable for our study. We request you to fill in these details to help us in our endeavor. Because of the nature of electronic systems, it is possible that respondents could be identified by some electronic record associated with the response. Neither the researcher nor anyone involved with this study will be capturing those data. Any reports or publications based on this research will use only group data and will not identify you or any individual as being affiliated with this project.
						    </p
						    <p><i style="font-size: 14px; font-weight: bold;">NOTE: You can save the survey any time and retrieve it later using the options at the <a id="goto_fill_continue" href="#fill_continue">end</a> of this page. </i></p>
						</div>
'''

def value_version(c):
	chars_to_remove = [ ' ', '-', '.', ',', ';', '/', '&', '(', ')', '\'' ]
	for k in chars_to_remove:
		c = c.replace(k, '')
	return c.lower()

def getListOfCountries():
	return ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antarctica', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Dem. Rep. Korea', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Fiji', 'Finland', 'France', 'French Southern and Antarctic Lands', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Lao PDR', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Northern Cyprus', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Republic of Congo', 'Republic of Korea', 'Romania', 'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'Somaliland', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The Gambia', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

def get_function_AMT_anonymity_newSurvey1_startPage(ts, cName, perPage=5, totQ=1000):
	htmlFileName="/homes/subramad/MohsenTask/templates/survey_%s_apache.html"%(cName)
	flag=os.path.isfile(htmlFileName)
	if flag==True:
		return htmlFileName
	if flag==False:
		htmlString=htmlStringBeginingAnonNewSurvey1
		htmlStringMid='''

<form name="input_%s" action="/%s_submitPage/" method="post">
<input type="hidden" name="time" value={{tsValue}}> 
<input type="hidden" name="uuidValue" value={{uuidValue}}> 
<center>
<script src="//code.jquery.com/jquery-1.10.2.js"></script>
	<div id="table_0" style="display:none;">
		<table style="width:70%%">
		<tr>
			<th colspan="2">Please Enter your demographic information</th>
		</tr>	
'''%(cName, cName)
		demDict={'nationality':'Nationality', 'location':'Country', 'gender': 'Gender', 'sex':'Sexual Orientation','age':'Age', 'education':'Education', 'student':'Student', 'employment':'Employment', 'income':'Income (approximate <i>US $</i> per annum)', 'religion':'Religion', 'politics':'Political view', 'race':'Race / Ethnicity', 'marital':'Marital Status'}

		demDict = {}

		demDict['nationality'] = 'What is your country of nationality?';
		demDict['location'] = 'What is your country of residence?';
		demDict['gender'] = 'Which of the following best identifies yours gender?';
		demDict['sex'] = 'Which of the following best describes your sexual orientation?';
		demDict['age'] = 'What is your age?';
		demDict['education'] = 'What is the highest degree or level of school you have completed? If currently enrolled, highest degree received.';
		demDict['employment'] = 'What is your employment status?';
		demDict['income'] = 'What is your Income (approximate <i>US $</i> per annum)?';
		demDict['religion'] = 'What is your present Religion, if any?';
		demDict['politics'] = 'Which of the following best defines your political view?';
		demDict['race'] = 'Please specify your race/ethnicity';
		demDict['marital'] = 'What is your marital status?';

		# ------ BEGIN: Definition of Attributes ------ #

		#!/usr/bin/env python
		# -*- coding: latin-1 -*-

		predefined_list = {}
		predefined_radio = {}
		
		predefined_list['nationality'] = sorted(getListOfCountries())
		predefined_list['location'] = predefined_list['nationality']
		predefined_radio['gender'] = [ 'Female', 'Male', 'Other' ]
		predefined_list['sex'] = sorted([ 'Lesbian, Gay or Homosexual', 'Straight or Heterosexual', 'Bisexual' ]) + [ 'Other', 'Don\'t know' ]
		predefined_radio['age'] = [ 'Under 12 years old', '12&ndash;17 years old', '18&ndash;24 years old', '25&ndash;34 years old', '35&ndash;44 years old', '45&ndash;54 years old', '55&ndash;64 years old', '65&ndash;74 years old', '75 years or older' ]
		predefined_list['education'] = [ 'None, or grade 1-8', 'High school incomplete (Grades 9-11)', 'High school graduate (Grade 12 or GED certificate)', 'Technical, trade, or vocational school AFTER high school', 'Some college, associate degree, no 4-year degree', 'College graduate (B.S., B.A., or other 4-year degree)', ' Post-graduate training or professional schooling after college (e.g., toward a master\'s Degree or Ph.D.; law or medical school)' ]
		predefined_radio['student'] = [ 'No Time', 'Full Time', 'Part Time' ]
		predefined_list['employment'] = [ 'In full time work, permanent', 'In full time work, temp/contract', 'In part time work, permanent', 'In part time work, temp/contract', 'Part time work, part time student', 'Student only', 'Unemployed', 'Incapacity', 'Retired', 'Self-employed' ]
		predefined_list['income'] = [ 'Under 10,000', '10,000&ndash;20,000', '20,001&ndash;30,000', '30,001&ndash;40,000', '40,001&ndash;50,000', '50,001&ndash;60,000', '60,001&ndash;70,000', '70,001&ndash;100,000', '100,001&ndash;150,000', '150,001 or more' ]
		predefined_list['religion'] = sorted(list( set([ 'Agnostic (not sure if there is a God)', 'Atheist (do not believe in God)', 'Baha\'is', 'Buddhist', 'Catholic', 'Christian', 'Ethnic/Indigenous', 'Hindu', 'Indigenous', 'Irreligious and atheist', 'Jainism', 'Jewish (Judaism)', 'Judaism', 'Mormonism (Church of Jesus Christ of Latter-day Saints/LDS)', 'Muslim (Islam)', 'Orthodox (Greek, Russian, or some other orthodox church)', 'Protestant (Baptist, Methodist, Non-denominational, Lutheran, Presbyterian, Pentecostal, Episcopalian, Reformed, Church of Christ, ehovah\'s Witness, etc.)', 'Roman Catholic (Catholic)', 'Sikh', 'Sikhism', 'Spiritism', 'Taoist/Confucianist/Chinese traditional religionist', 'Unitarian' ]) )) + [ 'Other', 'Nothing in particular', 'Don\'t know' ]
		predefined_list['politics'] = [ 'Very conservative', 'Conservative', 'Moderate', 'Liberal', 'Very liberal' ] + [ 'Other', 'Don\'t know' ]
		predefined_list['race'] = sorted([ 'American Indian or Alaska Native', 'Asian', 'Black or African American', 'Native Hawaiian or Other Pacific Islander', 'White', 'Hispanic or Latino', 'Not Hispanic or Latino' ]) + [ 'Other', 'Don\'t know' ]
		predefined_radio['marital'] = [ 'Single (Never Been Married)', 'Living with a Partner', 'Married/Remarried', 'Separated', 'Widowed', 'Divorced' ]

		fields_to_remove = [ 'student' ]

		# ------ END: Definition of Attributes ------ #

		BRIGHT = 90
		FONT_W = "bold"
		cont_rows = 0
		radio_count = -1
		resp_radio = {}
		even_style = "background:rgba(255,255,255,0.06);"

		for dem in predefined_list:
			if predefined_list[dem][0] != 'Select':
				predefined_list[dem] = [ 'Select' ] + predefined_list[dem]

		for dem in ['nationality', 'location', 'gender', 'sex', 'age', 'education', 'student', 'employment', 'income', 'religion', 'politics', 'race', 'marital']:
			strStyleAdd = ''
			if ~(cont_rows & 1):
				strStyleAdd = ' style="%s"' % even_style

#			htmlStringMid+='''
#				<tr>
#					<td>%s</td>
#					<td> <input type="text" name="dem_%s_%s" value={{dem_%s_%s}}> </td>
#				</tr>'''%(demDict[dem], cName, dem, cName, dem)
			if dem in fields_to_remove:
				continue
			if 1:
				if dem in predefined_list:
					htmlStringMid+='''
	                			<tr id="getBolder%d">
	                        			<td>%s</td>
							<td><select name="dem_%s_%s" style="width: 300px; max-width: 300px;">
							''' % (cont_rows, demDict[dem], cName, dem)
					cont_rows += 1
					for v in predefined_list[dem]:
						htmlStringMid += '''<option style="width: 250px; max-width: 250px;" value="%s" {{ dem_%s_%s_%s }}>%s</option>''' % (value_version(v), cName, dem, value_version(v), v)
				
					htmlStringMid+='''</select></td></tr>'''
				if dem in predefined_radio:
					radio_count += 1
					htmlStringMid+='''
					        <tr>
							<td id="radio%d">%s</td>
							<td>''' % (radio_count, demDict[dem])
					for i in range(len(predefined_radio[dem])):
						v = predefined_radio[dem][i]
						divstyle = ""
						# divstyle += "display: inline-block;"
						# if i != len(predefined_radio[dem]) - 1:
							# divstyle += " margin-right: 16px;"
							# htmlStringMid += '''&nbsp&nbsp&nbsp'''
						htmlStringMid += '''<div id=getBolder%d style="%s"><input type="radio" name="dem_%s_%s" value="%s" {{ dem_%s_%s_%s }}>%s</div>''' % (cont_rows, divstyle, cName, dem, value_version(v), cName, dem, value_version(v), v)
						resp_radio[cont_rows] = radio_count
						cont_rows += 1
						
					htmlStringMid+='''</td></tr>'''

		radio_count += 1
		htmlStringMid+='''<style type="text/css">'''
		htmlStringMid+='''.radioactive { font-weight: %s; }''' % (FONT_W)
		for i in range(cont_rows):
			htmlStringMid+='''
					  #getBolder%d:hover {
					  	font-weight: %s;
						filter: brightness(%d%%);
						-webkit-filter: brightness(%d%%);
						-moz-filter: brightness(%d%%);
						-o-filter: brightness(%d%%);
						-ms-filter: brightness(%d%%);
					  }
				       ''' % (i, FONT_W, BRIGHT, BRIGHT, BRIGHT, BRIGHT, BRIGHT)
		htmlStringMid+='''</style>'''
		for i in range(cont_rows):
			if i in resp_radio:
				htmlStringMid += '''
						 <script>
						   $("#getBolder%d").hover(
						   function(){
				    		   	$('#radio%d').addClass('radioactive');
				    		   },
						   function(){
				        		$('#radio%d').removeClass('radioactive');
						   });
						</script>
						 ''' % (i, resp_radio[i], resp_radio[i])
		for i in range(radio_count):
			for j in range(cont_rows):
				if j not in resp_radio or resp_radio[j] != i:
					continue
				htmlStringMid += '''
						 <script>
						   $("#radio%d").hover(
						   function(){
						   	$('#radio%d').addClass('radioactive');
				    		   	$('#getBolder%d').addClass('radioactive');
				    		   },
						   function(){
						   	$('#radio%d').removeClass('radioactive');
				        		$('#getBolder%d').removeClass('radioactive');
						   });
						</script>
						 ''' % (i, i, j, i, j)

		htmlStringMid+='''	
		</table>
	</br></br>
	<script>
	    document.addEventListener('DOMContentLoaded', function()
	    {
	    	document.getElementById('table_0').style.display = 'block';
		document.getElementById('table_0').style.display = 'none';
		document.getElementById('table_1').style.display = 'block';
		var ult_table = 1;
		var iind = 1;
		var nCons = 0;
		while(1){ el = $("#table_" + iind.toString()); if(el[0] == undefined) { nCons += 1; if(nCons == 60000) break; } else { nCons = 0; ult_table = iind } iind += 1; }
		$("#table_0").insertAfter("#table_" + ult_table.toString());
		if(window.location.href.search("fill_continue") != -1)
		  $("#''' + cName + '''_textToken").focus();
		$("#goto_fill_continue").attr("onclick", "$(\'#''' + cName + '''_textToken\').focus()");
	    }, false);
	</script>
	</div>
	</br>
	</br>
</center>

<center>
<div id="table_1" style="display:none;">
<table style="width:70%">
<tr>
  <th style="width:10%">Serial</th>
  <th>Text</th>
    <th>Would you post this anonymously?</th>		
      <th>Would you post this non-anonymously?</th>
      </tr>
		'''
		fName='/homes/subramad/MohsenTask/data/test.json'
		i=0
		resFile=open('/homes/subramad/MohsenTask/res/resfile.json', "w")
		for l in open(fName):
			l=l.strip()
			tempDict=json.loads(l)
			i+=1
			surveySerial="%s_text%d"%(cName, i)
			serial=tempDict['serial']
			txt=tempDict['text']
			anonTag=tempDict['anon_label']
			tempDict={'surveySerial':surveySerial, 'serial': serial, 'text':txt, 'anon_label':anonTag}
			#print>>resFile, """%s_text%d|%s|%s|%s"""%(cName, i, txt, anonName, anonTag)
			print>>resFile, json.dumps(tempDict)
			htmlStringMid+='''
<tr id="rown%d" style="height: 120px; padding-top: 10px; padding-bottom: 10px;">
	<td>%i</td>
	<td>%s</td>
	<td><input type="radio" name="%s_text%d" value="anonymous" {{ %s_text%d_anonymous }}>Anonymous</td>		
	<td><input type="radio" name="%s_text%d" value="non-anonymous" {{ %s_text%d_non_anonymous }}>Non Anonymous</td>
</tr>
			'''%(i, i, txt, cName, i, cName, i, cName, i, cName, i)
			htmlStringMid+='''<style type="text/css"> #rown%d:hover { font-weight: %s; filter: brightness(%d%%); -webkit-filter: brightness(%d%%); -moz-filter: brightness(%d%%); -o-filter: brightness(%d%%); -ms-filter: brightness(%d%%); }</style>''' % (i, FONT_W, BRIGHT, BRIGHT, BRIGHT, BRIGHT, BRIGHT)
			if i%perPage==0:
				htmlStringMid+='''
					</table>
					'''
				buttonText1=''
				prevI=i - 2*perPage + 1
				nextI= i + 1
				if prevI > 0:
					buttonText1='''<button type="button" onclick="showHide('table_%d', 'table_%d')">Previous %d texts</button>'''%(prevI, prevI + perPage, perPage)
				buttonText2=''
				if nextI < totQ:
					buttonText2='''<button type="button" onclick="showHide('table_%d', 'table_%d')">Next %d texts</button>'''%(nextI, nextI - perPage, perPage)	
				else:
					buttonText2='''<button type="button" onclick="showHide('table_0', 'table_%d')">Next</button>''' % (nextI - perPage)
					
				htmlStringMid+='''
					<br>
					'''+buttonText1+'\n'+buttonText2+'\n</br>'+'''
					</br>
					</div>
					'''
				if i != totQ:	
					htmlStringMid+='''
					<div id="table_%d" style="display:none;">
				'''%(i+1)
					htmlStringMid+='''
<table style="width:70%">
<tr>
  <th style="width:10%">Serial</th>
  <th>Text</th>
    <th>Would you post this anonymously?</th>		
      <th>Would you post this non-anonymously?</th>
      </tr>
		'''
				
		resFile.close()

		htmlStringMid+='''
		        <input type="submit" name="Submit" value="Finish survey" id="doneSurvey" style="display: none; margin-bottom: 4px;"><br><hr></hr></input>
			<div>
                          Go to <strong>question</strong> number: <textarea id="gotopage_text" name="gotopage_text" value="" placeholder="1-1000" rows="1" cols="6" style="resize: none; vertical-align: -50%;"></textarea> <button type="button" onclick="pleaseGoToQuestion(document.getElementById('gotopage_text').value);">Go</button>
			</div>
			<br>
			<div>
			  <button type="button" onclick="pleaseGoToLastPage();">Go to last page</button>
			</div>

			  <script>
			    function pleaseGoToLastPage()
			    {
			      var mtable = 0;
			      for(var i = 1; i < 6000; i++)
			      {
			        el = $("#table_" + i.toString());
			        if(el[0] == undefined)
			          continue;
			        if($("#table_" + i.toString()).css('display') == 'block')
			          mtable = i;
			      }
			      showHide('table_' + (0).toString(), 'table_' + (mtable).toString());
			    }

			    function pleaseGoToQuestion(questionStr)
			    {
			      allnumbers = 1;
			      for(var l = 0; l < questionStr.length; l++)
			        if(questionStr.charCodeAt(l) < 48 || questionStr.charCodeAt(l) > 57)
			          allnumbers = 0;
			      if(!allnumbers)
			      {
			        alert("Please enter a valid number of question!");
			        return;
			      }

			      var questionNumber = parseInt(questionStr);

			      var mtable = -1;
			      var htable = -1;
			      for(var i = 0; i < 6000; i++)
			      {
			        el = $("#table_" + i.toString());
				if(el[0] == undefined)
				  continue;
				if($("#table_" + i.toString()).css('display') == 'block')
				  htable = i;
				if(i && questionNumber >= i && questionNumber < i + 10)
				  mtable = i;
			      }

			      if(mtable == -1 || htable == -1)
			      {
			        alert("Please enter a valid number of question!");
				return;
			      }

			      showHide('table_' + (mtable).toString(), 'table_' + (htable).toString());
			    }

			    $('#gotopage_text').keypress( function(e){
			      if(e.keyCode == 13)
			      {
			        pleaseGoToQuestion(document.getElementById('gotopage_text').value);
				e.preventDefault();
			      }
			    });
			  </script>
			<hr></hr>
		'''

		htmlStringMid+='''
<input type="submit" name="Submit" value="Submit" id="doneSurvey" style="display: none; margin-bottom: 4px;">
<button style="display: none" type="button" onclick="showToggle('table_0')">Show/hide demographic information</button>
<br><br>
<button style="display: none" type="button" onclick="showHide('table_1', 'table_0')" id="sttfrombeg">Go to beginning of Survey</button>
<input style="display: inline-block;" type="submit" name="Save" value="Save the survey so far" id="saveSurvey">
</form>
<br>
 </center>
<br>

	'''
		htmlStringMid+='''
<hr></hr>
<hr></hr>
<div>
</br>
<center>
	<form name="input_%s_retrieve" action="/%s_retrievePage/" method="post">
	<input type="hidden" name="time" value={{tsValue}}> 
	<input type="hidden" name="uuidValue" value={{uuidValue}}> 

	<strong id="fill_continue">If you want to retrieve your previous session, please enter the token and press Retrieve (It might take a few minutes):</strong> <input type="text" id="%s_textToken" name="tokenValueRetrieve" value=""> <input type="submit" value="Retrieve"></br></br>
	</form>
</br>

<hr></hr>
<hr></hr>
</br>
</center>
</div>
'''%(cName, cName, cName)

		htmlString+=htmlStringMid

		htmlString+=htmlStringEnding
		htmlFileName="survey_%s_apache.html"%(cName)
		html=open(htmlFileName, "w")
		print>>html, htmlString.encode('ascii', 'xmlcharrefreplace')
		html.close()
		return htmlFileName
########### END: HANDLER HELPERS ########################



@never_cache
@csrf_exempt
def return_AMT_anonymity_newSurvey1_startPage(request):
	cName='AMT_anonymity_newSurvey1'
	if request.method=='GET':
		ip=request.META['REMOTE_ADDR']
		ts=int(time.time())
		randomNumber=str(uuid.uuid4())
		perPage=10
		totQ=1000
		bigDict={'tsValue':ts, 'uuidValue':randomNumber}
		for i in range(1, totQ+1):
			serialName= '%s_text%d'%(cName, i)
			bigDict[serialName]=''
				
		res=get_function_AMT_anonymity_newSurvey1_startPage(ts, cName, perPage, totQ)
		response=render_to_response(res, bigDict)
		return response
@never_cache
@csrf_exempt
def return_AMT_anonymity_newSurvey1_submitPage(request):
	cName='AMT_anonymity_newSurvey1'
	if request.method=='POST':
		paramDict=request.POST
		paramDict=request.POST
		if 'Save' in paramDict.keys():
			return return_AMT_anonymity_newSurvey1_savePage(request)
		ts=int(paramDict['time'])
		randomNumber=str(paramDict['uuidValue'])
		resFile='/homes/subramad/MohsenTask/res/%s_res.%d.%s.txt'%(cName, ts, randomNumber)
		res=open(resFile, 'w')
		totQ=1000
		keys=paramDict.keys()
		already = set()
		for i in range(1, totQ+1):
			serialName= '%s_text%d'%(cName, i)
			bigDict={'serialName': '%s_text%d'%(cName, i)}
			try:
				bigDict[serialName]=paramDict[serialName]
				already.add(serialName)
			except:
				pass
			print>>res, json.dumps(bigDict)
		for k in sorted ( list( set(keys).difference(already) ) ):
			if k[:3] != 'dem':
				continue
			smallDict={ k : paramDict[k] }
			print>>res, json.dumps(smallDict)
		res.close()
		response=render_to_response('survey_done_amt.html', {'token':randomNumber})
		return response

@never_cache
@csrf_exempt
def return_AMT_anonymity_newSurvey1_savePage(request):
	cName='AMT_anonymity_newSurvey1'
	if request.method=='POST':
		paramDict=request.POST
		ts=int(paramDict['time'])
		randomNumber=str(paramDict['uuidValue'])
		resFile='/homes/subramad/MohsenTask/savedSession/%s.txt'%(randomNumber)
		res=open(resFile, 'w')
		print>>res,json.dumps(paramDict)
		response=render_to_response('survey_saved_AMT_anonymity_newSurvey1.html', {'token':randomNumber})
		return response


@never_cache
@csrf_exempt
def return_AMT_anonymity_newSurvey1_retrievePage(request):
	cName='AMT_anonymity_newSurvey1'
	demRadios = [ 'gender', 'age', 'student', 'marital' ]
	if request.method=='POST':
		perPage=10
		totQ=1000
		paramDict=request.POST
		ts=int(time.time())
		randomNumber=str(paramDict['tokenValueRetrieve'])
		randomNumber=randomNumber.strip()
		resFile='/homes/subramad/MohsenTask/savedSession/%s.txt'%(randomNumber)
		if os.path.isfile(resFile)==False:
			response=render_to_response('tokenNotFound_apache.html',{'tsValue':ts, 'token':randomNumber})
			return response
		f=open(resFile, "r")
		l=f.read()
		savedParamDict=json.loads(l)
		ts=int(savedParamDict['time'])
		f.close()
		bigDict={'tsValue':ts, 'uuidValue':randomNumber}
		
		for i in range(1, totQ+1):
			serialName= '%s_text%d'%(cName, i)
			bigDict[serialName+'_anonymous']=''	
			bigDict[serialName+'_non_anonymous']=''
			try:
				a=savedParamDict[serialName]
				a=a.replace('-', '_')
				bigDict[serialName+'_'+ a]= 'checked'
			except:
				pass			

		for k in savedParamDict:
			if k[:3] != 'dem':
				continue
			isRadio = False
			for r in demRadios:
				if '_' + r in k:
					isRadio = True

			if isRadio:
				bigDict[k+'_'+savedParamDict[k]]='checked'
			else:
				bigDict[k+'_'+savedParamDict[k]]='selected'
			
		res=get_function_AMT_anonymity_newSurvey1_startPage(ts, cName, perPage, totQ)
		response=render_to_response(res, bigDict)
		return response

####### END: HANDLERS #####################
#################################### END: New Survey demographics 1 #############################



#################################### BEGIN: New Survey 2 #############################
####### BEGIN: HANDLER HELPERS #####################


####### END: HANDLER HELPERS #####################


####### BEGIN: HANDLERS #####################


#################################### END: Survey 2 #############################


#################################### BEGIN: Survey deleted tweets wtih demographics 1 #############################
########### BEGIN: HANDLER HELPERS ########################


########### END: HANDLER HELPERS ########################


####### END: HANDLERS #####################
#################################### END: Deletion survey 1 demographics 1 #############################







