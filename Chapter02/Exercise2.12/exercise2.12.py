#!/usr/bin/env python3

from reviews.models import Contributor

contributor = Contributor.objects.get(first_names='Rowel')

contributor.book_set.all()
