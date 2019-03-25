from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, ProductImage, Comment
from .forms import CommentForm
# for views/slug
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from functools import reduce, partial
from django.contrib.auth.decorators import login_required

# upload photo, find my shade
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        script_dir = sys.path[0]
        upload = os.path.join(script_dir, 'static/'+uploaded_file_url)
        shade = get_colors(upload)
        request.session['shades'] = shade
        template = 'products/getColor.html'
        context = { 'shade' : shade }
        return render(request, template, context)
    return render(request, 'products/upload.html')

def get_colors(infile):
    # set number of outputted colors, size, and resize
    numcolors=3
    swatchsize=100
    resize=150
    # open file
    image = Image.open(infile)
    image = image.resize((resize, resize))
    # crop photo
    width, height = image.size # get dimensions
    newSize = 100
    left = (width - (width-newSize))/2
    top = (height - (height-newSize))/2
    right = (width + (width-newSize))/2
    bottom = (height + (height-newSize))/2
    image = image.crop((left, top, right, bottom))
    # convert
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    #add alpha
    result.putalpha(0)
    # get color from the image
    colors = result.getcolors(resize*resize)
    shades = []
    # posx = 0
    for count, col in colors:
        shades.append(col[0:-1])
    return shades

def range(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([255, 255, 255])
    vector = white-color
    shade = color + vector * percent
    a = []
    # to remove decimal point
    for val in shade:
        a.append(int(val))
    return tuple(a)

def get_range(color):
    value = [] # the whole rgb
    percent = [.10,.20,.30,.40,.50,.60,.70,.80]
    for val in color:
        value.append(tuple(val)) # original
        for per in percent:
            a = range(val, per) # ranges 
            value.append(a)
    return value

# check for closest rgb
def colorDifference(testColor, otherColor):
    difference = 0
    difference += abs(testColor[0]-otherColor[0])
    difference += abs(testColor[1]-otherColor[1])
    difference += abs(testColor[2]-otherColor[2])
    return difference

# convert string query to tuple
def convert_query(lists):
    test = []
    short = [i.strip('()') for i in lists]
    short = [i.replace(' ','') for i in short]
    short = [i.split(',') for i in short]
    for i in short:
        b = []
        for x in i:
            a = int(x)
            b.append(a)
        test.append(tuple(b))
    return test

def color_match(request):
    color = request.session['shades']
    # check for original shade and range ------------------
    value = get_range(color) # list
    query = Product.objects.filter(rgb__in=value) # works
    # end --------------------
    # get rgb list that is only foundation from database ------
    obj = Product.objects.values_list('rgb', flat=True).filter(makeup_type__exact='Foundation')
    # -------------
    # if no 100% shade match find the closest shade --------
    closest = [] # save all the closest shades from orig
    shades = convert_query(obj) # works bitch / the database shades available
    myTuple = [tuple(i) for i in color] # shades from user
    for i in myTuple:
        closestColor = min(shades, key=partial(colorDifference, i))
        closest.append(closestColor)
    close = Product.objects.filter(rgb__in=closest) # works
    # ---------------------------
    context = { 'test': myTuple,'colors':query, 'empty':close}
    return render(request,'products/colorMatch.html',context)

def search(request):
    try:
        q =request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query':q, 'products':products}
        template = 'products/results.html'
    else:
        template = 'products/home.html'
        context = {}
    return render(request, template, context)

def home(request):
    products = Product.objects.all()
    template = 'products/home.html'
    context = {"products":products}
    return render(request, template, context)

def showall(request):
    products = Product.objects.all()
    context = {'products': products}
    template = 'products/all.html'
    return render(request, template, context)


def single(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        comment = Comment.objects.filter(product=product)
        images = ProductImage.objects.filter(product=product)
        

        #This part is the problem

        # if request.method == 'POST':
        #     comment_form = CommentForm(request.POST or None)
        #     if comment_form.is_valid():
        #         content = request.Post.get('content')
        #         comment.objects.create(post=post, content=content)
        #         comment.save()
        #         return HttpResponseRedirect(post.get_absolute_url())
        # else:
        #     comment_form = CommentForm()
        
        context = {
            'product': product, 
            'images': images,
            'comment' : comment,
            # 'comment_form': comment_form
            }

        template = 'products/single.html'
        return render(request, template, context)
    except:
        raise Http404

def add_comment(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('single_product', slug=product.slug)
    else:
        form = CommentForm()
    return render(request, 'products/add_comment.html', {'form':form})



def aboutus(request):
    template = 'aboutus/aboutus.html'
    return render(request, template, {})
