from django.db import models
from django.core.urlresolvers import reverse

class ComponentType(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'component_type'
        verbose_name_plural = 'component_types'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('components:component_list_by_component_type', args=[self.slug])

class Component(models.Model):

    TOWER = (('Lattice', 'Lattice'),
            ('Concrete', 'Concrete'),
            ('Hybrid', 'Hybrid'),
            ('Wood', 'Wood'))

    GEN_TYPE = (('Asynchronous', 'Asyncronous'),
                ('Double fed induction generator', 'Double fed induction generator'),
                ('Seperate-exited synchronous', 'Seperate-exited synchronous'),
                ('Self-exited synchronous', 'Self-exited synchronous'))

    component_type = models.ForeignKey(ComponentType, related_name='components')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    manufacturer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='components/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    compatible_to = models.ManyToManyField('polls.WEC_Typ')

    weight_t = models.IntegerField(blank=True, null=True)

    ratio = models.IntegerField(blank=True, null=True)
    stages = models.IntegerField(blank=True, null=True)

    tower_type = models.CharField(max_length=20, choices=TOWER, default='Hybrid', verbose_name='Tower_type')

    generator_type = models.CharField(max_length=20, choices=GEN_TYPE, default='Asynchronous', verbose_name='Generator_type')
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
        return reverse('components:component_detail', args=[self.id, self.slug])