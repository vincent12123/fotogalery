from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Task

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()  # Filter tasks by current user
    return render_template("index.html", tasks=tasks)

@main_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    name = request.form.get("name")
    priority = request.form.get("priority")
    date = request.form.get("date")
    if name:
        new_task = Task(name=name, priority=priority, date=date, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("main_bp.index"))

@main_bp.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:  # Ensure the task belongs to the current user
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("main_bp.index"))

@main_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:  # Ensure the task belongs to the current user
        if request.method == "POST":
            task.name = request.form.get("name")
            task.priority = request.form.get("priority")
            task.date = request.form.get("date")
            db.session.commit()
            return redirect(url_for("main_bp.index"))
        return render_template("edit_task.html", task=task)
    return redirect(url_for("main_bp.index"))