# -*- coding: utf-8 -*-


from cromlech.configuration.utils import load_zcml
from cromlech.i18n import register_allowed_languages
from cromlech.dawnlight import DawnlightPublisher
from cromlech.browser import PublicationBeginsEvent, PublicationEndsEvent
from cromlech.browser import IPublicationRoot
from zope.interface import implements
from zope.location import Location
from zope.component.hooks import setSite
from zope.event import notify
from cromlech.webob.request import Request
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from zope.component import getGlobalSiteManager


def configuration(global_conf, zcml_file, langs):
    """A factory for the configuration middleware.
    It's usually used to initialize some parameters,
    register components and possibly wrap the requested
    apps.
    """

    load_zcml(zcml_file)

    allowed = langs.strip().replace(',', ' ').split()
    register_allowed_languages(allowed)

    def app_wrapper(app):
        """The effective middleware. Here, we do not make use
        of the wrapping capabilities, but it can be used to
        add other explicit middlewares.
        """
        return app

    return app_wrapper

view_lookup = ViewLookup(view_locator(query_view))


class Site(Location):
    implements(IPublicationRoot)

    title = u"Example Site"
    description = u"An Example application."

    def __init__(self, name):
        self.name = name

    def getSiteManager(self):
        return getGlobalSiteManager()


def app(global_conf, name, zcml_file=None, **kwargs):
    """A factory used to bootstrap the TrajectApplication.
    As the TrajectApplication will use SQL, we use this
    'once and for all' kind of factory to configure the
    SQL connection and inject the demo datas.
    """
    if zcml_file:
        load_zcml(zcml_file)

    def publisher(environ, start_response):
        request = Request(environ)
        site = Site(name)
        setSite(site)
        notify(PublicationBeginsEvent(site, request))
        publisher = DawnlightPublisher(view_lookup=view_lookup)
        response = publisher.publish(request, site, handle_errors=True)
        notify(PublicationEndsEvent(request, response))
        setSite()
        return response(environ, start_response)
    return publisher
