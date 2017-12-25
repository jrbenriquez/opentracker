var Login = function() {
    var r = function() {
        $(".login-form").validate({
            errorElement: "span",
            errorClass: "help-block help-block-error",
            focusInvalid: !1,
            rules: {
                email: {
                    required: !0,
                    email: !0
                },
                password: {
                    required: !0
                },
                remember: {
                    required: !1
                }
            },
            messages: {
                email: {
                    required: "Email is required."
                },
                password: {
                    required: "Password is required."
                }
            },
            invalidHandler: function(r, e) {
                $(".alert-danger", $(".login-form")).show()
            },
            highlight: function(r) {
                $(r).closest(".form-group").addClass("has-error")
            },
            success: function(r) {
                r.closest(".form-group").removeClass("has-error"), r.remove()
            },
            errorPlacement: function(r, e) {
                r.insertAfter(e.closest(".input-icon"))
            },
            submitHandler: function(r) {
                r.submit()
            }
        }), $(".login-form input").keypress(function(r) {
            return 13 == r.which ? ($(".login-form").validate().form() && $(".login-form").submit(), !1) : void 0
        }), $(".forget-form input").keypress(function(r) {
            return 13 == r.which ? ($(".forget-form").validate().form() && $(".forget-form").submit(), !1) : void 0
        }), $("#forget-password").click(function() {
            $(".login-form").hide(), $(".forget-form").show()
        }), $("#back-btn").click(function() {
            $(".login-form").show(), $(".forget-form").hide()
        })
    };


    var f = function() {
            $(".forget-form").validate({
                errorElement: "span",
                errorClass: "help-block",
                focusInvalid: !1,
                ignore: "",
                rules: {
                    email: {
                        required: !0,
                        email: !0
                    }
                },
                messages: {
                    email: {
                        required: "Email is required."
                    }
                },
                invalidHandler: function(e, r) {},
                highlight: function(e) {
                    $(e).closest(".form-group").addClass("has-error")
                },
                success: function(e) {
                    e.closest(".form-group").removeClass("has-error"), e.remove()
                },
                errorPlacement: function(e, r) {
                    e.insertAfter(r.closest(".input-icon"))
                },
                submitHandler: function(e) {
                    $.ajax({
                        url: '/account/password_reset/',
                        type: 'POST',
                        data: {
                            email: $('#email_reset').val(),
                            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                        },
                        success: function(data) {
                            console.log(data);
                            if (data.status == 'success') {
                                $(".alert-success", e).show();
                            }
                        },
                        error: function(error) {
                            console.log(error);
                            alert("Unable to send password reset link.");
                            console.log(error);
                        }
                    });
                }
            }), $(".forget-form input").keypress(function(e) {
                return 13 == e.which ? ($(".forget-form").validate().form() && $(".forget-form").submit(), !1) : void 0
            }), jQuery("#forget-password").click(function() {
                jQuery(".login-form").hide(), jQuery(".forget-form").show()
            }), jQuery("#back-btn").click(function() {
                jQuery(".login-form").show(), jQuery(".forget-form").hide()
            })
        };
    return {
        init: function() {
            r(), f(), $(".login-bg").backstretch([
                    "/static/assets/pages/img/login/bg1.jpg",
                    "/static/assets/pages/img/login/bg2.jpg",
                    "/static/assets/pages/img/login/bg3.jpg",
                    "/static/assets/pages/img/login/bg4.jpg",
                    "/static/assets/pages/img/login/bg5.jpg"
                ], {
                fade: 1e3,
                duration: 8e3
            }), $(".forget-form").hide()
        }
    }
}();
jQuery(document).ready(function() {
    Login.init()
});