$(document).ready(function(){

    // ----------------------- Drop down logic ----------------------- //
    $('#nav-dropdown').hide();

    $('#nav-dropdown-button, #nav-dropdown').click(function(){
        $('#nav-dropdown').toggle();
    })

    $('#nav-dropdown').hover(function(){
        $('#nav-dropdown').show();
    }, function(){
        $('#nav-dropdown').hide();
    })

    // ----------------------- Nav Search logic ----------------------- //

    function goToSearch(){
        var searchTerm = $('#nav-search-input').val();
        window.location.href = '../search?query=' + searchTerm;
    }

    $('#nav-search-button').click(goToSearch);
    
    $('#nav-search-input').focus() // focus on search box 
    // when enter key is pressed on search box (for accesability)
    $('#nav-search-input').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            goToSearch();
        }
    });

})