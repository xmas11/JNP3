JNP3
====

Jak odpalac:
============
Wrzucilem do repo 4 skrypty : run_service[1-4].sh .
Odpalamy je w trzech roznych konsolach, w takiej kolejnosci jak mowia numerki. Pamietajcie o odpowiednim srodowisku jak ktos korzysta z virtual env. Skrypty zadzialaja, jesli macie nastepujaca strukture katalogow:

costam/<br>
----JNP3/<br>
--------szachuj/ <br>
------------manage.py <br>
------------szach/ <br>
--------README.md <br>
--------run_service[1-4].sh <br>
----apache-solr-3.5.0/ <br>
----rabbitmq_server-3.2.2/ <br>

btw -> ktoś zmienił run_service2.sh, tak, że nie odpowiada on już tej strukturze katalogów.

Nowosci:
========

REST + indexedDB
Dodaj do koszyka - dodaje szachy do lokalnej bazy danych
Wyślij szachy - można przejrzeć jakie szachy są w lokalnej bazie danych, a później wysłać je na serwer.
Dodałem też przeglądanie w adminie szachów.

Dodałem varnish cache. Aby go zainstalować, należy odpalić skrypt install_varnish.sh z folderu varnish(skrypt jest dedykowany pod Ubuntu, więc Filip będziesz go musiał trochę zmodyfikować). run_service4.sh odpala proces varnish.
Wtedy nasz serwer jest dostępny pod localhost:4000(pod :8000 też, ale bez varnish cache) - varnish cache forwarduje odpowiednie requesty do serwera i wszystko działa niezależnie. 

Dodaje full-text-search. Korzystamy z Haystack, a z tylu dziala solr. Standardowo : pip install django-haystack


Instalacja i odpalanie solr (mozna trzymac gdziekolwiek, nie musi byc wewnatrz projektu:
Pierwszy akapit https://django-haystack.readthedocs.org/en/latest/installing_search_engines.html



Bede musial to troche poprawic, bo na razie wyszukiwanie nie dziala jakos rewelacyjnie.


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
