# -*- coding: utf-8 -*-

from cromlech.configuration.utils import load_zcml
from cromlech.i18n import register_allowed_languages
from cromlech.dawnlight import DawnlightPublisher
from cromlech.browser import PublicationBeginsEvent, PublicationEndsEvent
from cromlech.browser import IPublicationRoot
from zope.interface import implements
from zope.location import Location
from zope.event import notify
from cromlech.webob.request import Request
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from zope.component import getGlobalSiteManager
from ..utils import view_lookup, Site


class Root(Location):
    implements(IPublicationRoot)

    title = u"Example Site"
    description = u"An Example application."

    def __init__(self, name):
        self.name = name

    def getSiteManager(self):
        return getGlobalSiteManager()
        

class Application(object):

    def __init__(self, global_cond, name, zcml_file, langs='en'):
        # We register our SQLengine under a given name
        engine = create_and_register_engine(url, name)
        
        # We bind out SQLAlchemy definition to the engine
        engine.bind(Library)

        # We now instanciate the TrajectApplication
        # The name and engine are passed, to be used for the querying.
        self.name = name
        self.engine = engine
        self.publisher = DawnlightPublisher(view_lookup=view_lookup)
        
        # We register our Traject patterns.
        # TODO

        return app

    def __call__(self, environ, start_response):
        with SQLAlchemySession(self.engine):
            with transaction.manager:
                with Interaction():
                    # todo
