$(document).ready(function() {
  console.log("this is working");
  $(".plant-box").on("click", function(event) {
    event.preventDefault();
    $(this).toggleClass("selected");
  });

<<<<<<< HEAD
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
        let notes = []
        for(var i=0; i<selected.length; i++){
            selection.push(selected[i].getAttribute('data-id'))
            notes.push(selected[i].childNodes[9].value)
        }
        console.log(selection)
        console.log(notes)
=======
  $("#plant-submit").on("click", function(event) {
    event.preventDefault();
    if (event.isDefaultPrevented()) {
      // default event is prevented
    } else {
      event.returnValue = false;
    }
    let selected = document.getElementsByClassName("selected");
    if (selected.length === 0) {
      alert("Please select your plants");
      return;
    }
    let selection = [];
    let notes = [];
    for (var i = 0; i < selected.length; i++) {
      selection.push(selected[i].getAttribute("data-id"));
      notes.push(selected[i].childNodes[9].value);
    }
    console.log(selection);
    console.log(notes);
>>>>>>> 4e7a1e055b377beb798ac73e92379f5200999ba8

    $.ajax({
      method: "POST",
      url: "/users_plants",
      data: { plantid: selection, notes: notes },
      success: function(response) {
        console.log(response);
        window.location.href = "/profile";
      },
      error: function() {
        console.log("error");
      }
    });
  });
});
