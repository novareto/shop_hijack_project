# -*- coding: utf-8 -*-

import transaction
from cromlech.browser import IPublicationRoot
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

from . import DB_KEY, Base
from .utils import view_lookup, Site
from .containers import Shops, Employees, Incidents


@implementer(IPublicationRoot)
class Root(Location):
    traversable('shops', 'employees', 'incidents')
    
    def __init__(self, name):
        self.name = name
        self.shops = Shops(self, 'shops')
        self.employees = Employees(self, 'employees')
        self.incidents = Incidents(self, 'incidents')

    def getSiteManager(self):
        return getGlobalSiteManager()


class Application(object):

    def __init__(self, global_conf, url, zcml, langs='en'):
        # load the ZCML
        load_zcml(zcml)

        # register the allowed languages
        register_allowed_languages([lang.strip() for lang in langs.split(',')])

        # create, register and populate the base DB/Engine
        engine = create_and_register_engine(url, DB_KEY)
        engine.bind(Base)

        # instanciate and keep the useful things
        self.root = Root()
        self.engine = engine
        self.publisher = DawnlightPublisher(view_lookup=view_lookup)

    def __call__(self, environ, start_response):
        request = Request(environ)
        with transaction.manager as tm:
            with Site(self.root) as root:
                with SQLAlchemySession(self.engine, transaction_manager=tm):
                    response = self.publisher.publish(
                        request, root, handle_errors=True)
        return response(environ, start_response)
