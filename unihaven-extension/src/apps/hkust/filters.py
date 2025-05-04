import django_filters
from django.db.models import Q, F, Func, Value, FloatField, Case, When
from django.utils import timezone
from .models import Accommodation

class AccommodationFilter(django_filters.FilterSet):
    
    available_from = django_filters.DateFilter(
        method='filter_availability',
        label='Available From (YYYY-MM-DD)'
    )
    
    available_to = django_filters.DateFilter(
        method='filter_availability',
        label='Available To (YYYY-MM-DD)'
    )

    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    campus = django_filters.CharFilter(
        method='filter_by_campus',
        label='Distance To HKUST Campus (Ascending Order)'
    )


    class Meta:
        model = Accommodation
        fields = [
            "type",
            "number_of_beds", 
            "number_of_bedrooms", 
        ]

    def filter_availability(self, queryset, name, value):
        
        available_from = self.data.get('available_from')
        available_to = self.data.get('available_to')
        
        queryset = queryset.filter(
            availability_start__lte=F('availability_end')
        )
        

        if available_from and available_to:

            if isinstance(available_from, str):
                available_from = timezone.datetime.strptime(available_from, '%Y-%m-%d').date()
            if isinstance(available_to, str):
                available_to = timezone.datetime.strptime(available_to, '%Y-%m-%d').date()
            if available_from > available_to:
                return queryset.none()
            
            return queryset.filter(
                availability_start__lte=available_from,
                availability_end__gte=available_to
            )
        
        if name == 'available_from' and value:
            return queryset.filter(availability_start__lte=value, availability_end__gte=value)
        elif name == 'available_to' and value:
            return queryset.filter(availability_end__gte=value, availability_start__lte=value)
        
        return queryset

    def filter_by_campus(self, queryset, name, value):
        HKUST_CAMPUSES = {
            "Main Campus": "Main Campus",
        }

        # Check if the selected campus is valid
        if value in HKUST_CAMPUSES:
            campus_name = HKUST_CAMPUSES[value]

            # Filter and sort accommodations in Python
            def extract_distance(accommodation):
                distances = {}
                for entry in accommodation.distance:
                    if campus_name in entry:
                        print (entry)
                        # Extract the numeric distance from the string
                        try:
                            parts = entry.split(" ")
                            print("parts:", parts)
                            dis = float(parts[-2])
                            print("dis:", dis)
                            distances[campus_name] = dis
                        except (IndexError, ValueError) as e:
                            print(f"Error parsing entry: {entry}, Error: {e}")
                            distances[campus_name] = float('inf')
                print(f"Distances dictionary: {distances}")
                return distances

            def get_selected_campus_distance(accommodation):
                distances = extract_distance(accommodation)
                return distances.get(campus_name, float('inf'))

            sorted_accommodations = sorted(queryset, key=get_selected_campus_distance)
            print("Sorted accommodations:", sorted_accommodations)

            sorted_ids = [accommodation.property_id for accommodation in sorted_accommodations]
            print("Sorted IDs:", sorted_ids)
            preserved_order = Case(*[When(property_id=pk, then=pos) for pos, pk in enumerate(sorted_ids)])
            return queryset.filter(property_id__in=sorted_ids).order_by(preserved_order)
        
        return queryset
        
        
