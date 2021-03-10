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

var extraStateInfo = {};

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}


function initialize() {
    initializeMap();
}

function initializeMap() {
    var url = getAPIBaseURL() + '/total_cases_and_vaccination';
    console.log(url);
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(info) {
            for (var k = 0; k < info.length; k++) {
                var infos = info[k];
                var state = {};
                state["vaccination"] = infos['vaccination'];
                state["cases"] = infos['cases'];
                extraStateInfo[infos["region_name"]] = state;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
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
    template += getStateInfo(geography.properties.name);
    template += '</div>';
    return template;

}
//ask jeff
function getStateInfo(statename) {
    var info = extraStateInfo[statename];
    var s = '<strong>Cases: </strong>' + info['cases'] + '<br>\n';
    s += '<strong>Vaccinations: </strong>' + info['vaccination'] + '<br>\n';
    return s;

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

function onStateClick(geography) {
    var url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/state_detail?state=' + geography.properties.name;
    window.location.href = url;

}