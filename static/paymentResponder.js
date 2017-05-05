//var myIP = "169.254.94.117";
//var myIP = "127.0.0.1"
var myIP = "192.168.2.1"
function updateTable() {
  $.getJSON('http://'+myIP+':5000/today', function(data) {
    var payments = data.results;
    $('#running-total').html(data.total);
    $('#recent-payments').empty();
    $('#recent-payments').addClass('table');
    $('#recent-payments').append('<tr><th>Name</th><th>Donation</th><th>Time</th></tr>');
    $.each(payments,function(idx, val) {
      $('#recent-payments').append(
        '<tr><td>'+val['name']+'</td><td>£'+val['amount']+'</td><td>'+val['timestamp']+'</td></tr>');
    });
  });
};


updateTable();
socket = io.connect('http://'+myIP, { port: 8081, rememberTransport: false});
socket.on('connect', function() {
  // sends to socket.io server the host/port of oscServer
  // and oscClient
  socket.emit('config', {
    server: {
      port: 3333,
      host: myIP
    },
    client: {
      port: 3334,
      host: '127.0.0.1'
    }
  });
});

socket.on('message', function(obj) {
  if (obj[0] == '/payment') {
    card_id = obj[1];
    amount = obj[2];
    $("#amount").html('£'+amount);
    $("#payment-confirmed").fadeIn().delay(750).fadeOut();
    window.setTimeout(updateTable, 2000);
  }
});
