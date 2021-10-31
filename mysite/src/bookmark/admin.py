from django.contrib import admin
from bookmark.models import Bookmark

# Register your models here.
# admin 사이트에 테이블을 반영 - admin 사이트에 보여주는 모습을 정함

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    # 'id'는 무조건 들어가야 함, 자동적으로 1 ~ n까지 1씩 증가
    list_display = ('id', 'title', 'url')
    