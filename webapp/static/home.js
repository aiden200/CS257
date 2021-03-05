/*
 * map-sample-usa.js
 * Jeff Ondich
 * 11 November 2020
 *
 * Simple sample using the Datamaps library to show how to incorporate
 * a US map in your project.
 *
 * Datamaps is Copyright (c) 2012 Mark DiMarco
 * https://github.com/markmarkoh/datamaps
 */

window.onload = initialize;

// This is example data that gets used in the click-handler below. Also, the fillColor
// specifies the color those states should be. There's also a default color specified
// in the Datamap initializer below.

var extraStateInfo = {
    /*
    MN: { population: 5640000, jeffhaslivedthere: true, fillColor: '#2222aa' },
    CA: { population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa' },
    NM: { population: 2100000, jeffhaslivedthere: false, fillColor: '#2222aa' },
    OH: { population: 0, jeffhaslivedthere: false, fillColor: '#aa2222' }
    */

};

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}


function initialize() {
    initializeMap();
}

function initializeMap() {
    var map = new Datamap({
        element: document.getElementById('map-container'), // where in the HTML to put the map
        scope: 'usa', // which map?
        projection: 'equirectangular', // what map projection? 'mercator' is also an option
        done: onMapDone, // once the map is loaded, call this function
        data: extraStateInfo, // here's some data that will be used by the popup template
        fills: { defaultFill: '#999999' },
        geographyConfig: {
            //popupOnHover: false, // You can disable the hover popup
            //highlightOnHover: false, // You can disable the color change on hover
            popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
            borderColor: '#eeeeee', // state/country border color
            highlightFillColor: '#bbbbbb', // color when you hover on a state/country
            highlightBorderColor: '#000000', // border color when you hover on a state/country
        }
    });
}

// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick);
}

function hoverPopupTemplate(geography, data) {

    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n';

    var url = getAPIBaseURL() + '/total_cases?region_contains=' + geography.properties.name;
    console.log(url);
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(info) {
            for (var k = 0; k < info.length; k++) {
                var infos = info[0];
                template += '<strong>Cases: </strong>' + infos['cases'] + '<br>\n';
            }
            template += '</div>';
            console.log(template);
            return template
        })
        .then(function(message) {
            var casesElement = document.getElementById('basic info');
            if (casesElement) {
                casesElement.innerHTML = message;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    url = getAPIBaseURL() + '/total_vaccinations?region_contains=' + geography.properties.name;
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(info) {
            for (var k = 0; k < info.length; k++) {
                var infos = info[k];
                template += '<strong>Vaccinations: </strong>' + infos['vaccinations'] + '<br>\n';
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    template += '</div>';
    return template;

}

window.onclick = function(event) {
    if (event.target.className.indexOf('dropbtn') == -1) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
}


function filterFunction() {
    var input = document.getElementById("myInput");
    var url = getAPIBaseURL() + '/total_cases?region_contains=' + input.value;
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(info => {
            var listBody = '';
            if (info.length === 0) { listBody += "No results!" } else {
                for (var k = 0; k < info.length; k++) {
                    var infos = info[k];
                    let s = infos['region_name'] + '"'
                    listBody += '<a href="/state_detail?state=' + s + 'class="home">' + infos['region_name'] + " cases: " + infos['cases'] + '</a>' + '</br>';
                }
            }
        
            
            document.getElementById('list_container').innerHTML = listBody;
            document.getElementById("list_container").classList.toggle("show");
            document.getElementById("home").setAttribute("class", "highlight3");
        })
        .catch(function(error) {
            console.log(error);
        });
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onStateClick(geography) { //change this target page to another one.
    var url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/state_detail?state=' + geography.properties.name;
    window.location.href = url;
    // geography.properties.name will be the state/country name (e.g. 'Minnesota')
    // geography.id will be the state/country name (e.g. 'MN')
    /*
    var stateSummaryElement = document.getElementById('state-summary');
    if (stateSummaryElement) {
        var summary = '<p><strong>State:</strong> ' + geography.properties.name + '</p>\n' +
            '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
        if (geography.id in extraStateInfo) {
            var info = extraStateInfo[geography.id];
            summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
        }

        stateSummaryElement.innerHTML = summary;
    }
    */

}