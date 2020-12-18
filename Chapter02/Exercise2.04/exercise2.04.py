#!/usr/bin/env python3

from datetime import date
from reviews.models import Book, Publisher

publisher = Publisher.objects.get(name='Packt Publishing')

book = Book.objects.create(title='Advanced Deep Learning with Keras', publication_date=date(2018, 10, 31),
                           isbn='9781788629416', publisher=publisher)
