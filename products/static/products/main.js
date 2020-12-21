$(document).ready(function(){
  createSlider();
  checkboxes();
  showAll();
  setCheck();
});

function createSlider(){
  $('.products-slider').slick({
    dots: true,
    arrows: true,
    slidesToShow: 3,
    slidesToScroll: 3,
    nextArrow: '<button class="next-btn"><i class="fas fa-chevron-right"></i></button>',
    prevArrow: '<button class="prev-btn"><i class="fas fa-chevron-left"></i></button>',
    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        }
      },
      {
        breakpoint: 576,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        }
      },]
  });
}

function checkboxes(){
  $('input[type="checkbox"]').click(function(){
    var inputValue = $(this).attr("value");
    $("." + inputValue).toggle();
});
}

function showAll(){
  $('.show-all').on('click', function(e){
    e.preventDefault();
    $('.men').toggle();
    $('.women').toggle();
    $('.children').toggle();
    setCheck();
  });
}
function setCheck(){
  $('.check').prop('checked', true);
}


$(document).ready(function() {
  $('.flexslider').flexslider({
    animation: "slide",
    controlNav: "thumbnails"
  });
});

$(document).ready(function(){
  var searchForm = $('.search-form');
  var searchInput = searchForm.find("[name='q']");
  var typingTimer;
  var typingInterval = 1500;

  searchInput.keyup(function(event){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(perfomSearch, typingInterval);
  });

  function perfomSearch(){
    var query = searchInput.val();
    window.location.href = '/search/?q=' + query;
  }
});