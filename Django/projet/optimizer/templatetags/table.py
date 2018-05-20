from django import template
from django.template.defaultfilters import stringfilter
import pandas as pd
from django.conf import settings
import os
import csv

register = template.Library()

@register.assignment_tag
def print_table_html():
    path = os.path.join(settings.BASE_DIR, "resources/data.csv")
    return [line.rstrip('\n').split(',') for line in open(path)][1:]
