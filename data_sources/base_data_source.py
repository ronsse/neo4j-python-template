from abc import ABC, abstractmethod
import logging
from utils.data_extractor import DataExtractor
from models.neo_models import IPAddress


class DataSource(ABC):
    """
    Abstract base class representing a data source for loading and processing data into a Neo4j database.

    This class provides a generic structure for extracting data from various sources (like JSON, CSV, XML, etc.),
    transforming it, and loading it into a Neo4j graph database using Neo4j's object-graph mapping library, neomodel.

    Attributes:
        name (str): The name of the data source.
        directory (str): The directory path where the source data files are located.
        extractor (DataExtractor): An instance of DataExtractor for extracting data from files in the specified directory.

    Methods:
        load_data: Reads data from the source files, processes each data item using the process_dictionary method, and loads it into the database.
        safe_get: Safely navigates through a nested dictionary or list to retrieve a value, handling lists encountered in the path.
        process_dictionary: Abstract method to be implemented by subclasses, defining how individual data dictionaries should be processed.
        create_or_update_ip_address: (Unused) Creates or updates IPAddress nodes in the database based on given data and IP fields.
        process_ip_address: Processes a single IP address, creating or updating the corresponding IPAddress node in the database.
    """
    
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.extractor = DataExtractor(directory)
        self.null_fields_count = {}

    def load_data(self):
        datasets = self.extractor.extract_data()
        for filename, data in datasets.items():
            if isinstance(data, list):
                # If data is a list, process each dictionary in the list
                for data_dict in data:
                    self.process_dictionary(data_dict)
            elif isinstance(data, dict):
                # If data is a single dictionary, process it directly
                self.process_dictionary(data)
            else:
                raise ValueError(
                    f"Unexpected data type in file {filename}: {type(data)}"
                )
    
    def increment_null_field_count(self, field_name):
        if field_name in self.null_fields_count:
            self.null_fields_count[field_name] += 1
        else:
            self.null_fields_count[field_name] = 1
    
    def report_null_fields(self):
        print(f"Null Fields Report for {self.name}:")
        for field, count in self.null_fields_count.items():
            print(f"{field}: {count} nulls")
            
    def safe_get(self, dictionary, *keys):
        """
        Navigate through a nested dictionary or list safely.
        :param dictionary: The dictionary or list through which to search.
        :param keys: A list of keys to traverse, in order.
        :return: The value found, or None if any key is not present.
                If a list is encountered, returns a list of found values.
        """
        current = dictionary
        for key in keys:
            if isinstance(current, list):
                # If current is a list, apply remaining keys to all items in the list
                return [
                    self.safe_get(item, *keys[keys.index(key) :])
                    for item in current
                    if isinstance(item, dict)
                ]
            if not isinstance(current, dict):
                return None
            current = current.get(key)

        return current

    @abstractmethod
    def process_dictionary(self, data_dict):
        pass

    # Currently Unused this is an example of how to create an ip address node from the data in a deeply nested dictionary.
    #this will expect a dictionary of ip fields and their types and a connection node 
    #the ip_field is a string delimited by a period to represent the path to the ip address in the dictionary
    def create_or_update_ip_address(self, data, ip_fields, server_node):
        for ip_field, ip_type in ip_fields.items():
            ip_address = self.safe_get(data, *ip_field.split("."))
            if not ip_address:
                self.increment_null_field_count(ip_field)
            if isinstance(ip_address, list):
                for ip in ip_address:
                    if ip:
                        self.process_ip_address(ip, ip_type, server_node)
            elif ip_address:
                if ip_address:
                    self.process_ip_address(ip_address, ip_type, server_node)

    def process_ip_address(self, ip_address, ip_type, server_node):
        ip_node = IPAddress.nodes.get_or_none(ip_address=ip_address)
        if not ip_node:
            logging.info(f"Creating new IPAddress node: {ip_address}")
            ip_node = IPAddress(ip_address=ip_address, type=ip_type)
            ip_node.save()
            ip_node.server.connect(server_node)
        else:
            logging.info(f"Found existing IPAddress node: {ip_address}")
            # Update existing IPAddress node properties if needed
