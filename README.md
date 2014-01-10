JNP3
====

Nowosci:
========

Dodalem raabitMQ, i nawet dziala. Mozna sobie dodawac szachy.
Jesli chcecie odpalic u siebie na kompie:
Trzeba miec rabitMQ i miec odpalony proces z programem rabitmq-server (sudo jest potrzebne)
Przed odpaleniem './manage.py runserver' w osobnej konsoli odpalic './manage.py database_receiver'.
   Ta ostatnia komenda odpala proces, ktory pobiera dane z kolejki i wrzuca do bazy danych.

Calosc wiec dziala juz asynchronicznie

Ustalenia co do projektu:
=========================

Korzystamy z Django 1.6

Korzystamy z Python 2.7


Sugeruje korzystac z virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

Sugeruje korzystac z ipython: pip install ipython

Opis projektu:
==============

zaszachuj.pl - serwis który pozwala coś zaszachować i się pod tym podpisać. Dla ludzi nieobeznanych z tematem - można na to patrzeć jak na stronkę w której dodaje się krotki: "<podpis, tekst>", które są publicznie dostępne. Wydaje mi się, że te krotki wystarczą na wykorzystanie wszystkich feature'ów.
