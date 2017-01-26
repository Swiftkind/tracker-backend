from django.contrib import admin

from .models import (
                        Company,
                        Project,
                        ProjectMember,
                        Log
                    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'account')
    search_fields = ('name', 'company', 'account')

    inlines = (ProjectMemberInline,)


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'end', 'member', 'is_approved', 'log')
    list_filter = ('member',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Log, LogAdmin)