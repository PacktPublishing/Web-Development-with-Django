#!/usr/bin/env python3

from reviews.models import Contributor

Contributor.objects.create(first_names='Peter', last_names='Wharton', email='PeterWharton@example.com')
Contributor.objects.create(first_names='Peter', last_names='Tyrrell', email='PeterTyrrell@example.com')
contributors = Contributor.objects.filter(first_names='Peter')
Contributor.objects.filter(first_names='Rowel')
Contributor.objects.filter(first_names='Nobody')

