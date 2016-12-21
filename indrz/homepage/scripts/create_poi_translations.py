import psycopg2


conn2 = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur2 = conn2.cursor()


def generate_poi_translation_msgid():
    sel_building_floor_id = """SELECT f.cat_name FROM (
        SELECT DISTINCT ON (cat_name) cat_name, parent_id
        FROM django.poi_manager_poicategory) AS f ORDER BY parent_id DESC ;"""
    # print(sel_building_floor_id)

    cur2.execute(sel_building_floor_id)
    res_floor_id = cur2.fetchall()

    print(res_floor_id)

    with open('poi-trans.txt', 'w') as f:
        for r in res_floor_id:
            f.write('msgid "' + r[0] + '"')  #msgid "Public Infrastructure"
            f.write('\n')
            f.write('msgstr ""')
            f.write('\n\n')


def generate_poi_translation_template():
    sel_building_floor_id = """SELECT f.cat_name FROM (
        SELECT DISTINCT ON (cat_name) cat_name, parent_id
        FROM django.poi_manager_poicategory) AS f ORDER BY parent_id DESC ;"""
    # print(sel_building_floor_id)

    cur2.execute(sel_building_floor_id)
    res_floor_id = cur2.fetchall()

    print(res_floor_id)

    with open('poi-trans.html', 'w') as f:
        f.write('{% load i18n %}' + '\n\n')
        for r in res_floor_id:
            f.write('{% trans "' + r[0] + '" %}\n')  #msgid "Public Infrastructure"



generate_poi_translation_template()