/*!
    * Start Bootstrap - SB Admin v6.0.0 (https://startbootstrap.com/templates/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-sb-admin/blob/master/LICENSE)
    */
(function ($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the "href" property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        window.addEventListener("touchmove", function (e) { e.preventDefault(); }, { passive: false })
        $("body").toggleClass("sb-sidenav-toggled");
    });
})(jQuery);

$(document).ready(function () {
    $("body").on("click", "#btnSelectAll", function () {
        if ($(this).hasClass("allChecked")) {
            $("input[type='checkbox']", ".table").prop("checked", false);
        } else {
            $("input[type='checkbox']", ".table").prop("checked", true);
        }
        $(this).toggleClass("allChecked");
    })

    $("#divVendor > div:first").addClass("collapse show");

    $("input#cnpj").on("keyup", function (e) {
        $(this).val(
            $(this).val()
                .replace(/\D/g, "")
                .replace(/^(\d{2})(\d{3})?(\d{3})?(\d{4})?(\d{2})?/, "$1.$2.$3/$4-$5"));
    });

    setTimeout(function () {
        $("#messages").hide();
    }, 3000);
});
