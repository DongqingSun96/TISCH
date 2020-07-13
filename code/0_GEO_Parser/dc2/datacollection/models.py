from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
import os
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)
from django.db.models.signals import m2m_changed


try:
    import json
except ImportError:
    import simplejson as json

PAPER_STATUS = (
    ('imported', 'paper entered awaiting datasets'),
    ('datasets', 'datasets imported awaiting download'),
    ('transfer', 'datasets download in progress'),
    ('downloaded', 'datasets downloaded awaiting analysis'),
    ('complete', 'analysis complete/complete'),
    ('error', 'error/hold- see comments'),
)

GENERAL_STATUS = (
    ('new', 'newly imported'),
    ('ok', 'validated'),
)


class DCModel(models.Model):
    """Implements common fns that will be inherited by all of the models
    NOTE: this is an ABSTRACT class, otherwise django will try to make a db
    for it.
    """

    class Meta:
        abstract = True

    def to_json(self):
        """Returns the model as a json string"""
        tmp = {}
        for k in list(self.__dict__.keys()):
            tmp[k] = "%s" % self.__dict__[k]
        return json.dumps(tmp)

class Papers(DCModel):
    """Papers are publications that are publicly available
    The fields are:
    pmid - the pubmed id of the publication
    unique_id - the unique identifier for an external db, e.g. GSEID
    user - the user who currated the dataset
    title - the title of the publication
    reference - shorthand of the publication details
    abstract - the abstract of the publication
    pub_date - the publication date
    authors - list of the paper's authors
    last_aut_email - the email address of the last/corresponding author
    journal- paper's journal

    status- SEE PAPER_STATUS above
    comments- any comments about this paper
    """
    #def __init__(self, *args):
    #    super(Papers, self).__init__(*args)
    #    self._meta._donotSerialize = ['user']
    class Meta:
        verbose_name_plural = 'papers'

    pmid = models.IntegerField(null=True, blank=True, default=None)
    #NOTE: papers can have multiple unique_ids attached--if so, comma-sep them
    unique_id = models.CharField(max_length=255, null=True, blank=True, default="")
    # user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True, default="")
    reference = models.CharField(max_length=255, null=True, blank=True, default="")
    abstract = models.TextField(null=True, blank=True, default="")
    pub_date = models.DateField(null=True, blank=True, default=None)
    date_collected = models.DateTimeField(null=True, blank=True, default=None)
    authors = models.CharField(max_length=1000, null=True, blank=True, default="")
    last_auth_email = models.EmailField(null=True, blank=True, default=None)

    journal = models.ForeignKey('Journals', on_delete=models.CASCADE,
                                null=True, blank=True, default=None)
    status = models.CharField(max_length=255, choices=PAPER_STATUS,
                              null=True, blank=True, default="imported")
    #a place for curators to add comments

    comments = models.TextField(null=True, blank=True, default="")

    def _get_lab(self):
        """Returns the last author in the authors list"""
        try:
            return smart_str(self.authors.split(",")[-1:][0]).strip()
        except:
            return smart_str(self.authors).strip()


    lab = models.CharField(max_length=1000, null=True, blank=True, default="")

    pub_summary = models.CharField(max_length=1000, null=True, blank=True, default="")
    # a dirty trick to print first author, journal, and pub_date

    def __str__(self):
        return smart_str(self.title)

class Journals(DCModel):
    """Journals that the papers are published in"""

    class Meta:
        verbose_name_plural = 'journals'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    issn = models.CharField(max_length=9, null=True, blank=True, default="")
    impact_factor = models.FloatField(default=0.0, null=True)

    def __str__(self):
        return smart_str(self.name)


class CellTypes(DCModel):
    """Sample's tissue/cell type, e.g. embryonic stem cell, b lymphocytes, etc.
    """

    class Meta:
        verbose_name_plural = 'cell types'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True, default='new', choices=GENERAL_STATUS)

    #tissue_type = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return smart_str(self.name)
    comments = models.CharField(max_length=255, null=True, blank=True, default="")
    aliases =   models.CharField(max_length=255, null=True, blank=True, default=None)

class CellLines(DCModel):
    """Sample's cell lines.  I really don't know what distinguishes
    cell lines from cell populations or strains and mutations, but i'm going
    to create the tables just to be inclusive
    """

    class Meta:
        verbose_name_plural = 'cell lines'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True, default='new', choices=GENERAL_STATUS)

    def __str__(self):
        return smart_str(self.name)
    comments = models.CharField(max_length=255, null=True, blank=True, default="")
    aliases =   models.CharField(max_length=255, null=True, blank=True, default=None)

class TissueTypes(DCModel):
    """Tissue Types"""

    class Meta:
        verbose_name_plural = 'tissues'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True, default='new', choices=GENERAL_STATUS)
    comments = models.CharField(max_length=255, null=True, blank=True, default="")
    def __str__(self):
        return smart_str(self.name)
    aliases =   models.CharField(max_length=255, null=True, blank=True, default=None)

class CellPops(DCModel):
    class Meta:
        verbose_name_plural = 'cell populations'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True, default='new', choices=GENERAL_STATUS)

    def __str__(self):
        return smart_str(self.name)
    comments = models.CharField(max_length=255, null=True, blank=True, default="")
    aliases =   models.CharField(max_length=255, null=True, blank=True, default=None)



class DiseaseStates(DCModel):
    """Information field for datasets"""

    class Meta:
        verbose_name_plural = 'disease states'

    name = models.CharField(max_length=255, null=True, blank=True, default="")
    comments = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True, default='new', choices=GENERAL_STATUS)
    def __str__(self):
        return smart_str(str(self.name))
    aliases =   models.CharField(max_length=255, null=True, blank=True, default=None)

