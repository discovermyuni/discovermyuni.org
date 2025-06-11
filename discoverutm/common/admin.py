from django import forms
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path
from django.urls import reverse
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_perms
from guardian.shortcuts import remove_perm

from .models import Organization
from .models.organization import OrganizationRequest


class ObjectLevelPermissionForm(forms.Form):
    model_choice = forms.ChoiceField(choices=[], required=True, label="Model")

    def __init__(self, *args, group=None, model_filter=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group

        # Dynamically build model choices
        model_choices = []
        for model in apps.get_models():
            opts = model._meta  # noqa: SLF001
            perms = getattr(opts, "permissions", [])
            if perms:
                model_choices.append((f"{opts.app_label}.{opts.model_name}", opts.verbose_name.title()))

        self.fields["model_choice"].choices = model_choices

        if model_filter:
            model = apps.get_model(*model_filter.split("."))
            opts = model._meta  # noqa: SLF001
            perm_defs = opts.permissions

            self.fields["object_permissions"] = forms.MultipleChoiceField(
                label=f"{opts.verbose_name.title()} Object Permissions",
                widget=forms.CheckboxSelectMultiple,
                choices=self._build_choices(model, perm_defs),
                required=False,
            )

            self.initial["object_permissions"] = self._get_current_perms(model, perm_defs)

    def _build_choices(self, model, perm_defs):
        choices = []
        for obj in model.objects.all():  # no limit here, since model is now filtered
            for codename, _label in perm_defs:
                value = f"{codename}|{model._meta.label}|{obj.pk}"  # noqa: SLF001
                display = f"{codename} — {obj}"
                choices.append((value, display))
        return choices

    def _get_current_perms(self, model, perm_defs):
        perms = []
        for obj in model.objects.all():
            for codename, _ in perm_defs:
                if self.group and codename in get_perms(self.group, obj):
                    perms.append(f"{codename}|{model._meta.label}|{obj.pk}")  # noqa: SLF001
        return perms

    def save(self):
        model = apps.get_model(*self.cleaned_data["model_choice"].split("."))
        perm_defs = model._meta.permissions  # noqa: SLF001
        selected = set(self.cleaned_data.get("object_permissions", []))

        for obj in model.objects.all():
            for codename, _ in perm_defs:
                key = f"{codename}|{model._meta.label}|{obj.pk}"  # noqa: SLF001
                if key in selected:
                    assign_perm(codename, self.group, obj)
                else:
                    remove_perm(codename, self.group, obj)


class UniversalGroupAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            path(
                "<int:group_id>/object-perms/",
                self.admin_site.admin_view(self.manage_object_perms),
                name="group_object_perms",
            ),
            *super().get_urls(),
        ]

    def change_view(self, request, object_id, *args, **kwargs):
        extra_context = kwargs.get("extra_context", {})
        extra_context["object_perm_url"] = reverse("admin:group_object_perms", args=[object_id])
        return super().change_view(request, object_id, *args, extra_context=extra_context)

    def manage_object_perms(self, request, group_id):
        group = Group.objects.get(pk=group_id)

        # SITE ADMINS ONLY BEGONE NORMIES
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse("admin:index"))

        if request.method == "POST":
            form = ObjectLevelPermissionForm(request.POST, group=group)
            if form.is_valid():
                form.save()
                self.message_user(request, "Object permissions updated.")
                return HttpResponseRedirect(reverse("admin:auth_group_change", args=[group.pk]))
        else:
            form = ObjectLevelPermissionForm(group=group)

        return TemplateResponse(
            request,
            "admin/universal_object_permissions.html",
            {
                "title": f"Object-Level Permissions for Group: {group.name}",
                "form": form,
                "group": group,
            },
        )


admin.site.unregister(Group)
admin.site.register(Group, UniversalGroupAdmin)

admin.site.register(Organization)

admin.site.register(OrganizationRequest)
