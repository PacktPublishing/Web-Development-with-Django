#!/usr/bin/env python3

from reviews.models import Contributor

Contributor.objects.get(last_names='Wharton').delete()

Contributor.objects.get(last_names='Wharton')
