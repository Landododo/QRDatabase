from django.db import models

# Create your models here.
class gds_files(models.Model):
    # all values in um if not noted
    file_name = models.CharField(max_length=50)
    num_qrs = models.IntegerField()
    qr_size = models.FloatField()
    qrs_per_row = models.IntegerField()
    qrs_per_col = models.IntegerField()
    spacing = models.FloatField()
    padding = models.FloatField()
    time_uploaded = models.CharField(max_length=50)
    last_updated = models.CharField(max_length=50)

    def __str__(self):
        return(self.file_name + " for a "+\
               self.qrs_per_row + "x" + self.qrs_per_col+" grid")
    
class sample_images(models.Model):
    """gds_file_id: the id of the gds file that the sample image is part of,
    file_name = name of image file,
    width = width of image in pixels,
    height = height in pixels,
    row = row of the qr code that is being highlighted by this part of database (starts with row 0 and 0,0 is in bottom left of grid),
    col = col of the qr code that is being highlighted by this part of database (starts with col 0 and 0,0 is in bottom left of grid),
    abs_x = absolute x value of the qr code (bottom left corner),
    abs_y = absolute y value of the qr code (bottom left corner),
    num_codes = number of codes in the image,
    img_id = a unique image id, with this id being shared by all qr codes in the image in the database"""
    gds_file_id = models.IntegerField()
    file_name = models.CharField(max_length = 50)
    width = models.IntegerField()
    height = models.IntegerField()
    row = models.IntegerField()
    col = models.IntegerField()
    abs_x = models.FloatField()
    abs_y = models.FloatField()
    num_codes = models.IntegerField()
    img_id = models.IntegerField()
    is_anchor = models.IntegerField()