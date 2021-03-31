# from django.urls import reverse_lazy
# from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from .models import Course
#
# class OwnerMixin(object):
#     def get_queryset(self):
#         qs = super(OwnerMixin, self).get_queryset()
#         return qs.filter(owner=self.request.user)
#
# class OwnerEditMixin(object):
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super(OwnerEditMixin, self).form_valid(form)
#
# class OwnerCourseMixin(OwnerMixin):
#     model = Course
#
# class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
#     fields = ['subject', 'title', 'slug', 'overview']
#     success_url = reverse_lazy('manage_course_list')
#     template_name = 'courses/manage/course/form.html'
#
# class ManageCourseListView(OwnerCourseMixin, ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#     def get_queryset(self):
#         qs = super(ManageCourseListView, self).get_queryset()
#         return qs.filter(owner=self.request.user)
#
#
# class CourseCreateView(OwnerCourseEditMixin, CreateView):
#     pass
#
# class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
#     pass
#
# class CourseDeleteView(OwnerCourseMixin, DeleteView):
#     template_name = 'courses/manage/course/delete.html'
#     success_url = reverse_lazy('manage_course_list')


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ['title']
    def str(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title



class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str(__self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()