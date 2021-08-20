$(document).ready(function(){
    $('#nav-dropdown').hide();

    $('#nav-dropdown-button, #nav-dropdowm').click(function(){
        $('#nav-dropdown').toggle();
    })

    $('#nav-dropdown').hover(function(){
        $('#nav-dropdown').show();
    }, function(){
        $('#nav-dropdown').hide();
    })
})