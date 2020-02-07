from typing import TypeVar

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, FormView, DeleteView

ResponseType = TypeVar('ResponseType', bound=HttpResponse)


class AjaxViewMixin:
    """
    Миксин для проверки запроса на тип ajax.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise PermissionDenied('Доступны только AJAX-запросы')
        return super().dispatch(request, *args, **kwargs)


class BackPathTrackerMixin:
    """
    Миксин для записи url обращения к представлениям в сессию.
    """

    def write_back_path_to_session(self, back_path_key: str = 'back_path'):
        self.request.session[back_path_key] = self.request.get_full_path()

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # запись url только после успешного получения response
        self.write_back_path_to_session()
        return response


class MessageViewMixin:
    """
    Миксин для добавления системных сообщений в контекст шаблонов.
    """

    message_subject: str = None
    message_text: str = None
    message_icon: str = None
    message_link: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject, text, icon, link = self.get_message()
        context.update(dict(message_subject=subject, message_text=text, message_icon=icon, message_link=link))
        return context

    def get_message(self) -> tuple:
        return self.message_subject, self.message_text, self.message_icon, self.message_link


class TitleViewMixin:
    """
    Миксин для добавления переменной title в контекст шаблонов.
    """

    title: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            title=self.get_title()
        ))
        return context

    def get_title(self) -> str:
        return self.title


class JsonContextMixin:
    """
    Миксин для расширения контекста JsonResponse.
    """

    json_extra_context: dict = None

    def get_json_response_data(self, **kwargs) -> dict:
        if self.json_extra_context is not None:
            kwargs.update(self.json_extra_context)
        return kwargs


class CustomViewMixin(JsonContextMixin):
    """
    Кастомный миксин для представлений с поддержкой ajax-запросов/ответов.
    """

    json_response_var: str = 'template'
    wait_json: bool = True  # Если в любом случае нужно получить http-ответ - установить этот флаг как False

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.is_ajax() and self.wait_json:
            response = self.get_json_response(response)
        return response

    def get_json_response(self, http_response: ResponseType, **json_extra_context) -> JsonResponse:
        data = self.get_json_response_data(
            **{self.json_response_var: http_response.rendered_content}, **json_extra_context
        )
        return JsonResponse(data, safe=False)

    def get_json_response_with_context(self, **context_kwargs) -> JsonResponse:
        return JsonResponse(data={**context_kwargs})


class CustomFormViewMixin(CustomViewMixin):
    """
    Кастомный миксин для представлений с поддержкой ajax и обработки данных форм.
    """

    json_response_var: str = 'form'
    form_context_name: str = 'form'

    def form_invalid(self, form, **json_extra_context):
        response = super().form_invalid(form)
        if self.request.is_ajax() and self.wait_json:
            response = self.get_json_response(response, errors=form.errors, **json_extra_context)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.form_context_name] = context.pop('form')
        return context


class CustomDeleteView(CustomViewMixin, DeleteView):

    pass


class CustomView(CustomViewMixin, View):

    pass


class CustomFormView(CustomFormViewMixin, FormView):

    pass


class CustomCreateView(CustomFormViewMixin, CreateView):

    pass


class CustomUpdateView(CustomFormViewMixin, UpdateView):

    pass


class CustomDetailView(CustomViewMixin, DetailView):

    pass


class CustomTemplateView(CustomViewMixin, TemplateView):

    pass
