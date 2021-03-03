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

function list_search() {
    var input = document.getElementById("myInput");
    var url = getAPIBaseURL() + '/total_cases?region_contains=' + input.value;
    var listBody = [];
    fetch(url, {method:'get'})
        .then((response) => response.json())
        .then(info => {
            for (var k = 0; k < info.length; k++) {
                var infos = info[k];
                var in_list = [];
                in_list.push(infos['region_name'],infos['cases']);
                listBody.push(in_list);
            }
            if (listBody.length === 0) {listBody.push("No results!")}
            alert(listBody);
            
            return listBody;
            

        })

        
    .catch(function(error) {
        console.log(error);
    });
    alert(info)
    return await info;
    
}

function getResults() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
    var i;
    var a = list_search();
    alert(a);
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
}