from django.urls import reverse


class ConfirmDeleteMixin:
    """
    One view of delete
    """
    template_name = "planner/common/confirm_delete.html"
    confirm_title = None
    confirm_message = None

    def get_confirm_title(self):
        if self.confirm_title:
            return self.confirm_title
        model_name = self.model._meta.verbose_name.title()
        return f"Delete {model_name}"

    def get_confirm_message(self):
        if self.confirm_message:
            return self.confirm_message
        return f'Are you sure you want to delete "{self.get_object()}"?'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "title": self.get_confirm_title(),
            "message": self.get_confirm_message()
        })
        return ctx