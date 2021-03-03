window.onload = initialize;

function initialize() {
    var element = document.getElementById('total_cases_graph_button');
    element.onclick = onCasesButton;
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onCasesButton() {
    var url = getAPIBaseURL() + '/cases_by_date';
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(info) {
            var listBody = '';
            for (var k = 0; k < info.length; k++) {
                var infos = info[k];
                listBody += '<li>' + infos['state'] +
                    ', ' + infos['day'] +
                    '-' + infos['cases']; +
                '</li>\n';
            }

            var casesElement = document.getElementById('total_cases_graph_button');
            if (casesElement) {
                casesElement.innerHTML = listBody;
            }
        })



    .catch(function(error) {
        console.log(error);
    });


}

function filterFunction() {
    var input = document.getElementById("myInput");
    var url = getAPIBaseURL() + '/total_cases?region_contains=' + input.value;
    fetch(url, {method:'get'})
        
        .then((response) => response.json())
        .then(info => {
            var listBody = '';
            if (info.length === 0) {listBody += "No results!"}
            else{
                for (var k = 0; k < info.length; k++) {
                    var infos = info[k];
                    listBody += '<a href="/" class="home">' + infos['region_name'] + " cases: " + infos['cases'] + '</a>' + '</br>';
                }
            }

            document.getElementById('list_container').innerHTML = listBody;
            document.getElementById("home").setAttribute("class", "highlight3");

        
            
        })

        
    .catch(function(error) {
        console.log(error);
    });
    
    
}



