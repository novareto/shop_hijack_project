# -*- coding: utf-8 -*-

import transaction
from cromlech.browser import IPublicationRoot, PublicationBeginsEvent
from cromlech.configuration.utils import load_zcml
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight.directives import traversable
from cromlech.i18n import register_allowed_languages
from cromlech.sqlalchemy import SQLAlchemySession
from cromlech.sqlalchemy import create_and_register_engine
from cromlech.webob.request import Request
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.location import Location
from cromlech.security import Interaction
from zope.event import notify

from . import DB_KEY, Base
from .utils import view_lookup, Site
from .models import Shop, Employee, Incident
from .containers import ShopsRoot, EmployeesRoot, IncidentsRoot


@implementer(IPublicationRoot)
class Root(Location):
    traversable('shops', 'employees', 'incidents')

    def __init__(self):
        self.shops = ShopsRoot(self, 'shops', Shop)
        self.employees = EmployeesRoot(self, 'employees', Employee)
        self.incidents = IncidentsRoot(self, 'incidents', Incident)

    def getSiteManager(self):
        return getGlobalSiteManager()


ROOT = Root()


class Application(object):

    def __init__(self, engine):
        self.engine = engine
        self.publisher = DawnlightPublisher(view_lookup=view_lookup)

    def __call__(self, environ, start_response):
        request = Request(environ)
        with transaction.manager as tm:
            with Interaction():
                with Site(ROOT) as root:
                    with SQLAlchemySession(self.engine, transaction_manager=tm):
                        notify(PublicationBeginsEvent(root, request))
                        response = self.publisher.publish(
                            request, root, handle_errors=True)
                        result = response(environ, start_response)
        return result


def app_factory(global_conf, url, zcml, langs):
    # load the ZCML
    load_zcml(zcml)

    # register the allowed languages
    register_allowed_languages([lang.strip() for lang in langs.split(',')])

    # create, register and populate the base DB/Engine
    engine = create_and_register_engine(url, DB_KEY)
    engine.bind(Base)
    Base.metadata.create_all()
    return Application(engine)
