import os
import json
import pkg_resources

from collections import UserDict

import xmltodict

from pathlib import Path


class Sequence(UserDict):
    """
    Wrap an INDI/Ekos imaging sequence
    """
    @classmethod
    def from_json(
            cls,
            template_file=pkg_resources.resource_filename(
                __name__,
                os.path.join("templates", "timdimm_sequence_template.json")
            )
        ):
        """
        Instantiate from a JSON file
        """
        with open(template_file, 'r') as fp:
            return cls(json.load(fp))

    @classmethod
    def from_xml(cls, seqfile="sequence.esq"):
        """
        Instantiate from an XML file
        """
        with open(seqfile, 'r') as fp:
            return cls(xmltodict.parse(fp.read()))

    def to_xml(self, outfile="sequence.esq"):
        """
        Convert internal dict to XML and write to file
        """
        with open(outfile, 'w') as fp:
            fp.write(xmltodict.unparse(self.data, pretty=True))

    def to_json(self, outfile="sequence.json"):
        """
        Convert internal dict to JSON and write to file
        """
        with open(outfile, 'w') as fp:
            json.dump(self.data, fp, indent=4)


class Observation:
    """
    Job entry in an INDI/Ekos Scheduler list
    """
    def __init__(self, target="Target", ra=0.0, dec=0.0, priority=10, sequence=Path.home() / "sequence.esq"):
        template = pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_list_template.json"))

        with open(template, 'r') as fp:
            full_config = json.load(fp)

        # use the first entry in the scheduler list template as the boiler-plate to build from
        self.config = full_config['SchedulerList']['Job'][0]

        # configure from the arguments
        self.config['Target'] = target
        self.config['Priority'] = f"{priority}"  # XML can only be strings so we make sure they are
        self.config['Coordinates']['J2000RA'] = f"{ra}"
        self.config['Coordinates']['J2000DE'] = f"{dec}"
        self.config['Sequence'] = str(sequence)


class Schedule:
    """
    Wrap an INDI/Ekos Scheduler list and provide ways to build them programmatically
    and write them to valid XML
    """
    def __init__(self):
        template = pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_list_template.json"))

        with open(template, 'r') as fp:
            self.config = json.load(fp)

        # zero out the list of jobs to initiate
        self.config['SchedulerList']['Job'] = []

    def add_observation(self, observation):
        """
        Add an Observation instance to the schedule
        """
        self.config['SchedulerList']['Job'].append(observation.config)
