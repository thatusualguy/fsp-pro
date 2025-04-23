from django.shortcuts import render


def index(request):
    return render(
        request,
        "rc_app/public/index.html",
        {
            "title_feature": "Что умеет?",
            "features": [
                {
                    "icon_path": "/icon/icon_cursor.svg",
                    "title": "Автоматизация заявок и регистрации",
                    "description": "Платформа позволяет подавать, редактировать и отслеживать заявки на соревнования в пару кликов"
                },
                {
                    "icon_path": "/icon/icon_collection.svg",
                    "title": "Система управления командами",
                    "description": "Легко формировать команды, приглашать участников, находить команду единомышленников"
                },
                {
                    "icon_path": "/icon/icon_speaker.svg",
                    "title": "Прозрачные результаты и рейтинги",
                    "description": "После каждого соревнования обновляется профиль спортсмена: отображаются участие, баллы, победы и история активности — формируется рейтинг"
                },
                {
                    "icon_path": "/icon/icon_web.svg",
                    "title": "Соревнования из любой точки России",
                    "description": "Соревнования по пяти дисциплинам, в любом регионе страны. Мгновенно найти нужное событие по дате, формату и месту проведения"
                }
            ],
            "title_soon": "Скоро",
            "soon_events": [
                {
                    "link": "#event1",
                    "date": "12 <span>мая</span>",
                    "title": "Кубок России по продуктовому программированию"
                },
                {
                    "link": "#event2",
                    "date": "23 <span>мая</span>",
                    "title": "Финал Кубка России по продуктовому программированию"
                }
            ],
            "actions": [
                {
                    "link": "#action1",
                    "icon": "/icon/icon_world.svg",
                    "title": "Найти открытые соревнования"
                },
                {
                    "link": "#action2",
                    "icon": "/icon/icon_add_person.svg",
                    "title": "Присоединиться к команде"
                },
                {
                    "link": "#action3",
                    "icon": "/icon/icon_teams.svg",
                    "title": "Создать команду"
                }
            ],
            "regions": [
                {
                    "link": "/app/region/moscow/",
                    "title": "Москва",
                    "description": ""
                },
                {
                    "link": "/app/region/CFD/",
                    "title": "ЦЕНТРАЛЬНЫЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "17 областей"
                },
                {
                    "link": "/app/region/SFD/",
                    "title": "ЮЖНЫЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "8 областей"
                },
                {
                    "link": "/app/region/NWFD/",
                    "title": "СЕВЕРО-ЗАПАДНЫЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "17 областей"
                },
                {
                    "link": "/app/region/FEFD/",
                    "title": "ДАЛЬНЕВОСТОЧНЫЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "17 областей"
                },
                {
                    "link": "/app/region/NCFD/",
                    "title": "СЕВЕРО-КАВКАЗСКИЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "17 областей"
                },
                {
                    "link": "/app/region/VFD/",
                    "title": "ПРИВОЛЖСКИЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "14 областей"
                },
                {
                    "link": "/app/region/UFD/",
                    "title": "УРАЛЬСКИЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "6 областей"
                },
                {
                    "link": "/app/region/SibFD/",
                    "title": "СИБИРСКИЙ ФЕДЕРАЛЬНЫЙ ОКРУГ",
                    "description": "10 областей"
                },
                {
                    "link": "/app/region/NR/",
                    "title": "НОВЫЕ РЕГИОНЫ",
                    "description": "4 области"
                }
            ],
            "current_filters": {
                "type": "online",
                "region": "all",
                "date": None
            },
            "competitions_by_month": [
                {
                    "name": "Май",
                    "events": [
                        {
                            "id": "prod-cup-may",
                            "day": 12,
                            "title": "Кубок России по продуктовому программированию",
                            "url": "/app/competition/prod-cup-may/",
                            "badges": [
                                {"text": "Регистрация началась", "type": "status-registration"},
                                {"text": "Онлайн", "type": "type-online"}
                            ],
                            "meta": None,
                            "event_type": "online",
                            "event_region": "all"
                        },
                        {
                            "id": "prod-cup-final-may",
                            "day": 23,
                            "title": "Финал Кубка России по продуктовому программированию",
                            "url": "/app/competition/prod-cup-final-may/",
                            "badges": [],
                            "meta": "Москва",
                            "event_type": "unknown",
                            "event_region": "msk"
                        }
                    ]
                },
                {
                    "name": "Июнь",
                    "events": []
                }
            ]
        }
    )


def competitions_detail(request, slug):
    return render(request, 'rc_app/public/competitions_detail.html')


def regions_detail(request, slug):
    return render(request, 'rc_app/public/regions_detail.html')


def login(request):
    return render(request, 'rc_app/login/login.html')