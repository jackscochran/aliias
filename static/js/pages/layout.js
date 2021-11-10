$(document).ready(function(){
    
    // ----------------------- Drop down logic ----------------------- //
    $('#nav-dropdown').hide();
    $('#nav-slideup-button').hide();

    function slideDown(){
        $('#nav-dropdown').slideDown("slow");
        $('#nav-dropdown-button').hide();
        $('#nav-slideup-button').show();
    }

    function slideUp(){
        $('#nav-dropdown').slideUp("slow");
        $('#nav-dropdown-button').show();
        $('#nav-slideup-button').hide();
    }

    $('#nav-dropdown-button').click(function(){
        slideDown()
    });

    $('#nav-slideup-button').click(function(){
        slideUp();
    });

    $('#nav-dropdown').hover(function(){
        $('#nav-dropdown').show();
    }, function(){
        slideUp();
    });

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