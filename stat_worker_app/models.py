"""
    The model of an request.
"""

import os
import csv
import uuid
import io
from openpyxl import load_workbook
from os.path import join
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class ComputeRequestModel(models.Model):
    """
        The model of an compute request Holds all values to run a computation.
    """

    methods = (
        ('1', 'Normalverteilung'),
        ('2', 'Gleichverteilung'),
        ('3', 'Binomialverteilung '),
    )

    sources = (
        ('1', 'Datei'),
        ('2', 'Eingabe'),
    )

    method = models.CharField(max_length=1, choices=methods, default='1')
    source = models.CharField(max_length=1, choices=sources, default='1')

    # Datei
    file = models.FileField(upload_to='media/')
    filename = ''

    # manuelle Eingabe

    data1 = models.TextField(default='')
    data2 = models.TextField(default='')

    data1_list = []
    data2_list = []

    def set_tabledata(self, data1, data2):
        self.data1_list = data1.split(',')
        self.data2_list = data2.split(',')

    def valid_table(self):
        return len(self.data1) == len(self.data2)

    def valid_file(self, name):
        """ Returns true if the file has an valid extension (in fact has to be .csv or .xlsx). """

        if name[-4:] == ".csv" or name[-5:] == ".xlsx":
            return True
        else:
            return False

    def prepare_file(self, source):
        """
            Creates an array from a csv-file or from raw data. The array acts a an internal common format. For
            excelfiles simply the name will be returned.
        """

        data = []
        datafile_name = 'unknown'

        if source == '1' and self.filename != '':
            if self.filename[-5:] == ".xlsx":  # excel-file
                # with OpenPyXL
                # https://openpyxl.readthedocs.io/en/stable/optimized.html
                # in mem because of problems with closing a file....
                with open(self.filename, "rb") as f:
                    in_mem_file = io.BytesIO(f.read())

                wb = load_workbook(in_mem_file, read_only=True)
                ws = wb.worksheets[0]

                for row in ws.rows:  # row is a tupel
                    # just 2 values allowed
                    data1 = row[0].value
                    data2 = row[1].value

                    data.append([data1, data2])

                wb.close()
                datafile_name = self.__create_csv_file(data)

                if (os.path.isfile(self.filename)):
                    os.remove(self.filename)

            elif self.filename[-4:] == ".csv":  # csv-file
                fs = FileSystemStorage()
                stream = fs.open(self.filename, 'r')

                streamLines = []
                for row in stream:
                    streamLines.append(row.split(';'))

                stream.close()

                for item in streamLines:
                    str_data1 = str(item[0]).replace(',', '.')
                    str_data2 = str(item[1]).replace(',', '.')

                    data11 = float(str_data1)
                    data22 = float(str_data2)

                    data.append([data11, data22])

                datafile_name = self.__create_csv_file(data)

                if (os.path.isfile(self.filename)):
                    os.remove(self.filename)

        elif source == '2':  # table
            index = 0

            for i in self.data1_list:
                data.append([float(i), float(self.data2_list[index])])
                index = index + 1

            datafile_name = self.__create_csv_file(data)

        return datafile_name

    def __create_csv_file(self, data):
        """
            Creates a well formed csv file (',' separated with decimal '.' instead of ',') within media path and
            returns its full qualified name.
        """

        path = join(settings.MEDIA_ROOT)
        name = 'data-' + str(uuid.uuid4()) + '.csv'

        file_path = join(path, name)
        new_file = open(file_path, 'w', newline='')

        csv_writer = csv.writer(new_file)
        for item in data:
            csv_writer.writerow(item)

        new_file.close()

        return new_file.name
