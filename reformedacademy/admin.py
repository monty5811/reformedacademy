"""
Defines admin functionality for the reformedacademy app.

Copyright (C) 2014 by Reformed Forum <reformedforum.org>

This file is part of Reformed Academy.

Reformed Academy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Reformed Academy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Reformed Academy.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.contrib import admin
from django.core.urlresolvers import reverse
from reformedacademy import models


class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    prepopulated_fields = {"slug": ("name",)}


class CourseAdmin(admin.ModelAdmin):
    model = models.Course
    prepopulated_fields = {"slug": ("name",)}


class TaskInline(admin.TabularInline):
    model = models.Task
    extra = 1
    fields = ('name', 'order', 'changeform_link')
    readonly_fields = ('changeform_link', )

    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse(
                'admin:reformedacademy_task_change', args=(instance.id,)
            )
            print changeform_url
            return u'<a href="{}" onclick="return showAddAnotherPopup(this);">Details</a>'.format(changeform_url)
        return u'Details (save first)'

    changeform_link.allow_tags = True
    changeform_link.short_description = ''


class TaskAssetInline(admin.TabularInline):
    model = models.TaskAsset
    extra = 1
    raw_id_fields = ('asset',)


class TaskPassageInline(admin.TabularInline):
    model = models.PassageIndex
    extra = 1
    exclude = ('book',)


class TaskAdmin(admin.ModelAdmin):
    mode = models.Task
    inlines = [TaskAssetInline, TaskPassageInline]
    filter_horizontal = ('books',)


class LessonAdmin(admin.ModelAdmin):
    model = models.Lesson
    inlines = [TaskInline]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'course', 'order')
    list_filter = ('course',)
    list_editable = ('order',)
    ordering = ('course', 'order')


class InstructorAdmin(admin.ModelAdmin):
    model = models.Instructor
    prepopulated_fields = {"slug": ("name",)}


class BookISBNInline(admin.TabularInline):
    model = models.BookISBN
    extra = 1


class BookPassageInline(admin.TabularInline):
    model = models.PassageIndex
    extra = 1
    exclude = ('task',)


class BookAdmin(admin.ModelAdmin):
    model = models.Book
    inlines = [BookISBNInline, BookPassageInline]
    filter_horizontal = ('authors',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Lesson, LessonAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.Author)
admin.site.register(models.Book, BookAdmin)


