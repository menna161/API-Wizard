import logging
import functools
import sublime
import sublime_plugin
from .network import Network
from .variables import sublime_ip, ip
from .html_helper import Html


def get_network(self, networks, find_all=False):
    search_networks = {Network.get(n) for n in networks.split(',')}
    current_regions = self.view.sel()
    logger.debug('Searching for network(s) {}'.format(networks))
    for network in search_networks:
        if (not network):
            message = 'Invalid network {}'.format(network)
            logger.debug(message)
            self.view.show_popup_menu(message)
            return
    else:
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(0, 0))
        found_regions = self.view.find_all(sublime_ip.v4.any, sublime.IGNORECASE)
        matching_networks = set()
        found_networks = {self.view.substr(r) for r in found_regions}
        logger.debug('Found {} IP like objects'.format(len(found_networks)))
        for found_network in found_networks:
            if (found_network in matching_networks):
                continue
            logger.debug('Getting network "{}"'.format(found_network))
            for search_network in search_networks:
                network_object = Network.get(found_network)
                if (network_object and Network.contains(search_network, network_object)):
                    matching_networks.add(found_network)
                    break
        self.view.sel().clear()
        if matching_networks:
            moved_view = False
            for region in found_regions:
                cleaned_region = Network.clean_region(self.view, region)
                if (self.view.substr(cleaned_region) in matching_networks):
                    self.view.sel().add(cleaned_region)
                    if (not moved_view):
                        self.view.show_at_center(cleaned_region.begin())
                        moved_view = True
        else:
            logger.debug('No matches')
            self.view.sel().add_all(current_regions)
            self.view.show_at_center(current_regions[0].begin())
