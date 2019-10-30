
# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import json

display = Display()

class LookupModule(LookupBase):

    def run(self, routes, variables=None, **kwargs):

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        display.vvvv("Input routes JSON: %s" % routes)
        ret = []
        for route in routes[0]:
            try:
                if route['state'] != "active":
                    next
                else: 
                    elem = {}
                    needed = {k: v for k, v in route.items() if v is not None} 
                    elem['dest'] = needed['destination_cidr_block']
                    
                    sources = needed.keys()
                    sources.remove('destination_cidr_block')
                    sources.remove('state')
                    sources.remove('origin')

                    if len(sources) != 1:
                        raise AnsibleParserError()
                    else:
                        source = sources[0]

                    if needed[source]:
                        elem[source] = needed[source]
                        ret.append(elem)
                    else:
                        # Always use ansible error classes to throw 'final' exceptions,
                        # so the Ansible engine will know how to deal with them.
                        # The Parser error indicates invalid options passed
                        raise AnsibleParserError()
            except AnsibleParserError:
                raise AnsibleError("Error parsing routes in: %s" % routes)

        return ret

