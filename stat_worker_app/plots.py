"""
    Worker to build unique filename.
"""

import uuid


class Plots:
    """
        Creates a unique filename
    """

    def create_plot_files(self, file_name):
        """
            Creates a well formed png file.
        """
        if file_name == 'result_boxplot.png':
            new_name_boxplot = 'result_boxplot-' + str(uuid.uuid4()) + '.png'
            return new_name_boxplot
        if file_name == 'result_regplot.png':
            new_name_regplot = 'result_regplot-' + str(uuid.uuid4()) + '.png'
            return new_name_regplot
        if file_name == 'result_jointplot.png':
            new_name_jointplot = 'result_jointplot-' + str(uuid.uuid4()) + '.png'
            return new_name_jointplot
        if file_name == 'result_distplot.png':
            new_name_distplot = 'result_distplot-' + str(uuid.uuid4()) + '.png'
            return new_name_distplot
        if file_name == 'result_pairplot.png':
            new_name_pairplot = 'result_pairplot-' + str(uuid.uuid4()) + '.png'
            return new_name_pairplot
        if file_name == 'result_residplot.png':
            new_name_residplot = 'result_residplot-' + str(uuid.uuid4()) + '.png'
            return new_name_residplot
        if file_name == 'result_histplot.png':
            new_name_histplot = 'result_histplot-' + str(uuid.uuid4()) + '.png'
            return new_name_histplot
