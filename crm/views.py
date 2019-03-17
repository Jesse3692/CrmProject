import hashlib
from django.shortcuts import render,HttpResponse,redirect,reverse
from crm import models
from crm.forms import RegForm
from utils.pagination import Pagination

# Create your views here.


