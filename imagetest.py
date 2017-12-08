from PIL import Image
def imageAdjust(s):
        im = Image.open(s)
        (x,y) = im.size
        x_ = x
        y_ = y
        while x_ > 300:
            x_ /= 2
            y_ /= 2
        x_ = int(x_)
        y_ = int(y_)
        out = im.resize((x_, y_), Image.ANTIALIAS)
        out.save(s)
imageAdjust("D://dulux/sb.png")
