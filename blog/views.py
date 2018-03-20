from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponse
from blog.models import List
import django.utils.timezone as timezone


# Create your views here.

def edit(request, blog="default"):
    return render(request, "edit_v2.html", {"name": blog})


def read(request, blog="default"):
    if List.objects.filter(name=blog)==0:
        return HttpResponse(404)

    return render(request, "view_v2.html", {"name": blog})


def get(request, blog="default"):
    # b=Blog.objects.filter(id=blog).values("name", "markdown", "content", "nav")[0]
    # return HttpResponse(b.markdown)
    def file_iterator(file_name, chunk_size=512):
        try:
            with open('data/%s' % file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        except Exception as e:
            yield "# 这是一个新文档"

    md_name = "%s.md" % blog

    response = StreamingHttpResponse(file_iterator(md_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(md_name)
    return response


def add(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        name = request.POST.get('url', None)
        keyword = request.POST.get('keyword', None)
        description = request.POST.get('description', None)
        content = request.POST.get('content', None)
        try:
            List.objects.create(title=title, name=name, keyword=keyword, description=description,
                                createtime=timezone.now())
            with open('data/%s.md' % name, "w+") as f:
                f.write(content)
            return HttpResponse("添加成功")
        except Exception as e:
            return HttpResponse("添加失败:%s" % e)


def put(request):
    if request.method == "POST":
        content = request.POST.get('content', None)
        name = request.POST.get('name', None)
        try:
            ret = List.objects.filter(name=name).update(updatetime=timezone.now())
            if ret == 0:
                return HttpResponse(2)
        except Exception as e:
            return HttpResponse(1)

        try:
            with open('data/%s.md' % name, "w+") as f:
                f.write(content)
            return HttpResponse("修改成功")
        except Exception as e:
            return HttpResponse("修改失败:%s" % e)


def index(request):
    ret = List.objects.all().order_by('-updatetime')
    return render(request, 'index.html', {"ret": ret})
