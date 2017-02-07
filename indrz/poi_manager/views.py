import collections

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view

from poi_manager.models import PoiCategory, Poi
from poi_manager.forms import PoiCategoryForm, PoiForm
from poi_manager.serializers import PoiSerializer, PoiCategorySerializer

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm
from mptt.templatetags.mptt_tags import cache_tree_children


def poi_category_list(request, campus_id, format=None):
    return render(request, "poi/poi-category.html",
                  {'nodes': PoiCategory.objects.filter(enabled=True)})


@api_view(['GET', ])
def get_poi_by_id(request, campus_id, poi_id, format=None):
    try:
        poi_qs = Poi.objects.filter(fk_campus=campus_id).filter(id=poi_id).filter(enabled=True)
        serializer = PoiSerializer(poi_qs, many=True)
        return Response(serializer.data)

    except Exception as e:
        raise APIException(detail=e)


@api_view(['GET', ])
def poi_category_json(request, campus_id, format=None):
    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = node.cat_name
        result['icon'] = node.icon_css_name

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(enabled=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return Response(dicts)


@api_view(['GET', ])
def get_poi_by_category(request, campus_id, category_name, format=None):
    if request.method == 'GET':
        try:
            cats = PoiCategory.objects.filter(enabled=True).get(cat_name__contains=category_name)

            if cats:

                poi_qs = Poi.objects.filter(fk_poi_category=cats.id).filter(enabled=True)
                if poi_qs:
                    serializer = PoiSerializer(poi_qs, many=True)
                    return Response(serializer.data)
        except Exception as e:
            raise APIException(detail=e)


@api_view(['GET', ])
def get_poi_by_cat_id(request, campus_id, cat_id, format=None):
    if request.method == 'GET':

        poicat_qs = PoiCategory.objects.filter(enabled=True).get(pk=cat_id)
        cat_children = PoiCategory.objects.add_related_count(poicat_qs.get_children(),Poi,'fk_poi_category', 'cat_name')

        poi_ids = []

        for x in poicat_qs.get_children():
            poi_ids.append(x.id)

        qs_objs = Poi.objects.filter(fk_poi_category_id__in=poi_ids).filter(enabled=True)

        if cat_children:
            serializer = PoiSerializer(qs_objs, many=True)
            return Response(serializer.data)
        elif len(poi_ids)==0:
            qs = Poi.objects.filter(fk_poi_category_id = cat_id).filter(enabled=True)
            serializer = PoiSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'something booomed with category id : ' + cat_id})


@api_view(['GET', ])
def get_poi_by_cat_name(request, campus_id, category_name, format=None):
    cats = PoiCategory.objects.filter(cat_name__icontains=category_name).filter(enabled=True)
    # list = cats.get_descendants()


    # from itertools import chain
    # result_list = list(chain(page_list, article_list, post_list))

    if cats:
        if len(cats) > 1:
            qs = []
            for cat in cats:
                poi_qs = Poi.objects.filter(fk_poi_category=cat.id).filter(enabled=True)
                qs.append(poi_qs)

        else:
            poi_qs = Poi.objects.filter(fk_poi_category=cats[0].id).filter(enabled=True)
    else:
        # return Response({'error': 'No Poi found with the given category name: ' + category_name} )
        return Response({'error': 'no category found with the given category name: ' + category_name})

    if poi_qs:
        serializer = PoiSerializer(poi_qs, many=True)

        return Response(serializer.data)

    else:
        return Response({'error': 'sorry no poi entries found assigned to the category name : ' + category_name})


@api_view(['GET', ])
def get_poicat_by_id(request, campus_id, cat_id, format=None):
    cats = PoiCategory.objects.filter(enabled=True).get(pk=cat_id)
    serializer = PoiCategorySerializer(cats)
    return Response(serializer.data)


@api_view(['GET', ])
def poi_category_by_name(request, campus_id, category_name, format=None):
    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = node.cat_name
        result['icon'] = node.icon_css_name

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(cat_name__icontains=category_name).filter(enabled=True))
    dicts = []
    if root_nodes:

        for n in root_nodes:
            dicts.append(recursive_node_to_dict(n))

        return Response(dicts)
    else:
        return Response({'error': 'no category found with the name : ' + category_name})


@api_view(['GET', ])
def poi_list(request, campus_id, format=None):
    try:
        poi_qs = Poi.objects.filter(enabled=True)
        serializer = PoiSerializer(poi_qs, many=True)
        return Response(serializer.data)

    except Exception as e:
        raise APIException(detail=e)


@api_view(['GET', ])
def poi_by_name(request, campus_id, poi_name, format=None, **kwargs):
    poi_qs = Poi.objects.filter(fk_campus=campus_id).filter(name__icontains=poi_name).filter(enabled=True)
    floor = request.GET.get('floor')

    if floor:
        poi_qs = Poi.objects.filter(fk_campus=campus_id).filter(name__icontains=poi_name).filter(floor_num=floor).filter(enabled=True)

    if poi_qs:
        att = poi_qs.values()
        print(att)

        poi_entries = []

        for value in att:
            poi_entries.append(value)

        return Response(poi_entries)
    else:
        return Response({'error': 'something went wrong no POI with that name found'})


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = PoiCategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return poi_category_list(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = PoiCategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'poi/add-poi-category.html', {'form': form})


def add_poi(request, category_name_slug):
    try:
        cat = PoiCategory.objects.get(slug=category_name_slug)
    except PoiCategory.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PoiForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return poi_category_list(request)
        else:
            print(form.errors)
    else:
        form = PoiForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'poi/add-poi.html', context_dict)


def move_category(request, category_pk):
    category = get_object_or_404(PoiCategory, pk=category_pk)
    if request.method == 'POST':
        form = MoveNodeForm(category, request.POST)
        if form.is_valid():
            try:
                category = form.save()
                return HttpResponseRedirect(category.get_absolute_url())
            except InvalidMove:
                pass
    else:
        form = MoveNodeForm(category)

    return render_to_response('poi/poi-form.html', {
        'form': form,
        'category': category,
        'category_tree': PoiCategory.objects.all(),
    })
