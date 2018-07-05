from django.shortcuts import render,HttpResponse
import requests
from .models import Users,Apicall
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

import datetime as DT


def searchPage(request):
	git_token="0987dc0cfd4ab9b5f1e69bc7c8ec7149c753e5cc"
	headers = {'Authorization': 'token ' + git_token}
	users=None
	searchText=""
	length=0
	userlist=[]
	if request.GET.get('searchText'):
		searchText=request.GET['searchText']
		filterString=request.GET['filter']
		query=Apicall(searched_string=searchText,filter_string=filterString)
		query.save()
		if (filterString=="location" or filterString=="repos" or filterString=="followers"):
			response = requests.request('GET', 'https://api.github.com/search/users?q='+searchText+'+'+filterString+':'+searchText+"&per_page=100",headers=headers)

		else:
			response = requests.request('GET', 'https://api.github.com/search/users?q='+searchText+'+'+filterString+"&per_page=100", headers=headers)
		resjson=response.json()
		users=resjson['items']
		userlist.extend(users)
		while 'next' in response.links.keys():
			response=requests.request('GET',response.links['next']['url'], headers=headers)
			resjson=response.json()
			users=resjson['items']
			userlist.extend(users)
						
		items=userlist
		length=len(items)
		for user in items:
			if (not Users.objects.filter(login_name=user['login']).exists()):
				query=Users(avatar_url=user['avatar_url'],login_name=user['login'],url=user['html_url'])
				query.save()
			else:
				query=Users.objects.get(login_name=user['login'])
				query.avatar_url=user['avatar_url']
				query.url=user['html_url']
				query.save()
	return render(request, 'github_api_search/search.html',
		{
		'users':userlist,
		'length':length,
		'searchText':searchText,
		})


def saved(request):
	users=None
	if request.GET.get('fromDate') and request.GET.get('toDate'):
		fromDateString=request.GET['fromDate']
		toDateString=request.GET['toDate']
		fromDate = datetime.strptime(fromDateString,'%Y-%m-%d')
		toDate = datetime.strptime(toDateString,'%Y-%m-%d')

		users=Users.objects.filter(saved_time_stamp__range=(fromDate, toDate))
	else:
		users=Users.objects.all()
	length=len(users)
	paginator = Paginator(users, 40)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	return render(request, 'github_api_search/list.html',
		{
		'users':users,
		'length':length,
		})



def metrics(request):
	savedCount=None
	apiCallCount=None
	isDefault=True
	savedCountCurrentDay=None
	apiCallCountCurrentDay=None
	savedCountCurrentMonth=None
	apiCallCountCurrentMonth=None
	fromDateString=None
	toDateString=None
	if request.GET.get('fromDate') and request.GET.get('toDate'):
		fromDateString=request.GET['fromDate']
		toDateString=request.GET['toDate']
		fromDate = datetime.strptime(fromDateString,'%Y-%m-%d')
		toDate = datetime.strptime(toDateString,'%Y-%m-%d')
		savedCount=len(Users.objects.filter(saved_time_stamp__range=(fromDate, toDate)))
		apiCallCount=len(Apicall.objects.filter(time_stamp__range=(fromDate, toDate)))
		isDefault=False
	else:
		savedCountCurrentDay=len(Users.objects.filter(saved_time_stamp__range=((datetime.now()-DT.timedelta(days=7)).date(), datetime.now())))
		apiCallCountCurrentDay=len(Apicall.objects.filter(time_stamp__range=((datetime.now()-DT.timedelta(days=7)).date(), datetime.now())))
		savedCountCurrentMonth=len(Users.objects.filter(saved_time_stamp__range=(datetime.today().replace(day=1).date(), datetime.now())))
		apiCallCountCurrentMonth=len(Apicall.objects.filter(time_stamp__range=(datetime.today().replace(day=1).date(), datetime.now())))

	return render(request, 'github_api_search/metrics.html',
		{
		'savedCount':savedCount,
		'apiCallCount':apiCallCount,
		'savedCountCurrentDay':savedCountCurrentDay,
		'apiCallCountCurrentDay':apiCallCountCurrentDay,
		'savedCountCurrentMonth':savedCountCurrentMonth,
		'apiCallCountCurrentMonth':apiCallCountCurrentMonth,
		'isDefault':isDefault,
		'fromDate':fromDateString,
		'toDate':toDateString,
		})