import json
import os
import logging
import xml.etree.ElementTree as ET


class DataExtractor:
    """
    A utility class for extracting data from files within a specified directory.

    This class supports reading and parsing data from various file formats, including XML, CSV, and JSON.
    Extracted data is returned as a dictionary of dictionaries, with each top-level key being the filename.

    Attributes:
        directory (str): The directory path where the files are located.
        logger (logging.Logger): The logger instance for logging information and errors.

    Methods:
        extract_data: Iterates over each file in the specified directory, processing each based on its file format.
        _read_xml: Private method for parsing XML files.
        _process_element: Private method to recursively process each element in an XML file.

    Note:
        - The method for parsing CSV files is not implemented and should be added as per the specific requirements.
        - Errors encountered during file processing are logged using the logger.
    """
    def __init__(self, directory):
        self.directory = directory
        self.logger = logging.getLogger(__name__)

    def extract_data(self):
        """Extract data from files in the directory and return a dictionary of data"""
        data_dicts = {}
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            print(f"Processing file: {file_path}")  # Debugging line
            try:
                if filename.endswith(".xml"):
                    data_dicts[filename] = self._read_xml(file_path)
                elif filename.endswith(".csv"):
                    with open(file_path, "r") as f:
                        # CSV parsing logic
                        pass
                elif filename.endswith(".json"):
                    with open(file_path) as f:
                        data_dicts[filename] = json.load(f)
                else:
                    self.logger.warning(f"Unsupported file type: {filename}")
            except Exception as e:
                self.logger.error(f"Error processing file {file_path}: {e}")

        return data_dicts

    def _read_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return self._process_element(root)

    def _process_element(self, element):
        # Base case for processing text directly
        if len(element) == 0:
            return element.text.strip() if element.text else None

        # Process nested elements
        data = {}
        for child in element:
            child_data = self._process_element(child)

            # Handle lists for repeated tags
            if child.tag in data:
                if type(data[child.tag]) is list:
                    data[child.tag].append(child_data)
                else:
                    data[child.tag] = [data[child.tag], child_data]
            else:
                data[child.tag] = child_data

        return data
