#!/usr/bin/env python3

from reviews.models import Publisher

publisher = Publisher(name='Packt Publishing', website='https://www.packtpub.com', email='info@packtpub.com')
publisher.save()
publisher.email = 'customersupport@packtpub.com'
publisher.save()