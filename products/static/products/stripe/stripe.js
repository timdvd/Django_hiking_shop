$(document).ready(function(){

  var stripeFormModule = $(".stripe-payment-form");
  var stripeModuleToken = stripeFormModule.attr("data-token");
  var stripeModuleNextUrl = stripeFormModule.attr("data-next-url");
  var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card";
  
  var stripeTemplate = $.templates("#stripeTemplate");
  var stripeTemplateDataContext = {
      publishKey: stripeModuleToken,
      nextUrl: stripeModuleNextUrl,
      btnTitle: stripeModuleBtnTitle
  }
  var stripeTemplateHtml  = stripeTemplate.render(stripeTemplateDataContext)
  stripeFormModule.html(stripeTemplateHtml);


    var paymentForm = $('.payment-form');
    if (paymentForm.length > 1){
      paymentForm.css('display', 'none');
    }
    else if (paymentForm.length == 1){

      var pubKey = paymentForm.attr('data-token');
      var nextUrl = paymentForm.attr('data-next-url');

      var stripe = Stripe(pubKey);
      var elements = stripe.elements();

      // Custom styling can be passed to options when creating an Element.
      var style = {
          base: {
              color: '#32325d',
              lineHeight: '36px',
              fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
              fontSmoothing: 'antialiased',
              fontSize: '24px',
              '::placeholder': {
                color: '#aab7c4'
              }
            },
            invalid: {
              color: '#fa755a',
              iconColor: '#fa755a'
            }
      };
      
      // Create an instance of the card Element.
      var card = elements.create('card', {style: style});
      
      // Add an instance of the card Element into the `card-element` <div>.
      card.mount('#card-element');

      // Create a token or display an error when the form is submitted.
      var form = $('#payment-form');
      var btnLoad = form.find('.btn-load');
      var btnLoadDefaultHtml = btnLoad.html();
      var btnLoadDefaultClasses = btnLoad.attr('class');

      form.on('submit', function(event) {
        event.preventDefault();
        var $this = $(this);
        btnLoad.blur();
        var loadTime = 1500;
        var currentTimeout;
        var errorHtml     = "<i class='fa fa-warning'></i> An error occured";
        var loadingHtml   = "<i class='fa fa-spin fa-spinner'></i> Loading...";
        var errorClasses  = 'btn btn-danger disabled';
        var loadingClasses= 'btn btn-success disabled';
        stripe.createToken(card).then(function(result) {
                if (result.error) {
                // Inform the customer that there was an error.
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
                currentTimeout = buttonStatus(
                  btnLoad,
                  errorHtml,
                  errorClasses,
                  1000, currentTimeout
                )
                } else {
                  currentTimeout = buttonStatus(
                    btnLoad,
                    loadingHtml,
                    loadingClasses,
                    2000,
                    currentTimeout
                  )
                // Send the token to your server.
                stripeTokenHandler(nextUrl, result.token);
                }
            });
      });

      function buttonStatus(elem, newHtml, newClasses, loadingTime, timeout){
        if(!loadingTime){
          loadingTime = 1500;
        }
        elem.html(newHtml);
        elem.removeClass(btnLoadDefaultClasses);
        elem.addClass(newClasses);
        return setTimeout(function(){
          elem.html(btnLoadDefaultHtml);
          elem.removeClass(newClasses);
          elem.addClass(btnLoadDefaultClasses);
        }, loadingTime);

      }

      function redirectToNext(nextPath, time){
        if(nextPath){
          setTimeout(function(){
            window.location.href = nextPath;
          }, time);
        }
      }

      function stripeTokenHandler(token) {
          // Insert the token ID into the form so it gets submitted to the server
          console.log(token.id);
          var paymentMethodEndpoint = '/billing/payment-method/create/';
          var data = {
            'token': token.id
          }
          $.ajax({
            data: data,
            url: paymentMethodEndpoint,
            method: 'POST',
            success: function(data){
              var successMsg = data.message || 'Success! Your card was added.';
              card.clear();
              if(nextUrl){
                successMsg = successMsg + '<br/>Redirecting...';
              }
              if($.alert){
                $.alert(successMsg);
              }else{
                alert(successMsg);
              }
              btnLoad.html(btnLoadDefaultHtml);
              btnLoad.attr('class', btnLoadDefaultClasses);
              redirectToNext(nextUrl, 1500);
            },
            error: function(error){
              //console.log(error);
              $.alert({title: 'An error occured', content: 'Please try adding your card again.'});
              btnLoad.html(btnLoadDefaultHtml);
              btnLoad.attr('class', btnLoadDefaultClasses);
            },
          });
        }
      }
});