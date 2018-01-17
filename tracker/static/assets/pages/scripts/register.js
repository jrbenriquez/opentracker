var Login = function() {
    var r = function() {
        $("#login-form").validate({
            errorElement: "span",
            errorClass: "help-block help-block-error",
            focusInvalid: !1,
            rules: {
                email: {
                    required: !0,
                    email: !0
                },
                password1: {
                    required: !0,
                },
                password2: {
                    required: !0,
                    equalTo: "#register_password"
                },
                first_name: {
                    required: !0
                },
                last_name: {
                    required: !0
                },
                birthday: {
                    required: !0
                },
                mobile_number: {
                    required: !0,
                    valid_mobile: !0
                },
            },
            messages: {
                email: {
                    required: "Email is required."
                },
                password1: {
                    required: "Password is required."
                }
            },
            invalidHandler: function(r, e) {
                $(".alert-danger", $("#login-form")).show()
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
        }), $("#login-form input").keypress(function(r) {
            return 13 == r.which ? ($("#login-form").validate().form() && $("#login-form").submit(), !1) : void 0
        }), $("#back-btn").click(function() {
            $("#login-form").show(), $(".forget-form").hide()
        })
    };

    return {
        init: function() {
            r(), $(".login-bg").backstretch([
                    "/static/assets/pages/img/login/bg1.jpg",
                    "/static/assets/pages/img/login/bg2.jpg",
                    "/static/assets/pages/img/login/bg3.jpg",
                    "/static/assets/pages/img/login/bg4.jpg",
                    "/static/assets/pages/img/login/bg5.jpg"
                ], {
                fade: 1e3,
                duration: 8e3
            })
        }
    }
}();
jQuery(document).ready(function() {
    Login.init()
});