from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import fields

class Gearbox(models.Model):

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    manufacturer = models.CharField(max_length=200)
    image = models.ManyToManyField('polls.Image')
    description = models.TextField(blank=True)
    compatible_to = models.ManyToManyField('polls.WEC_Typ')
    weight_t = models.IntegerField(blank=True, null=True, verbose_name='Weight [t]')

    ratio = models.IntegerField(blank=True, null=True)
    stages = models.IntegerField(blank=True, null=True)

    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def compatibleWEC(self):
        return self.compatible_to.all()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('components:gearbox_detail', args=[self.id, self.slug])

class Generator(models.Model):

    GEN_TYPE = (('Asynchronous', 'Asyncronous'),
                ('Double fed induction generator', 'Double fed induction generator'),
                ('Seperate-exited synchronous', 'Seperate-exited synchronous'),
                ('Self-exited synchronous', 'Self-exited synchronous'))

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    manufacturer = models.CharField(max_length=200)
    image = fields.GenericRelation('polls.Image')
    description = models.TextField(blank=True)
    compatible_to = models.ManyToManyField('polls.WEC_Typ')
    weight_t = models.IntegerField(blank=True, null=True, verbose_name='Weight [t]')

    generator_type = models.CharField(max_length=20, choices=GEN_TYPE, default='Asynchronous')
    voltage = models.IntegerField(blank=True, null=True)
    rpm = models.IntegerField(blank=True, null=True)

    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def compatibleWEC(self):
        return self.compatible_to.all()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('components:gearbox_detail', args=[self.id, self.slug])

class Tower(models.Model):

    TOWER = (('Lattice', 'Lattice'),
            ('Concrete', 'Concrete'),
            ('Hybrid', 'Hybrid'),
            ('Wood', 'Wood'))

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    manufacturer = models.CharField(max_length=200)
    image = models.ManyToManyField('polls.Image')
    description = models.TextField(blank=True)
    compatible_to = models.ManyToManyField('polls.WEC_Typ')
    weight_t = models.IntegerField(blank=True, null=True, verbose_name='Weight [t]')

    tower_type = models.CharField(max_length=20, choices=TOWER, default='Hybrid')

    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def compatibleWEC(self):
        return self.compatible_to.all()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('components:gearbox_detail', args=[self.id, self.slug])
