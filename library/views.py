from django.shortcuts import render, redirect, reverse, HttpResponse
from library import models
from functools import wraps


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        if user == 'admin' and pwd == 'admin':
            url = request.GET.get('url')
            if url:
                return_url = url
            else:
                return_url = reverse('publisher')

            ret = redirect(return_url)
            ret.set_signed_cookie('is_login', '1', salt='yan', httponly=True)

            return ret
        else:
            error = '用户名或密码错误'
    return render(request, 'login.html', locals())


def logout(request):
    ret = redirect('/login/')
    ret.delete_cookie('is_login')
    return ret


def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        is_login = request.get_signed_cookie('is_login', salt='yan', default='')
        if is_login != '1':
            return redirect('/login/?url={}'.format(request.path_info))
        ret = func(request, *args, **kwargs)
        return ret
    return inner


@login_required
def publisher_list(request):
    all_publishers = models.Publisher.objects.all().order_by('id')
    return render(request, 'publisher_list.html', {'all_publishers': all_publishers})


@login_required
def publisher_add(request):
    if request.method == 'POST':
        pub_name = request.POST.get('pub_name')
        if not pub_name:
            return render(request, 'publisher_add.html', {'error': '出版社名称不能为空'})

        if models.Publisher.objects.filter(name=pub_name):
            return render(request, 'publisher_add.html', {'error': '出版社名称已存在'})

        models.Publisher.objects.create(name=pub_name)
        return redirect(reverse('publisher'))

    return render(request, 'publisher_add.html')


@login_required
def publisher_del(request):
    pk = request.GET.get('pk')
    models.Publisher.objects.filter(pk=pk).delete()

    return redirect(reverse('publisher'))


@login_required
def publisher_edit(request, pk):
    pub_obj = models.Publisher.objects.get(pk=pk)

    if request.method == 'GET':
        return render(request, 'publisher_edit.html', {'pub_obj': pub_obj})
    else:
        pub_name = request.POST.get('pub_name')

        pub_obj.name = pub_name
        pub_obj.save()
        return redirect('/publisher/')


@login_required
def book_list(request):
    all_books = models.Book.objects.all()
    return render(request, 'book_list.html', {'all_books': all_books, 'name': 'publisher_list.html'})


@login_required
def book_add(request):
    error = ''
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        if not book_name:
            error = '书名不能为空'
        elif models.Book.objects.filter(name=book_name):
            error = '书名已存在'
        else:
            models.Book.objects.create(name=book_name, publisher_id=pub_id)
            return redirect('/book_list/')

    all_publishers = models.Publisher.objects.all()
    return render(request, 'book_add.html', {'all_publishers': all_publishers, 'error': error})


@login_required
def book_del(request):
    pk = request.GET.get('id')
    models.Book.objects.filter(pk=pk).delete()
    return redirect('/book_list/')


@login_required
def book_edit(request):
    pk = request.GET.get('id')
    book_obj = models.Book.objects.get(pk=pk)
    print(book_obj)

    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        models.Book.objects.filter(pk=pk).update(name=book_name, publisher_id=pub_id)

        return redirect('/book_list/')

    all_publishers = models.Publisher.objects.all()
    print(all_publishers)
    return render(request, 'book_edit.html', {'book_obj': book_obj, 'all_publishers': all_publishers})


@login_required
def author_list(request):
    all_authors = models.Author.objects.all()
    return render(request, 'author_list.html', {'all_authors': all_authors})


@login_required
def author_add(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.books.set(book_ids)
        return redirect('/author_list/')

    all_books = models.Book.objects.all()
    return  render(request, 'author_add.html', {'all_books': all_books})


@login_required
def author_del(request):
    pk = request.GET.get('id')
    models.Author.objects.filter(pk=pk).delete()
    return redirect('/author_list/')


@login_required
def author_edit(request):
    pk = request.GET.get('id')
    author_obj = models.Author.objects.get(pk=pk)

    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')
        author_obj.name = author_name
        author_obj.save()
        author_obj.books.set(book_ids)

        return redirect('/author_list/')

    all_books = models.Book.objects.all()
    return render(request, 'author_edit.html', {'author_obj': author_obj, 'all_books': all_books})


# 删除指定url name的id项
def delete(request, name, pk):
    print(name, pk)
    print('删除')

    # 从models中获取 url name对应的 类对象
    cls = getattr(models, name.capitalize())
    if not cls:
        return HttpResponse('检测表名')
    ret = cls.objects.filter(pk=pk)
    if ret:
        ret.delete()
    else:
        return HttpResponse('要删除的数据不存在')

    return redirect(name)

