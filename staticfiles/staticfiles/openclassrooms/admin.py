from django.contrib import admin
from django.db import models
from .models.project import Project
from .models.skill import Skill
from .models.technology import Technology


class ProjectAdmin(admin.ModelAdmin):
    """
    add list of skill and technology to affect to projects, and upsize description field
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 10, 'cols': 80})
        return super().formfield_for_dbfield(db_field, **kwargs)
    filter_horizontal = ('skill', 'technology')
    list_display = ('title', 'url_github')

class SkillAdmin(admin.ModelAdmin):
    """
    used to modify display of the skill table in the django admin console
    """
    list_display = ('name', 'description')

class TechnologyAdmin(admin.ModelAdmin):
    """
    used to modify display of the technology table in the django admin console
    """
    list_display = ('name','description',)

"""
tables to include in django administration page
"""
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Technology, TechnologyAdmin)
