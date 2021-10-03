function search(query){

    function displayResult(ticker, companyFullName){
        var resultHTML = '<div class="search-result"><h3>' + ticker + ' <small>' + companyFullName+ '</small></h3><a href="/stocks/' + ticker + '">View Company</a><hr></div>';
    
        $('#search-results').append(resultHTML);
    }

    if(!query){
        $('.search-result').remove();
        $('#no-results-message').show();
        $('#loading-message').hide();
        return
    }

    $('.search-result').remove();
    $('#no-results-message').hide();
    $('#loading-message').show();

    //API Call

    $.ajax({
        url: '/api/search-stock',
        type: 'GET',
        data: {'query': query},
        async: true,
        dataType: 'JSON',
        success: function(data){
           
            $('#loading-message').hide();

            if (data['results'].length == 0){
                $('#no-results-message').display(); // no search results
            }

            var results = data['results'];
            
            if (results){

                for(const ticker in results){
                    displayResult(ticker, results[ticker]);
                }

            }

            return results;

        },
        error: function(){
            console.error('Company API called failed')
        }
    }); 
    
}

$(document).ready(function(){
    const urlParams = new URLSearchParams(window.location.search);
    var query = urlParams.get('query');
    if (query){
        $('#query-input').val(query); //set input value to url parameter
        search(query);
    }

    //add event listeners to search bar
    // when enter key is pressed on search box (for accesability)
    $('#query-input').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            search($(this).val());
        }
    });

    $('#query-icon').click(function(){
        search($('#query-input').val())
    });

});
