import re

from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view

from buildings.models import BuildingFloorSpace
from buildings.serializers import BuildingFloorSpaceSerializer



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    # ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
    #     and grouping quoted words together.
    #     Example:
    #
    #     >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    #     ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    #
    # '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


@api_view(['GET'])
def search_indrz(request, campus_id, search_string):
    # query_string = ''
    # found_entries = None

    # if using a url like http://www.campus.com/search/?q=sometext
    # use this if statement and indent code block

    # if ('q' in request.GET) and request.GET['q'].strip():
    #     query_string = request.GET['q']

    entry_query = get_query(search_string, ['short_name', 'long_name', 'room_code', 'room_description'])

    # return only first 20 results
    found_entries = BuildingFloorSpace.objects.filter(fk_building__fk_campus=campus_id).filter(entry_query)[:20]

    # buildings_on_campus = BuildingFloorSpace.objects.filter(Q(short_name__icontains=search_string) | Q(room_code__icontains=search_string))
    serializer = BuildingFloorSpaceSerializer(found_entries, many=True)

    if found_entries:

        return Response(serializer.data)

    # elif:
    #     pass
        # return Response({'error': 'sorry nothing found with the text:  ' + search_string})

    else:
        return Response({'error': 'sorry nothing found with the text:  ' + search_string})

# old silly search
# @api_view(['GET'])
# def campus_search(request, campus_id, search_string, format=None):
#     """
#     Search campus spaces in system and pois
#     """
#     if request.method == 'GET':
#
#         buildings_on_campus = BuildingFloorSpace.objects.filter(Q(short_name__icontains=search_string) | Q(room_code__icontains=search_string))
#         serializer = BuildingFloorSpaceSerializer(buildings_on_campus, many=True)
#
#         return Response(serializer.data)

