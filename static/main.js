$(document).ready(function(){
    console.log('this is working')
    $('.plant-box').on('click', function(event){
        event.preventDefault()
        $(this).toggleClass('selected')
    })

    $('#plant-submit').on('click', function(event){
        event.preventDefault()
        if(event.isDefaultPrevented()){
            // default event is prevented
        }else{
            event.returnValue = false;
        }
        let selected = document.getElementsByClassName('selected')
        if (selected.length === 0) {
            alert("Please select your plants")
            return
        }
        let selection = []
        for(var i=0; i<selected.length; i++){
            selection.push(selected[i].getAttribute('data-id'))
        }
        console.log(selection)

        $.ajax({
            method: "POST",
            url: '/users_plants',
            data: {plantid: selection},
            success: function(response){
                console.log(response)
                window.location.href = '/profile'  
            },
            error: function() {
                console.log("error")
            }
        })
        
    })

    
})
