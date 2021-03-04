"""
    All graphics work goes here.
"""

import seaborn as sns
import pandas as pd
from .plots import Plots
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage


class Distribution:
    """
        Returns the kind of result.html as a string

        :param fileurl: the path of the file
        :param kom: the kind of method to use
        :return: a string for choosing the wright result.html in the views.py
    """

    list_pictures = []

    @staticmethod
    def build_grafic(filepath, method):
        redirect_path = 'unknown'
        list_pictures = []
        if method == '1':
            # function for creating a boxplot
            boxplot = Distribution.__boxplot(filepath)
            list_pictures.append([boxplot, 'Boxplot'])

            # function for creating a jointplot
            jointplot = Distribution.__jointplot(filepath)
            list_pictures.append([jointplot, 'Jointplot'])

            # function for creating a regression-graph
            regplot = Distribution.__regplot(filepath)
            list_pictures.append([regplot, 'Regplot'])

            # function for creating a distribution - graph
            distplot = Distribution.__dist_function(filepath)
            list_pictures.append([distplot, 'Distplot'])

            # function for creating a pairplot-graph
            pairplot = Distribution.__pairplot(filepath)
            list_pictures.append([pairplot, 'Pairplot'])

            # function for displaying the residuen
            residplot = Distribution.__residuenplot(filepath)
            list_pictures.append([residplot, 'Residuenplot'])

            # function for display the histogramm
            histplot = Distribution.__histplot(filepath)
            list_pictures.append([histplot, 'Histoplot'])

        elif method == '2':
            # function for creating a boxplot
            boxplot = Distribution.__boxplot(filepath)
            list_pictures.append([boxplot, 'Boxplot'])

            # function for creating a distribution - graph
            distplot = Distribution.__dist_function(filepath)
            list_pictures.append([distplot, 'Distplot'])

            # function for creating a pairplot-graph
            pairplot = Distribution.__pairplot(filepath)
            list_pictures.append([pairplot, 'Pairplot'])

        elif method == '3':
            # function for creating a boxplot
            boxplot = Distribution.__boxplot(filepath)
            list_pictures.append([boxplot, 'Boxplot'])

            # function for creating a jointplot
            jointplot = Distribution.__jointplot(filepath)
            list_pictures.append([jointplot, 'Jointplot'])

            # function for creating a distribution - graph
            distplot = Distribution.__dist_function(filepath)
            list_pictures.append([distplot, 'Distplot'])

            # function for creating a histogram-graph
            histplot = Distribution.__histplot(filepath)
            list_pictures.append([histplot, 'Histoplot'])

        if filepath:
            fs = FileSystemStorage()
            fs.delete(filepath)

        return list_pictures

    @staticmethod
    def __getList(list_pictures):
        return list_pictures

    @staticmethod
    def __boxplot(fileurl):
        """
            Generates the picture of the boxplot

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        boxplot_picture = sns.boxplot(data=df)
        file_name = 'result_boxplot.png'
        boxplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + boxplot)
        plt.clf()

        return boxplot

    @staticmethod
    def __jointplot(fileurl):
        """
            Generates the picture of the jointplot

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        jointplot_picture = sns.jointplot(x='XValues', y='YValues', data=df)
        file_name = 'result_jointplot.png'
        jointplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + jointplot)
        plt.clf()

        return jointplot

    @staticmethod
    def __dist_function(fileurl):
        """
            Generates the picture of the distribution-function

            :param fileurl: the fileinput of the user
        """

        # creating a distplot
        # sns.set()
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        distribution = sns.distplot(df.YValues)
        file_name = 'result_distplot.png'
        distplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + distplot)
        plt.clf()

        return distplot

    @staticmethod
    def __pairplot(fileurl):
        """
            Generates the picture of the pairplot-function

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        pairplot_picture = sns.pairplot(data=df, hue='XValues')
        file_name = 'result_pairplot.png'
        pairplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + pairplot)
        plt.clf()

        return pairplot

    @staticmethod
    def __regplot(fileurl):
        """
            Generates the picture of the Regression-Analyses

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        regplot_picture = sns.regplot(x='XValues', y='YValues', data=df)
        file_name = 'result_regplot.png'
        regplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + regplot)
        plt.clf()

        return regplot

    @staticmethod
    def __residuenplot(fileurl):
        """
            Generates the picture of the residuen of the distribution

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)

        residplot_picture = sns.residplot(x='XValues', y='YValues', data=df)
        file_name = 'result_residplot.png'
        residplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + residplot)
        plt.clf()

        return residplot

    @staticmethod
    def __histplot(fileurl):
        """
            Generates the picture of the boxplot

            :param fileurl: the fileinput of the user
        """
        plots = Plots()

        data = pd.read_csv(fileurl, sep=',', names=['XValues', 'YValues'])
        df = pd.DataFrame(data=data)
        histplot_picture = sns.distplot(df.XValues, hist=True)
        file_name = 'result_histplot.png'
        histplot = plots.create_plot_files(file_name)

        plt.savefig('stat_worker_app/static/' + histplot)
        plt.clf()

        return histplot
