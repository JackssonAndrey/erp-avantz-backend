from django.urls import path, include
from .views import (
    index, delete, store_person_physical, details_physical_person, find_physical_persons, find_legal_persons,
    store_legal_person, details_legal_person, edit_legal_person, edit_person_physical, find_providers,
    find_last_physical_person, find_last_providers
)

urlpatterns = [
    path('', index, name='list_all_persons'),
    path('delete/<int:id_person>', delete, name='delete_person'),

    path('physical/create/', store_person_physical,
         name='create_person_physical'),
    path('physical/details/<int:id_person>',
         details_physical_person, name='details_person'),
    path('physical', find_physical_persons, name='find_physical_persons'),
    path('physical/<str:personName>', find_physical_persons,
         name='find_physical_person_by_name'),
    path('physical/edit/<int:id_person>',
         edit_person_physical, name='edit_physical_persons'),
    path('physical/last/', find_last_physical_person,
         name='find_last_physical_person'),

    path('legal', find_legal_persons, name='find_legal_persons'),
    path('legal/<str:personName>', find_legal_persons,
         name='find_legal_person_by_name'),
    path('legal/create/', store_legal_person, name='store_legal_person'),
    path('legal/details/<int:id_person>',
         details_legal_person, name='details_legal_persons'),
    path('legal/edit/<int:id_person>',
         edit_legal_person, name='edit_legal_persons'),

    path('providers', find_providers, name='find_providers'),
    path('providers/last/', find_last_providers, name='find_last_providers')
]
