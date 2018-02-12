from PIL import Image, ExifTags
import sys

orientations = {3: 180, 6: 270, 8: 90}
for orientation_key in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation_key] == 'Orientation':
        break


for infile in sys.argv[1:]:
    try:
        img = Image.open(infile)
        exif = dict(img._getexif().items())
        img = img.rotate(orientations[exif[orientation_key]], expand=True)
        img.save(infile)
        img.close()
    except IOError as e:
        if e.message == "cannot identify image file '%s'" % infile:
            print infile, " is not an image file...skipping"
    except KeyError as e:
        if e.message == 274:
            pass # This image doesn't have rotation set. Hopefully it's good.
    except AttributeError as e:
        if e.message == "NoneType' object has no attribute 'items":
            pass # This image doesn't have any exif data
    except Exception as e:
        print "Got an unexpected error: ", e
