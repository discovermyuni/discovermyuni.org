from django_components import Component


class CompactPost(Component):
    template_file = "compact/post.html"
    css_file = "compact/post.css"

    def get_context_data(self, title, description, location, start_date, end_date):
        return {"title": title}


class ComfortablePost(Component):
    template_file = "comfortable/post.html"
    css_file = "comfortable/post.css"

    def get_context_data(self, title, description, location, start_date, end_date):
        return {"title": title}
