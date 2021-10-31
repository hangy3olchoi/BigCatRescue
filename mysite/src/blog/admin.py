from django.contrib import admin
from blog.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt', 'tag_list')
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    # slug 필드는 title 필드를 사용해 미리 채워지게 함.
    prepopulated_fields = {'slug': ('title',)}
    
# 이 작업이 끝나면 db작업이 마무리
    
    # ModelAdmin의 기능 중 get_queryset(request정보)이라는 기능이 있음
    def get_queryset(self, request):
        # prefetch_related('tags') - tags와 관련된 것을 미리 호출하여 사용할수 있도록 한다.
            # 즉, 태그가 기록된 정보가 있다면 읽어오겠다.
        return super().get_queryset(request).prefetch_related('tags')
    
    # tag 정보를 obj라는 객체로 만들어 지는데
    def tag_list(self, obj):
        # tag_list 리턴, ','로 join해라. 
        return ', '.join(o.name for o in obj.tags.all())