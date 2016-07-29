from django.shortcuts import render


def view_map(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        map_name = kwargs.pop('map_name', None)
        building_id, = request.GET.get('buildingid', 1),
        space_id, = request.GET.get('spaceid', 0),
        zoom_level, = request.GET.get('zlevel', 18),
        route_from, = request.GET.get('route_from', ''),
        route_to, = request.GET.get('route_to', ''),
        centerx, = request.GET.get('centerx', 0),
        centery, = request.GET.get('centery', 0),
        floor_num, = request.GET.get('floor', 0),

        context.update({
            'map_name': map_name,
            'building_id': building_id,
            'space_id': int(space_id),
            'zoom_level': zoom_level,
            'route_from': route_from,
            'route_to': route_to,
            'centerx':  float(centerx),
            'centery': float(centery),
            'floor_num': int(floor_num)
        })

    return render(request, context=context, template_name='map.html')
