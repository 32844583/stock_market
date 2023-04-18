  $(document).ready(function(){
    $("[id^='input-box']").keypress(function(event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        var input_value = $(this).val();
        $(this).replaceWith("<label>" + input_value + "</label>");
        var input_id = $(this).attr("id");
        var input_number = input_id.replace(/\D/g,'');
        $.ajax({
          url: "",
          type: "POST",
          data: {"input_value": input_value, "input_number": input_number},
          success: function(data) {
            console.log(data);
          }
        });
      }
    });

    var eventName;
    
    // $("tr").hover(function(){
    //     eventName = $(this).attr('name');
    //     var tid = $(this).attr('id');
    //     var date = $(this).find('td:eq(4)').text()
    //     var quantity = $(this).find('td:eq(2)').text()
    //     var reason = $(this).find('td:eq(6)').text()
    //     var price = $(this).find('td:eq(5)').text()
    //     console.log(date, price, reason, quantity)
    //     $.ajax({
    //         url: '',
    //         type: 'POST',
    //         data: {
    //           date: date,
    //           quantity: quantity,
    //           reason: reason,
    //           price: price,
    //           eventName: eventName
    //         },
    //         success: function(response){
    //           $('#list').append('<li>' + response.djangotoajax + '</li>');
    //         }
    //     });
    // });


    $("#1wk").click(function(){
      eventName = $(this).attr('name');
      $.ajax({
        url:'',
        type:'post',
        data:{
          eventName: eventName, 
          button_text: $(this).attr('id')
        },
        success: function(response){
            $('#list').append('<li>' + response.djangotoajax + '</li>');
            $('#plotly').html(response.newgraph);
        }
      });
    });

    $("#3mo").click(function(){
      eventName = $(this).attr('name');
      $.ajax({
        url:'',
        type:'post',
        data:{
          eventName: eventName, 
          button_text: $(this).text()
        },
        success: function(response){
            $('#list').append('<li>' + response.djangotoajax + '</li>');
            $('#plotly').html(response.newgraph);
        }
      });
    });
    $("#K").click(function(){
      eventName = $(this).attr('name');
      $.ajax({
        url:'',
        type:'post',
        data:{
          eventName: eventName,
          button_text: $(this).text()
        },
        success: function(response){
            $('#list').append('<li>' + response.djangotoajax + '</li>');
            $('#plotly').html(response.newgraph);
        }
      });
    });

    $("#RSI").click(function(){
      eventName = $(this).attr('name');
      $.ajax({
        url:'',
        type:'post',
        data:{
          eventName: eventName,
          button_text: $(this).text()
        },
        success: function(response){
            $('#list').append('<li>' + response.djangotoajax + '</li>');
            $('#plotly').html(response.newgraph);
        }
      });
    });
  });
