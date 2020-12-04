#!/usr/bin/env python
# DicomDirParser.py

from DicomModules.DicomReader import DicomReader
from os import listdir
from os.path import isfile, join, isdir
from zipfile import is_zipfile, ZipFile


class DicomDirParser:
    """
    Read and extract information from a DICOM directory

    Class attribute(s):
        directory - The path in which DICOM (.dcm) files have been located
    """

    def __init__(self, directory):

        # Check if the directory actually is a directory
        if isdir(directory):
            self.dir = ([join(directory, file) for file in listdir(directory)
                     if (isfile(join(directory, file)) and ".dcm" in file)])

        # Check if the directory is a .zip file
        elif is_zipfile(directory):
            subdirectory = "./"
            zip_file = ZipFile(directory, "r")
            # Extract all the .dcm files in the working directory
            self.dir = [zip_file.extract(file, subdirectory)
                        for file in zip_file.namelist() if file.endswith(".dcm")]

        else:
            raise ValueError("Could not find any DICOM (.dcm) file,"
                             " please Enter a valid directory!")

    def GetPatientIDs(self):
        """
        Return Patient IDs in the given directory
        """

        ids = [DicomReader(file).GetPatientID() for file in self.dir]

        return list(set(ids))

    def GetDicomsInfo(self, patient_id):
        """
        Return the total number of DICOM (.dcm) CT files for each patient in the given directory
        """

        ct_files = []
        rt_files = []
        for file in self.dir:
            if DicomReader(file).GetPatientID() == str(patient_id):

                # DICOM RT structures include "StructureSetROISequence"
                if DicomReader(file).GetStructureSetROISequence():
                    rt_files.append(file)

                # DICOM CT files doesn't include "StructureSetROISequence"
                else:
                    ct_files.append(file)

        return len(ct_files), rt_files[0]

    def GetOrganVolume(self, patient_id, organ):
        """
        Return the volume of the specified organ for the given Patient ID
        """

        # Define & Read the DICOM RT structure
        rt_file = self.GetDicomsInfo(patient_id)[1]
        rt_structure = DicomReader(rt_file)
        # Find the index of the organ in "StructureSetROISequence"
        organ_index = rt_structure.GetOrganIndex(organ)
        # Store the xyz coordinates representing the organ structure
        organ_contours = rt_structure.GetContoursCoordinate(organ_index)

        return rt_structure.GetConvexHullVolume(organ_contours)
