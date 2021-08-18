
$(document).ready(function(){
    fieldJSON ={
        inputElementName: 'registration-email',
        validationType: 'email',
        errorID: 'email-err'
    }

    $('.error-msg').hide()
    $('.register__model').hide()
    $('[name=' + fieldJSON.inputElementName + ']').blur(function(){
        formValidator.validateField(fieldJSON)
    })
    
    $('#register-button').click(function(){
        if(formValidator.validateField(fieldJSON)){
            // submit email to backend
            $.ajax({
                type: 'POST',
                url: '/api/register-email',
                data: {'email': $('[name=' + fieldJSON.inputElementName + ']').val()},
                async: false,
                dataType: 'JSON',
                success: function(data){
                    if (data['email_added']){
                        $('#visable-row').html("<div><span class='material-icons register__confirm-icon color-primary-green'>check_circle</span><h1>Thank you for registering!</h1><br><p>We'll keep you informed on the latest and greatest at ALIIAS Investments</p></div>")
                    }else{
                        $('#visable-row').html("<div><span class='material-icons register__confirm-icon color-secondary-yellow'>feedback</span><h1>Oops! Looks like this email is already in the system</h1><br><p>We'll keep you informed on the latest and greatest at ALIIAS Investments</p></div>")

                    }
                },
                error: function(data){
                    $('#visable-row').html(data)
                }
            })
        }
    });
    
});
