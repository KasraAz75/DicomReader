# DicomReader

**DicomReader** allows the user to parse a direcotry including DICOM (.dcm) files and determines the below information for each file: 
1. The [**Patient ID**](https://dicom.innolitics.com/ciods/ct-image/patient/00100020) from the DICOM CT Image files.
2. The total number of [**DICOM CT Image files**](https://dicom.innolitics.com/ciods/ct-image/general-study/0020000d).
3. The volume of an organ (e.g. "HEART") inside the [**RT Structure file**](https://dicom.innolitics.com/ciods/rt-structure-set/general-study/0020000d).

## Other information

The program includes two modules:
- **DicomFileReader:** It includes a class called DicomFileReader which extract information from a single Dicom CT Image or RT Structure file.
- **DicomDirParser:** A Directory of Dicom files feed into a class called DicomDirParser and information will be extracted from the directory.

## Dependencies

- [pydicom](https://github.com/pydicom/pydicom)
- [NumPy](https://numpy.org/doc/stable/)
- [SciPy](https://docs.scipy.org/doc/scipy/reference/)
- [Six](https://six.readthedocs.io/)
- [os](https://docs.python.org/3/library/os.html)
- [zipfile](https://docs.python.org/3/library/zipfile.html)

## Basic Usage
```ruby
#!/usr/bin/env python
# __main__.py

from DicomModules.DicomDirParser import DicomDirParser


def PatientsInfo(dir, organ):
    """
    Return the extracted information from the directory
    """

    info = {}
    # Parsing the directory including .dcm files
    dicom_dir = DicomDirParser(dir)

    for patient in dicom_dir.GetPatientIDs():
        patient_info = dict()

        # Patient ID for each scan
        patient_info["Patient ID"] = patient
        # Total number of CTs for each scan
        patient_info["Total number of DICOM CT files"] = dicom_dir.GetDicomsInfo(patient)[0]
        # The volume of the "HEART" structure
        patient_info[f"The volume of the {str(organ)} structure"] = \
            f"{dicom_dir.GetOrganVolume(patient, str(organ))} cm\u00b3"

        info[f"Patient{dicom_dir.GetPatientIDs().index(patient)+1}"] = patient_info

    return info


if __name__ == "__main__":

    # Ask for the .dcm files directory and the organ
    dir = input("Please insert the path in which DICOM files have been located: ") # ~/tmp/DicomDirectory
    organ = input("Please insert the organ whose volume you wish to get: ") # HEART

    patients_info = PatientsInfo(dir, organ)
    print(patients_info) 
    # {'Patient1': {'Patient ID': 'ECI002000', 'Total number of DICOM CT files': 112, 'The volume of the heart structure': '584.0180580929963 cm³'}, 
    #  'Patient2': {'Patient ID': '12778', 'Total number of DICOM CT files': 220, 'The volume of the heart structure': '637.2799206609833 cm³'}, 
    #  'Patient3': {'Patient ID': 'ECI003000', 'Total number of DICOM CT files': 106, 'The volume of the heart structure': '462.61748239564673 cm³'}}

```

## Contact
If you want to contact me you can reach me at [kasra.azizbaigi@gmail.com](mailto:kasra.azizbaigi@gmail.com)

## License
This project uses the following license: [GNU General Public License v3.0](https://github.com/KasraAz75/LRUCache/blob/main/LICENSE).
