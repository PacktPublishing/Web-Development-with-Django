#!/usr/bin/env python3

from reviews.models import Contributor


Contributor.objects.filter(last_names='Tyrrell').update(first_names='Mike')


Contributor.objects.get(last_names='Tyrrell').first_names