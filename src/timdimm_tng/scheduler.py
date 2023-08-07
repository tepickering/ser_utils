import os
import json
import pkg_resources

from collections import UserDict

import xmltodict

from pathlib import Path


class ScheduleBase(UserDict):
    """
    Base class for INDI/Ekos scheduler configurations with utilities to read/write
    them to XML/JSON
    """
    def from_json(
            self,
            filename=pkg_resources.resource_filename(
                __name__,
                os.path.join("templates", "timdimm_sequence_template.json")
            )
        ):
        """
        Instantiate from a JSON file
        """
        with open(filename, 'r') as fp:
            self.data = json.load(fp)

    def from_xml(self, filename="sequence.esq"):
        """
        Instantiate from an XML file
        """
        with open(filename, 'r') as fp:
            self.data = xmltodict.parse(fp.read())

    def to_xml(self, filename="sequence.esq"):
        """
        Convert internal dict to XML and write to file
        """
        with open(filename, 'w') as fp:
            fp.write(xmltodict.unparse(self.data, pretty=True))

    def to_json(self, filename="sequence.json"):
        """
        Convert internal dict to JSON and write to file
        """
        with open(filename, 'w') as fp:
            json.dump(self.data, fp, indent=4)


class Sequence(ScheduleBase):
    """
    Handle observing sequence configurations
    """
    def __init__(
        self,
        template=pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_list_template.json"))
    ):
        if 'json' in Path(template).suffix.lower():
            self.from_json(filename=template)
        else:
            self.from_xml(filename=template)


class Observation(ScheduleBase):
    """
    Job entry in an INDI/Ekos Scheduler list
    """
    def __init__(
        self,
        target="Target",
        ra=0.0,
        dec=0.0,
        priority=10,
        sequence=Path.home() / "sequence.esq",
        template=pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_list_template.json"))
    ):
        if 'json' in Path(template).suffix.lower():
            self.from_json(filename=template)
        else:
            self.from_xml(filename=template)

        # use the first entry in the scheduler list template as the boiler-plate to build from
        self.data = self.data['SchedulerList']['Job'][0]

        # configure from the arguments
        self.data['Target'] = target
        self.data['Priority'] = f"{priority}"  # XML can only be strings so we make sure they are
        self.data['Coordinates']['J2000RA'] = f"{ra}"
        self.data['Coordinates']['J2000DE'] = f"{dec}"
        self.data['Sequence'] = str(sequence)


class Schedule(ScheduleBase):
    """
    Wrap an INDI/Ekos Scheduler list and provide ways to build them programmatically
    and write them to valid JSON/XML
    """
    def __init__(
        self,
        template=pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_list_template.json"))
    ):
        if 'json' in Path(template).suffix.lower():
            self.from_json(filename=template)
        else:
            self.from_xml(filename=template)

        # zero out the list of jobs to initiate
        self.data['SchedulerList']['Job'] = []

    def add_observation(self, observation):
        """
        Add an Observation instance to the schedule
        """
        self.data['SchedulerList']['Job'].append(observation)
