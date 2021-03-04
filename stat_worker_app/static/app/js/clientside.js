/**
 * Holds the current number of rows.
 *
 * @type {number}
 */
let tableCurrentVal = 5;

/**
 * Parses a demand for a certain page.
 *
 * @param page The demanded page
 * @param contentFor The container which will be injected
 * @param source The calling navbar
 */
function getPage(page, contentFor, source) {
    $('#' + source + ' ul li.nav-item').removeClass('active');

    getContent('/' + page, contentFor, () => {
        $('li.' + page).addClass('active');
    });
}

/**
 * Helper function to show the selected files name.
 */
function fillUploadLabel() {
    let files = document.querySelector('#fileupload').files;
    if (files && files.length > 0) {
        document.querySelector('#fileuploadLabel').innerHTML = files[0].name;
    }
}

/**
 * Helper function to toggle between showing an file input or an table.
 */
function toggleFileTable() {
    eleFile = document.getElementById('optFile');
    eleTable = document.getElementById('optTable');

    $('#fileinput').removeClass('invisible visible');
    $('#table').removeClass('invisible visible');
    $('#addButton').removeClass('invisible visible');
    $('#delButton').removeClass('invisible visible');

    if (eleFile.checked) {
        $('#fileinput').addClass('visible');
        $('#table').addClass('invisible');
        $('#addButton').addClass('invisible');
        $('#delButton').addClass('invisible');
    } else if (eleTable.checked) {
        $('#fileinput').addClass('invisible');
        $('#table').addClass('visible');
        $('#addButton').addClass('visible');
        $('#delButton').addClass('visible');
    }
}

/**
 * Helper function to add an row into the table.
 */
function addTableRow() {
    let numb = formatNumber(tableCurrentVal);

    let row = document.createElement("tr");
    row.setAttribute('id', numb);

    let col1 = document.createElement("td");
    let col2 = document.createElement("td");

    let input1 = document.createElement("input");
    input1.setAttribute('class', 'w-100');
    input1.setAttribute('id', numb + "1");
    input1.setAttribute('type', 'number');
    input1.setAttribute('placeholder', numb + "1");
    input1.setAttribute('step', '0.001');

    let input2 = document.createElement("input");
    input2.setAttribute('class', 'w-100');
    input2.setAttribute('id', numb + "2");
    input2.setAttribute('type', 'number');
    input2.setAttribute('placeholder', numb + "2");
    input2.setAttribute('step', '0.001');

    col1.appendChild(input1);
    col2.appendChild(input2);

    row.appendChild(col1);
    row.appendChild(col2);

    document.querySelector('#table tbody').appendChild(row);

    tableCurrentVal++;
}

/**
 * Helper function to remove the last row from the table. There will be a minimum of four rows.
 */
function removeTabeleRow() {
    if (tableCurrentVal > 5) {
        tableCurrentVal--;
        document.getElementById(formatNumber(tableCurrentVal)).remove();
    }
}

/**
 * Helper function. Receives a number and returns a number string with leading zero (for number < 10).
 *
 * @param number The number to return as string
 * @returns {string} The string
 */
function formatNumber(number) {
    return (number < 10 ? '0' : '') + number;
}

/**
 * Provides clientside validation for the compute-form.
 *
 * @param evt The event object
 */
function catchFormCompute(evt) {
    evt.preventDefault();

    let data = new FormData();
    let eleFile = document.getElementById('optFile');
    let eleTable = document.getElementById('optTable');

    if (eleFile.checked) {
        data.append('source', '1');
        let files = document.querySelector('#fileupload').files;
        if (files.length > 0) {
            fileName = files[0].name;
            fileExtensionShort = fileName.substring(fileName.length - 3);
            fileExtensionLong = fileName.substring(fileName.length - 4);

            if (fileExtensionShort === 'csv' || fileExtensionLong === 'xlsx') {
                data.append('file', files[0]);
            } else {
                alert('Es können nur CSV- oder Excel-Dateien (.csv, .xlsx) hochgeladen werden !');
                return;
            }
        }
        else {
            alert('Es wurde keine Datei ausgewählt !');
            return;
        }
    } else {
        data.append('source', '2');
        data.append('file', '');
    }

    let method = document.querySelector('#id_method').value;
    data.append('method', method);

    let data1 = [];
    let data2 = [];

    if (eleTable.checked) {
        for (let i = 1; i < (tableCurrentVal); i++) {
            let ele1 = document.getElementById(formatNumber(i) + "1");
            let ele2 = document.getElementById(formatNumber(i) + "2");
            s = formatNumber(i);
            if (ele1 && ele2) {
                let num1 = document.getElementById(formatNumber(i) + "1").value;
                let num2 = document.getElementById(formatNumber(i) + "2").value;

                if (!isNaN(Number.parseFloat(num1))) {
                    data1.push(num1);
                }
                if (!isNaN(Number.parseFloat(num2))) {
                    data2.push(num2);
                }
            }
        }

        if (data1.length === data2.length && data2.length > 0) {
            data.append('data1', data1);
            data.append('data2', data2);
        } else {
            alert('Bitte kontrollieren Sie die eingegebenen Werte !');
            return;
        }
    } else {
        data.append('data1', data1);
        data.append('data2', data2);
    }

    postContentFor('/compute', data, 'content');
}

/**
 * Helper function to execute simple get routines.
 *
 * @param route The route for the GET-Request
 * @param contentFor The target for the content
 * @param success A function to execute after success
 * @param error A function to execute if failed
 */
function getContent(route, contentFor, success, error) {
    fetch(route).then(function (resp) {
            if (resp.ok) {
                if (contentFor) {
                    resp.text().then(function (text) {
                        let ele = document.getElementById(contentFor);
                        ele.innerHTML = text;

                        if (route === '/compute') {
                            document.getElementById('formCompute').addEventListener('submit', catchFormCompute);
                        }
                    });

                    if (success) success();
                }
            } else {
                // error but fulfilled
                alert(resp.statusText);
                if (err) err();
            }
        }
    ).catch(function (err) {
            // error and not fulfilled
            alert(err.toString());
            if (error) error();
        }
    );
}

/**
 * Helper function to execute simple post routines.
 *
 * @param route The route for the GET-Request
 * @param data The data (form data object)
 * @param resultFor The target for the result
 */
function postContentFor(route, data, resultFor) {
    fetch(route, {
        method: 'POST',
        credentials: "include",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: data,
    }).then(function (resp) {
            if (resp.ok) {
                if (resultFor) {
                    resp.text().then(function (text) {
                        let ele = document.getElementById(resultFor);
                        ele.innerHTML = text;
                    });
                }
            }
            else {
                // error but fulfilled
                alert(resp.statusText);
            }
        }
    ).catch(function (err) {
            // error and not fulfilled
            alert(err.toString());
            if (error) error();
        }
    );
}

/**
 * A helper function. Gets a cookie by its name.
 *
 * adapted from https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax
 * @param name The name of the cookie
 * @returns The demanded cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}