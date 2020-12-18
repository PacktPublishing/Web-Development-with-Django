#!/usr/bin/env python3

from reviews.models import Contributor

contributor = Contributor.objects.create(first_names='Rowel', last_names='Atienza', email='RowelAtienza@example.com')
