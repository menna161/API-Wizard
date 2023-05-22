import logging
import functools
import sublime
import sublime_plugin
from .network import Network
from .variables import sublime_ip, ip
from .html_helper import Html


def get_network(self, network, find_all=False):
    search_network = Network.get(network)
    current_regions = self.view.sel()
    logger.debug('Searching for network {}'.format(search_network))
    if (not search_network):
        logger.debug('Invalid network {}'.format(network))
    else:
        for region in self.view.sel():
            cursor = region.end()
            searched_from_start = (cursor is 0)
            while True:
                found_region = self.view.find(sublime_ip.v4.any, cursor, sublime.IGNORECASE)
                if (not found_region):
                    self.view.sel().clear()
                    if (not searched_from_start):
                        self.view.sel().add(sublime.Region(0, 0))
                        searched_from_start = True
                        cursor = 0
                        continue
                    self.view.sel().add_all(current_regions)
                    break
                cleaned_region = Network.clean_region(self.view, found_region)
                network_re_match = self.view.substr(cleaned_region)
                logger.debug('Network RE match {}'.format(network_re_match))
                found_network = Network.get(network_re_match)
                logger.debug('Network Object {} generated'.format(found_network))
                if (found_network and Network.contains(search_network, found_network)):
                    self.view.sel().clear()
                    self.view.show_at_center(cleaned_region.begin())
                    logger.debug('Network found in {} {}'.format(cleaned_region.begin(), cleaned_region.end()))
                    self.view.sel().add(sublime.Region(cleaned_region.begin(), cleaned_region.end()))
                    break
                cursor = cleaned_region.end()
    self._find_input_panel(network)
