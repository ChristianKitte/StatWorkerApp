"""
    Handels the requests.

    Most of them simply returns an template based page
"""

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ComputeRequestForm
from .models import ComputeRequestModel
from .distribution import Distribution


def base(req):
    """
        Returns the base

        :param req: the request
        :return: base.html
    """
    return render(req, 'app/base.html')


def about(req):
    """
        Returns the about

        :param req: the request
        :return: about.html
    """
    return render(req, 'app/about.html')


def compute(req):
    """
        For GET: returns the compute
        For POST: Evaluate the data and redirect to an result page

        :param req: the request
        :return: compute.html
    """
    if req.method == 'POST':
        global list_pictures

        model = ComputeRequestModel()
        form = ComputeRequestForm(req.POST, instance=model)  # bound form

        if req.POST['source'] == '1':  # file
            file = req.FILES['file']  # raise an error if missing

            if model.valid_file(file.name):
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                fileurl = fs.path(filename)

                model.filename = fileurl
            else:
                return HttpResponseRedirect('/compute', {'form': form})

        if req.POST['source'] == '2':  # table
            model.set_tabledata(req.POST['data1'], req.POST['data2'])

            if model.valid_table() == False:
                return HttpResponseRedirect('/compute', {'form': form})

        # Prepare the data to get a normalized dataset
        compute_data = model.prepare_file(req.POST['source'])
        list_pictures = Distribution.build_grafic(compute_data, req.POST['method'])

        if req.POST['method'] == '1':
            render(req, 'app/results_nv.html', {'list_pictures': list_pictures})
            return HttpResponseRedirect('/results_nv')
        elif req.POST['method'] == '2':
            render(req, 'app/results_gv.html', {'list_pictures': list_pictures})
            return HttpResponseRedirect('/results_gv')
        elif req.POST['method'] == '3':
            render(req, 'app/results_bv.html', {'list_pictures': list_pictures})
            return HttpResponseRedirect('/results_bv')

    elif req.method == 'GET':
        form = ComputeRequestForm()  # unbound form
        return render(req, 'app/compute.html', {'form': form})


def imprint(req):
    """
        Returns the imprint

        :param req: the request
        :return: imprint.html
    """
    return render(req, 'app/imprint.html')


def methods(req):
    """
        Returns the methods

        :param req: the request
        :return: methods.html
    """
    return render(req, 'app/methods.html')


def privacy(req):
    """
        Returns the privacy

        :param req: the request
        :return: privacy.html
    """
    return render(req, 'app/privacy.html')


def results_nv(req):
    """
        Returns the result for 'Normalverteilung'

        :param req: the request
        :return: results_nv.html
    """
    return render(req, 'app/results_nv.html', {'list_pictures': list_pictures})


def results_bv(req):
    """
        Returns the result 'Binomialverteilung'

        :param req: the request
        :return: results_bv.html
    """
    return render(req, 'app/results_bv.html', {'list_pictures': list_pictures})


def results_gv(req):
    """
        Returns the result for 'Gleichverteilung'

        :param req: the request
        :return: results_nv.html
    """
    return render(req, 'app/results_gv.html', {'list_pictures': list_pictures})


def welcome(req):
    """
        Returns the welcome

        :param req: the request
        :return: welcome.html
    """
    return render(req, 'app/welcome.html')
