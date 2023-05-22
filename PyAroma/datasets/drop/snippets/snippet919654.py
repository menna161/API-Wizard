from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models_new import Student, Teacher, Manager, Course, Course_select_table, Course_Teacher, Major, Dept
from app.forms import EditProfileForm
from app import db


@app.route('/course_drop/<CourseNum>', methods=['GET'])
@login_required
def course_drop(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if (not (CourseNum in course_selected)):
            flash('您未选择该门课程！')
        else:
            current_user.drop_course(CourseNum)
            db.session.commit()
            flash('您已成功退选该门课程。')
        return redirect(url_for('course_select_table'))
