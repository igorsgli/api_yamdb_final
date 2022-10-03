import django_filters

from reviews.models import Title, Genre, Category


class ModelFilter(django_filters.FilterSet):
    genre = django_filters.ModelChoiceFilter(field_name='genre__slug',
                                             to_field_name='slug',
                                             queryset=Genre.objects.all())

    category = django_filters.ModelChoiceFilter(field_name='category__slug',
                                                to_field_name='slug',
                                                queryset=Category.objects.all()
                                                )

    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
