from django.db import models


class Szach(models.Model):
    """
        Main model for storing dips in database
    """

    subject = models.TextField(max_length=1024, blank=False)
    signature = models.TextField(max_length=128, blank=False)
    stamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Subject ' + self.subject + '\nSignature ' + \
               self.signature + '\n' + str(self.stamp)

    class Meta:
        ordering = ('stamp',)
