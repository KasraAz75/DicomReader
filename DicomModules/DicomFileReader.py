#!/usr/bin/env python
# DicomReader.py

import numpy as np
import pydicom as dicom
from six import string_types
from scipy.spatial import ConvexHull


class DicomReader:
    """
    Read and extract information from a DICOM / DICOM RT (.dcm) file

    Class attribute(s):
        data - Dicom (.dcm) file to be read
    """

    def __init__(self, data):

        if isinstance(data, dicom.dataset.Dataset):
            self.ds = data

        elif isinstance(data, string_types):
            try:
                self.ds = dicom.dcmread(data)
            except:
                # Raise error if the data is not .dcm file
                raise ValueError("The input data is not a .dcm type file!")
            else:
                # Raise error if the data is imperfect
                if "PatientID" not in self.ds:
                    raise AttributeError

        else:
            raise AttributeError

    def GetPatientID(self):
        """
        Return "PatientID" from the input file
        """

        return self.ds.PatientID

    def GetStructureSetROISequence(self):
        """
        Return "Structure Set ROI Sequence", if exist!
        """

        # DICOM RT structures include "StructureSetROISequence"
        if "StructureSetROISequence" in self.ds:
            return self.ds.StructureSetROISequence

        # DICOM CT structures doesn't include "StructureSetROISequence"
        else:
            return ""

    def GetOrganIndex(self, organ):
        """
        Return index of the given organ in the "Structure Set ROI Sequence
        """

        structure = self.GetStructureSetROISequence()
        # Iterate over "StructureSetROISequence" to find the index of the organ
        organ_index = ([i for i in range(len(structure)) if structure[i].ROIName == str(organ).upper()])

        return organ_index[0]

    def GetContoursCoordinate(self, roi_index):
        """
        Return an array of contours, each includes multiple 3D coordinates,
        given index of the "ROI Contour Sequence"
        """

        roi = self.ds.ROIContourSequence
        # Iterate over contour sequence, store coordinates as xyz arrays
        contours = ([np.array(self.Get3DPoints(plan.ContourData), dtype="object")
                    for plan in roi[roi_index].ContourSequence])
        # Store coordinates for each contour as a numpy array
        contours = np.array(contours, dtype="object")

        return np.vstack(contours[:])

    def Get3DPoints(self, array):
        """
        Return an array of xyz points, given the input array
        """

        n = 3
        return [np.array(array[i:i+n], dtype=np.float32) for i in range(0, len(array), n)]

    def GetConvexHullVolume(self, coordinates):
        """
        Compute the volume of a convex hull based on the volume
        summation of all tetrahedrons including points on each
        of the convex hull's simplexes
        """

        # Define a convex hull using the input coordinates
        hull = ConvexHull(coordinates)
        # Define simplexes and coordinates of the vertices of simplexes
        simplexes = np.column_stack((np.repeat(hull.vertices[0], hull.nsimplex), hull.simplices))
        vertices = hull.points[simplexes]

        return np.sum(self.TetrahedronVolume(vertices[:, 0], vertices[:, 1], vertices[:, 2], vertices[:, 3])) / 1000

    def TetrahedronVolume(self, v1, v2, v3, v4):
        """
        Return the volume of a Tetrahedron, given its vertices
        """

        return np.abs(np.einsum('ij,ij->i', v1 - v4, np.cross(v2 - v4, v3 - v4))) / 6
