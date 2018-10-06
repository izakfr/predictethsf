
'use strict';

$(document).ready((function () {

    //notifications

    var sideNav = $('.side-menu');
    $('.notifs').on('click', function (e) {
        e.preventDefault();
        $(this).siblings().toggleClass('show-notifs')
    });


    //side menu

    $('.open-menu').on('click', function () {
       sideNav.addClass('show-side-menu');
    });
    $('.close-menu').on('click', function () {
        sideNav.removeClass('show-side-menu');
    });
    var sideMenu = document.getElementById('side-menu');
    window.onclick = function(event) {
        if (event.target === sideMenu) {
            sideNav.removeClass('show-side-menu');
        }
    };
    $(window).on('resize', function () {
        if ((window.innerWidth > 760) && sideNav.hasClass('show-side-menu')){
            sideNav.removeClass('show-side-menu');
        }
    });

    //select plugin initialization

    $('select').niceSelect();

    $('.owl-carousel').owlCarousel({
        animateOut: 'slideOutDown',
        animateIn: 'flipInX',
        items:1,
        margin:30,
        stagePadding:30,
        smartSpeed:450,
        autoplay: true,
        loop: true
    });

    //modal show hide animation

    function modalAnim(x) {
        $('.modal .modal-dialog')
            .attr('class', 'modal-dialog  ' + x + '  animated');
    }
    var _modal = $('.modal');
    _modal.on('show.bs.modal', function () {
        var anim = "zoomIn";
        modalAnim(anim);
    });
    _modal.on('hide.bs.modal', function () {
        var anim = "fadeOutUp";
        modalAnim(anim);
    });


    //dashboard responsiveness

    var sliderContainer = $('.slide-container');
    var navToggleBtn = $('.side-nav-toggle');
    var dashNav = $('.side-nav');

    if(window.innerWidth < 760){
        sliderContainer.toggleClass('full-width');
        dashNav.toggleClass('open-cls-nav');
        navToggleBtn.removeClass('fa-angle-left').addClass('fa-bars');
    }

    navToggleBtn.on('click', function () {
        if(window.innerWidth < 760){
            dashNav.toggleClass('open-cls-nav');
        }else{
            sliderContainer.toggleClass('full-width');
            dashNav.toggleClass('open-cls-nav');
            if (sliderContainer.hasClass('full-width')){
                navToggleBtn.removeClass('fa-angle-left').addClass('fa-bars')
            }else{
                navToggleBtn.removeClass('fa-bars').addClass('fa-angle-left')
            }
        }
    });

    $(window).on('resize', function () {
        if ((window.innerWidth > 760) && dashNav.hasClass('open-cls-nav')){
            dashNav.removeClass('open-cls-nav');
            sliderContainer.removeClass('full-width');
            navToggleBtn.removeClass('fa-bars').addClass('fa-angle-left');
        }else if((window.innerWidth < 760) && !dashNav.hasClass('open-cls-nav')){
            dashNav.addClass('open-cls-nav');
            sliderContainer.addClass('full-width');
            navToggleBtn.removeClass('fa-angle-left').addClass('fa-bars');
        }
    });

    $('.cls-nav').on('click', function () {
        dashNav.toggleClass('open-cls-nav');
    });


    // perfect scrollbar initialization

    $('.links-container').perfectScrollbar();
    $('.mini').perfectScrollbar();


    //login and register forms switch

    $('.tab').on('click', function (e) {
        e.preventDefault();
        $('.frm').addClass('hide');
        $('.'+$(this).data('frm')).removeClass('hide');
        $('.tab').removeClass('active');
        $(this).addClass('active');
    });

}));


// loader beacon

$(window).on('load', function(){
    $('.preloader').fadeOut('slow',function(){
        $(this).remove();
    });
});