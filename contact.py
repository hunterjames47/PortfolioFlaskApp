from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        email_msg = Mail(
            from_email="your_verified_email@example.com",
            to_emails="your_email@example.com",
            subject="New Portfolio Contact",
            html_content=f"<p><b>{name}</b> ({email}) says:</p><p>{message}</p>"
        )

        try:
            sg = SendGridAPIClient(current_app.config["sendgrid_key"])
            sg.send(email_msg)
            flash("Message sent!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")

        return redirect(url_for("contact.contact"))

    return render_template("contact.html")