from django.contrib import admin



def thumbnail_preview(self, obj):
    if obj.image:
        return mark_safe('<img src="{}" width="50"/>'.format(obj.image.url))
    return "-"

    

@admin.action(description='نشر الموضيع المحددة')
def make_publish(modeladmin, request, queryset):
    queryset.update(status='publish')

@admin.action(description='إرسال الى المسودة')
def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')

@admin.action(description='تنشيط المحددة')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
@admin.action(description=' غير نشط')
def make_unactive(modeladmin, request, queryset):
    queryset.update(active=False)


# Register your models here.
@admin.register(blog_Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')

@admin.register(blog_Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','description', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')


@admin.register(blog_Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview','title', 'author', 'post_date', 'status', 'num_posts')
    list_filter = ('post_date', 'status')
    search_fields = ('title', 'author__username', 'content')
    date_hierarchy = 'post_date'
    ordering = ('-post_date',)
    filter_horizontal = ('category',)
    readonly_fields = ('post_updated',)
    exclude = ('num_posts',)

    