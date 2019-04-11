    const newTask = $('form#newTask')
   newTask.on('submit', function(event){
    event.preventDefault();
        $.ajax({
           url: '/addTask',
           type: 'POST',
           data:{ task: $('input[name=task]').val()}
        })
       .done(function(resp){
                 if (resp.error){
                     showalert(resp.message, resp.alertType)
                 }else{
                    $('input[name=task]').val('');
                    $('#incomplete').load(document.URL +  '  #incomplete-tasks');
                    $('#complete').load(document.URL +  ' #complete-tasks');
                    showalert(resp.message, resp.alertType);
                 }
            });
        });

   function showalert(message,alerttype) {

    $('#alert_placeholder').append('<div id="alertdiv" class="alert alert-' +  alerttype + ' alert-dismissible fade show" role="alert">' + message +' <button type="button" class="close" data-dismiss="alert" aria-label="Close"></button><span aria-hidden="true">&times;</span></button></div>')

    setTimeout(function() { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
      $("#alertdiv").removeClass('show');
      setTimeout(function(){
        $("#alertdiv").remove();
      }, 1000);
    }, 3000);
  }

