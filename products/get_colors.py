# from PIL import Image, ImageDraw
# import numpy as np
# import matplotlib.pyplot as plt


# def get_colors(infile, outfile, numcolors=3, swatchsize=100, resize=150):

#     image = Image.open(infile)
#     image = image.resize((resize, resize))
    
#     # crop photo
#     width, height = image.size # get dimensions
    
#     newSize = 100
#     left = (width - (width-newSize))/2
#     top = (height - (height-newSize))/2
#     right = (width + (width-newSize))/2
#     bottom = (height + (height-newSize))/2
#     image = image.crop((left, top, right, bottom))
    
#     result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
#     result.putalpha(0)
#     colors = result.getcolors(resize*resize)

#     # Save colors to file
    

#     pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
#     draw = ImageDraw.Draw(pal)

#     posx = 0
#     for count, col in colors:
#         draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
#         posx = posx + swatchsize
#         print(col)

#     del draw
#     pal.save(outfile, "PNG")
    
#     #show color
    
#     cols = np.asarray(col)
#     cols = np.delete(cols, -1)
#     print(cols)
#     plt.imshow(cols.reshape(1,1,3))


image = Image.open(image_path)
quantized = image.quantize(colors=5, kmeans=3)
palette = quantized.getpalette()[:15]
print palette

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        infile = fs.url(filename)
        # return render(request, 'products/upload.html', {
        #     'infile': infile
        # })

        def get_colors(infile, outfile, numcolors=3, swatchsize=100, resize=150):

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

            result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
            result.putalpha(0)
            colors = result.getcolors(resize*resize)

            # Save colors to file
            pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
            draw = ImageDraw.Draw(pal)

            posx = 0
            for count, col in colors:       
                draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
                posx = posx + swatchsize
                print(col)

            del draw
            pal.save(outfile, "PNG")

            # end
  
        return render(request, 'products/upload.html', {})
    return render(request, 'products/upload.html', {})

def lighter(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([255, 255, 255])
    vector = white-color
    return color + vector * percent


Here is a function from my gist to lighten any color that I think will work with any color format known to  matplotlib. I think setting an amount > 1 might darken too.

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    # get the shades
def get_colors(infile):
    # set number of outputted colors, size, and resize
    numcolors=5
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
    # # Save colors to file
    # pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    # draw = ImageDraw.Draw(pal)

    shades = []
    posx = 0
    for count, col in colors:
        # draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        # posx = posx + swatchsize
        shades.append(col[0:-1])

    return shades

def range(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([255, 255, 255])
    vector = white-color
    shade = color + vector * percent
    a = []
    for val in shade:
        a.append(int(val))
    return tuple(a)

def color_match(request):
    color = request.session['shades']
    value = []
    for val in color:
        a = range(val, .20) # lighter
        b = range(val, .100) # darker
        value.append(tuple(val)) # original
        value.append(a)
        value.append(b)
    query = Product.objects.filter(rgb__in=value)    
    context = { 'query':query }
    return render(request,'products/colorMatch.html',context)
